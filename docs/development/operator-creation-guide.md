# NeoSetup Operator Creation Guide

This guide covers creating, validating, and maintaining NeoSetup operators - the configuration profiles that define
different development environment setups.

## Table of Contents

- [Overview](#overview)
- [Operator Structure](#operator-structure)
- [Creating New Operators](#creating-new-operators)
- [Validation](#validation)
- [Best Practices](#best-practices)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Overview

NeoSetup operators are YAML configuration files that define complete development environment setups. They support
inheritance, allowing you to create specialized configurations that build upon existing ones.

### Operator Hierarchy

```text
base → matrix → jiveturkey
 ↓
minimal
```

- **base**: Essential tools and minimal configuration
- **matrix**: Matrix-themed aesthetic with additional tools
- **jiveturkey**: Power-user setup with security tools and advanced configuration
- **minimal**: Bare-bones setup (extends base)

## Operator Structure

Every operator must be located in `neosetup/operators/<operator_name>/` with at minimum:

```text
operators/
└── my_operator/
    ├── vars.yml      # Main configuration (required)
    └── README.md     # Documentation (recommended)
```

### Required Metadata

Every `vars.yml` must include:

```yaml
---
# Operator metadata
operator_name: "my_operator"
operator_version: "1.0.0"
operator_description: "Brief description of what this operator provides"

# Optional metadata
operator_author: "Your Name"
extends: "parent_operator"  # Optional inheritance
operator_tags: [ "development", "security" ]  # Optional categorization
```

### Configuration Sections

Operators can define these configuration sections:

#### Shell Configuration

```yaml
shell_config:
  preferred_shell: "zsh"
  framework: "oh-my-zsh"
  oh_my_zsh_theme: "robbyrussell"
  oh_my_zsh_plugins:
    - git
    - docker
    - zsh-autosuggestions
  aliases:
    ll: "ls -alF"
    gs: "git status"
  environment:
    EDITOR: "vim"
    PAGER: "less"
  paths:
    - "$HOME/.local/bin"
    - "$HOME/bin"
```

#### Tmux Configuration

```yaml
tmux_config:
  theme: "matrix"
  prefix: "C-a"
  settings:
    base_index: 1
    history_limit: 10000
    mouse: true
  plugins:
    enabled: true
    sensible: true
    resurrect: true
```

#### Tools Configuration

```yaml
tools_config:
  essential_tools:
    - name: "fd"
      description: "Better find"
      package:
        macos: "fd"
        debian: "fd-find"
        redhat: "fd-find"
```

#### Docker Configuration

```yaml
docker_config:
  install_compose: true
  compose_version: "v2"
  enable_buildkit: true
```

#### Custom Shell Functions

```yaml
shell_functions:
  - name: "mkcd"
    description: "Create directory and cd into it"
    body: |
      mkdir -p "$1" && cd "$1"
```

## Creating New Operators

### Method 1: Using the Generator (Recommended)

The easiest way to create a new operator is using the built-in generator:

```bash
cd neosetup

# Interactive mode (recommended for beginners)
python3 scripts/create_operator.py --interactive

# Command line mode
python3 scripts/create_operator.py my_operator \
  --parent base \
  --template standard \
  --description "My custom development environment" \
  --author "Your Name"
```

#### Available Templates

- **minimal**: Basic shell configuration only
- **standard**: Shell + Tmux + Essential tools
- **advanced**: Full configuration with all sections

#### Generator Options

```bash
# List available templates
python3 scripts/create_operator.py --list-templates

# List available parent operators
python3 scripts/create_operator.py --list-parents

# Full command line example
python3 scripts/create_operator.py security_ops \
  --parent matrix \
  --template advanced \
  --version "1.0.0" \
  --description "Security-focused development environment" \
  --author "Security Team" \
  --tags "security,devops"
```

### Method 2: Manual Creation

1. **Create Directory Structure**

   ```bash
   mkdir -p neosetup/operators/my_operator
   ```

2. **Create vars.yml**

   ```yaml
   ---
   operator_name: "my_operator"
   operator_version: "1.0.0"
   operator_description: "My custom operator"

   # Your configuration sections here...
   ```

3. **Create README.md**

   ```markdown
   # My Operator

   Description of what this operator provides.

   ## Usage
   \`\`\`bash
   make install OPERATOR=my_operator
   \`\`\`
   ```

## Validation

Always validate your operators before using them:

```bash
# Validate specific operator
python3 scripts/validate_operator.py my_operator

# Validate all operators
python3 scripts/validate_operator.py --all

# Show detailed info messages
python3 scripts/validate_operator.py my_operator --info
```

### Common Validation Errors

1. **Missing Required Fields**

   ```text
   Error: Required field 'operator_name' is missing
   Fix: Add operator_name: "my_operator" to vars.yml
   ```

2. **Invalid Field Types**

   ```text
   Error: Field 'operator_name' must be a string, got int
   Fix: Use quotes around string values
   ```

3. **Pattern Validation**

   ```text
   Error: Field 'operator_name' doesn't match required pattern
   Fix: Use lowercase letters, numbers, and underscores only
   ```

4. **Invalid Parent Reference**

   ```text
   Error: Parent operator 'nonexistent' not found
   Fix: Use an existing parent or create the parent operator
   ```

### Field Validation Rules

- **operator_name**: lowercase, alphanumeric + underscore, max 50 chars
- **operator_version**: semantic version (e.g., "1.0.0", "2.1.0-beta")
- **preferred_shell**: "zsh", "bash", "fish", or "auto"
- **tmux_prefix**: format "C-x" where x is a letter
- **oh_my_zsh_plugins**: max 20 plugins (warning beyond 15)

## Best Practices

### Naming Conventions

- Use descriptive, lowercase names with underscores: `security_dev`, `minimal_web`
- Avoid generic names like `config` or `setup`
- Include your username/team for personal operators: `jiveturkey`, `security_team`

### Version Management

- Follow semantic versioning: `major.minor.patch`
- Increment major for breaking changes
- Increment minor for new features
- Increment patch for bug fixes

### Configuration Organization

1. **Start Simple**: Begin with basic configuration and add complexity gradually
2. **Use Inheritance**: Extend existing operators rather than duplicating configuration
3. **Document Choices**: Add comments explaining non-obvious configuration choices
4. **Test Thoroughly**: Validate and test your operator before sharing

### Tool Selection

- **Essential tools**: Include only tools you actually use
- **Platform compatibility**: Test package names across different OS
- **Fallback options**: Provide alternatives where possible

```yaml
aliases:
  ls: "eza --color=always 2>/dev/null || ls --color=auto"
```

### Security Considerations

- **Never include secrets**: Don't put passwords, API keys, or tokens in operators
- **Review Docker images**: Only use trusted container images in shell functions
- **Validate inputs**: Shell functions should validate user inputs

## Examples

### Minimal Operator

```yaml
---
operator_name: "minimal_dev"
operator_version: "1.0.0"
operator_description: "Minimal development setup"
extends: "base"

shell_config:
  aliases:
    py: "python3"
    ll: "ls -la"
```

### Themed Operator

```yaml
---
operator_name: "cyberpunk_dev"
operator_version: "1.2.0"
operator_description: "Cyberpunk-themed development environment"
extends: "matrix"

shell_config:
  aliases:
    hack: "echo 'Access granted... 🔐'"
    scan: "nmap -sn"

  environment:
    THEME_MODE: "cyberpunk"

tools_config:
  theme_tools:
    - name: "cmatrix"
      description: "Digital rain effect"
      package:
        macos: "cmatrix"
        debian: "cmatrix"
```

### Specialized Development Operator

```yaml
---
operator_name: "python_ml"
operator_version: "2.0.0"
operator_description: "Python machine learning development setup"
extends: "base"
operator_tags: [ "python", "ml", "data-science" ]

shell_config:
  aliases:
    py: "python3"
    pip: "pip3"
    jlab: "jupyter lab"
    nb: "jupyter notebook"

  environment:
    PYTHONPATH: "$HOME/projects/python"
    JUPYTER_CONFIG_DIR: "$HOME/.jupyter"

tools_config:
  ml_tools:
    - name: "jupyter"
      description: "Interactive notebooks"
    - name: "pandas"
      description: "Data manipulation"
    - name: "numpy"
      description: "Numerical computing"
```

## Testing Your Operator

### 1. Validation Testing

```bash
# Validate configuration
python3 scripts/validate_operator.py my_operator

# Run comprehensive tests
python3 tests/test_operator_validation.py
```

### 2. Dry Run Testing

```bash
# Test without making changes
cd neosetup
make dry-run OPERATOR=my_operator

# Test specific roles
ansible-playbook playbooks/site.yml --tags "shell" --check
```

### 3. Live Testing

```bash
# Install in test environment
make install OPERATOR=my_operator

# Test specific features
source ~/.zshrc  # or ~/.bashrc
alias_test       # Test your aliases
function_test    # Test your functions
```

## Troubleshooting

### Common Issues

1. **Operator not found**

   ```bash
   Error: Operator 'my_operator' not found

   # Check if directory exists
   ls operators/

   # Ensure vars.yml exists
   ls operators/my_operator/vars.yml
   ```

2. **YAML syntax errors**

   ```bash
   Error: mapping values are not allowed here

   # Validate YAML syntax
   python3 -c "import yaml; yaml.safe_load(open('operators/my_operator/vars.yml'))"
   ```

3. **Package installation failures**

- Verify package names for your OS
- Check if custom package managers (homebrew, snap) are needed
- Use the test environment first

4. **Shell configuration not loading**

   ```bash
   # Manually source configuration
   source ~/.zshrc

   # Check for syntax errors
   zsh -n ~/.zshrc
   ```

5. **Permission issues**

   ```bash
   # Some tasks need sudo privileges
   make install OPERATOR=my_operator --ask-become-pass
   ```

### Getting Help

1. **Check existing operators** for examples and patterns
2. **Run validation** with `--info` flag for detailed feedback
3. **Review logs** in `/tmp/neosetup.log` for detailed error information
4. **Test incrementally** - start with basic configuration and add complexity

### Debug Mode

Enable verbose output for troubleshooting:

```bash
# Verbose Ansible output
make install OPERATOR=my_operator VERBOSE=true

# Debug specific tasks
ansible-playbook playbooks/site.yml --tags "shell" -vvv
```

## Contributing

When contributing operators to the project:

1. **Validate thoroughly** using all available tools
2. **Test on multiple platforms** (Linux, macOS)
3. **Document unique features** in the operator's README
4. **Follow security best practices**
5. **Include appropriate tags** for discoverability

Your operator should enhance the NeoSetup ecosystem while maintaining compatibility and security standards.
