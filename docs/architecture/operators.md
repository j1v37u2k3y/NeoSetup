# 🎭 Operator System Architecture

## Overview

The operator pattern is NeoSetup's core innovation - a configuration inheritance system that allows users to choose
their "reality" from minimal to power-user setups.

## What is an Operator?

An operator is a collection of configuration variables, tool preferences, and customizations that define a complete
development environment personality. Think of it as a "configuration profile" or "theme" for your entire system.

## Operator Hierarchy

```
base
 ├── Minimal configuration
 ├── Essential tools only
 └── Default settings
     ↓
matrix
 ├── Extends: base
 ├── Matrix theme and colors
 ├── Cyberpunk aesthetic
 └── Additional Matrix tools
     ↓
jiveturkey
 ├── Extends: matrix
 ├── Power-user configuration
 ├── Security tools
 └── Advanced aliases
```

## How Operators Work

### 1. Variable Loading Order

Variables are loaded in inheritance order, with each operator able to override parent values:

```yaml
# operators/base/vars.yml
shell_theme: "robbyrussell"
tools:
  - git
  - curl
  - wget

# operators/matrix/vars.yml
extends: base
shell_theme: "powerlevel10k"  # Overrides base
tools:
  - cmatrix  # Adds to base tools
  - neofetch
```

### 2. Ansible Implementation

The operator system is implemented using Ansible's variable precedence:

```yaml
# playbooks/site.yml
- name: Load operator variables
  include_vars: "operators/{{ item }}/vars.yml"
  loop: "{{ operator_chain }}"
  when: item is defined
```

### 3. Configuration Merging

Operators can:

- **Override** scalar values (strings, numbers, booleans)
- **Extend** lists and dictionaries
- **Compose** multiple configurations

## Operator Structure

Each operator consists of:

```
operators/
└── myoperator/
    └── vars.yml          # Configuration variables
```

### vars.yml Schema

```yaml
# Metadata
operator_name: "myoperator"
extends: "parent_operator"  # Optional inheritance

# Shell configuration
shell_config:
  shell: "zsh"
  theme: "powerlevel10k"
  plugins:
    - zsh-autosuggestions
    - zsh-syntax-highlighting
  aliases:
    ll: "ls -la"
    gs: "git status"
  environment:
    EDITOR: "vim"
    PAGER: "less"

# Tool preferences
tools_config:
  modern_cli_tools:
    - eza
    - bat
    - ripgrep
  development_tools:
    - docker
    - docker-compose
  security_tools: # Operator-specific
    - nmap
    - netcat

# Tmux configuration
tmux_config:
  theme: "matrix"
  prefix_key: "C-a"
  plugins:
    - tmux-resurrect
    - tmux-continuum

# Docker configuration
docker_config:
  compose_version: "v2"
  buildkit: true
```

## Creating Custom Operators

### Step 1: Define the Operator

Create `operators/myoperator/vars.yml`:

```yaml
operator_name: "myoperator"
extends: "matrix"  # Build on existing operator

shell_config:
  theme: "agnoster"
  aliases:
    myalias: "echo 'Hello from my operator!'"

tools_config:
  custom_tools:
    - my-special-tool
    - another-tool
```

### Step 2: Register the Operator

Add to `group_vars/all/operators.yml`:

```yaml
available_operators:
  - base
  - matrix
  - jiveturkey
  - myoperator  # Add your operator

operator_inheritance:
  myoperator:
    parents:
      - matrix
```

### Step 3: Use the Operator

```bash
make install OPERATOR=myoperator
```

## Operator Inheritance Rules

### 1. Single Inheritance

Each operator can extend one parent operator:

```yaml
extends: matrix  # Inherits from matrix
```

### 2. Variable Precedence

Child operator variables override parent variables:

- **Last loaded wins** for scalar values
- **Lists are merged** (child items added to parent)
- **Dictionaries are deep merged**

### 3. Composition Pattern

Operators can be composed for complex configurations:

```yaml
# Future feature: multiple inheritance
extends:
  - security
  - development
  - cloud
```

## Best Practices

### 1. Keep Operators Focused

Each operator should represent a clear use case:

- `base` - Minimalist
- `developer` - General development
- `security` - Security testing
- `data-science` - Data analysis

### 2. Document Operator Purpose

Include clear documentation in vars.yml:

```yaml
# Operator: security
# Purpose: Security testing and penetration testing tools
# Extends: matrix
# Author: j1v37u2k3y
```

### 3. Test Inheritance

Always test that child operators properly extend parents:

```bash
# Test inheritance chain
make dry-run OPERATOR=child
```

### 4. Version Operators

Consider versioning for breaking changes:

```yaml
operator_version: "1.0.0"
minimum_ansible_version: "2.9"
```

## Operator Lifecycle

### Development Phase

1. Create in `operators/` directory
2. Test locally with `make install`
3. Iterate on configuration

### Testing Phase

1. Test on multiple platforms
2. Verify inheritance works
3. Check for conflicts

### Release Phase

1. Document in README
2. Add to operator registry
3. Share with community

### Maintenance Phase

1. Update for new tools
2. Fix reported issues
3. Maintain compatibility

## Advanced Features

### Dynamic Operator Selection

Operators can be selected based on system facts:

```yaml
- name: Auto-select operator
  set_fact:
    neosetup_operator: "{{ 'macos' if ansible_os_family == 'Darwin' else 'linux' }}"
```

### Conditional Features

Enable features based on operator:

```yaml
- name: Install security tools
  when: neosetup_operator == 'jiveturkey'
  include_tasks: security_tools.yml
```

### Operator Validation

Validate operator configuration:

```yaml
- name: Validate operator
  assert:
    that:
      - operator_name is defined
      - operator_version is defined
    fail_msg: "Invalid operator configuration"
```

## Troubleshooting

### Common Issues

**Operator not found**:

```bash
# Check operator exists
ls operators/myoperator/vars.yml
```

**Inheritance not working**:

```bash
# Debug variable loading
ansible-playbook playbooks/site.yml -vvv
```

**Variable conflicts**:

```bash
# Check variable precedence
ansible-inventory --list --vars
```

## Future Enhancements

### Planned Features

1. **Operator Registry** - Central repository of operators
2. **Operator Composition** - Multiple inheritance
3. **Operator Versioning** - Semantic versioning support
4. **Operator Dependencies** - Required tools/roles
5. **Operator Marketplace** - Share and discover operators

### Community Operators

Encourage community contributions:

- `webdev` - Frontend development
- `backend` - API development
- `mobile` - Mobile app development
- `gamedev` - Game development
- `embedded` - Embedded systems

---

*"The operator is the one who can see the code behind the Matrix."*
