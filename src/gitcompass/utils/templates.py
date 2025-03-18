"""Template management for GitCompass."""

import os
import yaml
from typing import Any, Dict, List, Optional, Union
import json
import shutil
from pathlib import Path

from gitcompass.utils.config import Config


class TemplateManager:
    """Manage templates for GitCompass.
    
    Templates provide standardized configurations for issues, projects,
    and other GitHub resources. They can be used to ensure consistency
    and apply best practices across repositories.
    """
    
    def __init__(self, config: Config):
        """Initialize template manager.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self._template_dirs = self._get_template_dirs()
        
    def _get_template_dirs(self) -> List[str]:
        """Get template directories in order of precedence.
        
        Returns:
            List of template directory paths
        """
        # Templates are searched in this order:
        # 1. Current working directory (.gitcompass/templates)
        # 2. User home directory (~/.gitcompass/templates)
        # 3. Package templates (src/gitcompass/templates)
        
        templates_dirs = []
        
        # Current directory
        cwd_templates = os.path.join(os.getcwd(), ".gitcompass", "templates")
        if os.path.isdir(cwd_templates):
            templates_dirs.append(cwd_templates)
            
        # User home directory
        home_templates = os.path.expanduser("~/.gitcompass/templates")
        if os.path.isdir(home_templates):
            templates_dirs.append(home_templates)
            
        # Package templates
        pkg_templates = os.path.join(os.path.dirname(__file__), "..", "templates")
        if os.path.isdir(pkg_templates):
            templates_dirs.append(pkg_templates)
            
        return templates_dirs
    
    def get_template(self, template_name: str, template_type: str) -> Optional[Dict[str, Any]]:
        """Get a template by name and type.
        
        Args:
            template_name: Name of the template
            template_type: Type of template (issue, project, milestone, etc.)
            
        Returns:
            Template data as dictionary or None if not found
        """
        # Search in all template directories
        for template_dir in self._template_dirs:
            template_path = os.path.join(template_dir, template_type, f"{template_name}.yaml")
            
            if os.path.isfile(template_path):
                try:
                    with open(template_path, "r") as f:
                        return yaml.safe_load(f)
                except Exception as e:
                    print(f"Warning: Failed to load template {template_path}: {str(e)}")
        
        return None
    
    def list_templates(self, template_type: Optional[str] = None) -> Dict[str, List[str]]:
        """List available templates.
        
        Args:
            template_type: Optional filter by template type
            
        Returns:
            Dictionary with template types as keys and lists of template names as values
        """
        templates = {}
        
        for template_dir in self._template_dirs:
            if template_type:
                type_dir = os.path.join(template_dir, template_type)
                if os.path.isdir(type_dir):
                    if template_type not in templates:
                        templates[template_type] = []
                    templates[template_type].extend(self._list_templates_in_dir(type_dir))
            else:
                # List all template types
                for type_name in os.listdir(template_dir):
                    type_path = os.path.join(template_dir, type_name)
                    if os.path.isdir(type_path):
                        if type_name not in templates:
                            templates[type_name] = []
                        templates[type_name].extend(self._list_templates_in_dir(type_path))
        
        return templates
    
    def _list_templates_in_dir(self, directory: str) -> List[str]:
        """List template names in a directory.
        
        Args:
            directory: Directory path
            
        Returns:
            List of template names (without extension)
        """
        template_names = []
        
        for filename in os.listdir(directory):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                template_name = os.path.splitext(filename)[0]
                if template_name not in template_names:
                    template_names.append(template_name)
                    
        return template_names
    
    def create_template(
        self, 
        template_name: str,
        template_type: str,
        template_data: Dict[str, Any],
        description: Optional[str] = None,
        global_template: bool = False
    ) -> str:
        """Create a new template.
        
        Args:
            template_name: Name for the template
            template_type: Type of template (issue, project, milestone, etc.)
            template_data: Template data
            description: Optional template description
            global_template: If True, save to user's home directory instead of working directory
            
        Returns:
            Path to created template file
        """
        # Determine target directory
        if global_template:
            base_dir = os.path.expanduser("~/.gitcompass/templates")
        else:
            base_dir = os.path.join(os.getcwd(), ".gitcompass", "templates")
            
        # Ensure directory exists
        template_dir = os.path.join(base_dir, template_type)
        os.makedirs(template_dir, exist_ok=True)
        
        # Add description to template data
        if description:
            template_data["description"] = description
            
        # Write template file
        template_path = os.path.join(template_dir, f"{template_name}.yaml")
        with open(template_path, "w") as f:
            yaml.dump(template_data, f, default_flow_style=False)
            
        return template_path
    
    def apply_template(
        self, 
        template_name: str,
        template_type: str,
        override_values: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Apply a template, optionally with custom values.
        
        Args:
            template_name: Name of the template
            template_type: Type of template
            override_values: Optional values to override in the template
            
        Returns:
            Template data with overrides applied
            
        Raises:
            ValueError: If template is not found
        """
        template = self.get_template(template_name, template_type)
        
        if not template:
            raise ValueError(f"Template '{template_name}' of type '{template_type}' not found")
            
        # Create a copy of the template
        result = template.copy()
        
        # Apply overrides
        if override_values:
            self._deep_update(result, override_values)
            
        return result
    
    def _deep_update(self, original: Dict[str, Any], update: Dict[str, Any]) -> None:
        """Deep update a dictionary with values from another.
        
        Args:
            original: Dictionary to update
            update: Dictionary with values to apply
        """
        for key, value in update.items():
            if key in original and isinstance(original[key], dict) and isinstance(value, dict):
                self._deep_update(original[key], value)
            else:
                original[key] = value
                
    def export_template(self, template_name: str, template_type: str, output_path: str) -> None:
        """Export a template to a file.
        
        Args:
            template_name: Name of the template
            template_type: Type of template
            output_path: Path to save the exported template
            
        Raises:
            ValueError: If template is not found
        """
        template = self.get_template(template_name, template_type)
        
        if not template:
            raise ValueError(f"Template '{template_name}' of type '{template_type}' not found")
            
        # Determine format from output path
        if output_path.endswith(".json"):
            with open(output_path, "w") as f:
                json.dump(template, f, indent=2)
        else:
            # Default to YAML
            with open(output_path, "w") as f:
                yaml.dump(template, f, default_flow_style=False)
                
    def import_template(
        self,
        input_path: str,
        template_name: str,
        template_type: str,
        global_template: bool = False
    ) -> str:
        """Import a template from a file.
        
        Args:
            input_path: Path to the template file (YAML or JSON)
            template_name: Name for the template
            template_type: Type of template
            global_template: If True, save to user's home directory
            
        Returns:
            Path to imported template file
            
        Raises:
            ValueError: If template file is invalid
        """
        # Read template file
        try:
            if input_path.endswith(".json"):
                with open(input_path, "r") as f:
                    template_data = json.load(f)
            else:
                with open(input_path, "r") as f:
                    template_data = yaml.safe_load(f)
        except Exception as e:
            raise ValueError(f"Failed to read template file: {str(e)}")
            
        if not isinstance(template_data, dict):
            raise ValueError("Template data must be an object/dictionary")
            
        # Create the template
        return self.create_template(
            template_name=template_name,
            template_type=template_type,
            template_data=template_data,
            global_template=global_template
        )