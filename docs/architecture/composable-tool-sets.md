# Composable Tool Sets — Design Spec

> Status: **Proposed** (2026-09-23) · Owner: j1v37u2k3y · Depends on: the fail-loud install gate and
> enforcing operator validator now on `main`.

## 1. Why this exists (the mission)

NeoSetup's whole reason to exist is: **one command stands up *your* dev environment, at *your*
customization level.** The operator model is the load-bearing idea — profiles that compose so shared
framing lives in one place and specializations layer on top.

But today the tool layer only expresses **one axis of composition**: inheritance along a single spine
(`jiveturkey → matrix → base`). Tool sets are keyed by *operator name*, so the only way to get a
different mix of tools is to author a whole new operator. That does **not** express the real need:

> "I want *my* tools. Other people want *other* tools, or the same, or a combo of all."

A security engineer wants the offensive arsenal. An SRE wants cloud + devops. A Python dev wants the
Python stack. Many want a **combo** — pentester-who-writes-Python = security + python + core. The
current model can't say that without a bespoke operator per person.

This spec adds the missing axis: **category tool sets that any operator can opt into and combine**,
and uses it to finally deliver `jiveturkey`'s advertised security/devops arsenal (currently declared
but not installed).

## 2. What's already in place (the foundation this builds on)

Three things landed on `main` this cycle that make an honest tool buildout **safe**:

- **Inheritance composition** — the installer unions `operator_tool_sets` across the full spine
  (`(operator_inheritance[op] + [op])`), not just the leaf operator.
- **Fail-loud gate** — `install_tools_unified.yml` asserts every declared tool is a `tool_registry`
  key. A typo'd or unregistered tool now **stops the run loudly** instead of silently installing
  nothing (the old silent-gate bug).
- **Enforcing validator** — `validate_operator.py` now checks types, patterns, and
  registry-membership, so bad tool references are caught at validation time.

Net: we can add tools and *trust they land*, or find out immediately if they don't.

## 3. Design

### 3.1 Category tool sets (new)

Introduce **category** tool sets in `roles/tools/vars/tool_registry.yml`, orthogonal to operators:

```yaml
tool_sets:
  core:        [htop, tree, jq, curl, wget, yamllint, act, pre-commit]
  modern_cli:  [eza, bat, ripgrep, fd, fzf, delta, btop]
  matrix_fun:  [cmatrix, neofetch, lolcat, figlet, cowsay, fortune]
  security:    [nmap, netcat, sqlmap, gobuster, ffuf, john, hashcat, wireshark, nuclei]
  cloud:       [kubectl, helm, awscli, azure-cli, terraform]
  devops:      [ansible, gh, lazygit]
  python:      [pyenv, poetry, pipx, black, flake8, mypy, isort, pytest, pylint, bandit, tox, ...]
  node:        [nvm]
  go:          [go]
  macos:       [duti, mas, mackup, stats, rectangle]
```

These are **named, reusable bundles** — the unit of "a combo."

### 3.2 Operators opt in

An operator declares which category sets it wants, in addition to what it inherits:

```yaml
# operators/jiveturkey/vars.yml
tool_categories: [security, cloud, devops]     # jiveturkey's combo
```

```yaml
# a hypothetical shared/community operator — someone else's combo
tool_categories: [security, python]            # pentester who scripts in Python
```

### 3.3 Composition algorithm (extends the current one)

```
tools_to_install =
    tool_sets.core
  + tool_sets.modern_cli
  + UNION( operator_tool_sets[o]  for o in (operator_inheritance[op] + [op]) )   # existing spine
  + UNION( tool_sets[c]           for c in (op.tool_categories | default([])) )  # NEW: opted-in categories
  + tools_config.additional_tools
```

Backward compatible: the existing operator-keyed `operator_tool_sets` and the inheritance spine stay
exactly as they are. Category sets are **additive**. `unique` de-dupes overlaps (someone opting into
`core` + `python` where both list a shared tool just gets it once).

> Migration note: over time, `base`'s and `matrix`'s operator-keyed sets can be re-expressed as the
> `core` / `matrix_fun` categories, collapsing the two mechanisms into one. Not required for v1.

## 4. Tool taxonomy & packaging (honest coverage)

Governing rule (unchanged, [`docs`](../../CLAUDE.md) Key Decision): **only register a tool on a
platform where it genuinely ships.** Never a fake package name that no-ops. The fail-loud gate makes a
mis-registration loud, but honest coverage keeps it from ever being declared.

Legend: ✅ ships in default repos · 🧩 needs a custom installer · ⚠️ distro-limited (verify) ·
`?` verify exact package/formula name during implementation.

| Tool | apt (ubuntu/debian) | brew (darwin) | redhat | Method | Notes |
|------|--------------------|---------------|--------|--------|-------|
| nmap | ✅ nmap | ✅ nmap | ✅ nmap | package | already registered |
| netcat | ✅ netcat-openbsd | ✅ netcat | ✅ nmap-ncat? | package | verify redhat pkg |
| sqlmap | ✅ sqlmap | ✅ sqlmap | ⚠️? | package | |
| john | ✅ john | ✅ john-jumbo? | ⚠️? | package | verify brew formula |
| hashcat | ✅ hashcat | ✅ hashcat | ⚠️? | package | |
| wireshark | ✅ wireshark/tshark | 🧩 cask wireshark | ⚠️? | package/cask | GUI; tshark for headless |
| gobuster | ⚠️ kali/parrot only | ✅ gobuster | ❌ | package | 🧩 installer for ubuntu/debian, or defer |
| ffuf | ⚠️ kali/parrot only | ✅ ffuf | ❌ | package | same as gobuster |
| nuclei | ❌ | ✅ nuclei | ❌ | 🧩 go install / release binary | mirror go pattern |
| kubectl | 🧩 apt repo | ✅ kubernetes-cli | 🧩 yum repo | 🧩 `kubectl_installer` | **installer to write** |
| helm | 🧩 script/apt repo | ✅ helm | 🧩 | 🧩 `helm_installer` | **installer to write** |
| awscli | 🧩 bundled installer | ✅ awscli | 🧩 | 🧩 `awscli_installer` | **installer to write** |
| azure-cli | 🧩 apt repo | ✅ azure-cli | 🧩 | 🧩 `azure_cli_installer` | **installer to write** |
| terraform | 🧩 hashicorp apt repo | ✅ terraform | 🧩 | 🧩 or package | brew clean; Linux repo |
| ansible | ✅ pip ansible | ✅ ansible | ✅ | pip | |
| gh | ✅ (existing installer) | ✅ gh | ✅ | 🧩 `github_cli` | already exists — the model |

Every `?` / ⚠️ is a **verify-before-register** item: confirm the package exists on that platform (the
container CI matrix — ubuntu/debian/kali/parrot/rocky/fedora — is the proving ground) or mark it
platform-limited. The dangling `kubectl_installer` / `helm_installer` / `azure_cli_installer`
references already in `tool_registry.yml` are exactly the installers below — write them, don't fake
them.

## 5. Installers to write

Mirror the existing `github_cli` / `nvm` / `go` / `pyenv` / `poetry` installer pattern in
`roles/tools/tasks/custom_installs/`. **Every one verifies before executing** — GPG-signed apt repo,
or download + `checksum:` before `unarchive`. No blind `curl | bash` (also cleans up the M1
remote-exec debt for these tools).

- `kubectl_installer.yml` — Linux: pinned release binary + sha256, or the official apt/yum repo w/
  signing key. macOS: `kubernetes-cli` via brew.
- `helm_installer.yml` — Linux: the get-helm-3 script pinned to a version + checksum, or apt repo.
- `awscli_installer.yml` — Linux: AWS CLI v2 bundled installer, verified. macOS: brew.
- `azure_cli_installer.yml` — Linux: Microsoft apt/yum repo + signing key. macOS: brew.
- (optional) `nuclei_installer.yml` — `go install` (reuse the go toolchain) or release binary + checksum.

## 6. Schema & validation

- Add `tool_categories` to `schema/operator_schema.yml` — `type: array`, items `type: string` with an
  `enum` of the defined category names (so a typo like `secuirty` fails validation loudly).
- Extend `validate_operator.py`'s registry-membership check to also confirm each `tool_categories`
  entry is a real key in `tool_sets`, and that every tool inside those sets is a `tool_registry` key.
- The install-time fail-loud assert already covers the composed result — no change needed there beyond
  including the category union in `tools_to_install` (§3.3).

## 7. Worked examples

- **jiveturkey** (the flagship): `extends: matrix` + `tool_categories: [security, cloud, devops]` →
  core + modern_cli + matrix_fun + jiveturkey's own set + security + cloud + devops. The real arsenal.
- **base**: nothing opted in → core + modern_cli. Genuinely minimal.
- **python_dev**: `tool_categories: [python]` → core + modern_cli + python. (Replaces today's
  operator-keyed `python_dev` set.)
- **A community "sre" operator**: `tool_categories: [cloud, devops]`.
- **A community "pentester_py" operator**: `tool_categories: [security, python]` — the combo the
  current model can't express.

## 8. Implementation phases

Each phase ships behind the fail-loud gate + validator, validated locally (Docker pre-commit +
real-ansible composition test + `validate_operator --all`) before merge. Each is its own PR.

1. **Engine + schema** — add `tool_sets`, the category union in the composition, and the
   `tool_categories` schema field + validation. Re-express `core`/`modern_cli` as categories.
   Backward compatible; no new tools yet. *(small, mechanical)*
2. **Cloud installers** — write `kubectl`/`helm`/`awscli`/`azure_cli` (+ optional `nuclei`) installers
   with verification; register `terraform`. *(the real infra work)*
3. **Security category** — register the apt/brew-clean security tools (sqlmap, john, hashcat,
   wireshark, nmap, netcat); handle gobuster/ffuf per-distro; build the `security` set.
4. **Wire the combos** — give `jiveturkey` its `tool_categories`; migrate `python_dev`/`nodejs_dev`/
   `go_dev` to categories; delete the dead `tools_config.*` blocks.
5. **Docs + TOOLS.md** — document the category model in the operator-creation guide; regenerate
   `TOOLS.md` from the now-real registry.

## 9. Testing

- **Composition sim + real-ansible play** (as used to verify the inheritance fix): assert each
  operator composes the expected union and that `declared ⊆ tool_registry`.
- **`validate_operator.py --all`** must stay green (enforcing validator).
- **Container CI matrix** (ubuntu/debian/kali/parrot/rocky/fedora) is where per-platform package
  coverage gets proven — this is the honest-coverage backstop. (Re-enable `Container Multi-OS Testing`,
  currently `disabled_inactivity`.)
- **Per-installer smoke**: each new installer verified in the container matrix (checksum/GPG path
  exercised).

## 10. Backward compatibility & risks

- **Compatible:** existing operators keep working — operator-keyed sets + inheritance are untouched;
  categories are additive.
- **Risk — package accuracy:** the classic trap. Mitigated three ways: honest-coverage rule (§4),
  the fail-loud gate (a wrong name stops the run), and the container matrix (proves coverage per
  distro).
- **Risk — remote-exec:** the new installers must verify (checksum/GPG), not blind `curl|bash`. This
  is a feature of the plan, not an afterthought — it also retires part of the M1 security debt.
- **Risk — scope creep:** the arsenal is large. Phases 2–3 are gated per-tool; ship what's verified,
  track the rest. Never fake coverage to look complete.

## 11. Open questions for the owner

1. **Category taxonomy** — is `[core, modern_cli, matrix_fun, security, cloud, devops, python, node,
   go, macos, windows]` the right cut? Split `security` into `recon` / `exploit` / `cracking`? Add a
   `wireless` or `forensics` category?
2. **jiveturkey's exact combo** — is `[security, cloud, devops]` right, or do you want your full
   Rick-toolset (burp, metasploit, bloodhound, nuclei, etc.) as a dedicated `offsec` category?
3. **Opt-in field name** — `tool_categories`? `tool_sets`? `include_sets`?
4. **base/matrix migration** — collapse their operator-keyed sets into `core`/`matrix_fun` categories
   now (Phase 1) or later?

---

*This spec is the blueprint; nothing here is built yet. The frame (composition + fail-loud gate +
validator) is on `main` and ready to carry it.*
