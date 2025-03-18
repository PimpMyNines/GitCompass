#!/usr/bin/env python3
"""
Example script to create an issue hierarchy (parent and sub-issues).

This example demonstrates how to:
1. Create a parent issue
2. Create multiple sub-issues linked to the parent
3. Update the parent issue with references to sub-issues
4. Optionally delete all test issues after verification
"""

import os
import sys
import argparse

# Add src directory to path for running directly from examples
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gitcompass.auth.github_auth import GitHubAuth
from src.gitcompass.issues.issue_manager import IssueManager
from src.gitcompass.utils.config import Config

def create_issue_hierarchy(repo, parent_title, sub_issues, cleanup=False):
    """Create a parent issue with multiple sub-issues.
    
    Args:
        repo: Repository in format owner/repo
        parent_title: Title of the parent issue
        sub_issues: List of sub-issue titles
        cleanup: If True, delete all created issues after creation
    
    Returns:
        Tuple containing (parent_issue, sub_issues, created_issues)
    """
    # Initialize configuration and authentication
    config = Config()
    auth = GitHubAuth(config)
    issue_manager = IssueManager(auth)
    
    # Track created issues for cleanup
    created_issues = []
    
    try:
        # Create parent issue
        parent_body = ("This is a parent issue that will have sub-issues.\n\n"
                      "## Tasks:\n")
        
        for task in sub_issues:
            parent_body += f"- [ ] {task}\n"
            
        print(f"Creating parent issue: {parent_title}")
        parent = issue_manager.create_issue(
            repo=repo,
            title=parent_title,
            body=parent_body,
            labels=["enhancement"]
        )
        print(f"Created parent issue #{parent['number']}")
        created_issues.append(parent["number"])
        
        # Convert tasks to sub-issues
        print("Converting tasks to sub-issues...")
        created_sub_issues = issue_manager.convert_tasks_to_issues(
            repo=repo,
            issue_number=parent['number'],
            labels=["task"]
        )
        
        print(f"Created {len(created_sub_issues)} sub-issues:")
        for issue in created_sub_issues:
            print(f"  - #{issue['number']}: {issue['title']}")
            created_issues.append(issue["number"])
        
        # Clean up if requested
        if cleanup:
            print("\n=== CLEANING UP TEST ISSUES ===")
            cleanup_issues(repo, created_issues, issue_manager)
            
        return parent, created_sub_issues, created_issues
        
    except Exception as e:
        print(f"Error: {str(e)}")
        # Try to clean up on error if requested
        if cleanup and created_issues:
            print("\n=== CLEANING UP ISSUES AFTER ERROR ===")
            cleanup_issues(repo, created_issues, issue_manager)
        sys.exit(1)

def cleanup_issues(repo, issue_numbers, issue_manager):
    """Close all issues created during the test.
    
    Args:
        repo: Repository in format owner/repo
        issue_numbers: List of issue numbers to close
        issue_manager: Initialized IssueManager
    """
    if not issue_numbers:
        return
        
    print(f"Closing {len(issue_numbers)} issues...")
    # Close sub-issues first, then the parent (reverse order of creation)
    for issue_number in sorted(issue_numbers, reverse=True):
        try:
            issue_manager.close_issue(repo, issue_number)
            print(f"  - Closed issue #{issue_number}")
        except Exception as e:
            print(f"  - Failed to close issue #{issue_number}: {str(e)}")
    
    print("Cleanup complete")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Create a GitHub issue hierarchy for testing")
    parser.add_argument("--repo", type=str, default="owner/repo", help="Repository in format owner/repo")
    parser.add_argument("--title", type=str, default="GitCompass Test Issue Hierarchy", 
                        help="Title for the parent issue")
    parser.add_argument("--cleanup", action="store_true", help="Clean up all issues after creation")
    args = parser.parse_args()
    
    # Repository to create issues in
    REPO = args.repo
    
    # Issue details
    PARENT_TITLE = args.title
    SUB_ISSUES = [
        "Design authentication database schema",
        "Implement OAuth2 provider integration",
        "Create user registration workflow",
        "Add password reset functionality",
        "Write authentication documentation"
    ]
    
    print(f"Creating issue hierarchy in repository: {REPO}")
    print(f"Parent issue: {PARENT_TITLE}")
    print(f"Number of sub-issues: {len(SUB_ISSUES)}")
    print(f"Cleanup mode: {'Enabled' if args.cleanup else 'Disabled'}")
    print("")
    
    # Create the issue hierarchy with optional cleanup
    create_issue_hierarchy(REPO, PARENT_TITLE, SUB_ISSUES, cleanup=args.cleanup)
