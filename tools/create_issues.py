#!/usr/bin/env python3
"""Create GitHub issues from Markdown files in the issues directory."""

import os
import re
import argparse
import yaml
import datetime
from pathlib import Path

try:
    from github import Github
except ImportError:
    print("Error: PyGithub package is not installed.")
    print("Install it with: pip install PyGithub")
    exit(1)


def parse_issue_file(file_path):
    """Parse a Markdown issue file into structured data."""
    with open(file_path, "r") as f:
        content = f.read()

    # Extract main issue
    main_issue_match = re.search(r"## Main Issue(.*?)## Sub-Issues", content, re.DOTALL)
    if not main_issue_match:
        raise ValueError(f"File {file_path} doesn't have the expected format (main issue section)")

    main_issue_text = main_issue_match.group(1)
    
    # Parse main issue metadata
    main_issue = {
        "title": extract_field(main_issue_text, "Title"),
        "description": extract_field(main_issue_text, "Description"),
        "type": extract_field(main_issue_text, "Type"),
        "priority": extract_field(main_issue_text, "Priority"),
        "start_date": extract_field(main_issue_text, "Start Date"),
    }

    # Extract sub-issues
    sub_issues_section = content.split("## Sub-Issues", 1)[1] if "## Sub-Issues" in content else ""
    sub_issue_blocks = re.findall(r"### \d+\.\s*(.*?)(?=### \d+\.|$)", sub_issues_section, re.DOTALL)
    
    sub_issues = []
    for block in sub_issue_blocks:
        # Split the block into header and content
        title_match = re.search(r"\*\*Title\*\*:\s*(.*?)$", block, re.MULTILINE)
        if not title_match:
            continue
            
        sub_issue = {
            "title": extract_field(block, "Title"),
            "description": extract_field(block, "Description"),
            "type": extract_field(block, "Type"),
            "priority": extract_field(block, "Priority"),
            "start_date": extract_field(block, "Start Date"),
        }
        
        # Extract tasks if present
        tasks_match = re.search(r"\*\*Tasks\*\*:(.*?)(?=\s*$|\s*\*\*\w+\*\*:)", block, re.DOTALL)
        if tasks_match:
            tasks_text = tasks_match.group(1).strip()
            tasks = []
            for line in tasks_text.split("\n"):
                line = line.strip()
                if line.startswith("- ["):
                    # Extract task text (strip checkbox notation)
                    task_text = line[5:].strip()
                    tasks.append(task_text)
            sub_issue["tasks"] = tasks
                    
        sub_issues.append(sub_issue)
        
    return {
        "main_issue": main_issue,
        "sub_issues": sub_issues
    }


def extract_field(text, field_name):
    """Extract a field value from markdown text."""
    pattern = r"\*\*" + re.escape(field_name) + r"\*\*:\s*(.*?)(?=\s*$|\s*\*\*\w+\*\*:)"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def create_github_issues(repo_name, issues_data, token=None, dry_run=False):
    """Create GitHub issues from parsed data."""
    if not token:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            raise ValueError("GitHub token not provided and GITHUB_TOKEN environment variable not set")
    
    g = Github(token)
    repo = g.get_repo(repo_name)
    
    main_issue = issues_data["main_issue"]
    sub_issues = issues_data["sub_issues"]
    
    # Format main issue body
    body = f"{main_issue['description']}\n\n"
    body += f"**Type:** {main_issue['type']}\n"
    body += f"**Priority:** {main_issue['priority']}\n"
    
    if main_issue['start_date']:
        try:
            # Convert string date to GitHub compatible date
            date_obj = datetime.datetime.strptime(main_issue['start_date'], "%m/%d/%Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            body += f"**Start Date:** {formatted_date}\n"
        except ValueError:
            body += f"**Start Date:** {main_issue['start_date']}\n"
    
    print(f"{'[DRY RUN] ' if dry_run else ''}Creating main issue: {main_issue['title']}")
    
    if not dry_run:
        parent_issue = repo.create_issue(
            title=main_issue["title"],
            body=body,
            labels=["enhancement" if main_issue["type"].lower() == "feature" else main_issue["type"].lower()]
        )
        print(f"Created issue #{parent_issue.number}: {parent_issue.title}")
        
        # Now create sub-issues
        for sub_issue in sub_issues:
            # Format sub-issue body
            sub_body = f"{sub_issue['description']}\n\n"
            sub_body += f"**Type:** {sub_issue['type']}\n"
            sub_body += f"**Priority:** {sub_issue['priority']}\n"
            
            if sub_issue['start_date']:
                try:
                    date_obj = datetime.datetime.strptime(sub_issue['start_date'], "%m/%d/%Y")
                    formatted_date = date_obj.strftime("%Y-%m-%d")
                    sub_body += f"**Start Date:** {formatted_date}\n"
                except ValueError:
                    sub_body += f"**Start Date:** {sub_issue['start_date']}\n"
            
            # Add parent reference
            sub_body += f"\nParent: #{parent_issue.number}\n"
            
            # Add tasks if present
            if "tasks" in sub_issue and sub_issue["tasks"]:
                sub_body += "\n## Tasks\n\n"
                for task in sub_issue["tasks"]:
                    sub_body += f"- [ ] {task}\n"
            
            print(f"Creating sub-issue: {sub_issue['title']}")
            sub_gh_issue = repo.create_issue(
                title=sub_issue["title"],
                body=sub_body,
                labels=["enhancement" if sub_issue["type"].lower() == "feature" else sub_issue["type"].lower()]
            )
            print(f"Created sub-issue #{sub_gh_issue.number}: {sub_gh_issue.title}")
            
            # Update parent issue with link to sub-issue
            if parent_issue.body and "## Sub-Issues" not in parent_issue.body:
                new_body = parent_issue.body + "\n\n## Sub-Issues\n\n"
            elif parent_issue.body and "## Sub-Issues" in parent_issue.body:
                new_body = parent_issue.body
            else:
                new_body = "## Sub-Issues\n\n"
                
            new_body += f"- #{sub_gh_issue.number}: {sub_gh_issue.title}\n"
            parent_issue.edit(body=new_body)
    else:
        # In dry run mode, just print what would be created
        print(f"Main issue body:\n{body}\n")
        for i, sub_issue in enumerate(sub_issues):
            print(f"Would create sub-issue {i+1}: {sub_issue['title']}")


def main():
    """Main function to parse arguments and create issues."""
    parser = argparse.ArgumentParser(description="Create GitHub issues from Markdown files")
    parser.add_argument("--repo", "-r", required=True, help="GitHub repository in format 'owner/repo'")
    parser.add_argument("--token", "-t", help="GitHub token (will use GITHUB_TOKEN env var if not provided)")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Dry run mode (don't create issues)")
    parser.add_argument("--files", "-f", nargs="*", help="Specific issue files to process")
    args = parser.parse_args()
    
    # Determine files to process
    issues_dir = Path(__file__).parent.parent / "issues"
    if args.files:
        issue_files = [Path(f) if os.path.exists(f) else issues_dir / f for f in args.files]
    else:
        issue_files = list(issues_dir.glob("*.md"))
    
    # Process each file
    for file_path in issue_files:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
            
        print(f"Processing {file_path}...")
        try:
            issues_data = parse_issue_file(file_path)
            create_github_issues(args.repo, issues_data, token=args.token, dry_run=args.dry_run)
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            
    print("Done!")


if __name__ == "__main__":
    main()