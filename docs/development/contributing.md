# 🤝 Contributing to NeoSetup

Welcome to the Matrix! We're excited to have you contribute to the most awesome Ansible-powered development environment automation.

## 🎯 Quick Start for Contributors

### Prerequisites

- Git and GitHub account
- Python 3.8+
- Basic understanding of Ansible
- Love for the Matrix theme 🔋

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/NeoSetup.git
cd NeoSetup

# Install development dependencies
pip install -r requirements.txt

# Setup development environment
cd neosetup
make dev-setup

# Install pre-commit hooks
pre-commit install

# Run tests to ensure everything works
make test
make lint
```

## 🎭 Code of Conduct

**Be excellent to each other.** We follow the [Contributor Covenant](https://www.contributor-covenant.org/):

- Use welcoming and inclusive language
- Respect differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

## 🚀 Contributing Guidelines

### What We're Looking For

- 🐛 **Bug fixes** - Help us squash those pesky bugs
- ✨ **New features** - Add awesome functionality
- 📚 **Documentation** - Improve guides and code comments
- 🎨 **Matrix theme enhancements** - Make it even more cyberpunk
- 🔧 **New operators** - Create specialized configurations
- 🧪 **Tests** - Improve coverage and reliability
- 🔒 **Security improvements** - Help keep everyone safe

### What We're NOT Looking For

- Breaking changes without discussion
- Code that doesn't follow our style guide
- Features that break the Matrix theme
- Untested changes
- Malicious or harmful code

## 📋 Development Process

### 1. Before You Start

- Check [existing issues](https://github.com/j1v37u2k3y/NeoSetup/issues) to avoid duplicates
- Open an issue to discuss major changes
- Look at the [roadmap](../TODO.md) for planned features

### 2. Development Workflow

```bash
# Create a feature branch
git checkout -b feature/awesome-enhancement

# Make your changes
# ... coding magic happens ...

# Test your changes
make dry-run OPERATOR=jiveturkey
make test
make lint

# Run operator validation
python3 scripts/validate_operator.py --all

# Commit with conventional commit format
git add .
git commit -m "feat: add awesome new feature"

# Push and create pull request
git push origin feature/awesome-enhancement
```

### 3. Pull Request Process

1. **Update documentation** - README, guides, code comments
2. **Add/update tests** - Ensure your code is tested
3. **Follow commit conventions** - Use conventional commit messages
4. **Keep it focused** - One feature/fix per PR
5. **Pass all checks** - CI/CD pipeline must be green

## 📝 Coding Standards

### Ansible Best Practices

```yaml
# ✅ Good - Use descriptive task names with emojis
- name: "🔧 Install essential development tools"
  package:
    name: "{{ item }}"
    state: present
  loop: "{{ dev_tools }}"
  tags: [tools]

# ❌ Bad - Vague task name, no tags
- name: "Install stuff"
  package:
    name: "{{ tools }}"
```

### Python Code Style

```python
# ✅ Good - Clear docstrings, type hints
def validate_operator(operator_name: str) -> bool:
    """Validate operator configuration against schema.

    Args:
        operator_name: Name of the operator to validate

    Returns:
        True if validation passes, False otherwise
    """
    # Implementation here

# ❌ Bad - No docstring, no types  
def validate(name):
    # Does something
```

### Shell Scripts

```bash
# ✅ Good - Error handling, documentation
#!/usr/bin/env bash
set -euo pipefail

# Install Matrix-themed tools
install_matrix_tools() {
    local tools=("$@")
    for tool in "${tools[@]}"; do
        echo "🔧 Installing ${tool}..."
        if ! command -v "${tool}" >/dev/null 2>&1; then
            install_tool "${tool}"
        fi
    done
}

# ❌ Bad - No error handling, unclear
#!/bin/bash
for i in $*; do
    install $i
done
```

### Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/):

```text
type(scope): short description

Longer description if needed

- List of changes
- Another change

Fixes #123
```

**Types**:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples**:

```text
feat(shell): add fish shell support
fix(tmux): resolve color display issues in terminal
docs(guides): update installation instructions for macOS
refactor(tools): consolidate package installation logic
test(operators): add validation tests for custom operators
```

## 🎯 Contributing Areas

### 🐛 Bug Fixes

1. **Reproduce the bug** - Create minimal reproduction steps
2. **Write a test** - Add test case that fails before your fix
3. **Fix the issue** - Implement the solution
4. **Verify the fix** - Ensure test passes and no regressions
5. **Document** - Update docs if needed

### ✨ New Features

1. **Discuss first** - Open an issue to discuss the feature
2. **Design** - Plan the implementation approach
3. **Implement** - Write the code with tests
4. **Document** - Add documentation and examples
5. **Test thoroughly** - Multiple OS, operators, edge cases

### 🎨 Matrix Theme Enhancements

Keep the cyberpunk aesthetic:

```bash
# ✅ Good Matrix theming
echo "🟢 Welcome to the Matrix, Neo..."
echo "🔴 Taking the red pill..."
echo "⚡ Entering the Matrix..."

# Colors: Use Matrix green (#00ff00), black backgrounds
# Symbols: Binary, matrix rain, cyberpunk elements
# Quotes: Reference Matrix movies appropriately
```

### 🔧 Creating New Operators

```bash
# Use the operator creation tool
cd neosetup
python3 scripts/create_operator.py --interactive

# Follow these guidelines:
# - Clear description and use case
# - Proper inheritance (extend existing operators)
# - Comprehensive tool selection
# - Custom functions when appropriate
# - Thorough testing
```

Example operator structure:

```yaml
# operators/myoperator/vars.yml
extends: matrix  # Inherit from matrix operator

description: "Specialized environment for data science"
author: "Your Name <email@example.com>"
version: "1.0.0"
tags: ["data-science", "python", "jupyter"]

# Additional packages
additional_packages:
  - name: "jupyter"
    description: "Interactive Python notebooks"
  - name: "pandas"
    description: "Data manipulation library"

# Custom aliases
shell_aliases:
  - { alias: "jlab", command: "jupyter lab" }
  - { alias: "jnb", command: "jupyter notebook" }

# Custom functions
shell_functions:
  - name: "data_env"
    description: "Activate data science environment"
    definition: |
      echo "🔬 Activating data science environment..."
      conda activate datascience
```

## 🧪 Testing

### Test Types

1. **Unit Tests** - Individual component testing
2. **Integration Tests** - End-to-end workflow testing  
3. **Operator Validation** - Schema and configuration testing
4. **Multi-OS Testing** - Docker container testing
5. **Security Testing** - Vulnerability scanning

### Running Tests

```bash
# Full test suite
make test

# Specific test types
make lint                                    # Code quality
ansible-lint .                               # Ansible linting
python3 tests/test_operator_validation.py    # Operator tests
python3 scripts/validate_operator.py --all  # Schema validation

# Docker container tests (like CI)
docker run --rm -v $(pwd):/neosetup ubuntu:20.04 bash -c "
  cd /neosetup &&
  apt update &&
  apt install -y python3 python3-pip &&
  ./setup install base
"
```

### Writing Tests

```python
# tests/test_new_feature.py
import unittest
from neosetup.scripts.validate_operator import validate_operator

class TestNewFeature(unittest.TestCase):
    """Test new feature functionality."""

    def test_feature_works(self):
        """Test that new feature works as expected."""
        result = validate_operator("test_operator")
        self.assertTrue(result)

    def test_feature_handles_errors(self):
        """Test error handling in new feature."""
        with self.assertRaises(ValueError):
            validate_operator("invalid_operator")

if __name__ == '__main__':
    unittest.main()
```

## 📚 Documentation

### Documentation Types

- **README.md** - Quick start and overview
- **Installation Guide** - Detailed setup instructions
- **Configuration Guide** - Customization options
- **API Documentation** - Code documentation
- **Troubleshooting** - Common issues and solutions

### Documentation Standards

```markdown
# Use clear headings with emojis
## 🔧 Configuration

# Provide working code examples
\`\`\`bash
# This is how you do it
./setup install matrix
\`\`\`

# Include expected output when helpful
Output:
\`\`\`
🟢 Welcome to the Matrix...
✅ Installation complete!
\`\`\`

# Link between related sections
See [Troubleshooting Guide](./troubleshooting.md) for common issues.
```

## 🎯 Issue and PR Templates

### Bug Reports

Use the bug report template with:

- Clear description
- Steps to reproduce
- Expected vs actual behavior  
- System information
- Logs and error messages

### Feature Requests

Use the feature request template with:

- Problem description
- Proposed solution
- Alternative solutions
- Additional context

### Pull Requests

Use the PR template with:

- Description of changes
- Related issues
- Testing checklist
- Screenshots/demos
- Breaking changes notes

## 🔒 Security

### Security Guidelines

- **No secrets in code** - Use environment variables
- **Validate inputs** - Sanitize user data
- **Follow least privilege** - Don't request unnecessary permissions
- **Security scanning** - All code goes through automated security scans
- **Responsible disclosure** - Report security issues privately

### Reporting Security Issues

**Do NOT open public issues for security vulnerabilities.**

Create private security advisory

Include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## 🎉 Recognition

### Contributors

All contributors are recognized in:

- GitHub contributors list
- Release notes  
- Special recognition for major contributions

### Maintainers

Active contributors may be invited to become maintainers with:

- Commit access
- Review responsibilities
- Release management

## 📞 Getting Help

### Development Questions

- **GitHub Discussions** - General questions
- **Matrix Chat** - Real-time development discussion (coming soon)
- **Issues** - Specific bugs or feature requests

### Resources

- [Ansible Documentation](https://docs.ansible.com/)
- [Matrix Trilogy](https://en.wikipedia.org/wiki/The_Matrix) - For theme inspiration
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Pre-commit Hooks](https://pre-commit.com/)

---

**Remember**: *"There is no spoon"* - The only limit is your imagination when contributing to NeoSetup!

Welcome to the resistance, and thank you for helping make NeoSetup even more awesome! 🤘

*This is your last chance. After this, there is no turning back. You contribute to the Matrix - you help us show the world how deep the rabbit hole goes.*

**🔴 Take the red pill**: Start contributing today!  
**🔵 Take the blue pill**: Stay a user forever  

The choice is yours, Neo.
