# ⚙️ NeoSetup Installation Guide

Complete guide for installing and configuring your Matrix-themed development environment.

## 📋 Prerequisites

### Required

- **Git** - For cloning the repository
- **Python 3.8+** - For Ansible automation
- **sudo access** - Some installations require elevated privileges

### Operating System Support

- ✅ Ubuntu 20.04+
- ✅ Debian 11+
- ✅ CentOS/RHEL 8+
- ✅ Fedora 35+
- ✅ macOS 11+

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

# Verbose installation
make install OPERATOR=jiveturkey VERBOSE=true
```

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
- Minimal tool set (curl, wget, jq, unzip)
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

- Advanced security tools (nmap, netcat, wireshark)
- Docker-based security functions
- Network analysis capabilities
- Development tools (terraform, kubectl, ansible)
- Penetration testing utilities

### macOS Operator

**Perfect for**: macOS users who want a polished native experience

```bash
./setup install macos
```

**Includes**: Everything from `base` plus:

- Complete Homebrew integration with architecture detection
- Window management with Rectangle
- System monitoring with Stats
- Configuration sync with Mackup
- macOS-specific aliases (`brewup`, `showfiles`, `hidefiles`)

### Python Dev Operator

**Perfect for**: Python developers

```bash
./setup install python_dev
```

**Includes**: Everything from `base` plus:

- Python version management with pyenv
- Package management (pip, pipx, Poetry)
- Code quality tools (black, flake8, mypy, isort, pylint)
- Testing frameworks (pytest, tox, coverage)
- Helper functions (`mkproject`, `pyinfo`, `pyformat`)

### Go Dev Operator

**Perfect for**: Go developers

```bash
./setup install go_dev
```

**Includes**: Everything from `base` plus:

- Go toolchain with module support
- Language server and IDE tools (gopls, goimports)
- Linting and security scanning (golangci-lint, gosec)
- Debugging and hot reload (delve, air)
- Helper functions (`mkgo`, `goinfo`, `gocover`, `gobench`)

### Node.js Dev Operator

**Perfect for**: JavaScript and TypeScript developers

```bash
./setup install nodejs_dev
```

**Includes**: Everything from `base` plus:

- Node.js version management with nvm
- Package managers (npm, yarn, pnpm)
- TypeScript development setup
- Testing and build tools (Jest, Vitest, Vite, esbuild)
- Helper functions (`mknode`, `nodeinfo`, `node-clean`)

### Windows WSL Operator

**Perfect for**: Windows users running WSL2

```bash
./setup install windows_wsl
```

**Includes**: Everything from `base` plus:

- WSL2-Windows interoperability tools
- Windows Terminal integration
- Cross-platform clipboard (`clip.exe` / `powershell.exe Get-Clipboard`)
- Windows path integration and aliases (`explorer`, `code`, `cmd`)

## 🔧 Advanced Configuration

### Custom Variables

Create `~/.ansible_local.yml` to override defaults:

```yaml
# Custom shell configuration
shell_env_vars:
  EDITOR: "nvim"
  BROWSER: "firefox"

# Custom aliases
shell_aliases:
  - { alias: "vim", command: "nvim" }
  - { alias: "k", command: "kubectl" }
  - { alias: "tf", command: "terraform" }

# Custom tmux settings
tmux_custom_config: |
  # Additional tmux configuration
  set -g mouse on
  set -g history-limit 10000
```

### Operator Inheritance

Operators use inheritance for clean configuration:

```text
base (essential tools)
 ├── matrix (+ Matrix theme) → jiveturkey (+ security tools)
 ├── macos (+ Homebrew & macOS productivity)
 ├── python_dev (+ pyenv, Poetry, quality tools)
 ├── go_dev (+ Go toolchain & dev utilities)
 ├── nodejs_dev (+ nvm, npm/yarn/pnpm, TypeScript)
 └── windows_wsl (+ WSL2 interoperability)
```

You can extend any existing operator by creating new ones in `neosetup/operators/`.

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
./setup install jiveturkey --ask-become-pass
```

**Network issues**:

```bash
# Test connectivity
curl -s https://github.com

# Use verbose mode
./setup install matrix --verbose
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
