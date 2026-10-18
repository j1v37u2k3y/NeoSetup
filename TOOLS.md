# NeoSetup Tools Reference

> **Auto-generated** - Do not edit manually. Run `python3 neosetup/scripts/generate_tools_doc.py` to regenerate.

This document lists all tools installed by each NeoSetup operator, composed from the
category tool-sets each operator opts into (see
[composable-tool-sets.md](docs/architecture/composable-tool-sets.md)).

## Operator Inheritance

| Operator | Inherits From | Total Tools |
|----------|---------------|-------------|
| `base` | - | 15 |
| `matrix` | base | 21 |
| `jiveturkey` | matrix + base | 49 |
| `macos` | base | 20 |
| `windows_wsl` | base | 20 |
| `python_dev` | base | 36 |
| `nodejs_dev` | base | 16 |
| `go_dev` | base | 16 |

---

## Base

Essential development tools included with every installation.

| Tool | Description | Category |
|------|-------------|----------|
| `act` | Run GitHub Actions locally | development |
| `bat` | Cat with syntax highlighting | modern_cli |
| `btop` | Modern top replacement | modern_cli |
| `curl` | Command-line URL transfer tool | network |
| `delta` | Better git diff | modern_cli |
| `eza` | Modern ls replacement | modern_cli |
| `fd` | Fast find replacement | modern_cli |
| `fzf` | Fuzzy finder | modern_cli |
| `htop` | Interactive process viewer | system |
| `jq` | JSON processor | power_user |
| `pre-commit` | Git pre-commit hooks framework | development |
| `ripgrep` | Fast grep replacement | modern_cli |
| `tree` | Directory tree viewer | system |
| `wget` | Non-interactive network downloader | network |
| `yamllint` | YAML linting and validation | development |

---

## Matrix

Matrix-themed tools layered on top of base.

| Tool | Description | Category |
|------|-------------|----------|
| `act` | Run GitHub Actions locally | development |
| `bat` | Cat with syntax highlighting | modern_cli |
| `btop` | Modern top replacement | modern_cli |
| `cmatrix` | Digital rain effect | matrix |
| `cowsay` | ASCII cow messages | matrix |
| `curl` | Command-line URL transfer tool | network |
| `delta` | Better git diff | modern_cli |
| `eza` | Modern ls replacement | modern_cli |
| `fastfetch` | System info with ASCII art (maintained neofetch successor) | matrix |
| `fd` | Fast find replacement | modern_cli |
| `figlet` | ASCII art text | matrix |
| `fortune` | Random quotes | matrix |
| `fzf` | Fuzzy finder | modern_cli |
| `htop` | Interactive process viewer | system |
| `jq` | JSON processor | power_user |
| `lolcat` | Rainbow text output | matrix |
| `pre-commit` | Git pre-commit hooks framework | development |
| `ripgrep` | Fast grep replacement | modern_cli |
| `tree` | Directory tree viewer | system |
| `wget` | Non-interactive network downloader | network |
| `yamllint` | YAML linting and validation | development |

---

## Jiveturkey

Power-user setup with the full red-team arsenal (offsec on Linux).

| Tool | Description | Category |
|------|-------------|----------|
| `act` | Run GitHub Actions locally | development |
| `bat` | Cat with syntax highlighting | modern_cli |
| `bloodhound` | Active Directory attack-path mapping (GUI; no working installer — see note) | security |
| `btop` | Modern top replacement | modern_cli |
| `burp-suite` | Web security testing proxy (GUI; macOS cask, Linux installer in Phase 3b) | security |
| `cmatrix` | Digital rain effect | matrix |
| `cowsay` | ASCII cow messages | matrix |
| `curl` | Command-line URL transfer tool | network |
| `delta` | Better git diff | modern_cli |
| `duf` | Modern, colorful disk usage / free-space viewer | monitoring |
| `eza` | Modern ls replacement | modern_cli |
| `fastfetch` | System info with ASCII art (maintained neofetch successor) | matrix |
| `fd` | Fast find replacement | modern_cli |
| `ffuf` | Fast web fuzzer | security |
| `figlet` | ASCII art text | matrix |
| `fortune` | Random quotes | matrix |
| `fzf` | Fuzzy finder | modern_cli |
| `gh` | GitHub CLI | development |
| `git-quick-stats` | Git repository statistics and contribution reports | git |
| `glances` | Cross-platform system monitoring dashboard | monitoring |
| `gobuster` | Directory/DNS/vhost brute-forcer | security |
| `grc` | Generic colouriser for command and log output | logs |
| `hashcat` | Advanced password recovery | security |
| `htop` | Interactive process viewer | system |
| `httpie` | Modern HTTP client | power_user |
| `impacket` | Python classes for working with network protocols (SMB/MSRPC/etc.) | security |
| `john` | John the Ripper password cracker | security |
| `jq` | JSON processor | power_user |
| `lazygit` | Git TUI | development |
| `lnav` | The Log File Navigator - interactive log viewer | logs |
| `lolcat` | Rainbow text output | matrix |
| `mc` | Midnight Commander | file_manager |
| `multitail` | Tail multiple log files in one split window | logs |
| `ncdu` | NCurses disk usage | power_user |
| `netcat` | Network utility | security |
| `nmap` | Network scanner | security |
| `nuclei` | Template-based vulnerability scanner (macOS via brew; Linux installer in Phase 3b) | security |
| `pre-commit` | Git pre-commit hooks framework | development |
| `procs` | Modern ps replacement with a richer, colorized view | monitoring |
| `ranger` | Terminal file manager | file_manager |
| `ripgrep` | Fast grep replacement | modern_cli |
| `shellcheck` | Shell script analyzer | development |
| `sqlmap` | Automatic SQL injection and takeover tool | security |
| `tldr` | Simplified man pages | power_user |
| `tree` | Directory tree viewer | system |
| `wget` | Non-interactive network downloader | network |
| `wireshark` | Network protocol analyzer | security |
| `yamllint` | YAML linting and validation | development |
| `yq` | YAML processor | power_user |

---

## Macos

macOS-specific utilities for system integration.

| Tool | Description | Category |
|------|-------------|----------|
| `act` | Run GitHub Actions locally | development |
| `bat` | Cat with syntax highlighting | modern_cli |
| `btop` | Modern top replacement | modern_cli |
| `curl` | Command-line URL transfer tool | network |
| `delta` | Better git diff | modern_cli |
| `duti` | macOS file type associations | macos |
| `eza` | Modern ls replacement | modern_cli |
| `fd` | Fast find replacement | modern_cli |
| `fzf` | Fuzzy finder | modern_cli |
| `htop` | Interactive process viewer | system |
| `jq` | JSON processor | power_user |
| `mackup` | Sync app settings | macos |
| `mas` | Mac App Store CLI | macos |
| `pre-commit` | Git pre-commit hooks framework | development |
| `rectangle` | Window management for macOS | macos |
| `ripgrep` | Fast grep replacement | modern_cli |
| `stats` | macOS system stats in menu bar | macos |
| `tree` | Directory tree viewer | system |
| `wget` | Non-interactive network downloader | network |
| `yamllint` | YAML linting and validation | development |

---

## Windows Wsl

Tools for Windows Subsystem for Linux integration.

| Tool | Description | Category |
|------|-------------|----------|
| `act` | Run GitHub Actions locally | development |
| `bat` | Cat with syntax highlighting | modern_cli |
| `btop` | Modern top replacement | modern_cli |
| `build-essential` | Essential build tools for compilation | wsl |
| `curl` | Command-line URL transfer tool | network |
| `delta` | Better git diff | modern_cli |
| `eza` | Modern ls replacement | modern_cli |
| `fd` | Fast find replacement | modern_cli |
| `fzf` | Fuzzy finder | modern_cli |
| `htop` | Interactive process viewer | system |
| `jq` | JSON processor | power_user |
| `powershell` | PowerShell Core for cross-platform scripting | wsl |
| `pre-commit` | Git pre-commit hooks framework | development |
| `python3-pip` | Python package installer | wsl |
| `ripgrep` | Fast grep replacement | modern_cli |
| `tree` | Directory tree viewer | system |
| `unzip` | Archive extraction utility | system |
| `wget` | Non-interactive network downloader | network |
| `wslu` | WSL utilities for Windows integration | wsl |
| `yamllint` | YAML linting and validation | development |

---

## Python Dev

Python development toolchain.

| Tool | Description | Category |
|------|-------------|----------|
| `act` | Run GitHub Actions locally | development |
| `bandit` | Security linter for Python | python |
| `bat` | Cat with syntax highlighting | modern_cli |
| `black` | Python code formatter | python |
| `btop` | Modern top replacement | modern_cli |
| `cookiecutter` | Project templating tool | python |
| `coverage` | Python code coverage measurement | python |
| `curl` | Command-line URL transfer tool | network |
| `delta` | Better git diff | modern_cli |
| `eza` | Modern ls replacement | modern_cli |
| `fd` | Fast find replacement | modern_cli |
| `flake8` | Python code linter | python |
| `fzf` | Fuzzy finder | modern_cli |
| `htop` | Interactive process viewer | system |
| `ipython` | Enhanced interactive Python shell | python |
| `isort` | Python import sorter | python |
| `jq` | JSON processor | power_user |
| `jupyter` | Interactive computing environment | python |
| `memory-profiler` | Monitor memory usage of Python code | python |
| `mkdocs` | Project documentation with Markdown | python |
| `mypy` | Static type checker for Python | python |
| `pipx` | Install and run Python applications in isolated environments | python |
| `poetry` | Python dependency management and packaging | python |
| `pre-commit` | Git pre-commit hooks framework | development |
| `py-spy` | Sampling profiler for Python programs | python |
| `pyenv` | Python version management | python |
| `pylint` | Python linter | python |
| `pytest` | Python testing framework | python |
| `ripgrep` | Fast grep replacement | modern_cli |
| `sphinx` | Documentation generator | python |
| `tox` | Python test automation across environments | python |
| `tree` | Directory tree viewer | system |
| `virtualenv` | Python virtual environment creator | python |
| `virtualenvwrapper` | Wrapper utilities for virtualenv | python |
| `wget` | Non-interactive network downloader | network |
| `yamllint` | YAML linting and validation | development |

---

## Nodejs Dev

Node.js development environment.

| Tool | Description | Category |
|------|-------------|----------|
| `act` | Run GitHub Actions locally | development |
| `bat` | Cat with syntax highlighting | modern_cli |
| `btop` | Modern top replacement | modern_cli |
| `curl` | Command-line URL transfer tool | network |
| `delta` | Better git diff | modern_cli |
| `eza` | Modern ls replacement | modern_cli |
| `fd` | Fast find replacement | modern_cli |
| `fzf` | Fuzzy finder | modern_cli |
| `htop` | Interactive process viewer | system |
| `jq` | JSON processor | power_user |
| `nvm` | Node.js version manager and global npm tooling | nodejs |
| `pre-commit` | Git pre-commit hooks framework | development |
| `ripgrep` | Fast grep replacement | modern_cli |
| `tree` | Directory tree viewer | system |
| `wget` | Non-interactive network downloader | network |
| `yamllint` | YAML linting and validation | development |

---

## Go Dev

Go toolchain and go-install developer tools.

| Tool | Description | Category |
|------|-------------|----------|
| `act` | Run GitHub Actions locally | development |
| `bat` | Cat with syntax highlighting | modern_cli |
| `btop` | Modern top replacement | modern_cli |
| `curl` | Command-line URL transfer tool | network |
| `delta` | Better git diff | modern_cli |
| `eza` | Modern ls replacement | modern_cli |
| `fd` | Fast find replacement | modern_cli |
| `fzf` | Fuzzy finder | modern_cli |
| `go` | Go toolchain and go-install-based developer tools | go |
| `htop` | Interactive process viewer | system |
| `jq` | JSON processor | power_user |
| `pre-commit` | Git pre-commit hooks framework | development |
| `ripgrep` | Fast grep replacement | modern_cli |
| `tree` | Directory tree viewer | system |
| `wget` | Non-interactive network downloader | network |
| `yamllint` | YAML linting and validation | development |

---

## Category Tool Sets

Named, reusable bundles operators compose. See `tool_sets` in `tool_registry.yml`.

### `core`

- `act` — Run GitHub Actions locally
- `curl` — Command-line URL transfer tool
- `htop` — Interactive process viewer
- `jq` — JSON processor
- `pre-commit` — Git pre-commit hooks framework
- `tree` — Directory tree viewer
- `wget` — Non-interactive network downloader
- `yamllint` — YAML linting and validation

### `modern_cli`

- `bat` — Cat with syntax highlighting
- `btop` — Modern top replacement
- `delta` — Better git diff
- `eza` — Modern ls replacement
- `fd` — Fast find replacement
- `fzf` — Fuzzy finder
- `ripgrep` — Fast grep replacement

### `matrix_fun`

- `cmatrix` — Digital rain effect
- `cowsay` — ASCII cow messages
- `fastfetch` — System info with ASCII art (maintained neofetch successor)
- `figlet` — ASCII art text
- `fortune` — Random quotes
- `lolcat` — Rainbow text output

### `jiveturkey_tools`

- `duf` — Modern, colorful disk usage / free-space viewer
- `gh` — GitHub CLI
- `git-quick-stats` — Git repository statistics and contribution reports
- `glances` — Cross-platform system monitoring dashboard
- `grc` — Generic colouriser for command and log output
- `httpie` — Modern HTTP client
- `lazygit` — Git TUI
- `lnav` — The Log File Navigator - interactive log viewer
- `mc` — Midnight Commander
- `multitail` — Tail multiple log files in one split window
- `ncdu` — NCurses disk usage
- `netcat` — Network utility
- `nmap` — Network scanner
- `procs` — Modern ps replacement with a richer, colorized view
- `ranger` — Terminal file manager
- `shellcheck` — Shell script analyzer
- `tldr` — Simplified man pages
- `yq` — YAML processor

### `python`

- `black` — Python code formatter
- `cookiecutter` — Project templating tool
- `flake8` — Python code linter
- `ipython` — Enhanced interactive Python shell
- `isort` — Python import sorter
- `jupyter` — Interactive computing environment
- `mypy` — Static type checker for Python
- `pipx` — Install and run Python applications in isolated environments
- `poetry` — Python dependency management and packaging
- `pyenv` — Python version management
- `pytest` — Python testing framework

### `node`

- `nvm` — Node.js version manager and global npm tooling

### `go`

- `go` — Go toolchain and go-install-based developer tools

### `macos`

- `duti` — macOS file type associations
- `mackup` — Sync app settings
- `mas` — Mac App Store CLI
- `rectangle` — Window management for macOS
- `stats` — macOS system stats in menu bar

### `windows_wsl`

- `build-essential` — Essential build tools for compilation
- `powershell` — PowerShell Core for cross-platform scripting
- `python3-pip` — Python package installer
- `wslu` — WSL utilities for Windows integration

### `security`

- `ffuf` — Fast web fuzzer
- `gobuster` — Directory/DNS/vhost brute-forcer
- `hashcat` — Advanced password recovery
- `john` — John the Ripper password cracker
- `netcat` — Network utility
- `nmap` — Network scanner
- `sqlmap` — Automatic SQL injection and takeover tool
- `wireshark` — Network protocol analyzer

### `offsec`

- `bloodhound` — Active Directory attack-path mapping (GUI; no working installer — see note)
- `burp-suite` — Web security testing proxy (GUI; macOS cask, Linux installer in Phase 3b)
- `ffuf` — Fast web fuzzer
- `gobuster` — Directory/DNS/vhost brute-forcer
- `hashcat` — Advanced password recovery
- `impacket` — Python classes for working with network protocols (SMB/MSRPC/etc.)
- `john` — John the Ripper password cracker
- `netcat` — Network utility
- `nmap` — Network scanner
- `nuclei` — Template-based vulnerability scanner (macOS via brew; Linux installer in Phase 3b)
- `sqlmap` — Automatic SQL injection and takeover tool
- `wireshark` — Network protocol analyzer

### `cloud`

- `awscli` — Amazon Web Services CLI (macOS via brew; Linux v2 installer is a follow-up)
- `azure-cli` — Azure command-line interface
- `helm` — Kubernetes package manager
- `kubectl` — Kubernetes command-line tool
- `terraform` — Infrastructure as Code tool

---

## Full Tool Registry

Complete list of all tools available in NeoSetup.

| Tool | Description | Category | Platforms |
|------|-------------|----------|-----------|
| `act` | Run GitHub Actions locally | development | custom |
| `awscli` | Amazon Web Services CLI (macOS via brew; Linux v2 installer is a follow-up) | cloud | darwin |
| `azure-cli` | Azure command-line interface | cloud | custom |
| `bandit` | Security linter for Python | python | pip |
| `bat` | Cat with syntax highlighting | modern_cli | darwin, debian, redhat, ubuntu |
| `black` | Python code formatter | python | pip |
| `bloodhound` | Active Directory attack-path mapping (GUI; no working installer — see note) | security | custom |
| `btop` | Modern top replacement | modern_cli | darwin, debian, redhat, ubuntu |
| `build-essential` | Essential build tools for compilation | wsl | debian, ubuntu, wsl |
| `burp-suite` | Web security testing proxy (GUI; macOS cask, Linux installer in Phase 3b) | security | darwin |
| `cmatrix` | Digital rain effect | matrix | darwin, debian, redhat, ubuntu |
| `cookiecutter` | Project templating tool | python | pipx |
| `coverage` | Python code coverage measurement | python | pip |
| `cowsay` | ASCII cow messages | matrix | darwin, debian, redhat, ubuntu |
| `curl` | Command-line URL transfer tool | network | darwin, debian, redhat, ubuntu |
| `delta` | Better git diff | modern_cli | darwin |
| `docker-compose` | Multi-container Docker applications | cloud | darwin, debian, redhat, ubuntu |
| `duf` | Modern, colorful disk usage / free-space viewer | monitoring | darwin, debian, ubuntu |
| `duti` | macOS file type associations | macos | darwin |
| `eza` | Modern ls replacement | modern_cli | darwin |
| `fastfetch` | System info with ASCII art (maintained neofetch successor) | matrix | darwin |
| `fd` | Fast find replacement | modern_cli | darwin, debian, redhat, ubuntu |
| `ffuf` | Fast web fuzzer | security | darwin, debian, ubuntu |
| `figlet` | ASCII art text | matrix | darwin, debian, redhat, ubuntu |
| `flake8` | Python code linter | python | pip |
| `fortune` | Random quotes | matrix | darwin, debian, redhat, ubuntu |
| `fzf` | Fuzzy finder | modern_cli | darwin, debian, redhat, ubuntu |
| `gh` | GitHub CLI | development | darwin, debian, redhat, ubuntu |
| `git-quick-stats` | Git repository statistics and contribution reports | git | darwin, debian, ubuntu |
| `glances` | Cross-platform system monitoring dashboard | monitoring | darwin, debian, redhat, ubuntu |
| `go` | Go toolchain and go-install-based developer tools | go | custom |
| `gobuster` | Directory/DNS/vhost brute-forcer | security | darwin, debian, ubuntu |
| `grc` | Generic colouriser for command and log output | logs | darwin, debian, redhat, ubuntu |
| `hashcat` | Advanced password recovery | security | darwin, debian, ubuntu |
| `helm` | Kubernetes package manager | cloud | custom |
| `htop` | Interactive process viewer | system | darwin, debian, redhat, ubuntu |
| `httpie` | Modern HTTP client | power_user | darwin, debian, redhat, ubuntu |
| `impacket` | Python classes for working with network protocols (SMB/MSRPC/etc.) | security | pip |
| `ipython` | Enhanced interactive Python shell | python | pip |
| `isort` | Python import sorter | python | pip |
| `john` | John the Ripper password cracker | security | darwin, debian, ubuntu |
| `jq` | JSON processor | power_user | darwin, debian, redhat, ubuntu |
| `jupyter` | Interactive computing environment | python | pip |
| `kubectl` | Kubernetes command-line tool | cloud | custom |
| `lazygit` | Git TUI | development | darwin |
| `lnav` | The Log File Navigator - interactive log viewer | logs | darwin, debian, redhat, ubuntu |
| `lolcat` | Rainbow text output | matrix | darwin, debian, redhat, ubuntu |
| `mackup` | Sync app settings | macos | darwin |
| `mas` | Mac App Store CLI | macos | darwin |
| `mc` | Midnight Commander | file_manager | darwin, debian, redhat, ubuntu |
| `memory-profiler` | Monitor memory usage of Python code | python | pip |
| `mkdocs` | Project documentation with Markdown | python | pip |
| `multitail` | Tail multiple log files in one split window | logs | darwin, debian, redhat, ubuntu |
| `mypy` | Static type checker for Python | python | pip |
| `ncdu` | NCurses disk usage | power_user | darwin, debian, redhat, ubuntu |
| `netcat` | Network utility | security | darwin, debian, redhat, ubuntu |
| `nmap` | Network scanner | security | darwin, debian, redhat, ubuntu |
| `nuclei` | Template-based vulnerability scanner (macOS via brew; Linux installer in Phase 3b) | security | darwin |
| `nvm` | Node.js version manager and global npm tooling | nodejs | custom |
| `pipx` | Install and run Python applications in isolated environments | python | darwin, debian, redhat, ubuntu |
| `poetry` | Python dependency management and packaging | python | custom |
| `powershell` | PowerShell Core for cross-platform scripting | wsl | debian, ubuntu, wsl |
| `pre-commit` | Git pre-commit hooks framework | development | pip |
| `procs` | Modern ps replacement with a richer, colorized view | monitoring | darwin |
| `py-spy` | Sampling profiler for Python programs | python | pip |
| `pyenv` | Python version management | python | custom |
| `pylint` | Python linter | python | pip |
| `pytest` | Python testing framework | python | pip |
| `python3-pip` | Python package installer | wsl | debian, ubuntu, wsl |
| `ranger` | Terminal file manager | file_manager | darwin, debian, redhat, ubuntu |
| `rectangle` | Window management for macOS | macos | darwin |
| `ripgrep` | Fast grep replacement | modern_cli | darwin, debian, redhat, ubuntu |
| `shellcheck` | Shell script analyzer | development | darwin, debian, redhat, ubuntu |
| `sphinx` | Documentation generator | python | pip |
| `sqlmap` | Automatic SQL injection and takeover tool | security | darwin, debian, ubuntu |
| `stats` | macOS system stats in menu bar | macos | darwin |
| `terraform` | Infrastructure as Code tool | cloud | custom |
| `tldr` | Simplified man pages | power_user | pip |
| `tox` | Python test automation across environments | python | pip |
| `tree` | Directory tree viewer | system | darwin, debian, redhat, ubuntu |
| `unzip` | Archive extraction utility | system | darwin, debian, redhat, ubuntu |
| `virtualenv` | Python virtual environment creator | python | pip |
| `virtualenvwrapper` | Wrapper utilities for virtualenv | python | pip |
| `wget` | Non-interactive network downloader | network | darwin, debian, redhat, ubuntu |
| `wireshark` | Network protocol analyzer | security | darwin, debian, ubuntu |
| `wslu` | WSL utilities for Windows integration | wsl | debian, ubuntu, wsl |
| `yamllint` | YAML linting and validation | development | pip |
| `yq` | YAML processor | power_user | darwin |

---

## Installation

Tools are automatically installed based on your chosen operator:

```bash
# Install with base operator (minimal)
make install OPERATOR=base

# Install with matrix operator (base + matrix-themed tools)
make install OPERATOR=matrix

# Install with jiveturkey operator (base + matrix + power-user + offsec on Linux)
make install OPERATOR=jiveturkey
```

## Adding Custom Tools

To request a new tool, open an issue with the `operator` label or submit a PR adding it to:

- `neosetup/roles/tools/vars/tool_registry.yml`

---

*Generated from `neosetup/roles/tools/vars/tool_registry.yml` +
`neosetup/group_vars/all/operators.yml` + each operator's `vars.yml`.*
