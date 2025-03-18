"""Unit tests for GitCompass GitHub authentication module."""

import os
from unittest.mock import MagicMock, patch

import pytest

from src.gitcompass.auth.github_auth import GitHubAuth
from src.gitcompass.utils.config import Config


@pytest.fixture
def mock_config():
    """Create a mock configuration object."""
    config = MagicMock(spec=Config)
    config.get.return_value = "test-token"
    config.has.return_value = True
    
    # Ensure that environment variable doesn't interfere with tests
    with patch.dict(os.environ, {"GITHUB_TOKEN": ""}, clear=True):
        yield config


@pytest.fixture
def mock_github():
    """Create a mock GitHub client object."""
    github_mock = MagicMock()
    return github_mock


@patch("src.gitcompass.auth.github_auth.Github")
def test_init_with_token(mock_github_class, mock_config):
    """Test initialization with a token."""
    # Arrange
    mock_github_instance = MagicMock()
    mock_github_class.return_value = mock_github_instance

    # Act
    auth = GitHubAuth(mock_config)

    # Assert
    assert auth._token == "test-token"
    mock_github_class.assert_called_once_with("test-token")
    assert auth._github_client == mock_github_instance


@patch("src.gitcompass.auth.github_auth.Github")
def test_init_with_env_token(mock_github_class):
    """Test initialization with a token from environment."""
    # Arrange
    mock_github_instance = MagicMock()
    mock_github_class.return_value = mock_github_instance

    # Mock environment variables
    with patch.dict(os.environ, {"GITHUB_TOKEN": "env-token"}):
        # Mock config that doesn't have a token
        config = MagicMock(spec=Config)
        config.get.return_value = None
        config.has.return_value = False

        # Act
        auth = GitHubAuth(config)

        # Assert
        assert auth._token == "env-token"
        mock_github_class.assert_called_once_with("env-token")


@patch("src.gitcompass.auth.github_auth.Github")
def test_missing_token(mock_github_class):
    """Test initialization with no token raises error."""
    # Arrange
    # Mock config that doesn't have a token
    config = MagicMock(spec=Config)
    config.get.return_value = None
    config.has.return_value = False

    # Remove environment variable if it exists
    with patch.dict(os.environ, {"GITHUB_TOKEN": ""}, clear=True):
        # Act & Assert
        with pytest.raises(ValueError, match="GitHub token not found"):
            GitHubAuth(config)


def test_client_property(mock_config):
    """Test the client property."""
    # Arrange
    auth = GitHubAuth(mock_config)
    mock_client = MagicMock()
    auth._github_client = mock_client

    # Act
    client = auth.client

    # Assert
    assert client == mock_client


def test_get_token(mock_config):
    """Test getting the token."""
    # Arrange
    auth = GitHubAuth(mock_config)
    auth._token = "test-token"

    # Act
    token = auth.get_token()

    # Assert
    assert token == "test-token"


def test_get_repository(mock_config):
    """Test getting a repository."""
    # Arrange
    auth = GitHubAuth(mock_config)
    mock_client = MagicMock()
    mock_repo = MagicMock()
    mock_client.get_repo.return_value = mock_repo
    auth._github_client = mock_client

    # Act
    repo = auth.get_repo("owner/repo")

    # Assert
    mock_client.get_repo.assert_called_once_with("owner/repo")
    assert repo == mock_repo
