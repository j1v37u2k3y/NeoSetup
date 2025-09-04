---
name: 🎯 New Operator Request
about: Request a new NeoSetup operator
title: '[OPERATOR] '
labels: [ 'enhancement', 'operator', 'triage' ]
assignees: [ 'jiveturkey' ]

---

# 🎯 New Operator Request

## 📋 Operator Overview

**Proposed Operator Name:**
**Target Use Case:**
**Extends:** [base/matrix/other]

## 🎯 Purpose & Goals

<!-- Describe what this operator should accomplish -->

## 🧰 Tools & Software

<!-- List the tools, software, and configurations this operator should include -->

### Essential Tools

- [ ]
- [ ]
- [ ]

### Development Tools

- [ ]
- [ ]
- [ ]

### Specialized Tools

- [ ]
- [ ]
- [ ]

## 🐚 Shell Configuration

<!-- Shell-specific requirements -->

### Aliases

```bash
# Proposed aliases
alias example="command"
```

### Functions

```bash
# Proposed shell functions
function example_func() {
    # function body
}
```

### Environment Variables

```bash
# Proposed environment variables
export EXAMPLE_VAR="value"
```

## 🖥️ Tmux Configuration

<!-- Tmux-specific requirements -->

- [ ] Custom key bindings
- [ ] Specific plugins
- [ ] Theme customizations
- [ ] Status bar modifications

## 🐳 Docker Integration

<!-- Docker-related requirements -->

- [ ] Docker containers to include
- [ ] Docker Compose setups
- [ ] Registry configurations
- [ ] Custom Docker functions

## 🎨 Theme & Aesthetics

<!-- Visual and theme requirements -->

- [ ] Should follow Matrix theme
- [ ] Custom color scheme (specify: ______)
- [ ] Custom ASCII art
- [ ] Themed prompts/messages

## 📱 Platform Requirements

<!-- Which platforms should this operator support? -->

- [ ] 🐧 Linux (Ubuntu/Debian)
- [ ] 🐧 Linux (RHEL/CentOS/Fedora)
- [ ] 🍎 macOS
- [ ] 🪟 Windows WSL2
- [ ] 🥧 Raspberry Pi/ARM

## 📋 Example Configuration

<!-- Provide a draft operator configuration -->

```yaml
---
operator_name: "example"
operator_version: "1.0.0"
operator_description: "Example operator description"
extends: "base"
operator_tags: [ "tag1", "tag2" ]

shell_config:
# Your shell configuration here

tmux_config:
# Your tmux configuration here

tools_config:
# Your tools configuration here
```

## 🧪 Validation Requirements

<!-- How should this operator be validated? -->

- [ ] Standard operator validation
- [ ] Custom validation rules
- [ ] Multi-platform testing
- [ ] Integration testing

## 👥 Target Audience

<!-- Who would use this operator? -->

- [ ] 🧑‍💻 General developers
- [ ] 🛡️ Security professionals
- [ ] ☁️ DevOps engineers
- [ ] 📊 Data scientists
- [ ] 🎮 Game developers
- [ ] 🌐 Web developers
- [ ] 📱 Mobile developers
- [ ] Other: _______

## 📊 Priority & Justification

<!-- Why is this operator needed? -->

### Business Case

<!-- Explain why this operator would be valuable -->

### User Impact

<!-- How many users would benefit from this operator? -->

### Complexity Assessment

<!-- Rate the implementation complexity -->

- [ ] 🟢 Simple - Basic tool installation and configuration
- [ ] 🟡 Medium - Some custom configuration and functions
- [ ] 🔴 Complex - Advanced integrations and custom tooling

## 🔗 References & Examples

<!-- Provide links to similar tools, documentation, or examples -->

-
-
-

## 🤝 Contribution Offer

<!-- Are you willing to help implement this operator? -->

- [ ] I can help design the operator
- [ ] I can help test the operator
- [ ] I can help document the operator
- [ ] I can provide feedback during development
- [ ] I'm willing to maintain this operator long-term

## 📚 Additional Context

<!-- Any other information about this operator request -->
