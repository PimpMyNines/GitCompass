# OctoMaster Project Guide for Claude

This guide contains useful information for AI assistants working on the OctoMaster project.

## Project Overview

OctoMaster is a Python-based GitHub project management tool that provides comprehensive management for GitHub projects, issues, sub-issues, and roadmaps. It replaces bash scripts with a more robust Python solution.

## Development Environment

### Installation

```bash
# Clone the repository
git clone https://github.com/PimpMyNines/github-project-management.git

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
# Or use make
make develop
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific tests
python -m pytest tests/unit/test_config.py

# Run with coverage
python -m pytest --cov=src/octomaster
```

### Common Development Tasks

```bash
# Format code
make format

# Run linting
make lint

# Build Docker image
make docker-build

# Clean up build artifacts
make clean
```

## Project Structure

- `src/octomaster/` - Main package code
  - `auth/` - Authentication handling
  - `issues/` - Issue management
  - `projects/` - Project management
  - `roadmap/` - Roadmap/milestone handling
  - `utils/` - Utility functions
  - `cli.py` - Command-line interface

- `tests/` - Test suite
  - `unit/` - Unit tests
  - `integration/` - Integration tests

- `docs/` - Documentation
- `examples/` - Example scripts
- `config/` - Configuration examples

## CLI Commands

Here are the main CLI commands available in OctoMaster:

```bash
# Get help
octomaster --help

# Get version
octomaster version

# Create an issue
octomaster issues create --repo owner/repo --title "Issue title" --body "Description"

# Create a sub-issue
octomaster issues create --repo owner/repo --title "Sub-issue title" --parent 123

# Convert tasks to sub-issues
octomaster issues convert-tasks --repo owner/repo --issue 123

# Create a project
octomaster projects create --name "Project Name" --repo owner/repo

# Create a milestone
octomaster roadmap create --repo owner/repo --title "v1.0" --due-date 2023-12-31

# Generate roadmap report
octomaster roadmap report --repo owner/repo
```

## GitHub Authentication

For GitHub operations, you need to set up authentication using one of these methods:

```bash
# Method 1: Set environment variable
export GITHUB_TOKEN=your-github-token

# Method 2: Configure in ~/.octomaster/config.yaml
auth:
  token: "your-github-token"
```

## Troubleshooting

- **Issue**: Import errors when running the CLI
  **Solution**: Make sure the package is installed in development mode with `pip install -e .`

- **Issue**: GitHub API authentication failures
  **Solution**: Check that GITHUB_TOKEN is set or configured properly

- **Issue**: Tests fail with module not found errors
  **Solution**: Ensure you're running from the project root and have installed dev dependencies

## Pull Request Process

When submitting a PR, follow these steps:

1. Create a feature branch
2. Make changes and test them
3. Push to GitHub
4. Create PR with a descriptive title and body
5. Reference the PR description file: `PR_DESCRIPTION.md`

## Code Style Conventions

- Use type hints for all function parameters and return values
- Follow black formatting (line length 100)
- Use docstrings for all public methods and functions
- Include doctest examples in docstrings when applicable
- Use snake_case for variables and function names
- Use CamelCase for class names

## Useful Resources

- [PyGithub Documentation](https://pygithub.readthedocs.io/en/latest/)
- [Click Documentation](https://click.palletsprojects.com/)
- [GitHub API Documentation](https://docs.github.com/en/rest)