# GitCompass - Essential Guide

## Key Commands

```bash
# Setup & Development
make develop      # Install in development mode
make lint         # Lint code (run before committing)
make test         # Run tests
make coverage     # Tests with coverage report
make format       # Auto-format code with black

# Build & Distribution
make dist         # Build distribution packages
make docker-build # Build Docker image
```

## Project Structure

```
src/gitcompass/       # Main package
├── auth/             # Authentication modules
├── issues/           # Issue management 
├── projects/         # Project management
├── roadmap/          # Roadmap & milestones
└── utils/            # Shared utilities & config
```

## Authentication

```bash
# Option 1: Environment variable
export GITHUB_TOKEN=your-github-token

# Option 2: Config file (~/.gitcompass/config.yaml)
auth:
  token: "your-github-token"
  # Optional: GitHub Enterprise settings
  api_url: "https://github.example.com/api/v3"
```

## Code Style

- Use type hints consistently
- Black formatting (line length 100)
- Snake_case for variables/functions, CamelCase for classes
- All classes should have docstrings
- New features require unit tests
- Main modules: auth, issues, projects, roadmap

## Common Solutions

- Import paths: `from gitcompass.module import Class` (not src.gitcompass)
- API mocking: Use fixtures in `tests/conftest.py` for unit tests
- Rate limiting: The auth module handles retries with exponential backoff
- Default repo: Set `default_repo: "owner/repo"` in config.yaml
- Logging: Configure in ~/.gitcompass/config.yaml (level INFO by default)

## Test Data Patterns

- Test fixtures in tests/conftest.py
- Mock responses in tests/fixtures/
- All API tests should handle non-deterministic data
- Use Pytest parametrize for testing edge cases