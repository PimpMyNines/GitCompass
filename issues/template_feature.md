# Template Support Feature

## Main Issue
- **Title**: Add support for templates in GitCompass
- **Type**: Feature
- **Priority**: High
- **Start Date**: 3/17/2025
- **Description**: 
  Implement a template system that allows users to standardize issue creation, project setup, and roadmap planning with pre-defined templates.

## Sub-Issues

### 1. Template Manager Implementation
- **Title**: Implement Template Manager Class
- **Type**: Implementation
- **Priority**: High
- **Start Date**: 3/17/2025
- **Description**:
  Create a Template Manager class that can load, store, and apply templates from multiple locations.
  
**Tasks**:
- [x] Define template directory structure
- [x] Implement template loading from multiple locations
- [x] Add support for YAML and JSON template formats
- [x] Add template modification and creation capabilities
- [x] Implement value substitution in templates

### 2. Issue Templates
- **Title**: Implement Issue Templates
- **Type**: Implementation
- **Priority**: High
- **Start Date**: 3/17/2025
- **Description**:
  Add support for issue templates that can be used to standardize issue creation.
  
**Tasks**:
- [x] Create basic issue template structure
- [x] Update CLI to support issue templates
- [x] Support template field substitution
- [x] Support template labels and other metadata
- [x] Add interactive mode for issue creation

### 3. Project Templates
- **Title**: Implement Project Templates
- **Type**: Implementation
- **Priority**: High
- **Start Date**: 3/17/2025
- **Description**:
  Add support for project board templates with customizable columns and settings.
  
**Tasks**:
- [x] Create basic project template structure
- [x] Update ProjectManager to support custom columns
- [x] Update CLI to support project templates
- [x] Support template value substitution
- [x] Add support for project automation rules

### 4. Roadmap Templates
- **Title**: Implement Roadmap Templates
- **Type**: Implementation
- **Priority**: High
- **Start Date**: 3/17/2025
- **Description**:
  Add support for roadmap templates with milestone patterns and timeframes.
  
**Tasks**:
- [x] Create basic roadmap template structure
- [x] Update RoadmapManager to support template-based milestones
- [x] Add support for relative dates in milestones
- [x] Implement quarter-based planning templates
- [x] Support label creation for roadmap milestones

### 5. Template Command Group
- **Title**: Implement Template CLI Commands
- **Type**: Implementation
- **Priority**: Medium
- **Start Date**: 3/17/2025
- **Description**:
  Add a new command group for managing templates.
  
**Tasks**:
- [x] Add `templates list` command
- [x] Add `templates show` command
- [x] Add `templates create` command
- [x] Add `templates export` command
- [x] Add proper documentation for template commands

### 6. Example Templates
- **Title**: Create Example Templates
- **Type**: Content
- **Priority**: Medium
- **Start Date**: 3/17/2025
- **Description**:
  Create a set of example templates for issues, projects, and roadmaps.
  
**Tasks**:
- [x] Create bug report and feature request templates
- [x] Create Agile/Kanban project templates
- [x] Create quarterly release roadmap templates
- [x] Create documentation for custom template creation
- [x] Add validation for template formats

### 7. Template Feature Tests
- **Title**: Add Tests for Template Features
- **Type**: Testing
- **Priority**: High
- **Start Date**: 3/17/2025
- **Description**:
  Add unit, integration, and end-to-end tests for template functionality.
  
**Tasks**:
- [x] Add unit tests for TemplateManager
- [x] Add integration tests for templates with GitHub API
- [x] Add end-to-end tests with mock data
- [x] Test template directory discovery
- [x] Test template value substitution