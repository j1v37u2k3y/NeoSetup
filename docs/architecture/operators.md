# 🎭 Operator System Architecture

## Overview

The operator pattern is NeoSetup's core innovation - a configuration inheritance system that allows users to choose
their "reality" from minimal to power-user setups.

## What is an Operator?

An operator is a collection of configuration variables, tool preferences, and customizations that define a complete
development environment personality. Think of it as a "configuration profile" or "theme" for your entire system.

## Operator Hierarchy

Eight operators ship today. The `jiveturkey → matrix → base` chain is the main spine; the remaining five
each extend `base` directly.

```text
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
 ├── Networking tools (nmap, netcat) + Docker-based security functions
 └── Advanced aliases

base → macos          (macOS integration)
base → windows_wsl    (Windows WSL2 integration)
base → python_dev     (Python toolchain)
base → nodejs_dev     (Node.js environment)
base → go_dev         (Go toolchain)
```

## How Operators Work

### 1. Variable Loading Order

Variables are loaded in inheritance order, with each operator able to override parent values:

```yaml
# operators/base/vars.yml
shell_config:
  oh_my_zsh_theme: "robbyrussell"

# operators/matrix/vars.yml
extends: base
shell_config:
  oh_my_zsh_theme: "powerlevel10k/powerlevel10k"   # Overrides base
```

Installed tools aren't listed in each `vars.yml` directly — they come from the tool sets in
`roles/tools/vars/tool_registry.yml` (`operator_tool_sets`), composed across the operator's inheritance
chain, plus anything in `tools_config.additional_tools`.

### 2. Ansible Implementation

The operator system is implemented using Ansible's variable precedence. Inheritance is declared as a flat
list per operator in `group_vars/all/operators.yml` (`operator_inheritance`), and the tool set is composed
across that chain — for example:

```yaml
# group_vars/all/operators.yml
operator_inheritance:
  jiveturkey: ["matrix", "base"]   # flat, ordered list of ancestors

# roles/tools/tasks/install_tools_unified.yml (simplified)
- name: Determine tools to install (composed across the inheritance spine)
  set_fact:
    tools_to_install: >-
      {{ (operator_tool_sets.modern_cli | default([]))
         + ((operator_inheritance[neosetup_operator] | default([]) + [neosetup_operator])
              | select('in', operator_tool_sets) | map('extract', operator_tool_sets) | flatten)
         + (tools_config.additional_tools | default([])) }}
```

### 3. Configuration Merging

Operators can:

- **Override** scalar values (strings, numbers, booleans)
- **Extend** lists and dictionaries
- **Compose** multiple configurations

## Operator Structure

Each operator consists of:

```text
operators/
└── myoperator/
    └── vars.yml          # Configuration variables
```

### vars.yml Schema

These are the real keys the roles consume (see the
[Operator Creation Guide](../development/operator-creation-guide.md) for the authoritative reference):

```yaml
# Metadata
operator_name: "myoperator"
operator_version: "1.0.0"
extends: "matrix"           # Optional single-parent inheritance

# Shell configuration
shell_config:
  preferred_shell: "zsh"    # auto, zsh, bash
  framework: "oh-my-zsh"    # oh-my-zsh (zsh) or bash-it (bash)
  oh_my_zsh_theme: "powerlevel10k/powerlevel10k"
  oh_my_zsh_plugins:
    - zsh-autosuggestions
    - zsh-syntax-highlighting
  aliases:
    gs: "git status"
  environment:
    EDITOR: "vim"
    PAGER: "less"

# Extra tools (must be registered in roles/tools/vars/tool_registry.yml)
tools_config:
  additional_tools:
    - nmap
    - netcat

# Tmux configuration
tmux_config:
  theme: "matrix"           # matrix, base, or custom
  prefix: "C-a"
  settings:
    mouse: true
    history_limit: 50000

# Docker configuration
docker_config:
  compose_version: "v2"
  enable_buildkit: true
```

## Creating Custom Operators

### Step 1: Define the Operator

Create `operators/myoperator/vars.yml`:

```yaml
operator_name: "myoperator"
operator_version: "1.0.0"
extends: "matrix"  # Build on existing operator

shell_config:
  oh_my_zsh_theme: "agnoster"
  aliases:
    myalias: "echo 'Hello from my operator!'"

tools_config:
  additional_tools:      # each must be registered in tool_registry.yml
    - httpie
    - lazygit
```

### Step 2: Register the Operator

Add to `group_vars/all/operators.yml`. `operator_inheritance` is a **flat, ordered list** of ancestors
(closest parent first), not a nested `parents:` mapping:

```yaml
available_operators:
  - base
  - matrix
  - jiveturkey
  - myoperator  # Add your operator

operator_inheritance:
  myoperator: ["matrix", "base"]   # flat ordered list of ancestors
```

### Step 3: Use the Operator

```bash
make install OPERATOR=myoperator
```

## Operator Inheritance Rules

### 1. Declaring a Parent

Each operator names a single parent via `extends` in its `vars.yml`:

```yaml
extends: matrix  # Inherits from matrix
```

The full ancestor chain (which drives tool composition) is declared as a flat list in
`operator_inheritance` — e.g. `jiveturkey: ["matrix", "base"]`.

### 2. Variable Precedence

Child operator variables override parent variables:

- **Last loaded wins** for scalar values
- **Lists are merged** (child items added to parent)
- **Dictionaries are deep merged**

### 3. Composition Pattern

An operator's full ancestor chain is expressed as a flat, ordered list in `operator_inheritance`. This is
how an operator composes multiple ancestors' tool sets — for example `jiveturkey` pulls in both `matrix` and
`base`:

```yaml
operator_inheritance:
  jiveturkey: ["matrix", "base"]
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
```

(NeoSetup itself pins Ansible to `>=14.2,<15` and requires Python 3.12+.)

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

> "The operator is the one who can see the code behind the Matrix."
