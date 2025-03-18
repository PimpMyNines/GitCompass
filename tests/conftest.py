"""Test fixtures for GitCompass tests."""

import os
import tempfile
import pytest
from unittest.mock import MagicMock, patch

import github

from src.gitcompass.utils.config import Config
from src.gitcompass.auth.github_auth import GitHubAuth


@pytest.fixture
def mock_config():
    """Create a mock configuration object."""
    config = MagicMock(spec=Config)
    config.get.return_value = "test-token"
    config.has.return_value = True
    return config


@pytest.fixture
def mock_github():
    """Create a mock GitHub client object."""
    github_mock = MagicMock()
    return github_mock


@pytest.fixture
def mock_github_auth(mock_config, mock_github):
    """Create a mock GitHub auth object with a mock GitHub client."""
    with patch("github.Github", return_value=mock_github):
        auth = GitHubAuth(mock_config)
        auth._github_client = mock_github
        auth._token = "test-token"
        return auth


@pytest.fixture
def mock_repo():
    """Create a mock GitHub repository."""
    repo = MagicMock(spec=github.Repository.Repository)
    repo.full_name = "owner/repo"
    return repo


@pytest.fixture
def mock_issue():
    """Create a mock GitHub issue."""
    issue = MagicMock(spec=github.Issue.Issue)
    issue.number = 123
    issue.title = "Test Issue"
    issue.body = "Test Issue Body"
    issue.state = "open"
    issue.html_url = "https://github.com/owner/repo/issues/123"
    
    # Mock labels
    label1 = MagicMock()
    label1.name = "bug"
    label2 = MagicMock()
    label2.name = "enhancement"
    issue.labels = [label1, label2]
    
    # Mock assignees
    assignee = MagicMock()
    assignee.login = "testuser"
    issue.assignees = [assignee]
    
    # Mock milestone
    milestone = MagicMock()
    milestone.title = "Test Milestone"
    milestone.number = 1
    issue.milestone = milestone
    
    return issue


@pytest.fixture
def mock_milestone():
    """Create a mock GitHub milestone."""
    milestone = MagicMock(spec=github.Milestone.Milestone)
    milestone.number = 1
    milestone.title = "Test Milestone"
    milestone.description = "Test Description"
    milestone.state = "open"
    milestone.due_on = None
    milestone.html_url = "https://github.com/owner/repo/milestone/1"
    milestone.open_issues = 5
    milestone.closed_issues = 3
    return milestone


@pytest.fixture
def mock_project():
    """Create a mock GitHub project."""
    project = MagicMock(spec=github.Project.Project)
    project.id = 456
    project.name = "Test Project"
    project.body = "Test Project Description"
    project.html_url = "https://github.com/owner/repo/projects/1"
    
    # Mock columns
    column1 = MagicMock()
    column1.id = 1
    column1.name = "To Do"
    
    column2 = MagicMock()
    column2.id = 2
    column2.name = "In Progress"
    
    column3 = MagicMock()
    column3.id = 3
    column3.name = "Done"
    
    project.get_columns.return_value = [column1, column2, column3]
    
    return project


@pytest.fixture
def temp_config_file():
    """Create a temporary configuration file."""
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".yaml", delete=False) as temp_file:
        temp_file.write("""
auth:
  token: test-token
defaults:
  repository: owner/repo
        """)
        temp_file_path = temp_file.name
    
    try:
        yield temp_file_path
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


@pytest.fixture
def real_config(temp_config_file):
    """Create a Config object with the temp config file."""
    return Config(config_file=temp_config_file)