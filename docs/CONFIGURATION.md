# GitCompass Configuration Guide

## Overview

GitCompass provides flexible configuration through multiple mechanisms, allowing you to set up the tool according to your workflow needs. This guide explains the available configuration options and how to use them.

## Configuration Sources

GitCompass looks for configuration in the following locations, in order of precedence (highest to lowest):

1. **Command-line arguments**: Parameters passed directly to commands
2. **Environment variables**: Prefixed with `GITCOMPASS_`
3. **Configuration files**: YAML files in specific locations
4. **Default values**: Built-in defaults for any unspecified options

## Configuration Files

GitCompass will look for configuration files in the following locations:

1. Path specified by the `GITCOMPASS_CONFIG` environment variable
2. `config.yaml` in the current working directory
3. `~/.gitcompass/config.yaml` in the user's home directory

The configuration file should be in YAML format, with the following structure:

```yaml
# Authentication settings
auth:
  # Authentication method: token or app
  method: token
  
  # Personal access token
  token: "your-github-token"
  
  # GitHub App settings (optional)
  app:
    app_id: 12345
    installation_id: 67890
    private_key_path: ~/.gitcompass/private-key.pem

# Default repository settings
defaults:
  # Default repository in format owner/repo
  repository: owner/repo
  
  # Default organization
  organization: your-org
  
  # Default labels to apply to created issues
  labels:
    - bug
    - enhancement
  
  # Default project settings
  project:
    template: basic

# API settings
api:
  # Rate limit handling
  rate_limit:
    enabled: true
    sleep_on_limit: true
  
  # Retry settings
  retry:
    max_attempts: 3
    backoff_factor: 2
    status_forcelist: [500, 502, 503, 504]

# Logging settings
logging:
  level: INFO
  file: ~/.gitcompass/logs/gitcompass.log
  format: "%(asctime)s [%(levelname)s] %(message)s"
```

## Environment Variables

Environment variables provide a convenient way to set configuration options without modifying files. GitCompass recognizes the following environment variables:

- `GITHUB_TOKEN`: Your GitHub personal access token
- `GITCOMPASS_CONFIG`: Path to a configuration file
- `GITCOMPASS_AUTH_TOKEN`: Your GitHub personal access token (alternative to `GITHUB_TOKEN`)
- `GITCOMPASS_AUTH_METHOD`: Authentication method (`token` or `app`)
- `GITCOMPASS_DEFAULTS_REPOSITORY`: Default repository in format `owner/repo`
- `GITCOMPASS_DEFAULTS_ORGANIZATION`: Default organization name
- `GITCOMPASS_LOGGING_LEVEL`: Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`)
- `GITCOMPASS_LOGGING_FILE`: Path to log file

Environment variables can be set using:

```bash
# Unix/macOS/Linux
export GITHUB_TOKEN=your-token

# Windows Command Prompt
set GITHUB_TOKEN=your-token

# Windows PowerShell
$env:GITHUB_TOKEN = "your-token"
```

## Command-Line Arguments

Command-line arguments provide the most direct way to configure operations. These options take precedence over environment variables and configuration files.

For example:

```bash
gitcompass issues create --repo owner/repo --title "Issue title" --labels bug enhancement
```

Run `gitcompass --help` to see all available commands and options.

## Authentication

GitCompass supports two authentication methods:

### Personal Access Token

This is the simplest method and recommended for most users:

```yaml
auth:
  method: token
  token: "your-github-token"
```

Or set the environment variable:

```bash
export GITHUB_TOKEN=your-token
```

### GitHub App

For more advanced use cases, you can use a GitHub App for authentication:

```yaml
auth:
  method: app
  app:
    app_id: 12345
    installation_id: 67890
    private_key_path: ~/.gitcompass/private-key.pem
```

## Default Settings

Default settings provide values for when specific options are not provided in commands:

```yaml
defaults:
  repository: owner/repo
  organization: your-org
  labels:
    - bug
    - enhancement
```

With these defaults, you can run commands without specifying all parameters:

```bash
# Uses the default repository from config
gitcompass issues create --title "New issue"

# Instead of having to type
gitcompass issues create --repo owner/repo --title "New issue"
```

## Logging Configuration

Configure logging behavior:

```yaml
logging:
  level: INFO  # DEBUG, INFO, WARNING, ERROR
  file: ~/.gitcompass/logs/gitcompass.log
  format: "%(asctime)s [%(levelname)s] %(message)s"
```

## API Settings

Configure how GitCompass interacts with the GitHub API:

```yaml
api:
  rate_limit:
    enabled: true  # Enable rate limit handling
    sleep_on_limit: true  # Sleep when rate limited
  
  retry:
    max_attempts: 3  # Number of retry attempts for failed API calls
    backoff_factor: 2  # Exponential backoff factor
    status_forcelist: [500, 502, 503, 504]  # HTTP status codes to retry
```

## Tips and Best Practices

1. **Use environment variables for sensitive information**: Don't commit tokens to version control.
2. **Create a configuration file for repeated use**: This avoids having to set the same options repeatedly.
3. **Set default repository**: If you primarily work with one repository, set it as the default.
4. **Configure logging**: Enable logging to help troubleshoot issues.
5. **Use appropriate authentication**: Personal access tokens are simpler, but GitHub Apps provide more granular permissions.

## Troubleshooting

If you're experiencing configuration issues:

1. Run with `--verbose` flag to see debug information
2. Check the log file for errors
3. Verify environment variables are set correctly
4. Ensure configuration files are valid YAML format
5. Confirm you have the necessary GitHub permissions