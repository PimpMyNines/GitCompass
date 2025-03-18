# GitCompass: GitHub Project Management Tool

<div align="center">

![GitCompass Logo](docs/gitcompass-logo.png)

[![Build Status](https://github.com/PimpMyNines/github-project-management/actions/workflows/tests.yml/badge.svg)](https://github.com/PimpMyNines/github-project-management/actions/workflows/tests.yml)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

A powerful Python-based tool for managing GitHub projects, issues, sub-issues, and roadmaps.

## 🌟 Features

- **🔑 Authentication**: Support for both personal access tokens and GitHub Apps
- **📊 Issue Management**: Create issues, sub-issues, and convert task lists to proper sub-issues
- **📋 Project Management**: Create and configure projects, manage columns and cards
- **🗓️ Roadmap Planning**: Create milestones and generate detailed roadmap reports
- **🔄 Cross-Repository Operations**: Work across multiple repositories
- **💼 Flexible Configuration**: Environment variables, config files, and CLI options

## 🚀 Installation

### From PyPI (Coming Soon)

```bash
pip install gitcompass
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/PimpMyNines/github-project-management.git
cd github-project-management

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Option 1: Install with pip
pip install -e .

# Option 2: Install with make
make install
```

### Docker

```bash
# Build the Docker image
docker build -t gitcompass .

# Run with Docker
docker run -it --rm -e GITHUB_TOKEN=your-token gitcompass --help
```

## 📋 Quick Start

### Authentication

Set your GitHub token:

```bash
export GITHUB_TOKEN=your-github-token
```

Or create a config file at `~/.gitcompass/config.yaml`:

```yaml
auth:
  token: "your-github-token"
```

### Using the CLI

```bash
# Create an issue
gitcompass issues create --repo owner/repo --title "New feature" --body "Feature description"

# Create a sub-issue
gitcompass issues create --repo owner/repo --title "Sub-task" --parent 123

# Convert tasks to sub-issues
gitcompass issues convert-tasks --repo owner/repo --issue 123

# Create a project
gitcompass projects create --name "Q2 Development" --repo owner/repo

# Create a milestone
gitcompass roadmap create --repo owner/repo --title "v1.0" --due-date 2023-12-31

# Generate roadmap report
gitcompass roadmap report --repo owner/repo
```

### Python API

```python
from gitcompass.auth.github_auth import GitHubAuth
from gitcompass.issues.issue_manager import IssueManager
from gitcompass.utils.config import Config

# Initialize
config = Config()
auth = GitHubAuth(config)
issue_manager = IssueManager(auth)

# Create an issue
issue = issue_manager.create_issue(
    repo="owner/repo",
    title="API Issue",
    body="Created via Python API",
    labels=["enhancement"]
)

print(f"Created issue #{issue['number']}")
```

## 📚 Documentation

For detailed documentation, see the [docs](./docs) directory:

- [Command-Line Reference](./docs/README.md)
- [API Documentation](./docs/API_REFERENCE.md)
- [Configuration Guide](./docs/CONFIGURATION.md)

## 💻 Examples

Check out the [examples](./examples) directory for practical usage examples:

- [Create Issue Hierarchy](./examples/create_issue_hierarchy.py) - Create parent issues with sub-tasks
- [Advanced Project Setup](./examples/advanced_project_setup.py) - Set up a complete project with milestones

## 🧪 Development

```bash
# Install development dependencies
make develop

# Run tests
make test

# Run linting
make lint

# Format code
make format
```

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTORS.md](./CONTRIBUTORS.md) for details on how to get started.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
