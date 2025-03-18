#\!/usr/bin/env python3
import os
import sys
import yaml
import re

# Define the workflows directory
workflows_dir = "/Users/slopresto/Projects/OctoMaster/.github/workflows"

# Define commands that should use Makefile targets
makefile_commands = {
    "install": ["pip install -e ."],
    "develop": ["pip install -e \".[dev]\""],
    "test": ["pytest"],
    "coverage": ["pytest --cov"],
    "lint": ["flake8"],
    "format": ["black", "isort"],
    "clean": ["rm -rf"],
    "dist": ["python -m build"],
    "docker-build": ["docker build"]
}

def check_workflow_file(file_path):
    """Check a workflow file for commands that should use Makefile targets."""
    direct_command_usage = []
    makefile_usage = []
    
    # Load the YAML file
    with open(file_path, 'r') as f:
        try:
            workflow = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error parsing {file_path}: {e}")
            return
    
    # Check for commands in steps
    for job_name, job in workflow.get('jobs', {}).items():
        for step in job.get('steps', []):
            if 'run' in step:
                run_commands = step['run'].split('\n')
                
                # Check for Makefile usage
                for cmd in run_commands:
                    if cmd.strip().startswith('make '):
                        target = cmd.strip().split()[1]
                        makefile_usage.append(f"Job '{job_name}' uses 'make {target}'")
                
                # Check for direct command usage
                for target, patterns in makefile_commands.items():
                    for pattern in patterns:
                        for cmd in run_commands:
                            if pattern in cmd and not cmd.strip().startswith('make '):
                                direct_command_usage.append(f"Job '{job_name}' directly uses '{cmd.strip()}' instead of 'make {target}'")
    
    return {
        'file': os.path.basename(file_path),
        'makefile_usage': makefile_usage,
        'direct_command_usage': direct_command_usage
    }

def main():
    """Main function to check all workflow files."""
    all_results = []
    
    # Check each YAML file in the workflows directory
    for filename in os.listdir(workflows_dir):
        if filename.endswith('.yml'):
            file_path = os.path.join(workflows_dir, filename)
            results = check_workflow_file(file_path)
            if results:
                all_results.append(results)
    
    # Print the results
    for result in all_results:
        print(f"\nFile: {result['file']}")
        
        print("\nMakefile Usage:")
        if result['makefile_usage']:
            for usage in result['makefile_usage']:
                print(f"  ✅ {usage}")
        else:
            print("  ❌ No Makefile targets used")
        
        print("\nDirect Command Usage (should use Makefile):")
        if result['direct_command_usage']:
            for usage in result['direct_command_usage']:
                print(f"  ❌ {usage}")
        else:
            print("  ✅ No direct commands found that should use Makefile")

if __name__ == "__main__":
    main()
