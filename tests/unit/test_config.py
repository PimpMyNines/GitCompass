"""Unit tests for configuration module."""

import os
import tempfile
import pytest
from unittest.mock import patch, mock_open

from src.octomaster.utils.config import Config


def test_config_initialization():
    """Test basic configuration initialization."""
    config = Config()
    assert isinstance(config.config_data, dict)


def test_config_from_file():
    """Test loading configuration from a file."""
    # Create a temporary config file
    config_content = """
    auth:
      token: test-token
    defaults:
      repository: owner/repo
    """
    
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_file.write(config_content)
        temp_file_path = temp_file.name
    
    try:
        # Load config from the temp file
        config = Config(config_file=temp_file_path)
        
        # Verify values were loaded
        assert config.get("auth.token") == "test-token"
        assert config.get("defaults.repository") == "owner/repo"
    finally:
        # Clean up temp file
        os.unlink(temp_file_path)


def test_config_from_environment():
    """Test loading configuration from environment variables."""
    # Set environment variables
    with patch.dict(os.environ, {
        "OCTOMASTER_AUTH_TOKEN": "env-token",
        "OCTOMASTER_DEFAULTS_REPOSITORY": "env-owner/env-repo"
    }):
        config = Config()
        
        # Environment variables should take precedence
        assert config.get("auth.token") == "env-token"
        assert config.get("defaults.repository") == "env-owner/env-repo"


def test_config_get_default():
    """Test getting a value with a default."""
    config = Config()
    
    # Get a value that doesn't exist
    value = config.get("non.existent.key", default="default-value")
    assert value == "default-value"


def test_config_has_key():
    """Test checking if a key exists."""
    # Create config with a known value
    config = Config()
    config.set("test.key", "test-value")
    
    # Check for existing and non-existing keys
    assert config.has("test.key") is True
    assert config.has("non.existent.key") is False


def test_config_set():
    """Test setting a configuration value."""
    config = Config()
    
    # Set a new value
    config.set("new.key", "new-value")
    assert config.get("new.key") == "new-value"
    
    # Update an existing value
    config.set("new.key", "updated-value")
    assert config.get("new.key") == "updated-value"
    
    # Set a nested value
    config.set("nested.key.child", "nested-value")
    assert config.get("nested.key.child") == "nested-value"


def test_config_environment_precedence():
    """Test that environment variables take precedence over file values."""
    # Create a config with file data
    config = Config()
    config.config_data = {
        "auth": {
            "token": "file-token"
        }
    }
    
    # Without environment variable, should get file value
    assert config.get("auth.token") == "file-token"
    
    # With environment variable, should get environment value
    with patch.dict(os.environ, {"OCTOMASTER_AUTH_TOKEN": "env-token"}):
        assert config.get("auth.token") == "env-token"
