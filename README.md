# OctoMaster

A powerful Python-based tool for managing GitHub projects, issues, sub-issues, and roadmaps.

## Overview

OctoMaster provides a comprehensive approach to GitHub project management, replacing bash scripts with a more robust Python-based solution. It streamlines issue tracking, project management, and roadmap planning using the GitHub API.

## Features

- **Issue Management**: Create issues and sub-issues, convert tasks to sub-issues
- **Project Management**: Create and configure projects with custom templates
- **Roadmap Management**: Create milestones and generate roadmap reports
- **Cross-Repository Operations**: Work with multiple repositories

## Directory Structure

```
OctoMaster/
├── config/                # Configuration examples and schemas
├── docs/                  # Documentation
├── examples/              # Example scripts
├── src/                   # Source code
│   └── octomaster/
│       ├── auth/          # Authentication handling
│       ├── issues/        # Issue management
│       ├── projects/      # Project management
│       ├── roadmap/       # Roadmap/milestone handling
│       └── utils/         # Utility functions
└── tests/                 # Test suite
    ├── unit/              # Unit tests
    └── integration/       # Integration tests
```

## Installation

```bash
# Clone the repository
git clone https://github.com/PimpMyNines/github-project-management.git

# Navigate to the tool directory
cd github-project-management

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
pip install -e .
```

## Quick Start

1. Set your GitHub token:

```bash
export GITHUB_TOKEN=your-github-token
```

2. Create an issue:

```bash
octomaster issues create --repo owner/repo --title "New feature request" --body "Implement this feature"
```

3. Create a project:

```bash
octomaster projects create --name "Q2 Development" --repo owner/repo
```

## Documentation

See the [docs](./docs) folder for detailed documentation.

## Examples

Check out the [examples](./examples) directory for usage examples.

## Testing

Run the tests with:

```bash
python -m pytest
```

## License

MIT
