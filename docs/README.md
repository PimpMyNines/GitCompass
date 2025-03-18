# GitCompass Documentation

## Introduction

GitCompass is a comprehensive Python-based tool for managing GitHub projects, issues, sub-issues, and roadmaps. It provides a robust alternative to bash scripts with better error handling, cross-platform support, and access to the full GitHub API.

## Installation

```bash
# Clone the repository
git clone https://github.com/PimpMyNines/github-project-management.git

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Configuration

GitCompass can be configured using:

1. Environment variables (prefixed with `GITCOMPASS_`)
2. Configuration files
3. Command-line parameters

### Configuration File

Create a configuration file at one of these locations:

1. Current directory: `config.yaml`
2. User home directory: `~/.gitcompass/config.yaml`
3. Custom location, set with `GITCOMPASS_CONFIG` environment variable

Example configuration file (`config.yaml`):

```yaml
# Authentication settings
auth:
  method: token
  token: "your-github-token"

# Default settings
defaults:
  repository: owner/repo
  organization: your-org
  labels:
    - bug
    - enhancement
```

## Authentication

Authenticate with GitHub using one of the following methods:

1. Set the `GITHUB_TOKEN` environment variable
2. Add your token to the configuration file
3. Use GitHub App authentication (for more advanced scenarios)

```bash
# Set token in environment
export GITHUB_TOKEN=your-github-token
```

## Command-Line Usage

### Managing Issues

```bash
# Create an issue
gitcompass issues create --repo owner/repo --title "Issue title" --body "Issue description"

# Create a sub-issue
gitcompass issues create --repo owner/repo --title "Sub-issue title" --parent 123

# Convert tasks to sub-issues
gitcompass issues convert-tasks --repo owner/repo --issue 123
```

### Managing Projects

```bash
# Create a project
gitcompass projects create --name "Project Name" --repo owner/repo

# Create a project with advanced template
gitcompass projects create --name "Detailed Project" --template advanced --org your-org

# Add issue to project
gitcompass projects add-issue --project-id 12345 --repo owner/repo --issue 123 --column "To Do"
```

### Managing Roadmaps

```bash
# Create a milestone
gitcompass roadmap create --repo owner/repo --title "v1.0 Release" --due-date 2023-12-31

# Generate roadmap report
gitcompass roadmap report --repo owner/repo

# Save roadmap report to file
gitcompass roadmap report --repo owner/repo --output roadmap.md
```

## Dry Run Mode

Most commands support a `--dry-run` (or `-d`) flag to show what would be done without making actual changes:

```bash
gitcompass issues create --repo owner/repo --title "Test Issue" --dry-run
```

## Python API Usage

GitCompass can also be used as a Python library:

```python
from gitcompass.auth.github_auth import GitHubAuth
from gitcompass.issues.issue_manager import IssueManager
from gitcompass.utils.config import Config

# Initialize configuration and authentication
config = Config()
auth = GitHubAuth(config)

# Create an issue manager
issue_manager = IssueManager(auth)

# Create an issue
issue = issue_manager.create_issue(
    repo="owner/repo",
    title="Issue title",
    body="Issue description",
    labels=["bug", "high-priority"],
    assignees=["username"]
)

# Print result
print(f"Created issue #{issue['number']}")
```

## Error Handling

GitCompass provides informative error messages and handles GitHub API rate limiting. If a command fails, the error message will provide details about what went wrong and how to fix it.

## Troubleshooting

If you encounter issues:

1. Check your GitHub token permissions
2. Verify configuration file format
3. Run commands with `--verbose` flag for more detailed output
4. Look for error messages in the logs

## More Information

See additional documentation files for more information on specific topics:

- [API Reference](./API_REFERENCE.md)
- [Configuration Guide](./CONFIGURATION.md)
- [Advanced Features](./ADVANCED_FEATURES.md)
