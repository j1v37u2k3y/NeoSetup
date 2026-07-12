# ❓ Frequently Asked Questions

Quick answers to the questions that come up most. Can't find yours? Check the
[Troubleshooting Guide](./troubleshooting.md) or search
[GitHub Issues](https://github.com/j1v37u2k3y/NeoSetup/issues).

## 🟢 General

### What is NeoSetup?

NeoSetup is a Matrix-themed development environment automation system built entirely with **Ansible**. It
configures your shell, tmux, CLI tools, and Docker into a consistent, cyberpunk-flavored setup using an
**operator** system that lets you choose how much customization you want — from minimal to power-user.

### Do I need to know Ansible to use it?

No. Day to day you use `make` commands (`make install OPERATOR=matrix`) or the `./setup` script. Ansible runs
under the hood. You only need Ansible knowledge if you want to *contribute* new roles or tasks — see the
[Contributing Guide](../development/contributing.md).

### Is it safe to run? Will it overwrite my dotfiles?

NeoSetup writes shell and tmux configuration managed by its roles. **Before running it on a machine with
configs you care about, back up your dotfiles** (`~/.zshrc`, `~/.bashrc`, `~/.tmux.conf`). To see exactly
what *would* change without touching anything, run a dry run first:

```bash
cd neosetup
make dry-run OPERATOR=matrix
```

Ansible is idempotent — re-running an install converges to the same state rather than stacking changes.

### What's the difference between NeoSetup and just copying someone's dotfiles?

Operators, idempotency, and multi-OS support. You pick a level of customization, it inherits sane defaults,
it detects your platform, and re-running it is safe. Dotfile repos give you one person's exact setup;
NeoSetup gives you a composable system.

## 📦 Installation

### How do I install it?

```bash
cd neosetup

# Full installation with an operator
make install OPERATOR=jiveturkey

# Or install just one component
make shell        # Shell configuration only
make tmux         # Tmux configuration only
make tools        # CLI tools only
make docker       # Docker only
```

See the [Installation Guide](./installation.md) for full details and prerequisites.

### Which operating systems are supported?

Actively supported: **Ubuntu, Debian, Kali, macOS**, and **Windows via WSL2**. CentOS/Rocky and Fedora are
exercised in container testing. There are dedicated operators for macOS (`macos`) and WSL2 (`windows_wsl`).
FreeBSD and native Windows are **not** supported. Bare-metal ARM alternatives are partial — track progress in
[issue #18](https://github.com/j1v37u2k3y/NeoSetup/issues/18).

### Does it work on macOS?

Yes. Use the `macos` operator, which integrates Homebrew (Intel and Apple Silicon paths are detected
automatically):

```bash
make install OPERATOR=macos
```

### Does it work on Windows?

Through **WSL2**, yes — use the `windows_wsl` operator. Native Windows (PowerShell without WSL) is not a
target.

### Do I need sudo / root?

Some tasks (installing system packages, Docker) need elevated privileges. Pass `--ask-become-pass` so Ansible
prompts for your sudo password when required:

```bash
make install OPERATOR=jiveturkey ANSIBLE_FLAGS="--ask-become-pass"
```

Shell and tmux configuration alone generally do **not** need sudo.

### How long does installation take?

The target is **under 5 minutes** for a typical install; time varies with how many tools your operator
installs and your network speed. Tool downloads dominate — a shell-only run (`make shell`) is nearly instant.

## 🎭 Operators

### What's an operator?

An operator is a named configuration bundle that decides which tools, aliases, functions, and theme you get.
Operators **inherit** from each other, so you compose rather than copy. See
[Operators System](../architecture/operators.md).

### Which operator should I pick?

| Operator | Best for |
|----------|----------|
| `base` | Minimal, essential tools and a clean config |
| `matrix` | The full Matrix theme + cyberpunk shell functions (`matrix_mode`, `wake_up`, `enter_matrix`) |
| `jiveturkey` | Power users — security tooling on top of matrix |
| `python_dev` / `nodejs_dev` / `go_dev` | Language-focused developer environments |
| `macos` / `windows_wsl` | Platform-specific integration |

Start with `matrix` if you want the full experience, `base` if you want it lean.

### Can I create my own operator?

Yes — that's the whole point. Use the generator or copy an existing operator:

```bash
cd neosetup
python3 scripts/create_operator.py --interactive
```

See the [Operator Creation Guide](../development/operator-creation-guide.md).

### How does operator inheritance work?

An operator declares `extends: <parent>` in its `vars.yml`. Variables are inherited from the parent and can
be overridden. For example, `jiveturkey` extends `matrix`, which extends `base` — so `jiveturkey` gets
everything from both, plus its own additions.

## 🔧 Customization

### How do I add a tool?

Tools only install if they're registered in `neosetup/roles/tools/vars/tool_registry.yml`. Add an entry
there (with the package name per platform), then reference the tool from your operator's tool set. Listing a
tool in an operator's `additional_tools` without a registry entry does nothing — it's silently skipped.

### How do I change the theme or shell?

Set the relevant role variable in your operator's `vars.yml` — e.g. `shell_framework` (oh-my-zsh, bash-it,
fish) or `tmux_theme` (matrix, base). See the [Configuration Guide](./configuration.md) and the
[Variable Naming Convention](../development/contributing.md#variable-naming-convention) for how variables are
scoped.

### Is there a minimal / no-frills installation mode?

Not yet as a single flag — it's on the roadmap
([issue #47](https://github.com/j1v37u2k3y/NeoSetup/issues/47)). Today, the closest thing is the `base`
operator plus installing only the components you want (`make shell`, `make tmux`).

## 🐛 Common Issues

### My shell didn't change after install

Reload your shell config or open a new terminal:

```bash
source ~/.zshrc   # or ~/.bashrc
```

If you changed your default shell, log out and back in for it to take effect.

### `ls` / `ll` renders a grid or throws `eza: Unknown argument`

Fixed in current `main`. The `ls` family (`ls`, `ll`, `la`, `l`, `lt`, `l.`) is now defined as shell
*functions* that forward arguments correctly. Re-run `make shell` and open a new terminal. If an old alias
lingers from a previous install, clear it with `unalias ls ll la l lt` and reload.

### "Tool not found" after install

Package names differ across distributions. Check whether the tool is registered for your platform in
`tool_registry.yml`. If it's missing an entry for your OS, that's a registry gap — open an issue or add the
mapping.

### Permission errors during install

Re-run with sudo prompting enabled:

```bash
make install OPERATOR=base ANSIBLE_FLAGS="--ask-become-pass"
```

More fixes in the [Troubleshooting Guide](./troubleshooting.md).

## 🚀 Updating & Versioning

### How do I update NeoSetup?

Pull the latest and re-run your install — it's idempotent, so it only applies what changed:

```bash
git pull
cd neosetup
make install OPERATOR=<your-operator>
```

### How is NeoSetup versioned?

NeoSetup follows [Semantic Versioning](https://semver.org/) via
[Commitizen](https://commitizen-tools.github.io/commitizen/), driven by
[Conventional Commits](https://www.conventionalcommits.org/). Versions live in `VERSION` and the
[CHANGELOG](../../CHANGELOG.md) is generated on release (`make bump`).

---

*"I can only show you the door. You're the one that has to walk through it."*

Still stuck? Open an [issue](https://github.com/j1v37u2k3y/NeoSetup/issues) — bug reports and questions both
welcome.
