# GitCompass Project Guide for Claude

This guide contains useful information for AI assistants working on the GitCompass project.

## Project Overview

GitCompass is a Python-based GitHub project management tool that provides comprehensive management for GitHub projects, issues, sub-issues, and roadmaps. It replaces bash scripts with a more robust Python solution.

## Development Environment

### Installation

```bash
# Clone the repository
git clone https://github.com/PimpMyNines/gitcompass.git

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
python -m pytest --cov=src/gitcompass
```

### Common Development Tasks

```bash
# Format code
make format

# Run linting
make lint

# Run tests
make test

# Run tests with coverage
make coverage

# Build Docker image
make docker-build

# Run Docker container
make docker-run

# Clean up build artifacts
make clean

# Build distribution package
make dist

# Install in development mode
make install

# Install development dependencies
make develop
```

## Project Structure

- `src/gitcompass/` - Main package code (Note: transitioning from octomaster)
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

Here are the main CLI commands available in GitCompass:

```bash
# Get help
gitcompass --help

# Get version
gitcompass version

# Create an issue
gitcompass issues create --repo owner/repo --title "Issue title" --body "Description"

# Create a sub-issue
gitcompass issues create --repo owner/repo --title "Sub-issue title" --parent 123

# Convert tasks to sub-issues
gitcompass issues convert-tasks --repo owner/repo --issue 123

# Create a project
gitcompass projects create --name "Project Name" --repo owner/repo

# Create a milestone
gitcompass roadmap create --repo owner/repo --title "v1.0" --due-date 2023-12-31

# Generate roadmap report
gitcompass roadmap report --repo owner/repo
```

## GitHub Authentication

For GitHub operations, you need to set up authentication using one of these methods:

```bash
# Method 1: Set environment variable
export GITHUB_TOKEN=your-github-token

# Method 2: Configure in ~/.gitcompass/config.yaml
auth:
  token: "your-github-token"
```

## Troubleshooting

- **Issue**: Import errors when running the CLI
  **Solution**: Make sure the package is installed in development mode with `make install` or `make develop`

- **Issue**: GitHub API authentication failures
  **Solution**: Check that GITHUB_TOKEN is set or configured properly

- **Issue**: Tests fail with module not found errors
  **Solution**: Ensure you're running from the project root and have installed dev dependencies with `make develop`

- **Issue**: Tests fail with `AssertionError: assert 'github_pat_...' == 'test-token'`
  **Solution**: These are expected failures in test_github_auth.py which checks for a hardcoded test token

- **Issue**: Linting errors when running `make lint`
  **Solution**: Run `make format` first to fix formatting issues, remaining errors should be addressed manually

## CI/CD and Release Process

### GitHub Actions Workflows

The project uses GitHub Actions for CI/CD with the following workflows. All workflows are configured to use the Makefile commands for consistency between local development and CI environments.

- **tests.yml**: Runs tests, linting, and Docker builds on PR and push events
  ```bash
  # Manually trigger tests
  gh workflow run "GitCompass Tests"
  ```

- **publish.yml**: Publishes package to PyPI when releases are created
  ```bash
  # Manual publish to TestPyPI
  gh workflow run "Publish GitCompass to PyPI" -f version=1.0.0
  ```

- **release.yml**: Creates new releases with version bumping and changelog generation
  ```bash
  # Create a new release
  gh workflow run "Create Release" -f version=1.0.0
  ```

### Required Repository Secrets

For the CI/CD pipelines to work, these secrets should be configured:
- `PYPI_API_TOKEN`: Token for publishing to PyPI
- `TEST_PYPI_API_TOKEN`: Token for publishing to TestPyPI
- `CODECOV_TOKEN`: Token for uploading coverage reports

### Release Process

1. Ensure all changes are merged to main
2. Trigger the "Create Release" workflow with the new version
3. The workflow will:
   - Update version in pyproject.toml
   - Create git tag
   - Generate changelog
   - Create GitHub release
   - Trigger the publish workflow

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

## Building and Publishing

Use the Makefile targets for building and installation whenever possible:

```bash
# Build package locally
make dist

# Install locally in development mode
make install

# Install with development dependencies
make develop

# Check built distribution
twine check dist/*

# Upload to TestPyPI (for testing)
twine upload --repository testpypi dist/*

# Upload to PyPI (for production)
twine upload dist/*
```

## Useful Resources

- [PyGithub Documentation](https://pygithub.readthedocs.io/en/latest/)
- [Click Documentation](https://click.palletsprojects.com/)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [Python Packaging User Guide](https://packaging.python.org/guides/distributing-packages-using-setuptools/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## Important Project Conventions

### Makefile Integration

All development tasks and CI/CD workflows should use the Makefile commands whenever possible:

- Local development should use `make` commands instead of direct Python calls 
- GitHub Actions workflows are configured to use Makefile targets for consistency
- When adding new functionality, consider adding appropriate Makefile targets

## Project Renaming History

The project was originally named "OctoMaster" but was renamed to "GitCompass" to better reflect its purpose as a navigation and roadmapping tool for GitHub projects. This renaming was completed in March 2025. The repository URL was also updated from "github-project-management" to "gitcompass".

If you find any remaining references to "OctoMaster" or "octomaster" in the codebase, these should be updated to "GitCompass" or "gitcompass" respectively.

## Directory Structure Transition

The Python package is still transitioning from the `octomaster` directory structure to `gitcompass`. While imports in external code (README examples, documentation) have been updated to use `from gitcompass.xxx import yyy`, the actual directory may still be `src/octomaster/` until the transition is complete. Internal imports may still use `from octomaster.xxx import yyy` until the directory is renamed.

## Note to Future AI Assistants

If you discover any information that would benefit future agents working on this project, please add it to this CLAUDE.md file. This includes:

1. Useful commands for development, testing, or deployment
2. Project-specific workflows or patterns
3. Common issues and their solutions
4. Dependencies and their purposes
5. Updates to the CI/CD process
6. Changes to Makefile targets or GitHub Actions workflows
7. Status of the transition from octomaster to gitcompass directory structure

Always maintain this file's organization and clarity to help future agents assist users more effectively. When working on the project, follow the established conventions and update this document if you learn something that would be useful to future agents.

Never include credits to yourself in commit messages or code comments unless specifically requested.