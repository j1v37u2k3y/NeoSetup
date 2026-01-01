---
name: 🐛 Bug Report
about: Report a bug to help us improve NeoSetup
title: '[BUG] '
labels: [ 'bug', 'triage' ]
assignees: [ 'jiveturkey' ]

---

# 🐛 Bug Report

## 📋 Description

<!-- A clear and concise description of what the bug is -->

## 🔄 Steps to Reproduce

1.
2.
3.
4.

## ✅ Expected Behavior

<!-- A clear description of what you expected to happen -->

## ❌ Actual Behavior

<!-- A clear description of what actually happened -->

## 🖥️ Environment

<!-- Please complete the following information -->

**System Information:**

- OS: [e.g., Ubuntu 22.04, macOS 13.0, CentOS 8]
- Shell: [e.g., zsh, bash]
- Ansible Version: [e.g., 6.5.0]
- Python Version: [e.g., 3.10.6]

**NeoSetup Configuration:**

- Operator used: [e.g., base, matrix, jiveturkey]
- Installation method: [e.g., make install, ansible-playbook]
- Branch/Version: [e.g., main, v1.2.3]

## 📋 Logs/Output

<!-- Please paste relevant log output or error messages -->

<details>
<summary>Click to expand logs</summary>

```text
# Paste your logs here
```

</details>

## 🎯 Operator Validation

<!-- Run operator validation and paste results -->

```bash
cd neosetup
python3 scripts/validate_operator.py --all
```

<details>
<summary>Validation Results</summary>

```text
# Paste validation results here
```

</details>

## 🧪 Additional Testing

<!-- Have you tried any workarounds or additional testing? -->

- [ ] Tried with different operator
- [ ] Ran in dry-run mode (`make dry-run`)
- [ ] Checked file permissions
- [ ] Verified Ansible inventory
- [ ] Tested on clean system

## 🟢 Matrix Theme Related

<!-- If this is Matrix theme related, check all that apply -->

- [ ] Matrix colors not displaying correctly
- [ ] ASCII art not rendering
- [ ] Matrix functions not working
- [ ] Terminal effects broken

## 📸 Screenshots

<!-- If applicable, add screenshots to help explain the problem -->

## 🔗 Additional Context

<!-- Add any other context about the problem here -->
