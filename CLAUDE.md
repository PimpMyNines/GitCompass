# GitCompass - Agent Reference Guide

## Essential Commands

```bash
# Development Workflow
make develop      # Install in development mode with dependencies
make lint         # Run linters (flake8, mypy, isort)
make test         # Run all tests
make coverage     # Run tests with coverage report
make format       # Auto-format with black

# Project Structure Exploration
find src -type f -name "*.py" | sort  # List all Python files
grep -r "class " --include="*.py" src # Find all classes
```

## Project Architecture

```
src/gitcompass/          # Main package
├── auth/                # GitHub authentication
├── issues/              # Issue and sub-issue management
├── projects/            # Project board management
├── roadmap/             # Milestone/roadmap features
├── templates/           # Template definitions
└── utils/               # Shared utilities
    ├── config.py        # Configuration handling
    └── templates.py     # Template management
```

## Testing Infrastructure

- **Unit tests**: `tests/unit/` - Mock-based component testing
- **Integration tests**: `tests/integration/` - Tests with GitHub API mocks
- **Mock fixtures**: `tests/fixtures/` - Contains API response mocks
- **Run specific test**: `python -m pytest tests/unit/test_config.py -v`

## Template System

Templates are stored in three locations (in order of precedence):
1. Current directory: `./.gitcompass/templates/`
2. User home: `~/.gitcompass/templates/`
3. Package: `src/gitcompass/templates/`

Template types:
- `issue`: Issue templates with fields and metadata
- `project`: Project board templates with columns
- `roadmap`: Milestone templates with timeframes

## Common Issues and Solutions

- **Authentication errors**: Check environment var `GITHUB_TOKEN` or config file
- **Import errors**: Use `from gitcompass.module import Class` (not src.gitcompass)
- **Rate limiting**: The auth module handles GitHub API rate limiting
- **Template not found**: Check path and ensure template type matches