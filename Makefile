# OctoMaster Makefile

.PHONY: all install test lint format clean docs

# Default target
all: install test lint

# Install the package in development mode
install:
	pip install -e .

# Install development dependencies
develop:
	pip install -e ".[dev]"
	# Create necessary directories
	mkdir -p ~/.octomaster/logs

# Run tests
test:
	python -m pytest

# Run tests with coverage
coverage:
	python -m pytest --cov=src/octomaster --cov-report=html --cov-report=term

# Run linting checks
lint:
	flake8 src/octomaster
	# TODO: Add mypy once type hints are more complete
	# mypy src/octomaster

# Format code
format:
	black src/octomaster tests
	isort src/octomaster tests

# Clean up build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build documentation
docs:
	echo "Documentation generation to be implemented"

# Package for distribution
dist: clean
	python -m build

# Docker commands
docker-build:
	docker build -t octomaster:latest .

docker-run:
	docker run -it --rm -e GITHUB_TOKEN=${GITHUB_TOKEN} octomaster:latest
