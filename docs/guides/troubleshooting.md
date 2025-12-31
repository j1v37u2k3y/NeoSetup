# 🔧 NeoSetup Troubleshooting Guide

Common issues and their solutions when using NeoSetup.

## 🚨 Quick Diagnostics

### Health Check

Run these commands to diagnose issues:

```bash
# Check system status
./setup status

# Test with dry-run (no changes made)
./setup dry-run

# Verbose output for debugging
./setup install jiveturkey --verbose

# Check Ansible installation
ansible --version

# Validate operator configuration
cd neosetup
python3 scripts/validate_operator.py --all
```

## 🔍 Common Installation Issues

### Ansible Not Found

**Error**: `ansible: command not found` or `ansible-playbook: command not found`

**Solutions**:

```bash
# Option 1: Install via pip (recommended)
pip3 install ansible

# Option 2: System package manager
# Ubuntu/Debian
sudo apt update && sudo apt install ansible

# CentOS/RHEL/Fedora
sudo dnf install ansible
# or
sudo yum install ansible

# macOS
brew install ansible

# Verify installation
ansible --version
```

### Permission Denied Errors

**Error**: `Permission denied` when installing system packages

**Solutions**:

```bash
# Use sudo password prompt
./setup install jiveturkey --ask-become-pass

# Or use make with sudo
cd neosetup
make install OPERATOR=jiveturkey --ask-become-pass

# Check sudo access
sudo -v
```

### Python Version Issues

**Error**: `Python 3.x is required` or module import errors

**Solutions**:

```bash
# Check Python version (need 3.8+)
python3 --version

# Install Python 3.8+
# Ubuntu/Debian
sudo apt install python3.8 python3.8-pip

# CentOS/RHEL
sudo dnf install python38 python38-pip

# Update pip
python3 -m pip install --upgrade pip

# Install required modules
pip3 install ansible pyyaml jinja2
```

### Git Clone Issues

**Error**: Repository cloning fails or SSL certificate issues

**Solutions**:

```bash
# Check Git version
git --version

# Update Git if needed
sudo apt update && sudo apt install git

# SSL certificate issues
git config --global http.sslVerify false  # Temporary fix
git config --global http.sslVerify true   # Re-enable after

# Clone with SSH instead
git clone git@github.com:j1v37u2k3y/NeoSetup.git
```

## 🐚 Shell Configuration Issues

### Shell Not Changing

**Error**: New shell configuration not taking effect

**Solutions**:

```bash
# Reload shell configuration
source ~/.zshrc     # For zsh
source ~/.bashrc    # For bash

# Check default shell
echo $SHELL

# Change default shell manually
chsh -s $(which zsh)

# Restart terminal completely
# Or open a new terminal session

# Check if oh-my-zsh is installed
ls -la ~/.oh-my-zsh
```

### Powerlevel10k Theme Issues

**Error**: Theme not loading or displaying incorrectly

**Solutions**:

```bash
# Reconfigure Powerlevel10k
p10k configure

# Check font installation (requires Nerd Fonts)
# Install MesloLGS NF font manually:
# https://github.com/romkatv/powerlevel10k#manual-font-installation

# Reset configuration
rm ~/.p10k.zsh
source ~/.zshrc

# Check tmux integration
tmux new-session -d -s test
tmux list-sessions
tmux kill-session -t test
```

### Plugin Loading Errors

**Error**: Zsh plugins not loading or causing errors

**Solutions**:

```bash
# Update oh-my-zsh
cd ~/.oh-my-zsh && git pull

# Check plugin directory
ls -la ~/.oh-my-zsh/plugins/

# Reinstall plugins
cd ~/.oh-my-zsh/plugins/
git clone https://github.com/zsh-users/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting

# Check for conflicting configurations
grep -r "plugins=" ~/.zshrc ~/.oh-my-zsh/
```

## 🖥️ Tmux Configuration Issues

### Tmux Not Starting

**Error**: `tmux: command not found` or tmux fails to start

**Solutions**:

```bash
# Install tmux
# Ubuntu/Debian
sudo apt install tmux

# CentOS/RHEL/Fedora
sudo dnf install tmux

# macOS
brew install tmux

# Check tmux version (need 2.1+)
tmux -V

# Test tmux manually
tmux new-session -d -s test
tmux list-sessions
tmux attach -t test
```

### Configuration Not Loading

**Error**: Custom tmux configuration not taking effect

**Solutions**:

```bash
# Check tmux config file
ls -la ~/.tmux.conf

# Reload tmux configuration
tmux source-file ~/.tmux.conf

# Or inside tmux session
# Ctrl+b : source-file ~/.tmux.conf

# Check for syntax errors
tmux -f ~/.tmux.conf new-session -d -s test
```

### Color Issues

**Error**: Colors not displaying correctly in tmux

**Solutions**:

```bash
# Check terminal color support
echo $TERM

# Set correct terminal type
export TERM=screen-256color    # For tmux
export TERM=xterm-256color     # For regular terminal

# Add to shell config
echo 'export TERM=screen-256color' >> ~/.zshrc

# Test colors
tmux new-session -d 'echo -e "\e[31mRed\e[0m \e[32mGreen\e[0m \e[34mBlue\e[0m"'
```

## 🛠️ Tool Installation Issues

### Package Not Found

**Error**: Specific CLI tools fail to install

**Solutions**:

```bash
# Update package lists
sudo apt update        # Debian/Ubuntu
sudo dnf update       # Fedora/RHEL

# Install missing dependencies
sudo apt install curl wget gpg software-properties-common

# Check tool availability
# For eza (modern ls)
which eza || echo "eza not installed"

# For bat (better cat)
which bat || which batcat

# Manual installation if package missing
# Example: Install eza manually
curl -sS https://raw.githubusercontent.com/eza-community/eza/main/deb.asc | sudo gpg --dearmor -o /usr/share/keyrings/gierens.gpg
echo "deb [signed-by=/usr/share/keyrings/gierens.gpg] http://deb.gierens.de stable main" | sudo tee /etc/apt/sources.list.d/gierens.list
sudo apt update && sudo apt install eza
```

### Snap/Flatpak Issues

**Error**: Snap or Flatpak packages fail to install

**Solutions**:

```bash
# Check snap service
sudo systemctl status snapd

# Start snap service
sudo systemctl start snapd
sudo systemctl enable snapd

# Update snap
sudo snap refresh

# For Flatpak
sudo apt install flatpak
flatpak remote-add --if-not-exists flathub \
  https://flathub.org/repo/flathub.flatpakrepo
```

### Docker Installation Issues

**Error**: Docker installation or setup fails

**Solutions**:

```bash
# Check if Docker is running
sudo systemctl status docker

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker  # Or logout/login

# Test Docker installation
docker run hello-world

# Check Docker version
docker --version
docker-compose --version

# Reinstall Docker if needed
sudo apt remove docker docker-engine docker.io containerd runc
./setup docker  # Reinstall via NeoSetup
```

## 🔒 Security Tool Issues

### Network Tool Permissions

**Error**: nmap or other network tools fail with permission errors

**Solutions**:

```bash
# Run with sudo for network scanning
sudo nmap -sS target.com

# Or add capabilities (more secure)
sudo setcap cap_net_raw,cap_net_admin=eip $(which nmap)

# Check firewall isn't blocking
sudo ufw status
sudo iptables -L

# For Wireshark capture permissions
sudo usermod -aG wireshark $USER
newgrp wireshark
```

### Container Security Functions

**Error**: Docker-based security functions not working

**Solutions**:

```bash
# Check Docker is accessible
docker ps

# Check security container images
docker images | grep security

# Pull required images
docker pull kalilinux/kali-rolling
docker pull remnux/remnux-distro

# Test container function
docker run --rm -it kalilinux/kali-rolling nmap --version
```

## 🖥️ System-Specific Issues

### macOS Issues

**Common macOS problems**:

```bash
# Install Homebrew first
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Command Line Tools
sudo xcode-select --install

# Permission issues with /usr/local
sudo chown -R $(whoami) /usr/local/Cellar
sudo chown -R $(whoami) /usr/local/lib
sudo chown -R $(whoami) /usr/local/bin

# Python path issues
export PATH="/usr/local/opt/python/libexec/bin:$PATH"
```

### WSL (Windows Subsystem for Linux) Issues

**Common WSL problems**:

```bash
# Update WSL
wsl --update

# Check WSL version
wsl -l -v

# Set as default
wsl --set-default Ubuntu-20.04

# Windows path issues
export PATH="$PATH:/mnt/c/Windows/System32"

# Fix line endings
git config --global core.autocrlf false
```

### CentOS/RHEL Issues

**Common Enterprise Linux problems**:

```bash
# Enable EPEL repository
sudo dnf install epel-release

# Or for CentOS 7
sudo yum install epel-release

# Install development tools
sudo dnf groupinstall "Development Tools"

# Python 3.8+ on older systems
sudo dnf install python38 python38-pip
alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
```

## 🧪 Development and Testing Issues

### Ansible Lint Errors

**Error**: Ansible playbook validation fails

**Solutions**:

```bash
# Install ansible-lint
pip3 install ansible-lint

# Run lint check
cd neosetup
ansible-lint .

# Check specific playbook
ansible-lint playbooks/site.yml

# Fix common issues
ansible-playbook playbooks/site.yml --syntax-check
```

### Operator Validation Errors

**Error**: Custom operator fails validation

**Solutions**:

```bash
# Validate specific operator
cd neosetup
python3 scripts/validate_operator.py myoperator

# Check schema
cat schema/operator_schema.yml

# Validate all operators
python3 scripts/validate_operator.py --all

# Get detailed validation info
python3 scripts/validate_operator.py --info
```

### CI/CD Pipeline Issues

**Error**: GitHub Actions workflows fail

**Solutions**:

```bash
# Run pre-commit locally (Docker-based - matches CI)
./scripts/run-precommit.sh run --all-files

# Install git hooks (uses Docker)
git config core.hooksPath .githooks

# Check workflow files
yamllint .github/workflows/*.yml

# Check secrets and variables
gh secret list
gh variable list
```

**Note**: CI runs 4 jobs: `pre-commit`, `security-scan`, `ansible-syntax`, `docs-validation`.
The `pre-commit` job runs all 20 hooks - same as local Docker pre-commit.

## 🔄 Recovery and Reset

### Complete Reset

**If everything is broken, start fresh**:

```bash
# Backup important files
cp ~/.zshrc ~/.zshrc.backup
cp ~/.tmux.conf ~/.tmux.conf.backup

# Remove NeoSetup configurations
rm -rf ~/.oh-my-zsh
rm -f ~/.zshrc ~/.tmux.conf
rm -rf ~/.neosetup

# Fresh installation
cd NeoSetup
./setup install base    # Start with minimal setup
```

### Selective Reset

**Reset specific components**:

```bash
# Reset shell only
rm -rf ~/.oh-my-zsh ~/.zshrc
./setup shell matrix

# Reset tmux only
rm -f ~/.tmux.conf
./setup tmux

# Reset tools only
./setup tools jiveturkey
```

## 📞 Getting Help

### Debug Information Collection

When reporting issues, collect this information:

```bash
# System information
uname -a
lsb_release -a  # Linux
sw_vers        # macOS

# Software versions
ansible --version
python3 --version
git --version
tmux -V

# NeoSetup status
./setup status

# Detailed logs
./setup install jiveturkey --verbose > install.log 2>&1
```

### Reporting Bugs

1. **Check existing issues**: [GitHub Issues](https://github.com/j1v37u2k3y/NeoSetup/issues)
2. **Create bug report**: Use the bug report template
3. **Include debug information**: System info, logs, steps to reproduce
4. **Minimal reproduction**: Try with `base` operator first

### Community Support

- **GitHub Discussions**: General questions and community help
- **Issues**: Bug reports and feature requests  
- **Matrix Chat**: Real-time community support (coming soon)

---

**Remember**: When in doubt, take the blue pill and start with the `base` operator.
You can always upgrade to `matrix` or `jiveturkey` later.
