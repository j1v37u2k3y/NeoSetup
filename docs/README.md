
# NeoSetup Documentation

Welcome to the complete documentation for NeoSetup - a Matrix-themed development environment
automation system built with Ansible.

## Documentation Structure

### [Guides](./guides/) - User Documentation

- **[Installation Guide](./guides/installation.md)** - Complete setup instructions for all methods
- **[Configuration Guide](./guides/configuration.md)** - Operators, customization, and advanced config
- **[Troubleshooting](./guides/troubleshooting.md)** - Common issues and solutions
- **[Font Setup](./guides/font-setup.md)** - Terminal font configuration for Matrix theme

### [Development](./development/) - Developer Documentation

- **[Contributing](./development/contributing.md)** - Development standards and workflow
- **[Operator Creation Guide](./development/operator-creation-guide.md)** - How to create custom operators

### [Architecture](./architecture/) - System Design

- **[Operators System](./architecture/operators.md)** - Understanding the operator pattern
- **[Benefits of Operators](./architecture/benefits-of-operators.md)** - Why operators vs other approaches

## Quick Links

- **[Main README](../README.md)** - Project overview and quick start
- **[Installation](./guides/installation.md)** - Get started now
- **[CHANGELOG](../CHANGELOG.md)** - Version history and releases
- **[GitHub Issues](https://github.com/j1v37u2k3y/NeoSetup/issues)** - Bugs, features, and roadmap

## Getting Help

1. **Quick Start**: Follow the [Installation Guide](./guides/installation.md)
2. **Issues**: Check the [Troubleshooting Guide](./guides/troubleshooting.md)
3. **Customization**: Read the [Configuration Guide](./guides/configuration.md)
4. **Bugs**: Search [GitHub Issues](https://github.com/j1v37u2k3y/NeoSetup/issues)
5. **Support**: Create a new issue with the bug report template

## Documentation Quality

- **Complete**: All referenced files exist and are comprehensive
- **Tested**: Examples work as documented
- **Current**: Reflects Phase 9 implementation
- **Standards**: Markdown format, 120 char lines, syntax highlighting

## Development Workflow

```bash
# Run pre-commit checks (Docker-based)
./scripts/run-precommit.sh run --all-files

# Install git hooks
git config core.hooksPath .githooks

# Dev setup
cd neosetup && make dev-setup
```

---

*"Unfortunately, no one can be told what the Matrix is. You have to see it for yourself."*

**Ready to enter the Matrix?** Start with the [Installation Guide](./guides/installation.md)!
