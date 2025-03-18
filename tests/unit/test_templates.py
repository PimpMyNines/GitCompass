"""Unit tests for the template manager module."""

import os
import tempfile
from unittest.mock import patch, mock_open, MagicMock
import json
import yaml

import pytest

from src.gitcompass.utils.templates import TemplateManager
from src.gitcompass.utils.config import Config


@pytest.fixture
def mock_config():
    """Create a mock configuration object."""
    config = MagicMock(spec=Config)
    return config


@pytest.fixture
def template_manager(mock_config):
    """Create a template manager with mocked config."""
    return TemplateManager(mock_config)


def test_get_template_dirs():
    """Test retrieving template directories."""
    # Create a temporary directory to use as cwd
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a mock config
        config = MagicMock(spec=Config)
        
        # Create a template manager
        template_manager = TemplateManager(config)
        
        # Create expected paths
        cwd_templates = os.path.join(temp_dir, ".gitcompass", "templates")
        home_templates = os.path.join(temp_dir, "home", ".gitcompass", "templates")
        pkg_templates = os.path.join(temp_dir, "pkg", "..", "templates")
        
        # Mock the os.path functions and os.path.join to return our expected paths
        with patch('os.path.isdir', return_value=True), \
             patch('os.getcwd', return_value=temp_dir), \
             patch('os.path.expanduser', return_value=os.path.join(temp_dir, "home")), \
             patch('os.path.dirname', return_value=os.path.join(temp_dir, "pkg")), \
             patch('os.path.join', side_effect=lambda *args: "/".join(args)):
            
            # Get template directories
            dirs = template_manager._get_template_dirs()
            
            # Should have 3 directories (cwd, home, package)
            assert len(dirs) == 3
            
            # Convert expected paths to use forward slashes for consistency
            expected_cwd = cwd_templates.replace(os.sep, "/")
            expected_home = home_templates.replace(os.sep, "/")
            expected_pkg = pkg_templates.replace(os.sep, "/")
            
            assert expected_cwd in [d.replace(os.sep, "/") for d in dirs]
            assert expected_home in [d.replace(os.sep, "/") for d in dirs]
            assert any(d.replace(os.sep, "/").endswith("templates") for d in dirs)


def test_list_templates(template_manager):
    """Test listing available templates."""
    # Mock template directory structure
    with patch.object(template_manager, '_template_dirs', ['/tmp/templates']), \
         patch('os.listdir', side_effect=[
             ['issue', 'project'],  # Root directories
             ['bug.yaml', 'feature.yaml'],  # Issue templates
             ['kanban.yml']  # Project templates
         ]), \
         patch('os.path.isdir', return_value=True):
        
        # List all templates
        templates = template_manager.list_templates()
        
        # Should have both template types
        assert 'issue' in templates
        assert 'project' in templates
        
        # Should have the correct template names
        assert sorted(templates['issue']) == ['bug', 'feature']
        assert templates['project'] == ['kanban']


def test_get_template(template_manager):
    """Test getting a template by name and type."""
    test_template = {
        'name': 'Bug Report',
        'description': 'Template for bug reports',
        'labels': ['bug']
    }
    
    # Mock template file reading
    with patch('os.path.isfile', return_value=True), \
         patch('builtins.open', mock_open(read_data=yaml.dump(test_template))), \
         patch.object(template_manager, '_template_dirs', ['/tmp/templates']):
        
        # Get template
        template = template_manager.get_template('bug', 'issue')
        
        # Should match test template
        assert template == test_template


def test_create_template(template_manager):
    """Test creating a new template."""
    test_template = {
        'name': 'Test Template',
        'description': 'Test description'
    }
    
    # Mock directory creation and file writing
    with patch('os.makedirs') as mock_makedirs, \
         patch('builtins.open', mock_open()) as mock_file, \
         patch('yaml.dump') as mock_yaml_dump:
        
        # Create template
        result = template_manager.create_template(
            template_name='test',
            template_type='issue',
            template_data=test_template,
            description='Custom description',
            global_template=False
        )
        
        # Should have created the directory
        mock_makedirs.assert_called_once()
        
        # Should have opened a file for writing
        mock_file.assert_called_once()
        
        # Should have written the template with yaml.dump
        mock_yaml_dump.assert_called_once()
        
        # Description should be in the template data
        template_data = mock_yaml_dump.call_args[0][0]
        assert 'description' in template_data
        assert template_data['description'] == 'Custom description'


def test_apply_template(template_manager):
    """Test applying a template with override values."""
    base_template = {
        'name': 'Base Template',
        'description': 'Base description',
        'nested': {
            'key1': 'value1',
            'key2': 'value2'
        }
    }
    
    override_values = {
        'description': 'Override description',
        'nested': {
            'key1': 'new_value1'
        }
    }
    
    # Mock getting the template
    with patch.object(template_manager, 'get_template', return_value=base_template):
        # Apply template with overrides
        result = template_manager.apply_template(
            template_name='test',
            template_type='issue',
            override_values=override_values
        )
        
        # Base values should be preserved
        assert result['name'] == 'Base Template'
        
        # Overrides should be applied
        assert result['description'] == 'Override description'
        
        # Nested overrides should work
        assert result['nested']['key1'] == 'new_value1'
        
        # Non-overridden nested values should remain
        assert result['nested']['key2'] == 'value2'


def test_template_not_found(template_manager):
    """Test behavior when template is not found."""
    # Mock empty template dirs
    with patch.object(template_manager, '_template_dirs', ['/nonexistent']), \
         patch('os.path.isfile', return_value=False):
        
        # Get non-existent template
        template = template_manager.get_template('nonexistent', 'issue')
        
        # Should return None
        assert template is None
        
        # Try to apply non-existent template
        with pytest.raises(ValueError, match="Template 'nonexistent' of type 'issue' not found"):
            template_manager.apply_template('nonexistent', 'issue')


def test_export_template(template_manager):
    """Test exporting a template to a file."""
    test_template = {
        'name': 'Export Template',
        'description': 'Template for testing export'
    }
    
    # Mock getting the template and file writing
    with patch.object(template_manager, 'get_template', return_value=test_template), \
         patch('builtins.open', mock_open()) as mock_file, \
         patch('json.dump') as mock_json_dump, \
         patch('yaml.dump') as mock_yaml_dump:
        
        # Export as JSON
        template_manager.export_template('test', 'issue', 'output.json')
        
        # Should have called json.dump
        mock_json_dump.assert_called_once()
        
        # Export as YAML
        template_manager.export_template('test', 'issue', 'output.yaml')
        
        # Should have called yaml.dump
        mock_yaml_dump.assert_called_once()


def test_import_template(template_manager):
    """Test importing a template from a file."""
    test_template = {
        'name': 'Import Template',
        'description': 'Template for testing import'
    }
    
    # Mock file reading and template creation
    with patch('os.path.isfile', return_value=True), \
         patch('builtins.open', mock_open(read_data=json.dumps(test_template))), \
         patch('json.load', return_value=test_template), \
         patch.object(template_manager, 'create_template', return_value='/path/to/template.yaml') as mock_create:
        
        # Import template from JSON
        result = template_manager.import_template(
            input_path='input.json',
            template_name='imported',
            template_type='issue'
        )
        
        # Should have called create_template with the loaded data
        mock_create.assert_called_once_with(
            template_name='imported',
            template_type='issue',
            template_data=test_template,
            global_template=False
        )
        
        # Should return the path from create_template
        assert result == '/path/to/template.yaml'


def test_import_template_invalid_file(template_manager):
    """Test importing an invalid template file."""
    # Mock file reading with invalid content
    with patch('os.path.isfile', return_value=True), \
         patch('builtins.open', mock_open(read_data='not valid json or yaml')), \
         patch('json.load', side_effect=json.JSONDecodeError('Invalid JSON', '', 0)), \
         patch('yaml.safe_load', side_effect=yaml.YAMLError):
        
        # Import should raise ValueError
        with pytest.raises(ValueError, match="Failed to read template file"):
            template_manager.import_template(
                input_path='invalid.json',
                template_name='invalid',
                template_type='issue'
            )


def test_deep_update():
    """Test deep update of dictionaries."""
    # Create a template manager
    config = MagicMock(spec=Config)
    template_manager = TemplateManager(config)
    
    # Test dictionaries
    original = {
        'key1': 'value1',
        'nested': {
            'nested_key1': 'nested_value1',
            'nested_key2': 'nested_value2'
        },
        'list': [1, 2, 3]
    }
    
    update = {
        'key1': 'new_value1',
        'nested': {
            'nested_key1': 'new_nested_value1',
            'nested_key3': 'nested_value3'
        },
        'new_key': 'new_value'
    }
    
    # Apply deep update
    template_manager._deep_update(original, update)
    
    # Check results
    assert original['key1'] == 'new_value1'  # Top-level override
    assert original['nested']['nested_key1'] == 'new_nested_value1'  # Nested override
    assert original['nested']['nested_key2'] == 'nested_value2'  # Preserved nested value
    assert original['nested']['nested_key3'] == 'nested_value3'  # New nested value
    assert original['new_key'] == 'new_value'  # New top-level key
    assert original['list'] == [1, 2, 3]  # Preserved list