# 🚀 NeoSetup Pull Request

## 📋 Description

<!-- Provide a clear description of what this PR accomplishes -->

## 🎯 Type of Change

<!-- Mark the appropriate option with an "x" -->

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] 🔧 Configuration change
- [ ] 🎨 Style/formatting change
- [ ] ♻️ Code refactor (no functional changes)
- [ ] ⚡ Performance improvement
- [ ] 🧪 Test addition or modification
- [ ] 🚀 CI/CD pipeline change

## 🎯 Operator/Component Affected

<!-- Mark all that apply -->

- [ ] 🎯 Base Operator
- [ ] 🟢 Matrix Operator
- [ ] 🦃 JiveTurkey Operator
- [ ] 🐚 Shell Role
- [ ] 🖥️ Tmux Role
- [ ] 🔧 Tools Role
- [ ] 🐳 Docker Role
- [ ] 📚 Documentation
- [ ] 🧪 Testing Infrastructure
- [ ] 🏗️ Build System

## ✅ Testing Checklist

<!-- Mark completed items with an "x" -->

- [ ] 🐳 Pre-commit passes (`./scripts/run-precommit.sh run --all-files`)
- [ ] 🧪 All existing tests pass
- [ ] ✅ Operator validation passes (`python3 scripts/validate_operator.py --all`)
- [ ] 🔄 Dry-run test completed (`make dry-run OPERATOR=<operator>`)
- [ ] 🐳 Multi-OS compatibility considered/tested
- [ ] 📚 Documentation updated

## 🟢 Matrix Theme Compliance

<!-- If this PR affects the Matrix theme, confirm compliance -->

- [ ] 🟢 Uses Matrix green color scheme (#00ff00)
- [ ] 🎭 Matrix ASCII art/effects work correctly
- [ ] 🎨 Terminal output maintains Matrix aesthetic
- [ ] 🔧 Matrix-specific functions/aliases included

## 🔗 Related Issues

<!-- Link to related issues using "Closes #123" or "Fixes #123" -->

- Closes #
- Related to #

## 🧪 How Has This Been Tested?

<!-- Describe the tests you ran and their results -->

**Test Configuration:**

- OS:
- Operator tested:
- Ansible version:

**Test commands run:**

```bash
# List the commands you used to test this change
```

## 📸 Screenshots/Logs

<!-- If applicable, add screenshots or log outputs -->

## 📚 Additional Notes

<!-- Add any additional context about the PR -->

## 🔍 Reviewer Checklist

<!-- For reviewers - do not modify -->

- [ ] Code follows the project's style guidelines
- [ ] Self-review completed
- [ ] Code is well-documented
- [ ] Changes generate no new warnings
- [ ] Tests are comprehensive and pass
- [ ] Matrix theme compliance verified
- [ ] Performance impact assessed
- [ ] Security implications considered

---

> This PR contributes to making NeoSetup the best Ansible automation system ever!
