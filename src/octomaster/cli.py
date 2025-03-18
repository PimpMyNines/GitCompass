#!/usr/bin/env python3
"""Command-line interface for GitCompass."""

import os
import sys

import click

from octomaster.auth.github_auth import GitHubAuth
from octomaster.issues.issue_manager import IssueManager
from octomaster.projects.project_manager import ProjectManager
from octomaster.roadmap.roadmap_manager import RoadmapManager
from octomaster.utils.config import Config

# Note: Package will be renamed to gitcompass but internal imports remain the same
# until directory structure is updated


@click.group()
def main():
    """GitCompass: GitHub Project Management Tool.

    A powerful Python-based tool for managing GitHub projects, issues, sub-issues, and roadmaps.
    """
    pass


@main.group()
def issues():
    """Manage GitHub issues and sub-issues."""
    pass


@issues.command("create")
@click.option("--title", "-t", required=True, help="Issue title")
@click.option("--body", "-b", default="", help="Issue body/description")
@click.option("--repo", "-r", required=True, help="Repository in format owner/repo")
@click.option("--labels", "-l", multiple=True, help="Labels to apply to the issue")
@click.option("--assignees", "-a", multiple=True, help="Users to assign to the issue")
@click.option("--milestone", "-m", type=int, help="Milestone ID")
@click.option("--parent", "-p", type=int, help="Parent issue number for creating sub-issues")
@click.option(
    "--dry-run", "-d", is_flag=True, help="Show what would be done without making changes"
)
def create_issue(title, body, repo, labels, assignees, milestone, parent, dry_run):
    """Create a new GitHub issue."""
    config = Config()
    auth = GitHubAuth(config)
    issue_manager = IssueManager(auth)

    try:
        if dry_run:
            click.echo(f"Would create issue with title: {title}")
            click.echo(f"In repository: {repo}")
            if parent:
                click.echo(f"As a sub-issue of: #{parent}")
            return

        result = issue_manager.create_issue(
            repo=repo,
            title=title,
            body=body,
            labels=labels,
            assignees=assignees,
            milestone=milestone,
            parent_issue=parent,
        )
        click.echo(f"Created issue #{result['number']}: {result['title']}")
        click.echo(f"URL: {result['html_url']}")
    except Exception as e:
        click.echo(f"Error creating issue: {str(e)}", err=True)
        sys.exit(1)


@issues.command("convert-tasks")
@click.option("--repo", "-r", required=True, help="Repository in format owner/repo")
@click.option("--issue", "-i", required=True, type=int, help="Issue number containing tasks")
@click.option("--labels", "-l", multiple=True, help="Labels to apply to created sub-issues")
@click.option(
    "--dry-run", "-d", is_flag=True, help="Show what would be done without making changes"
)
def convert_tasks(repo, issue, labels, dry_run):
    """Convert tasks in an issue to sub-issues."""
    config = Config()
    auth = GitHubAuth(config)
    issue_manager = IssueManager(auth)

    try:
        if dry_run:
            click.echo(f"Would convert tasks in issue #{issue} to sub-issues")
            click.echo(f"In repository: {repo}")
            return

        sub_issues = issue_manager.convert_tasks_to_issues(
            repo=repo, issue_number=issue, labels=labels
        )

        click.echo(f"Created {len(sub_issues)} sub-issues:")
        for sub in sub_issues:
            click.echo(f"  #{sub['number']}: {sub['title']}")
    except Exception as e:
        click.echo(f"Error converting tasks: {str(e)}", err=True)
        sys.exit(1)


@main.group()
def projects():
    """Manage GitHub projects."""
    pass


@projects.command("create")
@click.option("--name", "-n", required=True, help="Project name")
@click.option("--body", "-b", default="", help="Project description")
@click.option("--org", "-o", help="Organization (if not user project)")
@click.option("--repo", "-r", help="Repository (if repo project)")
@click.option(
    "--template",
    "-t",
    type=click.Choice(["basic", "advanced"]),
    default="basic",
    help="Project template type",
)
@click.option(
    "--dry-run", "-d", is_flag=True, help="Show what would be done without making changes"
)
def create_project(name, body, org, repo, template, dry_run):
    """Create a new GitHub project."""
    config = Config()
    auth = GitHubAuth(config)
    project_manager = ProjectManager(auth)

    try:
        if dry_run:
            click.echo(f"Would create project: {name}")
            if org:
                click.echo(f"In organization: {org}")
            elif repo:
                click.echo(f"In repository: {repo}")
            else:
                click.echo("As a user project")
            click.echo(f"Using template: {template}")
            return

        result = project_manager.create_project(
            name=name, body=body, org=org, repo=repo, template=template
        )
        click.echo(f"Created project: {result['name']}")
        click.echo(f"URL: {result['html_url']}")

        # Display columns
        if result["columns"]:
            click.echo("Columns:")
            for column in result["columns"]:
                click.echo(f"  {column['name']}")
    except Exception as e:
        click.echo(f"Error creating project: {str(e)}", err=True)
        sys.exit(1)


@main.group()
def roadmap():
    """Manage roadmap and milestones."""
    pass


@roadmap.command("create")
@click.option("--title", "-t", required=True, help="Milestone title")
@click.option("--due-date", "-d", help="Due date (YYYY-MM-DD format)")
@click.option("--description", help="Milestone description")
@click.option("--repo", "-r", required=True, help="Repository in format owner/repo")
@click.option(
    "--dry-run", "-d", is_flag=True, help="Show what would be done without making changes"
)
def create_milestone(title, due_date, description, repo, dry_run):
    """Create a new milestone for roadmap."""
    config = Config()
    auth = GitHubAuth(config)
    roadmap_manager = RoadmapManager(auth)

    try:
        if dry_run:
            click.echo(f"Would create milestone: {title}")
            click.echo(f"In repository: {repo}")
            if due_date:
                click.echo(f"Due date: {due_date}")
            return

        result = roadmap_manager.create_milestone(
            repo=repo, title=title, due_date=due_date, description=description
        )
        click.echo(f"Created milestone: {result['title']}")
        if result["due_on"]:
            click.echo(f"Due date: {result['due_on']}")
        click.echo(f"URL: {result['html_url']}")
    except Exception as e:
        click.echo(f"Error creating milestone: {str(e)}", err=True)
        sys.exit(1)


@roadmap.command("report")
@click.option("--repo", "-r", required=True, help="Repository in format owner/repo")
@click.option(
    "--output", "-o", help="Output file path for the report (if not specified, prints to console)"
)
def generate_report(repo, output):
    """Generate a roadmap progress report."""
    config = Config()
    auth = GitHubAuth(config)
    roadmap_manager = RoadmapManager(auth)

    try:
        report = roadmap_manager.generate_roadmap_report(repo)

        if output:
            with open(output, "w") as f:
                f.write(report)
            click.echo(f"Roadmap report saved to: {output}")
        else:
            click.echo(report)
    except Exception as e:
        click.echo(f"Error generating roadmap report: {str(e)}", err=True)
        sys.exit(1)


@main.command("version")
def version():
    """Show the GitCompass version."""
    from octomaster import __version__

    click.echo(f"GitCompass version {__version__}")


if __name__ == "__main__":
    main()
