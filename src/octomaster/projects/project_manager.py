"""GitHub project management module."""

from typing import Dict, List, Any, Optional, Union
import github
from github import Github
from octomaster.auth.github_auth import GitHubAuth

class ProjectManager:
    """Manage GitHub projects."""

    def __init__(self, auth: GitHubAuth):
        """Initialize project manager.

        Args:
            auth: GitHub authentication instance
        """
        self.auth = auth
        self.github = auth.client

    def create_project(self, 
                      name: str, 
                      body: str = "", 
                      org: Optional[str] = None,
                      repo: Optional[str] = None,
                      template: str = "basic") -> Dict[str, Any]:
        """Create a new GitHub project.

        Args:
            name: Project name
            body: Project description
            org: Organization name (if creating org project)
            repo: Repository name (if creating repo project)
            template: Project template to use

        Returns:
            Dictionary with project information
        """
        # Determine if this is an org, repo, or user project
        if org:
            # Create org project
            organization = self.github.get_organization(org)
            project = organization.create_project(name=name, body=body)
        elif repo:
            # Create repo project
            repository = self.github.get_repo(repo)
            project = repository.create_project(name=name, body=body)
        else:
            # Create user project
            user = self.github.get_user()
            project = user.create_project(name=name, body=body)
            
        # Configure project based on template
        if template == "basic":
            self._configure_basic_project(project)
        elif template == "advanced":
            self._configure_advanced_project(project)
            
        return {
            "id": project.id,
            "name": project.name,
            "body": project.body,
            "html_url": project.html_url,
            "columns": self._get_project_columns(project)
        }

    def _configure_basic_project(self, project: github.Project.Project) -> None:
        """Configure a basic project with standard columns.

        Args:
            project: GitHub project object
        """
        # Create standard columns
        project.create_column("To Do")
        project.create_column("In Progress")
        project.create_column("Done")

    def _configure_advanced_project(self, project: github.Project.Project) -> None:
        """Configure an advanced project with detailed columns.

        Args:
            project: GitHub project object
        """
        # Create detailed columns
        project.create_column("Backlog")
        project.create_column("To Do")
        project.create_column("In Progress")
        project.create_column("Review")
        project.create_column("Testing")
        project.create_column("Done")

    def _get_project_columns(self, project: github.Project.Project) -> List[Dict[str, Any]]:
        """Get project columns.

        Args:
            project: GitHub project object

        Returns:
            List of columns with their information
        """
        columns = []
        for column in project.get_columns():
            columns.append({
                "id": column.id,
                "name": column.name
            })
            
        return columns

    def add_issue_to_project(self, 
                          project_id: int, 
                          repo: str, 
                          issue_number: int,
                          column_name: Optional[str] = None) -> Dict[str, Any]:
        """Add an issue to a project column.

        Args:
            project_id: Project ID
            repo: Repository name in format "owner/repo"
            issue_number: Issue number
            column_name: Column name (if None, adds to first column)

        Returns:
            Dictionary with card information
        """
        # Get the issue
        repository = self.github.get_repo(repo)
        issue = repository.get_issue(issue_number)
        
        # Get the project and column
        for proj in self.github.get_user().get_projects():
            if proj.id == project_id:
                project = proj
                break
        else:
            # If not found in user projects, check org projects
            owner, _ = repo.split('/')
            for proj in self.github.get_organization(owner).get_projects():
                if proj.id == project_id:
                    project = proj
                    break
            else:
                # If still not found, check repo projects
                for proj in repository.get_projects():
                    if proj.id == project_id:
                        project = proj
                        break
                else:
                    raise ValueError(f"Project with ID {project_id} not found")
        
        # Get the target column
        if column_name:
            for column in project.get_columns():
                if column.name.lower() == column_name.lower():
                    target_column = column
                    break
            else:
                raise ValueError(f"Column '{column_name}' not found in project")
        else:
            # Default to first column
            target_column = project.get_columns()[0]
        
        # Create card in the column
        card = target_column.create_card(content_id=issue.id, content_type="Issue")
        
        return {
            "id": card.id,
            "project_id": project.id,
            "issue_number": issue_number,
            "column": target_column.name
        }
        
    def get_project(self, project_id: int, repo: Optional[str] = None, org: Optional[str] = None) -> Dict[str, Any]:
        """Get a project by ID.

        Args:
            project_id: Project ID
            repo: Repository name in format "owner/repo" (optional)
            org: Organization name (optional)

        Returns:
            Project information
        """
        # Check repo projects first if repo is provided
        if repo:
            repository = self.github.get_repo(repo)
            for proj in repository.get_projects():
                if proj.id == project_id:
                    project = proj
                    break
            else:
                project = None
        # Check org projects if org is provided
        elif org:
            organization = self.github.get_organization(org)
            for proj in organization.get_projects():
                if proj.id == project_id:
                    project = proj
                    break
            else:
                project = None
        # Otherwise, check user projects
        else:
            user = self.github.get_user()
            for proj in user.get_projects():
                if proj.id == project_id:
                    project = proj
                    break
            else:
                project = None

        if not project:
            raise ValueError(f"Project with ID {project_id} not found")

        # Get project info
        return {
            "id": project.id,
            "name": project.name,
            "body": project.body,
            "html_url": project.html_url,
            "columns": self._get_project_columns(project),
            "cards": self._get_project_cards(project)
        }
        
    def _get_project_cards(self, project: github.Project.Project) -> Dict[str, List]:
        """Get all cards in a project organized by column.

        Args:
            project: GitHub project object

        Returns:
            Dictionary with columns as keys and lists of cards as values
        """
        cards_by_column = {}
        
        for column in project.get_columns():
            column_cards = []
            for card in column.get_cards():
                card_info = {
                    "id": card.id,
                    "note": card.note
                }
                
                # Get issue info if card is linked to an issue
                if card.content_url:
                    # Extract issue URL from content_url
                    parts = card.content_url.split('/')
                    if len(parts) >= 2:
                        issue_number = int(parts[-1])
                        repo_owner = parts[-4]
                        repo_name = parts[-3]
                        
                        try:
                            repo = self.github.get_repo(f"{repo_owner}/{repo_name}")
                            issue = repo.get_issue(issue_number)
                            
                            card_info["issue"] = {
                                "number": issue.number,
                                "title": issue.title,
                                "state": issue.state,
                                "html_url": issue.html_url
                            }
                        except Exception:
                            # If issue can't be loaded, just include the number
                            card_info["issue"] = {
                                "number": issue_number
                            }
                    
                column_cards.append(card_info)
                
            cards_by_column[column.name] = column_cards
            
        return cards_by_column
