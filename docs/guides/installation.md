# ⚙️ NeoSetup Installation Guide

Complete guide for installing and configuring your Matrix-themed development environment.

## 📋 Prerequisites

### Required

- **Git** - For cloning the repository
- **Python 3.12+** - For Ansible automation (Ansible is pinned to `>=14.2,<15`)
- **sudo access** - Some installations require elevated privileges

### Operating System Support

Actively supported:

- ✅ Ubuntu 22.04+
- ✅ Debian 12+
- ✅ Kali / Parrot (rolling)
- ✅ macOS 11+ (via the `macos` operator)
- ✅ Windows via WSL2 (via the `windows_wsl` operator)

Exercised in container testing (CentOS Stream 9, Rocky 9, AlmaLinux 9, Fedora 40) but not a primary target.

## 🚀 Installation Methods

### Method 1: Interactive Setup (Recommended)

The easiest way to enter the Matrix:

```bash
# Clone the repository
git clone https://github.com/j1v37u2k3y/NeoSetup.git
cd NeoSetup

# Run interactive setup
./setup
```

The script will:

- Show system information
- Let you choose your operator (pill)
- Handle all dependencies automatically
- Guide you through the process

### Method 2: Direct Commands

If you know what you want:

```bash
# Full installation
./setup install jiveturkey    # Power-user with security tools
./setup install matrix        # Cyberpunk theme
./setup install base          # Minimal essentials

# Component installation
./setup shell matrix          # Configure shell only
./setup tmux                  # Setup tmux only  
./setup docker                # Install Docker only
./setup tools jiveturkey      # Install CLI tools only
```

### Method 3: Advanced Ansible

For developers and advanced users:

```bash
cd neosetup

# Install dependencies
make deps

# Full installation
make install OPERATOR=jiveturkey

# Component installation
make shell OPERATOR=matrix    # Shell configuration
make tmux OPERATOR=base       # Tmux configuration
make tools OPERATOR=jiveturkey # CLI tools
make docker                   # Docker setup

# Preview changes (dry run)
make dry-run OPERATOR=matrix

# Verbose installation (pass extra ansible-playbook flags via ANSIBLE_FLAGS)
make install OPERATOR=jiveturkey ANSIBLE_FLAGS="-vvv"
```

> **Note**: `make` accepts any registered operator via `OPERATOR=<name>` (all 8 operators). The `./setup`
> wrapper only knows `base`, `matrix`, and `jiveturkey` — for the others (`python_dev`, `nodejs_dev`,
> `go_dev`, `macos`, `windows_wsl`) use `make install OPERATOR=<name>`.

## 💊 Operator Guide

Choose your reality with different operator configurations:

### Base Operator

**Perfect for**: Servers, minimalists, clean environments

```bash
./setup install base
```

**Includes**:

- Essential shell configuration
- Basic aliases and functions
- Essential tool set (htop, tree, jq, curl, wget, yamllint, act, pre-commit) plus the shared modern-CLI
  tools (eza, bat, ripgrep, fd, fzf, delta, btop)
- Clean, professional appearance

### Matrix Operator

**Perfect for**: Developers who want style and functionality

```bash
./setup install matrix
```

**Includes**: Everything from `base` plus:

- Matrix-themed terminal with green colors
- Cyberpunk tmux configuration
- Matrix rain and ASCII art
- Custom Matrix shell functions:
  - `matrix_mode` - Toggle Matrix aesthetic
  - `wake_up` - System information display
  - `enter_matrix` - Full Matrix immersion

### JiveTurkey Operator

**Perfect for**: Security professionals, power users, hackers

```bash
./setup install jiveturkey
```

**Includes**: Everything from `matrix` plus:

- Networking tools (nmap, netcat)
- Docker-based security helper functions (impacket, metasploit, SMB/HTTP servers, etc. — these run tools
  from containers, so no host install is required)
- Power-user aliases and productivity functions

> **Not yet installed**: the heavier security/DevOps arsenal (wireshark, sqlmap, gobuster, ffuf, john,
> hashcat, kubectl, helm, awscli, terraform, ansible) is **planned/deferred** — it needs per-platform
> packaging and installers before it ships. Don't expect these on a fresh `jiveturkey` install today.

### Other Operators

Install any of these with `make install OPERATOR=<name>`:

- **python_dev** - Python toolchain (pyenv, poetry, pipx, black, flake8, mypy, pytest, jupyter)
- **nodejs_dev** - Node.js environment (nvm)
- **go_dev** - Go toolchain
- **macos** - macOS integration (Homebrew, productivity apps, window management)
- **windows_wsl** - Windows WSL2 integration and interoperability

## 🔧 Advanced Configuration

### Customizing an Operator

There is no separate user-override file — NeoSetup does not read `~/.ansible_local.yml` or any similar
external config. Customization happens by editing your operator's `vars.yml` (or creating your own operator
that extends an existing one). Use the real nested keys the roles actually consume:

```yaml
# neosetup/operators/<your-operator>/vars.yml
shell_config:
  # Aliases are a name -> command map
  aliases:
    vim: "nvim"
    k: "kubectl"
  # Oh My Zsh plugins
  oh_my_zsh_plugins:
    - git
    - docker
    - kubectl
  # Environment variables
  environment:
    EDITOR: "nvim"
    PAGER: "less"

# Extra tools to install (must be registered in roles/tools/vars/tool_registry.yml)
tools_config:
  additional_tools:
    - ncdu
    - httpie

# Tmux behaviour
tmux_config:
  theme: "matrix"      # matrix, base, or custom
  prefix: "C-a"
  settings:
    mouse: true
    history_limit: 10000
```

See the [Configuration Guide](./configuration.md) and the
[Operator Creation Guide](../development/operator-creation-guide.md) for the full set of keys.

### Operator Inheritance

Operators use inheritance for clean configuration. The main spine is:

```text
base (essential tools)
 ↓
matrix (extends base + Matrix theme)
 ↓
jiveturkey (extends matrix + power-user tools)
```

The remaining operators (`python_dev`, `nodejs_dev`, `go_dev`, `macos`, `windows_wsl`) each extend `base`
directly. You can extend any existing operator by creating a new one in `neosetup/operators/`.

## 🛠️ Development Installation

### Developer Setup

For contributing to NeoSetup:

```bash
# Clone repository
git clone https://github.com/j1v37u2k3y/NeoSetup.git
cd NeoSetup

# Install git hooks (uses Docker for pre-commit)
git config core.hooksPath .githooks

# Run pre-commit checks (Docker-based)
./scripts/run-precommit.sh run --all-files

# Validate operators
cd neosetup
python3 scripts/validate_operator.py --all
```

**Note**: Pre-commit runs in Docker to ensure local/CI parity. Docker must be installed.

### Testing Changes

```bash
# Always test with dry-run first
make dry-run OPERATOR=jiveturkey

# Test individual components
ansible-playbook playbooks/site.yml --tags "shell" --check

# Test specific operators
python3 scripts/validate_operator.py matrix

# Run comprehensive tests
python3 tests/test_operator_validation.py
```

## 📊 Validation & Quality Assurance

### Pre-Installation Checks

The system automatically validates:

- ✅ Operating system compatibility
- ✅ Required dependencies
- ✅ Operator configuration validity
- ✅ Network connectivity
- ✅ Disk space requirements

### Post-Installation Verification

```bash
# Check installation status
./setup status

# Verify tools are working
which eza bat btop ripgrep fzf

# Test shell configuration
echo $SHELL
zsh --version

# Test tmux setup
tmux new-session -d -s test
tmux kill-session -t test
```

## 🔒 Security Considerations

### Installation Security

- Scripts use `sudo` only when necessary
- All packages installed from official repositories
- Security scanning with CodeQL, Trivy, and Bandit
- No secrets or credentials stored in configurations

### Network Requirements

- GitHub access for cloning repository
- Package manager access (apt, yum, dnf, brew)
- Docker Hub access (if installing Docker)

### Firewall Considerations

Most tools work without firewall changes, but security tools may need:

- Network scanning permissions
- Docker network access
- Custom port configurations

## 📈 Performance Expectations

### Installation Time

- **Base operator**: ~2-3 minutes
- **Matrix operator**: ~3-4 minutes
- **JiveTurkey operator**: ~4-5 minutes

Target: <5 minutes for full installation on modern hardware.

### Resource Usage

- **Disk space**: 200MB - 1GB depending on operator
- **Memory**: Minimal during installation
- **CPU**: Light usage for compilation tasks

## 🆘 Installation Issues

See [Troubleshooting Guide](./troubleshooting.md) for common issues and solutions.

### Quick Fixes

**Ansible not found**:

```bash
pip3 install ansible
```

**Permission denied**:

```bash
cd neosetup
make install OPERATOR=jiveturkey ANSIBLE_FLAGS="--ask-become-pass"
```

**Network issues**:

```bash
# Test connectivity
curl -s https://github.com

# Use verbose mode
cd neosetup
make install OPERATOR=matrix ANSIBLE_FLAGS="-vvv"
```

## 🔄 Updates and Maintenance

### Updating NeoSetup

```bash
# Pull latest changes
git pull origin main

# Re-run setup to update
./setup install [your-operator]

# Or update specific components
./setup shell matrix
./setup tools jiveturkey
```

### Clean Installation

```bash
# Clean Ansible cache
cd neosetup
make clean

# Fresh installation
./setup install jiveturkey
```

---

**Next Steps**: After installation, see [Configuration Guide](./configuration.md) for customization options.
