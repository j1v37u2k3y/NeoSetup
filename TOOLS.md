# NeoSetup Tools Reference

> **Auto-generated** - Do not edit manually. Run `python3 neosetup/scripts/generate_tools_doc.py` to regenerate.

This document lists all tools installed by each NeoSetup operator.

## Operator Inheritance

```
base (essential tools)
  └── matrix (base + matrix-themed tools)
        └── jiveturkey (base + matrix + power-user tools)
```

## Quick Reference

| Operator     | Inherits From | Unique Tools | Total Tools |
|--------------|---------------|--------------|-------------|
| `base`       | -             | 8            | 8           |
| `matrix`     | base          | 6            | 21          |
| `jiveturkey` | base + matrix | 11           | 32          |

> **Note**: All operators also include `modern_cli` tools (7 tools) for enhanced terminal experience.

---

## Base

Essential development tools included with every installation.

| Tool         | Description                        | Category    |
|--------------|------------------------------------|-------------|
| `act`        | Run GitHub Actions locally         | development |
| `curl`       | Command-line URL transfer tool     | network     |
| `htop`       | Interactive process viewer         | system      |
| `jq`         | JSON processor                     | power_user  |
| `pre-commit` | Git pre-commit hooks framework     | development |
| `tree`       | Directory tree viewer              | system      |
| `wget`       | Non-interactive network downloader | network     |
| `yamllint`   | YAML linting and validation        | development |

---

## Matrix

Matrix-themed tools for the cyberpunk aesthetic.

| Tool       | Description                | Category |
|------------|----------------------------|----------|
| `cmatrix`  | Digital rain effect        | matrix   |
| `cowsay`   | ASCII cow messages         | matrix   |
| `figlet`   | ASCII art text             | matrix   |
| `fortune`  | Random quotes              | matrix   |
| `lolcat`   | Rainbow text output        | matrix   |
| `neofetch` | System info with ASCII art | matrix   |

---

## Jiveturkey

Power-user tools for advanced workflows.

| Tool         | Description           | Category     |
|--------------|-----------------------|--------------|
| `gh`         | GitHub CLI            | development  |
| `httpie`     | Modern HTTP client    | power_user   |
| `lazygit`    | Git TUI               | development  |
| `mc`         | Midnight Commander    | file_manager |
| `ncdu`       | NCurses disk usage    | power_user   |
| `netcat`     | Network utility       | security     |
| `nmap`       | Network scanner       | security     |
| `ranger`     | Terminal file manager | file_manager |
| `shellcheck` | Shell script analyzer | development  |
| `tldr`       | Simplified man pages  | power_user   |
| `yq`         | YAML processor        | power_user   |

---

## Modern Cli

Modern replacements for classic Unix tools.

| Tool      | Description                  | Category   |
|-----------|------------------------------|------------|
| `bat`     | Cat with syntax highlighting | modern_cli |
| `btop`    | Modern top replacement       | modern_cli |
| `delta`   | Better git diff              | modern_cli |
| `eza`     | Modern ls replacement        | modern_cli |
| `fd`      | Fast find replacement        | modern_cli |
| `fzf`     | Fuzzy finder                 | modern_cli |
| `ripgrep` | Fast grep replacement        | modern_cli |

---

## Macos Tools

macOS-specific utilities for system integration.

| Tool        | Description                    | Category |
|-------------|--------------------------------|----------|
| `duti`      | macOS file type associations   | macos    |
| `mackup`    | Sync app settings              | macos    |
| `mas`       | Mac App Store CLI              | macos    |
| `rectangle` | Window management for macOS    | macos    |
| `stats`     | macOS system stats in menu bar | macos    |

---

## Windows Wsl

Tools for Windows Subsystem for Linux integration.

| Tool              | Description                                  | Category |
|-------------------|----------------------------------------------|----------|
| `build-essential` | Essential build tools for compilation        | wsl      |
| `powershell`      | PowerShell Core for cross-platform scripting | wsl      |
| `python3-pip`     | Python package installer                     | wsl      |
| `wslu`            | WSL utilities for Windows integration        | wsl      |

---

## Python Dev

Python development toolchain.

| Tool           | Description                                                  | Category |
|----------------|--------------------------------------------------------------|----------|
| `black`        | Python code formatter                                        | python   |
| `cookiecutter` | Project templating tool                                      | python   |
| `flake8`       | Python code linter                                           | python   |
| `ipython`      | Enhanced interactive Python shell                            | python   |
| `isort`        | Python import sorter                                         | python   |
| `jupyter`      | Interactive computing environment                            | python   |
| `mypy`         | Static type checker for Python                               | python   |
| `pipx`         | Install and run Python applications in isolated environments | python   |
| `poetry`       | Python dependency management and packaging                   | python   |
| `pyenv`        | Python version management                                    | python   |
| `pytest`       | Python testing framework                                     | python   |

---

## Cloud Tools

Cloud and DevOps tools for AWS, Kubernetes, etc.

| Tool             | Description                         | Category |
|------------------|-------------------------------------|----------|
| `awscli`         | Amazon Web Services CLI             | cloud    |
| `docker-compose` | Multi-container Docker applications | cloud    |
| `helm`           | Kubernetes package manager          | cloud    |
| `kubectl`        | Kubernetes command-line tool        | cloud    |
| `terraform`      | Infrastructure as Code tool         | cloud    |

---

## Full Tool Registry

Complete list of all tools available in NeoSetup.

| Tool              | Description                                                  | Category     | Platforms                      |
|-------------------|--------------------------------------------------------------|--------------|--------------------------------|
| `act`             | Run GitHub Actions locally                                   | development  | custom                         |
| `awscli`          | Amazon Web Services CLI                                      | cloud        | darwin, debian, redhat, ubuntu |
| `azure-cli`       | Azure command-line interface                                 | cloud        | custom                         |
| `bat`             | Cat with syntax highlighting                                 | modern_cli   | darwin, debian, redhat, ubuntu |
| `black`           | Python code formatter                                        | python       | pip                            |
| `btop`            | Modern top replacement                                       | modern_cli   | darwin, debian, redhat, ubuntu |
| `build-essential` | Essential build tools for compilation                        | wsl          | debian, ubuntu, wsl            |
| `cmatrix`         | Digital rain effect                                          | matrix       | darwin, debian, redhat, ubuntu |
| `cookiecutter`    | Project templating tool                                      | python       | pipx                           |
| `cowsay`          | ASCII cow messages                                           | matrix       | darwin, debian, redhat, ubuntu |
| `curl`            | Command-line URL transfer tool                               | network      | darwin, debian, redhat, ubuntu |
| `delta`           | Better git diff                                              | modern_cli   | darwin, debian, redhat, ubuntu |
| `docker-compose`  | Multi-container Docker applications                          | cloud        | darwin, debian, redhat, ubuntu |
| `duti`            | macOS file type associations                                 | macos        | darwin                         |
| `eza`             | Modern ls replacement                                        | modern_cli   | darwin, debian, redhat, ubuntu |
| `fd`              | Fast find replacement                                        | modern_cli   | darwin, debian, redhat, ubuntu |
| `figlet`          | ASCII art text                                               | matrix       | darwin, debian, redhat, ubuntu |
| `flake8`          | Python code linter                                           | python       | pip                            |
| `fortune`         | Random quotes                                                | matrix       | darwin, debian, redhat, ubuntu |
| `fzf`             | Fuzzy finder                                                 | modern_cli   | darwin, debian, redhat, ubuntu |
| `gh`              | GitHub CLI                                                   | development  | darwin, debian, redhat, ubuntu |
| `helm`            | Kubernetes package manager                                   | cloud        | custom                         |
| `htop`            | Interactive process viewer                                   | system       | darwin, debian, redhat, ubuntu |
| `httpie`          | Modern HTTP client                                           | power_user   | darwin, debian, redhat, ubuntu |
| `ipython`         | Enhanced interactive Python shell                            | python       | pip                            |
| `isort`           | Python import sorter                                         | python       | pip                            |
| `jq`              | JSON processor                                               | power_user   | darwin, debian, redhat, ubuntu |
| `jupyter`         | Interactive computing environment                            | python       | pip                            |
| `kubectl`         | Kubernetes command-line tool                                 | cloud        | custom                         |
| `lazygit`         | Git TUI                                                      | development  | darwin, debian, redhat, ubuntu |
| `lolcat`          | Rainbow text output                                          | matrix       | darwin, debian, redhat, ubuntu |
| `mackup`          | Sync app settings                                            | macos        | darwin                         |
| `mas`             | Mac App Store CLI                                            | macos        | darwin                         |
| `mc`              | Midnight Commander                                           | file_manager | darwin, debian, redhat, ubuntu |
| `mypy`            | Static type checker for Python                               | python       | pip                            |
| `ncdu`            | NCurses disk usage                                           | power_user   | darwin, debian, redhat, ubuntu |
| `neofetch`        | System info with ASCII art                                   | matrix       | darwin, debian, redhat, ubuntu |
| `netcat`          | Network utility                                              | security     | darwin, debian, redhat, ubuntu |
| `nmap`            | Network scanner                                              | security     | darwin, debian, redhat, ubuntu |
| `pipx`            | Install and run Python applications in isolated environments | python       | darwin, debian, redhat, ubuntu |
| `poetry`          | Python dependency management and packaging                   | python       | custom                         |
| `powershell`      | PowerShell Core for cross-platform scripting                 | wsl          | debian, ubuntu, wsl            |
| `pre-commit`      | Git pre-commit hooks framework                               | development  | pip                            |
| `pyenv`           | Python version management                                    | python       | custom                         |
| `pytest`          | Python testing framework                                     | python       | pip                            |
| `python3-pip`     | Python package installer                                     | wsl          | debian, ubuntu, wsl            |
| `ranger`          | Terminal file manager                                        | file_manager | darwin, debian, redhat, ubuntu |
| `rectangle`       | Window management for macOS                                  | macos        | darwin                         |
| `ripgrep`         | Fast grep replacement                                        | modern_cli   | darwin, debian, redhat, ubuntu |
| `shellcheck`      | Shell script analyzer                                        | development  | darwin, debian, redhat, ubuntu |
| `stats`           | macOS system stats in menu bar                               | macos        | darwin                         |
| `terraform`       | Infrastructure as Code tool                                  | cloud        | darwin, debian, redhat, ubuntu |
| `tldr`            | Simplified man pages                                         | power_user   | darwin, debian, redhat, ubuntu |
| `tree`            | Directory tree viewer                                        | system       | darwin, debian, redhat, ubuntu |
| `wget`            | Non-interactive network downloader                           | network      | darwin, debian, redhat, ubuntu |
| `wslu`            | WSL utilities for Windows integration                        | wsl          | debian, ubuntu, wsl            |
| `yamllint`        | YAML linting and validation                                  | development  | pip                            |
| `yq`              | YAML processor                                               | power_user   | darwin, debian, redhat, ubuntu |

---

## Installation

Tools are automatically installed based on your chosen operator:

```bash
# Install with base operator (minimal)
make install OPERATOR=base

# Install with matrix operator (includes base + matrix tools)
make install OPERATOR=matrix

# Install with jiveturkey operator (includes base + matrix + power-user tools)
make install OPERATOR=jiveturkey
```

## Adding Custom Tools

To request a new tool, open an issue with the `operator` label or submit a PR adding it to:

- `neosetup/roles/tools/vars/tool_registry.yml`

---

*Generated from `neosetup/roles/tools/vars/tool_registry.yml`*
