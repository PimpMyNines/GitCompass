#!/usr/bin/env python3
"""Command-line interface for GitCompass."""

import sys
import json
import os

import click

from gitcompass.auth.github_auth import GitHubAuth
from gitcompass.issues.issue_manager import IssueManager
from gitcompass.projects.project_manager import ProjectManager
from gitcompass.roadmap.roadmap_manager import RoadmapManager
from gitcompass.utils.config import Config
from gitcompass.utils.templates import TemplateManager


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
@click.option("--title", "-t", help="Issue title")
@click.option("--body", "-b", help="Issue body/description")
@click.option("--repo", "-r", required=True, help="Repository in format owner/repo")
@click.option("--labels", "-l", multiple=True, help="Labels to apply to the issue")
@click.option("--assignees", "-a", multiple=True, help="Users to assign to the issue")
@click.option("--milestone", "-m", type=int, help="Milestone ID")
@click.option("--parent", "-p", type=int, help="Parent issue number for creating sub-issues")
@click.option("--template", help="Issue template to use")
@click.option(
    "--template-values", 
    help="JSON string or file path with values for template placeholders"
)
@click.option(
    "--interactive", "-i", is_flag=True, help="Interactive mode to fill template values"
)
@click.option(
    "--dry-run", "-d", is_flag=True, help="Show what would be done without making changes"
)
def create_issue(
    title, body, repo, labels, assignees, milestone, parent, 
    template, template_values, interactive, dry_run
):
    """Create a new GitHub issue."""
    config = Config()
    auth = GitHubAuth(config)
    issue_manager = IssueManager(auth)
    
    # Template handling
    template_data = {}
    if template:
        template_manager = TemplateManager(config)
        try:
            template_data = template_manager.get_template(template, "issue")
            if not template_data:
                click.echo(f"Template '{template}' not found. Creating issue without template.")
            else:
                # Apply template values
                if template_values:
                    # Check if it's a file path or JSON string
                    if os.path.isfile(template_values):
                        with open(template_values, 'r') as f:
                            values = json.load(f)
                    else:
                        values = json.loads(template_values)
                        
                    # Use values to fill template
                    template_data = template_manager.apply_template(
                        template_name=template,
                        template_type="issue",
                        override_values=values
                    )
                
                # Fill from template
                if not title and "fields" in template_data and "title" in template_data["fields"]:
                    if interactive:
                        title_prompt = template_data["fields"]["title"].get("description", "Title")
                        title = click.prompt(title_prompt, type=str)
                
                if not body and "fields" in template_data and "body" in template_data["fields"]:
                    template_body = template_data["fields"]["body"].get("template", "")
                    if interactive:
                        # In interactive mode, could open an editor
                        body = click.edit(template_body)
                    else:
                        body = template_body
                
                # Get labels from template if not provided
                if not labels and "labels" in template_data:
                    labels = template_data["labels"]
        except Exception as e:
            click.echo(f"Warning: Error applying template: {str(e)}", err=True)

    # Title is required
    if not title:
        if interactive:
            title = click.prompt("Issue title", type=str)
        else:
            click.echo("Error: Issue title is required. Provide --title or use --interactive.", err=True)
            sys.exit(1)

    try:
        if dry_run:
            click.echo(f"Would create issue with title: {title}")
            click.echo(f"In repository: {repo}")
            if template and template_data:
                click.echo(f"Using template: {template}")
            if body:
                click.echo("\nBody preview (truncated):")
                preview = body[:200] + ("..." if len(body) > 200 else "")
                click.echo(preview)
            if labels:
                click.echo(f"Labels: {', '.join(labels)}")
            if assignees:
                click.echo(f"Assignees: {', '.join(assignees)}")
            if milestone:
                click.echo(f"Milestone: {milestone}")
            if parent:
                click.echo(f"As a sub-issue of: #{parent}")
            return

        result = issue_manager.create_issue(
            repo=repo,
            title=title,
            body=body or "",
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
    help="Project template to use (predefined: 'basic', 'advanced', or custom template name)",
)
@click.option(
    "--template-values", 
    help="JSON string or file path with values for template placeholders"
)
@click.option(
    "--dry-run", "-d", is_flag=True, help="Show what would be done without making changes"
)
def create_project(name, body, org, repo, template, template_values, dry_run):
    """Create a new GitHub project."""
    config = Config()
    auth = GitHubAuth(config)
    project_manager = ProjectManager(auth)
    
    # Default to basic template if none specified
    if not template:
        template = "basic"
    
    # Handle custom templates
    custom_template = None
    if template not in ["basic", "advanced"]:
        template_manager = TemplateManager(config)
        custom_template = template_manager.get_template(template, "project")
        
        if not custom_template:
            click.echo(f"Template '{template}' not found. Using 'basic' template instead.")
            template = "basic"
        else:
            # Apply template values if provided
            if template_values:
                try:
                    # Check if it's a file path or JSON string
                    if os.path.isfile(template_values):
                        with open(template_values, 'r') as f:
                            values = json.load(f)
                    else:
                        values = json.loads(template_values)
                        
                    custom_template = template_manager.apply_template(
                        template_name=template,
                        template_type="project",
                        override_values=values
                    )
                except Exception as e:
                    click.echo(f"Warning: Error applying template values: {str(e)}", err=True)

    try:
        if dry_run:
            click.echo(f"Would create project: {name}")
            if org:
                click.echo(f"In organization: {org}")
            elif repo:
                click.echo(f"In repository: {repo}")
            else:
                click.echo("As a user project")
                
            if custom_template:
                click.echo(f"Using custom template: {template}")
                if "columns" in custom_template:
                    click.echo("With columns:")
                    for column in custom_template["columns"]:
                        column_name = column["name"] if isinstance(column, dict) else column
                        click.echo(f"  - {column_name}")
            else:
                click.echo(f"Using built-in template: {template}")
            return

        # Create the project
        if custom_template and "columns" in custom_template:
            # Use custom columns from template
            result = project_manager.create_project_with_columns(
                name=name, 
                body=body, 
                org=org, 
                repo=repo, 
                columns=custom_template["columns"]
            )
        else:
            # Use built-in template
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
                
        # Handle automation rules if specified in custom template
        if custom_template and "automation" in custom_template:
            click.echo("\nAutomation rules would be applied here.")
            # Note: GitHub API doesn't directly support automation rules via REST API
            # A full implementation would likely use GraphQL or UI automation
            
        # Handle labels if specified in custom template
        if custom_template and "labels" in custom_template and repo:
            click.echo("\nCreating labels from template:")
            repository = auth.client.get_repo(repo)
            for label_info in custom_template["labels"]:
                label_name = label_info["name"]
                label_color = label_info.get("color", "CCCCCC")
                label_description = label_info.get("description", "")
                
                try:
                    repository.create_label(name=label_name, color=label_color, description=label_description)
                    click.echo(f"  - Created label: {label_name}")
                except Exception as e:
                    if "already_exists" in str(e).lower():
                        click.echo(f"  - Label already exists: {label_name}")
                    else:
                        click.echo(f"  - Error creating label {label_name}: {str(e)}")
                        
    except Exception as e:
        click.echo(f"Error creating project: {str(e)}", err=True)
        sys.exit(1)


@main.group()
def roadmap():
    """Manage roadmap and milestones."""
    pass


@roadmap.command("create")
@click.option("--title", "-t", help="Milestone title")
@click.option("--due-date", "-d", help="Due date (YYYY-MM-DD format)")
@click.option("--description", help="Milestone description")
@click.option("--repo", "-r", required=True, help="Repository in format owner/repo")
@click.option("--template", help="Roadmap template to use")
@click.option(
    "--template-values", 
    help="JSON string or file path with values for template placeholders"
)
@click.option(
    "--quarter", help="Quarter identifier (e.g., 'Q1-2023') for template substitution"
)
@click.option(
    "--dry-run", "-d", is_flag=True, help="Show what would be done without making changes"
)
def create_milestone(title, due_date, description, repo, template, template_values, quarter, dry_run):
    """Create a new milestone for roadmap."""
    config = Config()
    auth = GitHubAuth(config)
    roadmap_manager = RoadmapManager(auth)
    
    # Template handling
    template_data = {}
    if template:
        template_manager = TemplateManager(config)
        try:
            template_data = template_manager.get_template(template, "roadmap")
            if not template_data:
                click.echo(f"Template '{template}' not found. Creating milestone without template.")
            else:
                # Apply template values
                values = {}
                
                # If quarter is specified, add it to values for substitution
                if quarter:
                    values["quarter"] = quarter
                
                # If template_values is provided, parse it
                if template_values:
                    if os.path.isfile(template_values):
                        with open(template_values, 'r') as f:
                            file_values = json.load(f)
                    else:
                        file_values = json.loads(template_values)
                    
                    # Update values with file_values
                    values.update(file_values)
                
                # If we have values to apply, use them
                if values:
                    template_data = template_manager.apply_template(
                        template_name=template,
                        template_type="roadmap",
                        override_values={"values": values}
                    )
                
                # If milestone data is in the template, use it
                if "milestones" in template_data and len(template_data["milestones"]) > 0:
                    # For this example, just use the first milestone
                    milestone = template_data["milestones"][0]
                    
                    # Apply any string substitutions
                    if quarter and isinstance(milestone.get("name"), str):
                        if not title:
                            title = milestone["name"].replace("{quarter}", quarter)
                    elif not title and "name" in milestone:
                        title = milestone["name"]
                        
                    if not description and "description" in milestone:
                        if quarter and isinstance(milestone["description"], str):
                            description = milestone["description"].replace("{quarter}", quarter)
                        else:
                            description = milestone["description"]
                    
                    # Handle relative dates if provided
                    if not due_date and "relative_date" in milestone:
                        import datetime
                        import re
                        
                        rel_date = milestone["relative_date"]
                        match = re.match(r"([+-])(\d+)\s+(\w+)", rel_date)
                        if match:
                            sign, amount, unit = match.groups()
                            amount = int(amount)
                            
                            today = datetime.datetime.now()
                            
                            if unit.lower() in ["day", "days"]:
                                delta = datetime.timedelta(days=amount)
                            elif unit.lower() in ["week", "weeks"]:
                                delta = datetime.timedelta(weeks=amount)
                            elif unit.lower() in ["month", "months"]:
                                # Approximate months
                                delta = datetime.timedelta(days=amount * 30)
                            else:
                                # Default to days
                                delta = datetime.timedelta(days=amount)
                                
                            if sign == "+":
                                target_date = today + delta
                            else:
                                target_date = today - delta
                                
                            due_date = target_date.strftime("%Y-%m-%d")
                            
        except Exception as e:
            click.echo(f"Warning: Error applying template: {str(e)}", err=True)
    
    # Title is required
    if not title:
        click.echo("Error: Milestone title is required. Provide --title or use a template.", err=True)
        sys.exit(1)

    try:
        if dry_run:
            click.echo(f"Would create milestone: {title}")
            click.echo(f"In repository: {repo}")
            if description:
                click.echo(f"Description: {description}")
            if due_date:
                click.echo(f"Due date: {due_date}")
            if template and template_data:
                click.echo(f"Using template: {template}")
                
                # If template has labels, show them
                if "labels" in template_data:
                    click.echo("Would create labels:")
                    for label in template_data["labels"]:
                        label_name = label["name"]
                        if quarter:
                            label_name = label_name.replace("{quarter}", quarter)
                        click.echo(f"  - {label_name}")
            return

        # Create the milestone
        result = roadmap_manager.create_milestone(
            repo=repo, title=title, due_date=due_date, description=description
        )
        click.echo(f"Created milestone: {result['title']}")
        if result["due_on"]:
            click.echo(f"Due date: {result['due_on']}")
        click.echo(f"URL: {result['html_url']}")
        
        # If template has labels, create them
        if template and template_data and "labels" in template_data:
            click.echo("\nCreating labels from template:")
            repository = auth.client.get_repo(repo)
            
            for label_info in template_data["labels"]:
                label_name = label_info["name"]
                if quarter:
                    label_name = label_name.replace("{quarter}", quarter)
                    
                label_color = label_info.get("color", "CCCCCC")
                
                label_description = label_info.get("description", "")
                if quarter and isinstance(label_description, str):
                    label_description = label_description.replace("{quarter}", quarter)
                
                try:
                    repository.create_label(name=label_name, color=label_color, description=label_description)
                    click.echo(f"  - Created label: {label_name}")
                except Exception as e:
                    if "already_exists" in str(e).lower():
                        click.echo(f"  - Label already exists: {label_name}")
                    else:
                        click.echo(f"  - Error creating label {label_name}: {str(e)}")
                    
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


@main.group()
def templates():
    """Manage GitCompass templates."""
    pass


@templates.command("list")
@click.option("--type", "-t", help="Template type to filter by")
@click.option("--format", "-f", type=click.Choice(["text", "json"]), default="text", help="Output format")
def list_templates(type, format):
    """List available templates."""
    config = Config()
    template_manager = TemplateManager(config)
    
    templates = template_manager.list_templates(type)
    
    if format == "json":
        click.echo(json.dumps(templates, indent=2))
    else:
        if not templates:
            click.echo("No templates found.")
            return
            
        for template_type, template_names in templates.items():
            click.echo(f"\n{template_type.upper()} TEMPLATES:")
            for name in template_names:
                click.echo(f"  - {name}")


@templates.command("show")
@click.argument("name")
@click.argument("type")
@click.option("--format", "-f", type=click.Choice(["yaml", "json"]), default="yaml", help="Output format")
def show_template(name, type, format):
    """Show template details."""
    config = Config()
    template_manager = TemplateManager(config)
    
    template = template_manager.get_template(name, type)
    
    if not template:
        click.echo(f"Template '{name}' of type '{type}' not found.")
        sys.exit(1)
        
    if format == "json":
        click.echo(json.dumps(template, indent=2))
    else:
        import yaml
        click.echo(yaml.dump(template, default_flow_style=False))


@templates.command("create")
@click.argument("name")
@click.argument("type")
@click.option("--from-file", "-f", help="Path to YAML or JSON file to use as template source")
@click.option("--description", "-d", help="Template description")
@click.option("--global", "is_global", is_flag=True, help="Create as global template")
def create_template(name, type, from_file, description, is_global):
    """Create a new template."""
    config = Config()
    template_manager = TemplateManager(config)
    
    try:
        if from_file:
            # Import from file
            template_path = template_manager.import_template(
                input_path=from_file,
                template_name=name,
                template_type=type,
                global_template=is_global
            )
            click.echo(f"Template created from file: {template_path}")
        else:
            # Create empty template
            template_data = {"name": name}
            if description:
                template_data["description"] = description
                
            template_path = template_manager.create_template(
                template_name=name,
                template_type=type,
                template_data=template_data,
                global_template=is_global
            )
            click.echo(f"Empty template created: {template_path}")
            click.echo("Edit this file to configure the template.")
    except Exception as e:
        click.echo(f"Error creating template: {str(e)}", err=True)
        sys.exit(1)


@templates.command("export")
@click.argument("name")
@click.argument("type")
@click.argument("output_path")
def export_template(name, type, output_path):
    """Export a template to a file."""
    config = Config()
    template_manager = TemplateManager(config)
    
    try:
        template_manager.export_template(name, type, output_path)
        click.echo(f"Template exported to: {output_path}")
    except Exception as e:
        click.echo(f"Error exporting template: {str(e)}", err=True)
        sys.exit(1)


@main.command("version")
def version():
    """Show the GitCompass version."""
    from gitcompass import __version__

    click.echo(f"GitCompass version {__version__}")


if __name__ == "__main__":
    main()
