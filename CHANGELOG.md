# 🚀 Changelog

All notable changes to NeoSetup will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Container testing infrastructure with multi-OS Docker support
- Comprehensive documentation refactoring
- Missing documentation files (installation, configuration, troubleshooting guides)

## [2.0.0] - 2025-09-02

### New Features

- **Complete Ansible Implementation** - Full rewrite from shell scripts to Ansible
- **Advanced Operator System** - Inheritance-based configuration with validation
- **Production-Ready CI/CD** - 15+ parallel GitHub Actions jobs
- **Multi-OS Testing** - Docker containers for Ubuntu, Debian, CentOS, Fedora
- **Security Scanning** - CodeQL, Trivy, Gitleaks, and Bandit integration
- **Quality Assurance** - Custom ansible-lint rules and Matrix theme validation
- **Developer Experience** - Pre-commit hooks, local testing, one-click setup

### Enhanced

- **Shell Role** - Unified framework support (Oh-My-Zsh, Bash-it, Fish)
- **Tmux Role** - Theme-based configuration with matrix/base themes
- **Tools Role** - Registry system with 30+ modern CLI tools
- **Docker Role** - BuildKit, Compose v2, security hardening

### Operators

- **base** - Essential tools with enhanced configuration
- **matrix** - Matrix theme with custom shell functions
- **jiveturkey** - Power-user setup with security tools

### Infrastructure

- **Schema Validation** - YAML schema with detailed error reporting
- **Operator Generation** - Interactive and CLI-based creation tools
- **Comprehensive Testing** - 12-test validation suite
- **Documentation** - Complete guides and architecture documentation

### Performance

- **Installation Time** - <5 minute target with automated benchmarking
- **Code Quality** - 90%+ ansible-lint score across all components

## [1.0.0] - 2025-01-15

### Initial Release

- Initial shell script implementation
- Basic oh-my-zsh configuration
- Essential CLI tools installation
- Matrix-themed terminal setup
- Docker configuration
- Basic tmux setup

### Features

- Three configuration levels (minimal, standard, full)
- Matrix ASCII art and themes
- Security tool integration
- Cross-platform support (Linux, macOS)

## Development Phases Completed

### Phase 8: Container Testing Infrastructure (2025-09-02)

- Fixed workflow_run trigger issues with proper branch checking
- Resolved "ansible_distribution is not defined" errors
- Aligned test execution with Makefile installation patterns
- Optimized CI/CD pipeline removing redundant jobs

### Phase 7: Pre-commit/CI Perfect Alignment (2025-08-31)

- Added safety dependency security scanning
- Optimized markdownlint configuration  
- Made CodeQL scanning resilient to repository settings
- Created bulletproof development workflow

### Phase 6: Enhanced Developer Experience & CI/CD (2025-08-29)

- Separated development vs runtime dependencies
- Upgraded Docker testing to Rocky Linux 9
- Standardized 120 character line length
- Created one-click developer setup script

### Phase 5: Developer Experience & Local Testing (2025-08-29)

- Comprehensive requirements.txt with development dependencies
- Fixed ansible-lint "common role not found" error
- Enhanced multi-OS Docker testing reliability
- Established enterprise-grade development workflow

### Phase 4: Testing & Quality Assurance (2025-08-23)

- Comprehensive CI/CD pipeline with 15+ parallel jobs
- Multi-OS testing with Docker containers
- Security scanning integration
- Project management infrastructure

### Phase 3: Operator System Enhancement (2025-08-23)

- Built comprehensive operator validation infrastructure
- Created schema-based validation with error reporting
- Implemented operator generation tools
- Enhanced all existing operators

### Phase 2: Code Consolidation & DRY Improvements (2025-08-23)

- Refactored all roles to eliminate code duplication
- Created shared Jinja2 templates
- Unified shell framework installation
- Modularized tmux configuration

### Phase 1: Documentation Consolidation (2025-08-23)

- Consolidated duplicate documentation
- Created organized docs/ structure
- Archived historical migration documents

## Migration Notes

### From 1.x to 2.0

**Breaking Changes:**

- Complete architecture change from shell scripts to Ansible
- Configuration file format changes
- Installation command changes

**Migration Path:**

1. Backup existing configurations
2. Fresh installation recommended
3. Migrate custom settings to new operator format
4. Use new `./setup` command instead of old scripts

**Benefits:**

- More reliable and idempotent installations
- Better error handling and recovery
- Comprehensive testing and validation
- Easier customization through operators

## Security Updates

- **2025-09-02**: Updated all dependencies to latest secure versions
- **2025-08-31**: Added comprehensive security scanning pipeline
- **2025-08-29**: Fixed cryptography dependencies for Rocky Linux

## Performance Improvements

- **2025-09-02**: Container tests now complete in <3 minutes
- **2025-08-29**: Installation time reduced to <5 minutes target
- **2025-08-23**: Parallel job execution in CI/CD pipeline

## Known Issues

### Current

- CodeQL scanning requires repository admin to enable in settings
- Some security tools require sudo privileges
- macOS arm64 support in progress

### Resolved

- ✅ Container tests triggering on feature branches
- ✅ Ansible facts gathering in container environments
- ✅ Pre-commit hooks alignment with CI validation
- ✅ Rocky Linux cryptography dependency issues

## Acknowledgments

Special thanks to contributors who helped make NeoSetup awesome:

- All beta testers and early adopters
- The Ansible community for excellent tools
- Matrix film series for eternal inspiration

---

*"Change is never painful, only resistance to change is painful."* - The Matrix

For more details, see individual commit messages and GitHub releases.
