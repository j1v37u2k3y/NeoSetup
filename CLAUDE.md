# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NeoSetup is a Matrix-themed development environment automation system built entirely with Ansible. It uses an innovative
operator-based configuration system to provide different levels of customization from minimal to power-user setups.

**Current Status: Phase 9 Complete** - Production-ready system with Docker-based pre-commit, consolidated CI/CD (4 jobs),
and complete local/CI parity for all 20 validation hooks.

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
│   │   ├── shell/          # Unified shell framework (oh-my-zsh, bash-it, fish)
│   │   ├── tmux/           # Theme-based tmux config (matrix/base themes)
│   │   ├── tools/          # Tool registry system (30+ tools)
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

- **shell**: Unified framework support (Oh-My-Zsh, Bash-it, Fish) with shared Jinja2 templates
- **tmux**: Theme-based configuration system with matrix/base themes and shared components
- **tools**: Tool registry with 30+ tools and cross-platform package management
- **docker**: Modern Docker setup with BuildKit, Compose v2, and security hardening
- **common**: Shared tasks and utilities for all roles

### Advanced Operator System

- **base**: Essential tools with enhanced configuration and validation
- **matrix**: Matrix theme with custom shell functions (matrix_mode, wake_up, enter_matrix)
- **jiveturkey**: Power-user setup with security tools (wireshark, terraform, kubectl, ansible)
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
python3 tests/test_operator_validation.py           # Run validation test suite
make lint                                           # Run ansible-lint
make test                                           # Run all tests

# Container testing (matches CI/CD)
.github/scripts/test_container.py --os ubuntu --operator jiveturkey

# Operator creation
python3 scripts/create_operator.py --interactive    # Interactive operator creation
python3 scripts/create_operator.py --list-templates # List available templates

# Debugging & verbose output
make install OPERATOR=jiveturkey VERBOSE=true
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

# Use verbose mode for debugging
make install OPERATOR=base VERBOSE=true
```

## Completed Development Phases

### ✅ Phase 1: Documentation Consolidation (COMPLETE)

- Consolidated duplicate documentation across the project
- Created organized structure under `docs/` directory
- Archived historical migration documents

### ✅ Phase 2: Code Consolidation & DRY Improvements (COMPLETE)

- Refactored all roles to eliminate code duplication
- Created shared Jinja2 templates and reusable components
- Unified shell framework installation and configuration
- Enhanced Docker role with BuildKit and Compose v2
- Modularized tmux configuration with theme system

### ✅ Phase 3: Operator System Enhancement (COMPLETE)

- Built comprehensive operator validation infrastructure
- Created schema-based validation with detailed error reporting
- Implemented interactive and CLI-based operator generation tools
- Enhanced all existing operators with new features and tools
- Added 12-test validation suite with full coverage

### ✅ Phase 4: Testing & Quality Assurance (COMPLETE)

- Implemented comprehensive CI/CD pipeline with 15+ parallel jobs
- Added multi-OS testing with Docker containers (Ubuntu, Debian, CentOS, Fedora)
- Integrated security scanning (CodeQL, Trivy, Gitleaks, Bandit)
- Created custom ansible-lint rules and Matrix theme validation
- Added performance benchmarking with 5-minute installation target
- Built project management infrastructure (issue templates, PR templates)

### ✅ Phase 5: Developer Experience & Local Testing (COMPLETE)

- Comprehensive requirements.txt with all development dependencies
- Updated Makefile with dev-setup command for easy environment setup
- Pre-commit hooks for automated validation before commits
- Local-first testing methodology (test before CI/CD)
- Resolved ansible-lint "common role not found" error
- Enhanced multi-OS Docker testing reliability
- Enterprise-grade development workflow established

### ✅ Phase 6: Enhanced Developer Experience & CI/CD Improvements (COMPLETE)

- Separated development vs runtime dependencies (clean architecture)
- Upgraded from Rocky Linux 8 to Rocky Linux 9 for Docker testing
- Standardized 120 character line length across all linters
- Created `./develop` script for comprehensive environment setup
- Fixed Docker container Ansible PATH issues
- Comprehensive dependency management with pip and venv

### ✅ Phase 7: Pre-commit/CI Perfect Alignment (COMPLETE)

- Added safety dependency security scanning with perfect CI alignment
- Optimized markdownlint configuration for archived documentation
- Made CodeQL security scanning resilient to repository settings issues
- Created bulletproof development workflow with immediate feedback
- Pre-commit now catches ALL issues that would fail in CI

### ✅ Phase 8: Container Testing Infrastructure (COMPLETE)

- Fixed workflow_run trigger issues with proper branch checking
- Resolved "ansible_distribution is not defined" errors with explicit fact gathering
- Corrected inventory path references in container test scripts
- Aligned test execution with actual Makefile installation patterns
- Removed redundant test jobs from CI/CD pipeline for efficiency
- Changed container tests from dry-run to actual execution with safe tags
- Complete documentation refactoring with comprehensive guides

### ✅ Phase 9: Docker Pre-commit & CI Consolidation (COMPLETE)

- Docker-based pre-commit environment for local/CI parity
- Consolidated CI from 10+ jobs to 4 focused jobs
- All 20 pre-commit hooks run identically in Docker and CI
- Simplified git hooks using .githooks directory
- Roadmap items migrated to GitHub Issues

### 🚀 Next Phase: Advanced Features (Phase 10)

See [GitHub Issues](https://github.com/j1v37u2k3y/NeoSetup/issues) for roadmap including multi-platform support,
cloud integrations, and language-specific operators.

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
