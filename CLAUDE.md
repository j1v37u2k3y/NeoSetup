# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NeoSetup is a Matrix-themed development environment automation system built entirely with Ansible. It uses an innovative
operator-based configuration system to provide different levels of customization from minimal to power-user setups.

**Current Version: 2.1.0** - Production-ready system with Docker-based pre-commit, consolidated CI/CD (4 jobs),
and complete local/CI parity for all 20 validation hooks. Releases follow [Semantic Versioning](https://semver.org/)
driven by [Conventional Commits](https://www.conventionalcommits.org/) via
[Commitizen](https://commitizen-tools.github.io/commitizen/); the version lives in `VERSION` and history is in
[CHANGELOG.md](CHANGELOG.md).

## Current Architecture

### Directory Structure

```text
NeoSetup/
├── .github/                  # GitHub workflows & templates
│   ├── workflows/            # CI/CD pipelines (4 focused jobs)
│   ├── ISSUE_TEMPLATE/       # Bug reports, feature requests
│   ├── scripts/              # CI helper scripts
│   ├── ansible-rules/        # Custom linting rules
│   └── pull_request_template.md
├── .githooks/                # Git hooks (Docker-based pre-commit)
│   └── pre-commit            # Delegates to scripts/run-precommit.sh
├── .editorconfig            # Code formatting standards (NEW!)
├── .gitignore               # Git ignore patterns
├── neosetup/                # Ansible implementation
│   ├── Makefile             # Convenient commands
│   ├── ansible.cfg          # Ansible configuration
│   ├── playbooks/           # Main playbooks
│   │   ├── site.yml        # Master playbook
│   │   └── shell.yml       # Shell-specific playbook
│   ├── roles/              # Modular Ansible roles (REFACTORED)
│   │   ├── shell/          # Unified shell framework (zsh/oh-my-zsh, bash/bash-it)
│   │   ├── tmux/           # Theme-based tmux config (matrix/base themes)
│   │   ├── tools/          # Tool registry system (60+ tools)
│   │   ├── docker/         # Modern Docker (BuildKit, Compose v2)
│   │   └── common/         # Shared tasks and utilities
│   ├── operators/          # Validated operator configurations
│   │   ├── base/           # Essential tools + minimal config
│   │   ├── matrix/         # Matrix theme + cyberpunk functions  
│   │   └── jiveturkey/     # Power-user + security tools
│   ├── schema/             # Validation schemas (NEW!)
│   │   └── operator_schema.yml
│   ├── scripts/            # Operator tools & validation (NEW!)
│   │   ├── validate_operator.py  # Schema-based validation
│   │   └── create_operator.py    # Interactive operator generator
│   ├── tests/              # Comprehensive test suite (NEW!)
│   │   └── test_operator_validation.py
│   ├── inventories/        # Ansible inventory configurations
│   ├── group_vars/         # Operator inheritance definitions
│   ├── callback_plugins/   # Matrix-themed output
│   └── requirements.yml    # Ansible dependencies
├── docs/                    # Complete documentation
│   ├── development/         # Operator creation guide & dev docs
│   ├── guides/             # User installation & config guides
│   ├── architecture/       # System design documentation
│   └── archive/           # Historical migration documents
├── scripts/                 # Project-level scripts
│   └── run-precommit.sh    # Docker-based pre-commit runner
├── Dockerfile.precommit    # Pre-commit Docker image
├── requirements.txt        # Python dependencies
├── setup                   # Setup script
├── README.md               # Main project documentation
└── CLAUDE.md               # This file

```

## Key Components

### Ansible Roles (Refactored & Enhanced)

- **shell**: Unified framework support for zsh (Oh-My-Zsh) and bash (Bash-it) with shared Jinja2 templates
- **tmux**: Theme-based configuration system with matrix/base themes and shared components
- **tools**: Tool registry with 60+ tools and cross-platform package management
- **docker**: Modern Docker setup with BuildKit, Compose v2, and security hardening
- **common**: Shared tasks and utilities for all roles

### Advanced Operator System

Eight operators ship and are all registered in `group_vars/all/operators.yml`. Inheritance spine:
`jiveturkey → matrix → base`; every other operator extends `base` directly.

- **base**: Essential tools with enhanced configuration and validation
- **matrix**: Matrix theme with custom shell functions (matrix_mode, wake_up, enter_matrix); extends base
- **jiveturkey**: Power-user setup with productivity + networking tools (nmap, netcat) and Docker-based
  security functions; extends matrix. Note: the heavier security/DevOps arsenal (wireshark, sqlmap, gobuster,
  ffuf, john, hashcat, kubectl, helm, awscli, terraform, ansible) is **planned/deferred**, not yet installed
  (needs per-platform packaging + installers).
- **macos**: macOS integration (Homebrew, productivity apps, window management); extends base
- **windows_wsl**: Windows WSL2 integration and interoperability; extends base
- **python_dev**: Python toolchain (pyenv, poetry, pipx, linters, jupyter); extends base
- **nodejs_dev**: Node.js environment (nvm); extends base
- **go_dev**: Go toolchain; extends base
- **Validation**: Schema-based validation with detailed error reporting and suggestions
- **Generation**: Interactive and CLI-based operator creation tools

### Production-Ready Features

- **CI/CD Pipeline**: 4 focused GitHub Actions jobs (pre-commit, security-scan, ansible-syntax, docs-validation)
- **Docker Pre-commit**: All 20 linting hooks run in Docker for local/CI parity
- **Security Scanning**: CodeQL, Trivy, Bandit, Safety, and detect-secrets integration
- **Quality Assurance**: Custom ansible-lint rules and Matrix theme validation
- **Multi-Platform Testing**: Docker containers for Ubuntu, Debian, CentOS, Fedora
- **Performance Benchmarking**: <5 minute installation target with automated testing

## Common Commands

### Installation Commands

```bash
cd neosetup

# Full installation with jiveturkey operator
make install OPERATOR=jiveturkey

# Install specific components
make shell        # Shell configuration only
make tmux         # Tmux configuration only
make tools        # CLI tools only
make docker       # Docker only

# Dry run to preview changes
make dry-run OPERATOR=matrix

# Clean Ansible cache
make clean
```

### Testing & Validation Commands

```bash
# Pre-commit (Docker-based - recommended)
./scripts/run-precommit.sh run --all-files          # Run all 20 hooks in Docker
git config core.hooksPath .githooks                 # Install git hook (uses Docker)

# Operator validation
cd neosetup
python3 scripts/validate_operator.py --all          # Validate all operators
python3 scripts/validate_operator.py base           # Validate specific operator

# Comprehensive testing
python3 tests/test_operator_validation.py           # Run the validation test suite (the working test entry point)
make lint                                           # Run ansible-lint
# Note: `make test` invokes molecule, but no molecule scenarios exist yet — use the command above instead.

# Container testing (matches CI/CD)
.github/scripts/test_container.py --os ubuntu --operator jiveturkey

# Operator creation
python3 scripts/create_operator.py --interactive    # Interactive operator creation
python3 scripts/create_operator.py --list-templates # List available templates

# Debugging & verbose output (VERBOSE=true is not wired; pass verbosity through ANSIBLE_FLAGS)
make install OPERATOR=jiveturkey ANSIBLE_FLAGS="-vvv"
```

## Development Guidelines

### Working with Operators

- Operators are defined in `neosetup/operators/*/vars.yml`
- Each operator can extend another using `extends: parent_operator`
- Variables are inherited and can be overridden

### Adding New Features

1. Create a new role in `neosetup/roles/`
2. Add tasks, templates, and handlers as needed
3. Include the role in `playbooks/site.yml`
4. Test with `make dry-run`

### Testing Changes

```bash
# Always test with dry-run first
make dry-run OPERATOR=jiveturkey

# Test individual roles
ansible-playbook playbooks/site.yml --tags "shell" --check

# Use verbose mode for debugging (verbosity is passed via ANSIBLE_FLAGS; VERBOSE=true is not wired)
make install OPERATOR=base ANSIBLE_FLAGS="-vvv"
```

## Project Status & History

NeoSetup is versioned with [Semantic Versioning](https://semver.org/) driven by
[Conventional Commits](https://www.conventionalcommits.org/) via
[Commitizen](https://commitizen-tools.github.io/commitizen/). The canonical version lives in `VERSION`
(currently **2.1.0**) and the full, per-release history — what shipped and when — is maintained in
[CHANGELOG.md](CHANGELOG.md), regenerated on each `make bump`.

- **Roadmap & planned work**: tracked in [GitHub Issues](https://github.com/j1v37u2k3y/NeoSetup/issues)
  (multi-platform support, cloud integrations, language-specific operators, and the deferred jiveturkey
  security/DevOps arsenal).
- **Release history**: see [CHANGELOG.md](CHANGELOG.md) rather than the older "phase" narrative.

## Important Notes

### File Locations

- **Documentation**: Complete documentation suite with installation, configuration, troubleshooting guides
- **Contributing**: Full contributing guide with development standards and workflows
- **Legal**: MIT License and comprehensive changelog
- **Operators**: Configuration in `neosetup/operators/` with full validation
- **Roles**: Ansible roles in `neosetup/roles/` with shared templates

### Best Practices

- Always use `make` commands for consistency
- Test changes with `--check` or `make dry-run`
- Follow Ansible best practices for roles and playbooks
- Maintain the Matrix theme in all output

### Common Issues and Solutions

- **Permission errors**: Some tasks need sudo, use `--ask-become-pass`
- **Shell not changing**: Source the config or restart terminal
- **Tools not found**: Check if package names differ on your OS

## Development Tracking

- GitHub Issues for tracking features, bugs, and roadmap
- Commit messages should be descriptive and follow conventional commits
- Document significant changes in git commit messages
- remember I only push code.
