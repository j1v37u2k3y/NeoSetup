# 🎛️ NeoSetup Configuration Guide

Customize your Matrix environment to match your workflow and preferences.

## 🎯 Understanding Operators

Operators are the core configuration system that defines what gets installed and how it's configured.

### Built-in Operators

| Operator      | Extends  | Description                                  | Best For                         |
|---------------|----------|----------------------------------------------|----------------------------------|
| `base`        | -        | Essential tools and minimal configuration    | Servers, clean environments      |
| `matrix`      | `base`   | Adds Matrix theme and cyberpunk aesthetics   | Developers who want style        |
| `jiveturkey`  | `matrix` | Adds security tools and power-user features  | Security professionals, hackers  |
| `macos`       | `base`   | Homebrew integration and macOS productivity  | macOS users                      |
| `python_dev`  | `base`   | pyenv, Poetry, testing and quality tools     | Python developers                |
| `go_dev`      | `base`   | Go toolchain, linters, and dev utilities     | Go developers                    |
| `nodejs_dev`  | `base`   | nvm, npm/yarn/pnpm, TypeScript setup         | Node.js/TypeScript developers    |
| `windows_wsl` | `base`   | WSL2 interoperability and Linux integration  | Windows WSL2 users               |

### Operator Inheritance

```text
base
├── Essential CLI tools (eza, bat, ripgrep, btop, fzf)
├── Basic shell configuration
├── Minimal tmux setup
└── Core aliases and functions
    │
    ├── matrix (extends base)
    │   ├── Matrix-themed colors and prompts
    │   ├── Cyberpunk tmux configuration
    │   ├── Matrix ASCII art and animations
    │   ├── Custom Matrix functions (matrix_mode, wake_up, enter_matrix)
    │   └── Green terminal color scheme
    │       │
    │       └── jiveturkey (extends matrix)
    │           ├── Security tools (nmap, netcat, wireshark)
    │           ├── Development tools (terraform, kubectl, ansible)
    │           └── Penetration testing utilities
    │
    ├── macos (extends base)
    │   ├── Homebrew integration with architecture detection
    │   ├── Window management (Rectangle) and system monitoring (Stats)
    │   └── macOS-specific aliases and clipboard integration
    │
    ├── python_dev (extends base)
    │   ├── Python version management (pyenv)
    │   ├── Package management (pip, pipx, Poetry)
    │   └── Code quality tools (black, flake8, mypy, pytest)
    │
    ├── go_dev (extends base)
    │   ├── Go toolchain and version management
    │   ├── Development tools (gopls, golangci-lint, delve)
    │   └── gRPC/protobuf and build/release tools
    │
    ├── nodejs_dev (extends base)
    │   ├── Node.js version management (nvm)
    │   ├── Package managers (npm, yarn, pnpm)
    │   └── TypeScript, testing, and build tools
    │
    └── windows_wsl (extends base)
        ├── WSL2-Windows interoperability
        ├── Windows Terminal integration
        └── Cross-platform clipboard and paths
```

## ⚙️ Custom Configuration

### Customizing Your Operator

The primary way to customize NeoSetup is by creating or editing an operator's `vars.yml` file.
See [Creating Custom Operators](#creating-custom-operators) below for full details.

### User Configuration File

> **Planned Feature**: Local user overrides via `~/.ansible_local.yml` are not yet implemented.
> For now, create a custom operator to override settings.

Example of the planned `~/.ansible_local.yml` override format:

```yaml
# Shell Environment Variables
shell_env_vars:
  EDITOR: "nvim"
  BROWSER: "firefox"
  TERMINAL: "alacritty"
  PAGER: "less"

# Custom Shell Aliases
shell_aliases:
  # Development shortcuts
  - { alias: "vim", command: "nvim" }
  - { alias: "v", command: "nvim" }
  - { alias: "lg", command: "lazygit" }

  # Kubernetes shortcuts
  - { alias: "k", command: "kubectl" }
  - { alias: "kgp", command: "kubectl get pods" }
  - { alias: "kgs", command: "kubectl get services" }

  # Terraform shortcuts
  - { alias: "tf", command: "terraform" }
  - { alias: "tfa", command: "terraform apply" }
  - { alias: "tfp", command: "terraform plan" }

  # Docker shortcuts
  - { alias: "d", command: "docker" }
  - { alias: "dc", command: "docker-compose" }
  - { alias: "dps", command: "docker ps" }

# Custom Shell Functions
shell_functions:
  - name: "mkcd"
    definition: |
      mkdir -p "$1" && cd "$1"

  - name: "extract"
    definition: |
      if [ -f "$1" ]; then
        case "$1" in
          *.tar.bz2)   tar xjf "$1"     ;;
          *.tar.gz)    tar xzf "$1"     ;;
          *.bz2)       bunzip2 "$1"     ;;
          *.rar)       unrar x "$1"     ;;
          *.gz)        gunzip "$1"      ;;
          *.tar)       tar xf "$1"      ;;
          *.tbz2)      tar xjf "$1"     ;;
          *.tgz)       tar xzf "$1"     ;;
          *.zip)       unzip "$1"       ;;
          *.Z)         uncompress "$1"  ;;
          *.7z)        7z x "$1"        ;;
          *)           echo "'$1' cannot be extracted" ;;
        esac
      else
        echo "'$1' is not a valid file"
      fi

# Tmux Custom Configuration
tmux_custom_config: |
  # Mouse support
  set -g mouse on

  # Increase history limit
  set -g history-limit 10000

  # Custom key bindings
  bind r source-file ~/.tmux.conf \; display "Config reloaded!"
  bind | split-window -h
  bind - split-window -v

# Tool Configuration Overrides
tool_config:
  git:
    user_name: "Your Name"
    user_email: "your.email@example.com"

  nvim:
    enable_plugins: true
    theme: "matrix"
```

### Component-Specific Configuration

> **Planned Feature**: The following component-specific overrides show the target configuration format.
> Currently, these values are set within operator `vars.yml` files, not as standalone overrides.

#### Shell Configuration

Shell settings within an operator's `vars.yml`:

```yaml
# Shell Framework (oh-my-zsh, bash-it, fish)
shell_framework: "oh-my-zsh"

# Shell Theme
shell_theme: "powerlevel10k/powerlevel10k"

# Shell Plugins
shell_plugins:
  - git
  - docker
  - kubectl
  - terraform
  - zsh-autosuggestions
  - zsh-syntax-highlighting
  - history-substring-search

# Powerlevel10k Configuration
p10k_config:
  show_battery: true
  show_time: true
  show_git: true
  two_lines: false
```

#### Tmux Configuration

Tmux settings within an operator's `vars.yml`:

```yaml
# Tmux Theme
tmux_theme: "matrix"  # Options: matrix, base, custom

# Tmux Settings
tmux_settings:
  prefix_key: "C-a"
  mouse_support: true
  history_limit: 10000
  base_index: 1

# Custom Status Bar
tmux_status_config: |
  set -g status-bg black
  set -g status-fg green
  set -g status-left '#[fg=green]#S '
  set -g status-right '#[fg=green]%H:%M %d-%b-%y'
```

#### Tool Configuration

Tool settings within an operator's `vars.yml`:

```yaml
# Modern CLI Tools
modern_tools:
  eza:
    enable: true
    aliases: [ "ls", "ll", "la" ]

  bat:
    enable: true
    theme: "Matrix"

  ripgrep:
    enable: true
    aliases: [ "grep" ]

  btop:
    enable: true
    theme: "matrix"

  fzf:
    enable: true
    key_bindings: true
    completion: true

# Security Tools (jiveturkey operator)
security_tools:
  nmap:
    enable: true
    custom_scripts: true

  wireshark:
    enable: true
    gui_support: false

  docker_security:
    enable: true
    custom_functions: true
```

## 🎨 Theming and Appearance

### Matrix Theme Customization

```yaml
# Matrix Theme Settings
matrix_theme:
  primary_color: "#00ff00"      # Matrix green
  secondary_color: "#008000"    # Dark green
  background_color: "#000000"   # Black
  text_color: "#00ff00"         # Bright green

  # ASCII Art
  show_matrix_banner: true
  show_matrix_rain: true
  show_neo_quotes: true

  # Animations
  enable_animations: true
  animation_speed: "medium"     # slow, medium, fast
```

### Custom Color Schemes

> **Planned Feature**: Custom color scheme support is not yet implemented.

Example of the planned color scheme format:

```yaml
# Custom Theme
custom_theme:
  name: "cyberpunk"
  colors:
    primary: "#ff0080"      # Hot pink
    secondary: "#8000ff"    # Purple  
    background: "#0a0a0a"   # Near black
    text: "#ffffff"         # White
    accent: "#00ffff"       # Cyan
```

## 🔧 Advanced Configuration

### Creating Custom Operators

Create a new operator by extending existing ones:

```bash
# Interactive operator creation
cd neosetup
python3 scripts/create_operator.py --interactive

# Or create manually
mkdir -p operators/myoperator
```

Example custom operator (`operators/myoperator/vars.yml`):

```yaml
# Custom operator configuration
extends: matrix  # Inherit from matrix operator

description: "Custom development environment for my workflow"
author: "Your Name"
version: "1.0.0"

# Override or add tools
additional_packages:
  - name: "golang"
    description: "Go programming language"
  - name: "nodejs"
    description: "Node.js runtime"

# Custom shell configuration
shell_aliases:
  - { alias: "go-test", command: "go test ./..." }
  - { alias: "npm-dev", command: "npm run dev" }

# Custom environment variables
shell_env_vars:
  GO111MODULE: "on"
  GOPROXY: "https://proxy.golang.org"
  NODE_ENV: "development"
```

### Environment-Specific Configurations

> **Planned Feature**: Environment-specific configuration profiles are not yet implemented.
> These show the target format for future environment presets.

#### Development Environment

```yaml
# Development-focused configuration (planned)
development_config:
  enable_debug_mode: true
  install_dev_tools: true
  setup_git_hooks: true
  configure_ide_support: true
```

#### Server Environment

```yaml
# Server-optimized configuration (planned)
server_config:
  minimal_installation: true
  disable_gui_tools: true
  enable_monitoring: true
  security_hardening: true
```

#### Docker Container

```yaml
# Container-optimized configuration (planned)
container_config:
  skip_system_packages: true
  minimal_shell_config: true
  disable_animations: true
  lightweight_tools: true
```

## 🔒 Security Configuration

> **Planned Feature**: Automated security hardening is not yet implemented in the Ansible roles.
> The jiveturkey operator installs security tools, but the configurations below are planned for a future release.

### Security Hardening

```yaml
# Security settings (planned)
security_config:
  # SSH Configuration
  ssh_hardening:
    disable_root_login: true
    use_key_auth: true
    change_default_port: false

  # Firewall Settings
  firewall:
    enable_ufw: true
    default_deny: true
    allow_ssh: true

  # System Hardening
  system_hardening:
    disable_unused_services: true
    secure_kernel_parameters: true
    audit_logging: true
```

### Security Tools Configuration

```yaml
# Security tools for jiveturkey operator
security_tools_config:
  nmap:
    enable_stealth_mode: true
    custom_scripts: true
    output_format: "xml"

  wireshark:
    capture_filters: [ "tcp", "udp", "icmp" ]
    disable_gui: true

  custom_functions:
    quick_scan: "nmap -sS -O -v"
    port_scan: "nmap -p- -v"
    vuln_scan: "nmap --script vuln"
```

## 📊 Monitoring and Logging

> **Planned Feature**: Monitoring and logging configuration is not yet implemented.

### System Monitoring

```yaml
# Monitoring configuration (planned)
monitoring_config:
  # Resource monitoring
  btop:
    update_interval: 2000
    show_temps: true
    show_battery: true

  # Log monitoring
  log_monitoring:
    enable: true
    watch_files:
      - "/var/log/syslog"
      - "/var/log/auth.log"
```

### Performance Tuning

```yaml
# Performance optimization (planned)
performance_config:
  # Shell performance
  shell_optimization:
    lazy_load_plugins: true
    async_loading: true
    minimal_prompt: false

  # System performance
  system_optimization:
    increase_history_size: true
    optimize_PATH: true
    cache_completions: true
```

## 🔄 Configuration Management

### Backup and Restore

Back up your configuration files manually before making changes:

```bash
# Backup current configuration
cp ~/.zshrc ~/.zshrc.backup
cp ~/.tmux.conf ~/.tmux.conf.backup

# Restore from backup
cp ~/.zshrc.backup ~/.zshrc
cp ~/.tmux.conf.backup ~/.tmux.conf

# Re-run setup to reset to operator defaults
./setup install [your-operator]
```

### Version Control

Track your operator customizations in git:

```bash
# Your operator vars are already tracked in the repo
cd neosetup/operators/myoperator
git add vars.yml
git commit -m "Updated operator configuration"
```

## 🛠️ Validation and Testing

### Configuration Validation

```bash
# Validate operator configuration
cd neosetup
python3 scripts/validate_operator.py myoperator

# Test configuration without applying
make dry-run OPERATOR=myoperator

# Validate custom configuration
ansible-playbook playbooks/site.yml --syntax-check
```

---

**Next Steps**: For troubleshooting configuration issues, see [Troubleshooting Guide](./troubleshooting.md).
