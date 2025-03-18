#!/usr/bin/env python3
"""
Example script to set up a complete project with issues and roadmap.

This example demonstrates how to:
1. Create a GitHub project
2. Set up a roadmap with milestones
3. Create and organize issues in the project
"""

import os
import sys
import datetime

# Add src directory to path for running directly from examples
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gitcompass.auth.github_auth import GitHubAuth
from src.gitcompass.issues.issue_manager import IssueManager
from src.gitcompass.projects.project_manager import ProjectManager
from src.gitcompass.roadmap.roadmap_manager import RoadmapManager
from src.gitcompass.utils.config import Config

def setup_project(repo, project_name, milestones, feature_sets):
    """Set up a complete project with roadmap and issues.
    
    Args:
        repo: Repository in format owner/repo
        project_name: Name for the project board
        milestones: List of milestone dictionaries (title, description, due_date)
        feature_sets: Dictionary of features to add (milestone_title -> features)
    """
    # Initialize managers
    config = Config()
    auth = GitHubAuth(config)
    issue_manager = IssueManager(auth)
    project_manager = ProjectManager(auth)
    roadmap_manager = RoadmapManager(auth)
    
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
                    
                    print(f"    Created {len(sub_issues)} sub-issues")
        
        # 4. Generate and print roadmap report
        print("\nGenerating roadmap report...")
        report = roadmap_manager.generate_roadmap_report(repo)
        print("\n" + report)
        
        return {
            "project": project,
            "milestones": milestone_map
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Configuration
    REPO = "owner/repo"  # Replace with your repository
    PROJECT_NAME = "Q3 Development"
    
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
    
    # Run the project setup
    setup_project(REPO, PROJECT_NAME, MILESTONES, FEATURE_SETS)
