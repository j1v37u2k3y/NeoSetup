# 🎛️ NeoSetup Configuration Guide

Customize your Matrix environment to match your workflow and preferences.

## 🎯 Understanding Operators

Operators are the core configuration system that defines what gets installed and how it's configured. Each
operator is a directory under `neosetup/operators/<name>/` containing a `vars.yml`. Operators inherit from
one another via `extends`, so you compose configuration rather than copy it.

### Built-in Operators

Eight operators ship with NeoSetup. The `jiveturkey → matrix → base` chain is the main spine; the rest
extend `base` directly.

| Operator      | Extends  | Description                                             | Best For                          |
|---------------|----------|--------------------------------------------------------|-----------------------------------|
| `base`        | -        | Essential tools and minimal configuration              | Servers, clean environments       |
| `matrix`      | `base`   | Matrix theme and cyberpunk aesthetics                  | Developers who want style         |
| `jiveturkey`  | `matrix` | Power-user productivity + networking tools             | Power users, security enthusiasts |
| `python_dev`  | `base`   | Python toolchain (pyenv, poetry, pipx, linters)        | Python developers                 |
| `nodejs_dev`  | `base`   | Node.js environment (nvm)                              | Node.js developers                |
| `go_dev`      | `base`   | Go toolchain                                           | Go developers                     |
| `macos`       | `base`   | macOS integration (Homebrew, window management)        | macOS users                       |
| `windows_wsl` | `base`   | Windows WSL2 integration and interoperability          | WSL2 users                        |

Install any operator with `make install OPERATOR=<name>`. (The `./setup` wrapper only knows `base`,
`matrix`, and `jiveturkey`; use `make` for the rest.)

### Operator Inheritance

```text
base
├── Essential CLI tools (htop, tree, jq, curl, wget, yamllint, act, pre-commit)
├── Shared modern-CLI tools (eza, bat, ripgrep, fd, fzf, delta, btop)
├── Basic shell configuration (oh-my-zsh + robbyrussell)
├── Minimal tmux setup
└── Core aliases and functions

matrix (extends base)
├── Matrix-themed colors and prompts
├── Cyberpunk tmux theme
├── Matrix animation tools (cmatrix, neofetch, lolcat, figlet, cowsay, fortune)
├── Custom Matrix functions:
│   ├── matrix_mode - Toggle Matrix aesthetic
│   ├── wake_up - System information display
│   └── enter_matrix - Full Matrix immersion
└── Green terminal color scheme

jiveturkey (extends matrix)
├── Powerlevel10k prompt + power-user oh-my-zsh plugins
├── Networking tools (nmap, netcat)
├── Docker-based security helper functions (impacket, metasploit, SMB/HTTP servers)
├── Productivity/observability tools (ncdu, httpie, tldr, lazygit, glances, duf, lnav, ...)
└── Extensive git/docker/kubectl aliases
```

> **Note**: jiveturkey's heavier security/DevOps arsenal (wireshark, sqlmap, gobuster, ffuf, john, hashcat,
> kubectl, helm, awscli, terraform, ansible) is **planned/deferred** — it is declared in the operator but not
> yet wired into installation (it needs per-platform packaging + installers). A fresh `jiveturkey` install
> gives you nmap/netcat plus the Docker-based security functions, not the full toolkit.

## ⚙️ Customizing Configuration

There is **no external override file** — NeoSetup does not read `~/.ansible_local.yml`, `~/.neosetup`, or any
similar user config. Customization happens in one of two places:

1. **Edit your operator's `vars.yml`** (`neosetup/operators/<name>/vars.yml`), or
2. **Create your own operator** that `extends` an existing one and adds only your overrides
   (see [Creating Custom Operators](#-creating-custom-operators) below).

Editing `vars.yml` uses the real nested keys the Ansible roles consume. The main sections are `shell_config`,
`shell_functions`, `tools_config`, `tmux_config`, and `docker_config`.

### Shell Configuration

```yaml
shell_config:
  # Shell selection: auto, zsh, or bash
  preferred_shell: "auto"

  # Framework: oh-my-zsh (zsh) or bash-it (bash)
  framework: "oh-my-zsh"
  oh_my_zsh_theme: "powerlevel10k/powerlevel10k"

  # Oh My Zsh plugins
  oh_my_zsh_plugins:
    - git
    - docker
    - kubectl
    - zsh-autosuggestions
    - zsh-syntax-highlighting
    - history-substring-search

  # Aliases are a simple name -> command map
  aliases:
    vim: "nvim"
    k: "kubectl"
    tf: "terraform"
    gs: "git status -sb"

  # Environment variables
  environment:
    EDITOR: "nvim"
    PAGER: "less"

  # Extra directories to prepend to PATH
  paths:
    - "$HOME/.local/bin"
    - "$HOME/bin"
```

> Note: `ls`, `ll`, `la`, `l`, `lt`, and `l.` are defined as argument-forwarding shell **functions**
> (eza-aware, with a clean `ls` fallback) in `roles/shell/templates/shared/aliases.j2`. Don't redeclare them
> as aliases — aliases shadow the functions and can't forward flags.

### Custom Shell Functions

```yaml
shell_functions:
  - name: "mkcd"
    description: "Create directory and cd into it"
    body: |
      mkdir -p "$1" && cd "$1"

  - name: "extract"
    description: "Extract any archive"
    body: |
      if [ -f "$1" ]; then
        case "$1" in
          *.tar.gz)  tar xzf "$1" ;;
          *.zip)     unzip "$1"   ;;
          *)         echo "'$1' cannot be extracted" ;;
        esac
      else
        echo "'$1' is not a valid file"
      fi
```

### Tools Configuration

Extra tools are added through `tools_config.additional_tools`. **A tool only installs if it is registered in
`neosetup/roles/tools/vars/tool_registry.yml`** — listing an unregistered name does nothing (and, after the
tool-model fix, the install fails loudly rather than silently skipping). Every operator also gets the shared
`modern_cli` tool set plus the tool sets of every operator in its inheritance chain.

```yaml
tools_config:
  additional_tools:
    - ncdu
    - httpie
    - lazygit
```

To add a brand-new tool, first register it in `tool_registry.yml` with its per-platform package names, then
reference it here. See the [Operator Creation Guide](../development/operator-creation-guide.md).

### Tmux Configuration

```yaml
tmux_config:
  theme: "matrix"      # matrix, base, or custom
  prefix: "C-a"        # Screen-style prefix
  terminal: "tmux-256color"

  settings:
    mouse: true
    base_index: 1
    pane_base_index: 1
    history_limit: 50000

  key_bindings:
    reload_config: "r"
    split_horizontal: "|"
    split_vertical: "-"
```

### Docker Configuration

```yaml
docker_config:
  install_compose: true
  compose_version: "v2"
  enable_buildkit: true
```

## 🎨 Theming and Appearance

The Matrix look is driven by the `matrix` tmux theme (`tmux_config.theme: "matrix"`), the Powerlevel10k
prompt, and the operator's greeting. The `matrix` and `jiveturkey` operators set a startup greeting:

```yaml
matrix_greeting: "🚀 Welcome back! Let's build something awesome!"
startup_command: "neofetch 2>/dev/null || echo '$matrix_greeting'"
```

To change the color scheme, switch the Powerlevel10k configuration (`p10k configure`) and choose the tmux
theme via `tmux_config.theme`. Custom tmux themes live in the `tmux` role.

## 🔧 Creating Custom Operators

The cleanest way to customize is to create your own operator that extends an existing one and overrides only
what you need.

```bash
# Interactive operator creation
cd neosetup
python3 scripts/create_operator.py --interactive
```

Example custom operator (`neosetup/operators/myoperator/vars.yml`):

```yaml
---
operator_name: "myoperator"
operator_version: "1.0.0"
operator_description: "Custom development environment for my workflow"
extends: "matrix"

shell_config:
  aliases:
    go-test: "go test ./..."
    npm-dev: "npm run dev"
  environment:
    GO111MODULE: "on"
    NODE_ENV: "development"

tools_config:
  additional_tools:
    - go        # must exist in tool_registry.yml
    - nvm
```

Register it in `neosetup/group_vars/all/operators.yml` (add it to `available_operators` and
`operator_inheritance`), then install with `make install OPERATOR=myoperator`. Full details are in the
[Operator Creation Guide](../development/operator-creation-guide.md).

## 🛠️ Validation and Testing

```bash
cd neosetup

# Validate operator configuration against the schema
python3 scripts/validate_operator.py myoperator
python3 scripts/validate_operator.py --all

# Run the operator validation test suite
python3 tests/test_operator_validation.py

# Test configuration without applying it
make dry-run OPERATOR=myoperator

# Syntax-check the playbook
ansible-playbook playbooks/site.yml --syntax-check
```

---

**Next Steps**: For troubleshooting configuration issues, see [Troubleshooting Guide](./troubleshooting.md).
