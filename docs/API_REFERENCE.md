# OctoMaster API Reference

## Overview

OctoMaster provides both a command-line interface and a Python API for managing GitHub projects, issues, and roadmaps. This document describes the Python API, which can be used to build custom integrations or scripts.

## Authentication

### `GitHubAuth`

The `GitHubAuth` class handles authentication with GitHub using either personal access tokens or GitHub Apps.

```python
from octomaster.auth.github_auth import GitHubAuth
from octomaster.utils.config import Config

# Create a configuration (loads from config file or environment variables)
config = Config()

# Create an auth instance
auth = GitHubAuth(config)

# Access the authenticated GitHub client
github_client = auth.client

# Get the authenticated user
user = auth.get_user()
print(f"Authenticated as: {user.login}")

# Get a repository
repo = auth.get_repo("owner/repo")
```

## Issue Management

### `IssueManager`

The `IssueManager` class provides methods for working with GitHub issues, including creating issues, updating issues, and converting tasks to sub-issues.

```python
from octomaster.issues.issue_manager import IssueManager

# Create an issue manager
issue_manager = IssueManager(auth)

# Create a new issue
issue = issue_manager.create_issue(
    repo="owner/repo",
    title="New feature request",
    body="We need to implement this feature...",
    labels=["enhancement", "priority-medium"],
    assignees=["developer-username"],
    milestone=1,  # Milestone ID
    parent_issue=42  # Optional parent issue number
)

# Update an existing issue
updated_issue = issue_manager.update_issue(
    repo="owner/repo",
    issue_number=123,
    title="Updated title",
    body="Updated description",
    state="closed",  # or "open"
    labels=["bug", "resolved"],
    assignees=["new-assignee"]
)

# Convert tasks in an issue to sub-issues
sub_issues = issue_manager.convert_tasks_to_issues(
    repo="owner/repo",
    issue_number=456,
    labels=["task"]
)

# Get issues from a repository
issues = issue_manager.get_issues(
    repo="owner/repo",
    state="open",  # "open", "closed", or "all"
    labels=["bug"]  # Optional filter by labels
)
```

## Project Management

### `ProjectManager`

The `ProjectManager` class provides methods for working with GitHub projects, such as creating projects, adding issues to projects, and organizing project columns.

```python
from octomaster.projects.project_manager import ProjectManager

# Create a project manager
project_manager = ProjectManager(auth)

# Create a new project
project = project_manager.create_project(
    name="Q2 Development",
    body="Project for Q2 development tasks",
    repo="owner/repo",  # Repository project
    # org="org-name",  # Organization project
    template="advanced"  # "basic" or "advanced"
)

# Add an issue to a project
card = project_manager.add_issue_to_project(
    project_id=project["id"],
    repo="owner/repo",
    issue_number=123,
    column_name="To Do"  # Optional column name
)

# Get project information
project_info = project_manager.get_project(
    project_id=12345,
    repo="owner/repo"  # Optional repository
    # org="org-name"  # Optional organization
)

# Accesss project cards
cards = project_info["cards"]
for column_name, column_cards in cards.items():
    print(f"Column: {column_name}")
    for card in column_cards:
        print(f"  - {card['issue']['title'] if 'issue' in card else card['note']}")
```

## Roadmap Management

### `RoadmapManager`

The `RoadmapManager` class provides methods for working with GitHub roadmaps using milestones.

```python
from octomaster.roadmap.roadmap_manager import RoadmapManager

# Create a roadmap manager
roadmap_manager = RoadmapManager(auth)

# Create a new milestone
milestone = roadmap_manager.create_milestone(
    repo="owner/repo",
    title="v1.0 Release",
    due_date="2023-12-31",  # YYYY-MM-DD format
    description="First stable release"
)

# Update a milestone
updated_milestone = roadmap_manager.update_milestone(
    repo="owner/repo",
    milestone_number=milestone["number"],
    title="v1.0 Final Release",
    state="closed",  # or "open"
    description="First stable release with all features",
    due_date="2024-01-15"
)

# Get all milestones (roadmap)
roadmap = roadmap_manager.get_roadmap("owner/repo")

# Generate a markdown report of the roadmap
report = roadmap_manager.generate_roadmap_report("owner/repo")

# Save the report to a file
with open("roadmap.md", "w") as f:
    f.write(report)
```

## Configuration

### `Config`

The `Config` class handles loading and accessing configuration from multiple sources: config files, environment variables, and command-line arguments.

```python
from octomaster.utils.config import Config

# Create a configuration (optionally with a specific config file)
config = Config(config_file="path/to/config.yaml")

# Get a configuration value (with optional default)
token = config.get("auth.token", default="default-value")

# Check if a configuration key exists
if config.has("defaults.repository"):
    repo = config.get("defaults.repository")

# Set a configuration value
config.set("auth.token", "new-token-value")
```

## Error Handling

OctoMaster methods raise descriptive exceptions when errors occur. It's recommended to use try-except blocks to handle these exceptions:

```python
try:
    issue = issue_manager.create_issue(
        repo="owner/repo",
        title="New issue"
    )
    print(f"Created issue #{issue['number']}")
except ValueError as e:
    print(f"Invalid input: {e}")
except Exception as e:
    print(f"Error: {e}")
```

## Complete Example

Here's a complete example that creates a new issue and adds it to a project:

```python
from octomaster.auth.github_auth import GitHubAuth
from octomaster.issues.issue_manager import IssueManager
from octomaster.projects.project_manager import ProjectManager
from octomaster.utils.config import Config

def main():
    # Initialize
    config = Config()
    auth = GitHubAuth(config)
    issue_manager = IssueManager(auth)
    project_manager = ProjectManager(auth)
    
    try:
        # Create an issue
        issue = issue_manager.create_issue(
            repo="owner/repo",
            title="New feature implementation",
            body="# Feature Description\n\n- [ ] Task 1\n- [ ] Task 2\n- [ ] Task 3",
            labels=["enhancement"]
        )
        print(f"Created issue #{issue['number']}")
        
        # Create a project if it doesn't exist yet
        project = project_manager.create_project(
            name="Feature Development",
            repo="owner/repo",
            template="basic"
        )
        print(f"Created project: {project['name']}")
        
        # Add the issue to the project
        card = project_manager.add_issue_to_project(
            project_id=project["id"],
            repo="owner/repo",
            issue_number=issue["number"],
            column_name="To Do"
        )
        print(f"Added issue to project column: {card['column']}")
        
        # Convert tasks to sub-issues
        sub_issues = issue_manager.convert_tasks_to_issues(
            repo="owner/repo",
            issue_number=issue["number"],
            labels=["task"]
        )
        print(f"Created {len(sub_issues)} sub-issues")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```
