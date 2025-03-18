#!/usr/bin/env python3
"""
Example script to set up a complete project with issues and roadmap.

This example demonstrates how to:
1. Create a GitHub project
2. Set up a roadmap with milestones
3. Create and organize issues in the project
4. Optionally delete all test resources after verification
"""

import os
import sys
import datetime
import argparse

# Add src directory to path for running directly from examples
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gitcompass.auth.github_auth import GitHubAuth
from src.gitcompass.issues.issue_manager import IssueManager
from src.gitcompass.projects.project_manager import ProjectManager
from src.gitcompass.roadmap.roadmap_manager import RoadmapManager
from src.gitcompass.utils.config import Config

def setup_project(repo, project_name, milestones, feature_sets, cleanup=False):
    """Set up a complete project with roadmap and issues.
    
    Args:
        repo: Repository in format owner/repo
        project_name: Name for the project board
        milestones: List of milestone dictionaries (title, description, due_date)
        feature_sets: Dictionary of features to add (milestone_title -> features)
        cleanup: If True, delete all created resources after setup
    """
    # Initialize managers
    config = Config()
    auth = GitHubAuth(config)
    issue_manager = IssueManager(auth)
    project_manager = ProjectManager(auth)
    roadmap_manager = RoadmapManager(auth)
    
    # Track created resources for cleanup
    created_resources = {
        "project_id": None,
        "milestones": [],
        "issues": []
    }
    
    try:
        # 1. Create the project
        print(f"Creating project: {project_name}")
        project = project_manager.create_project(
            name=project_name,
            body=f"Automated project for {repo}",
            repo=repo,
            template="advanced"  # Use advanced template with more columns
        )
        print(f"Created project: {project['name']} (ID: {project['id']})")
        created_resources["project_id"] = project["id"]
        
        # Store column info for later use
        columns = {column["name"]: column["id"] for column in project["columns"]}
        print(f"Project columns: {', '.join(columns.keys())}")
        
        # 2. Create milestones (roadmap)
        print("\nSetting up roadmap with milestones:")
        milestone_map = {}  # Store milestone info for referencing later
        
        for ms in milestones:
            milestone = roadmap_manager.create_milestone(
                repo=repo,
                title=ms["title"],
                due_date=ms["due_date"],
                description=ms["description"]
            )
            milestone_map[ms["title"]] = milestone["number"]
            created_resources["milestones"].append(milestone["number"])
            print(f"  - Created milestone: {milestone['title']} (Due: {milestone['due_on']})")
        
        # 3. Create issues for each feature set
        print("\nCreating issues for each feature set:")
        for milestone_title, features in feature_sets.items():
            milestone_id = milestone_map.get(milestone_title)
            if not milestone_id:
                print(f"Warning: Milestone '{milestone_title}' not found, skipping features")
                continue
                
            print(f"\nFeatures for milestone '{milestone_title}':")
            for feature in features:
                # Create the feature issue
                issue = issue_manager.create_issue(
                    repo=repo,
                    title=feature["title"],
                    body=feature["description"],
                    labels=feature.get("labels", []),
                    milestone=milestone_id
                )
                print(f"  - Created issue #{issue['number']}: {issue['title']}")
                created_resources["issues"].append(issue["number"])
                
                # Add to project in appropriate column
                column = feature.get("column", "To Do")
                card = project_manager.add_issue_to_project(
                    project_id=project["id"],
                    repo=repo,
                    issue_number=issue["number"],
                    column_name=column
                )
                print(f"    Added to '{column}' column")
                
                # Create sub-tasks if present
                tasks = feature.get("tasks", [])
                if tasks:
                    # Update issue body to include tasks
                    body = issue["body"]
                    body += "\n\n## Tasks\n\n"
                    for task in tasks:
                        body += f"- [ ] {task}\n"
                        
                    issue_manager.update_issue(
                        repo=repo,
                        issue_number=issue["number"],
                        body=body
                    )
                    
                    # Convert tasks to sub-issues
                    sub_issues = issue_manager.convert_tasks_to_issues(
                        repo=repo,
                        issue_number=issue["number"],
                        labels=["task"]
                    )
                    
                    # Track sub-issues for cleanup
                    for sub_issue in sub_issues:
                        created_resources["issues"].append(sub_issue["number"])
                    
                    print(f"    Created {len(sub_issues)} sub-issues")
        
        # 4. Generate and print roadmap report
        print("\nGenerating roadmap report...")
        report = roadmap_manager.generate_roadmap_report(repo)
        print("\n" + report)
        
        # 5. Cleanup resources if requested
        if cleanup:
            print("\n=== CLEANING UP TEST RESOURCES ===")
            cleanup_resources(repo, created_resources, issue_manager, project_manager, roadmap_manager)
        
        return {
            "project": project,
            "milestones": milestone_map,
            "created_resources": created_resources
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        # Attempt cleanup on error if requested
        if cleanup and created_resources:
            print("\n=== CLEANING UP RESOURCES AFTER ERROR ===")
            cleanup_resources(repo, created_resources, issue_manager, project_manager, roadmap_manager)
        sys.exit(1)

def cleanup_resources(repo, resources, issue_manager, project_manager, roadmap_manager):
    """Delete all resources created during the test.
    
    Args:
        repo: Repository in format owner/repo
        resources: Dictionary of created resource IDs/numbers
        issue_manager: Initialized IssueManager
        project_manager: Initialized ProjectManager
        roadmap_manager: Initialized RoadmapManager
    """
    # Delete issues (including sub-issues)
    if resources.get("issues"):
        print(f"Deleting {len(resources['issues'])} issues...")
        for issue_number in sorted(resources["issues"], reverse=True):
            try:
                issue_manager.close_issue(repo, issue_number)
                print(f"  - Closed issue #{issue_number}")
            except Exception as e:
                print(f"  - Failed to close issue #{issue_number}: {str(e)}")
    
    # Delete milestones
    if resources.get("milestones"):
        print(f"Deleting {len(resources['milestones'])} milestones...")
        for milestone_number in resources["milestones"]:
            try:
                roadmap_manager.delete_milestone(repo, milestone_number)
                print(f"  - Deleted milestone #{milestone_number}")
            except Exception as e:
                print(f"  - Failed to delete milestone #{milestone_number}: {str(e)}")
    
    # Delete project
    if resources.get("project_id"):
        try:
            project_manager.delete_project(resources["project_id"])
            print(f"Deleted project (ID: {resources['project_id']})")
        except Exception as e:
            print(f"Failed to delete project: {str(e)}")
    
    print("Cleanup complete")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Set up a GitHub project with issues and roadmap for testing")
    parser.add_argument("--repo", type=str, default="owner/repo", help="Repository in format owner/repo")
    parser.add_argument("--name", type=str, default="GitCompass End-to-End Test", help="Project name")
    parser.add_argument("--cleanup", action="store_true", help="Clean up all resources after creation")
    args = parser.parse_args()
    
    # Configuration
    REPO = args.repo
    PROJECT_NAME = args.name
    
    # Define milestones for the roadmap
    MILESTONES = [
        {
            "title": "Alpha Release",
            "description": "Initial alpha release with core features",
            "due_date": (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        },
        {
            "title": "Beta Release",
            "description": "Beta release with all planned features",
            "due_date": (datetime.datetime.now() + datetime.timedelta(days=60)).strftime("%Y-%m-%d")
        },
        {
            "title": "1.0 Release",
            "description": "First stable release",
            "due_date": (datetime.datetime.now() + datetime.timedelta(days=90)).strftime("%Y-%m-%d")
        }
    ]
    
    # Define features for each milestone
    FEATURE_SETS = {
        "Alpha Release": [
            {
                "title": "Implement user authentication",
                "description": "Add support for user authentication with OAuth providers",
                "labels": ["feature", "security"],
                "column": "To Do",
                "tasks": [
                    "Set up OAuth2 client",
                    "Implement login flow",
                    "Add token management",
                    "Create user profiles"
                ]
            },
            {
                "title": "Create basic UI components",
                "description": "Implement core UI components for the application",
                "labels": ["feature", "ui"],
                "column": "To Do",
                "tasks": [
                    "Design component library",
                    "Implement navigation system",
                    "Create form components",
                    "Add responsive layout"
                ]
            }
        ],
        "Beta Release": [
            {
                "title": "Add data visualization",
                "description": "Implement data visualization features",
                "labels": ["feature", "enhancement"],
                "column": "Backlog",
                "tasks": [
                    "Research chart libraries",
                    "Implement dashboard components",
                    "Create data export functionality",
                    "Add custom visualization options"
                ]
            }
        ],
        "1.0 Release": [
            {
                "title": "Performance optimization",
                "description": "Optimize application performance for production release",
                "labels": ["enhancement", "performance"],
                "column": "Backlog",
                "tasks": [
                    "Profile application",
                    "Optimize database queries",
                    "Implement caching",
                    "Reduce bundle size"
                ]
            },
            {
                "title": "Documentation and tutorials",
                "description": "Create comprehensive documentation for users",
                "labels": ["documentation"],
                "column": "Backlog",
                "tasks": [
                    "Write API documentation",
                    "Create user guides",
                    "Record tutorial videos",
                    "Update README and contributing guidelines"
                ]
            }
        ]
    }
    
    print(f"Setting up test project in repository: {REPO}")
    print(f"Project name: {PROJECT_NAME}")
    print(f"Cleanup mode: {'Enabled' if args.cleanup else 'Disabled'}")
    print("")
    
    # Run the project setup with optional cleanup
    setup_project(REPO, PROJECT_NAME, MILESTONES, FEATURE_SETS, cleanup=args.cleanup)
