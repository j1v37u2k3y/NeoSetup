#!/usr/bin/env python3
"""
Generate TOOLS.md documentation from tool_registry.yml

This script reads the tool registry and the operator spine (inheritance +
``operator_tool_categories``) plus each operator's own ``vars.yml`` to compose
the exact tool list each operator installs, then renders it as markdown.
"""

import sys
from pathlib import Path

import yaml


def load_yaml(path: Path) -> dict:
    """Load a YAML file into a dict (empty dict when missing or empty)."""
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def compose_operator_tools(
    operator: str,
    inheritance: dict,
    operator_tool_categories: dict,
    tool_sets: dict,
    operator_vars: dict,
) -> set:
    """Compose the full tool set an operator installs.

    Mirrors ``install_tools_unified.yml``: spine categories from
    ``operator_tool_categories`` (across ``operator_inheritance`` + self), plus
    the operator's own ``tool_categories`` and every value of
    ``tool_categories_by_platform``, plus ``tools_config.additional_tools``.
    Each category resolves against ``tool_sets``.
    """
    categories: list = []
    for op in list(inheritance.get(operator, []) or []) + [operator]:
        categories += list(operator_tool_categories.get(op, []) or [])

    categories += list(operator_vars.get("tool_categories") or [])
    by_platform = operator_vars.get("tool_categories_by_platform") or {}
    if isinstance(by_platform, dict):
        for cats in by_platform.values():
            categories += list(cats or [])

    tools: set = set()
    for category in categories:
        tools |= set(tool_sets.get(category, []) or [])

    additional = (operator_vars.get("tools_config") or {}).get("additional_tools") or []
    tools |= {t for t in additional if isinstance(t, str)}
    return tools


def compose_all_operators(
    inheritance: dict,
    operator_tool_categories: dict,
    tool_sets: dict,
    operators_dir: Path,
) -> dict:
    """Return a dict of operator_name -> sorted tool list for every operator."""
    composed: dict = {}
    for operator in operator_tool_categories.keys():
        op_vars = load_yaml(operators_dir / operator / "vars.yml")
        composed[operator] = sorted(
            compose_operator_tools(operator, inheritance, operator_tool_categories, tool_sets, op_vars)
        )
    return composed


def render_doc(
    tool_registry: dict,
    tool_sets: dict,
    composed_operators: dict,
    inheritance: dict,
) -> str:
    """Render the TOOLS.md markdown from composed operator tool lists."""
    operator_descriptions = {
        "base": "Essential development tools included with every installation.",
        "matrix": "Matrix-themed tools layered on top of base.",
        "jiveturkey": "Power-user setup with the full red-team arsenal (offsec on Linux).",
        "macos": "macOS-specific utilities for system integration.",
        "windows_wsl": "Tools for Windows Subsystem for Linux integration.",
        "python_dev": "Python development toolchain.",
        "nodejs_dev": "Node.js development environment.",
        "go_dev": "Go toolchain and go-install developer tools.",
    }

    def inherits_from(operator: str) -> str:
        chain = list(inheritance.get(operator, []) or [])
        return " + ".join(chain) if chain else "-"

    doc = """# NeoSetup Tools Reference

> **Auto-generated** - Do not edit manually. Run `python3 neosetup/scripts/generate_tools_doc.py` to regenerate.

This document lists all tools installed by each NeoSetup operator, composed from the
category tool-sets each operator opts into (see
[composable-tool-sets.md](docs/architecture/composable-tool-sets.md)).

## Operator Inheritance

| Operator | Inherits From | Total Tools |
|----------|---------------|-------------|
"""
    for operator, tools in composed_operators.items():
        doc += f"| `{operator}` | {inherits_from(operator)} | {len(tools)} |\n"

    doc += "\n---\n\n"

    for operator, tools in composed_operators.items():
        description = operator_descriptions.get(operator, "")
        doc += f"## {operator.replace('_', ' ').title()}\n\n"
        if description:
            doc += f"{description}\n\n"
        doc += "| Tool | Description | Category |\n"
        doc += "|------|-------------|----------|\n"
        for tool_name in tools:
            tool_info = tool_registry.get(tool_name, {})
            tool_desc = tool_info.get("description", "No description available")
            category = tool_info.get("category", "general")
            doc += f"| `{tool_name}` | {tool_desc} | {category} |\n"
        doc += "\n---\n\n"

    doc += "## Category Tool Sets\n\n"
    doc += "Named, reusable bundles operators compose. See `tool_sets` in `tool_registry.yml`.\n\n"
    for category, members in tool_sets.items():
        doc += f"### `{category}`\n\n"
        if not members:
            doc += "_(empty)_\n\n"
            continue
        for tool_name in sorted(members):
            tool_info = tool_registry.get(tool_name, {})
            tool_desc = tool_info.get("description", "No description available")
            doc += f"- `{tool_name}` — {tool_desc}\n"
        doc += "\n"

    doc += "---\n\n## Full Tool Registry\n\n"
    doc += "Complete list of all tools available in NeoSetup.\n\n"
    doc += "| Tool | Description | Category | Platforms |\n"
    doc += "|------|-------------|----------|-----------|\n"
    for tool_name, tool_info in sorted(tool_registry.items()):
        desc = tool_info.get("description", "No description")
        category = tool_info.get("category", "general")
        packages = tool_info.get("packages", {})
        platforms = ", ".join(sorted(packages.keys())) if packages else "custom"
        doc += f"| `{tool_name}` | {desc} | {category} | {platforms} |\n"

    doc += """
---

## Installation

Tools are automatically installed based on your chosen operator:

```bash
# Install with base operator (minimal)
make install OPERATOR=base

# Install with matrix operator (base + matrix-themed tools)
make install OPERATOR=matrix

# Install with jiveturkey operator (base + matrix + power-user + offsec on Linux)
make install OPERATOR=jiveturkey
```

## Adding Custom Tools

To request a new tool, open an issue with the `operator` label or submit a PR adding it to:
- `neosetup/roles/tools/vars/tool_registry.yml`

---

*Generated from `neosetup/roles/tools/vars/tool_registry.yml` + `neosetup/group_vars/all/operators.yml` + each operator's `vars.yml`.*
"""

    return doc


def main():
    """Main function to generate tools documentation."""
    script_dir = Path(__file__).parent
    neosetup_dir = script_dir.parent
    registry_path = neosetup_dir / "roles" / "tools" / "vars" / "tool_registry.yml"
    group_vars_path = neosetup_dir / "group_vars" / "all" / "operators.yml"
    operators_dir = neosetup_dir / "operators"
    output_path = neosetup_dir.parent / "TOOLS.md"

    if len(sys.argv) > 1:
        output_path = Path(sys.argv[1])

    if not registry_path.exists():
        print(f"Error: Tool registry not found at {registry_path}")
        sys.exit(1)

    print(f"Loading tool registry from {registry_path}")
    registry = load_yaml(registry_path)
    tool_registry = registry.get("tool_registry", {})
    tool_sets = registry.get("tool_sets", {})

    print(f"Loading operator spine from {group_vars_path}")
    group_vars = load_yaml(group_vars_path)
    inheritance = group_vars.get("operator_inheritance", {}) or {}
    operator_tool_categories = group_vars.get("operator_tool_categories", {}) or {}

    print("Composing per-operator tool lists...")
    composed = compose_all_operators(inheritance, operator_tool_categories, tool_sets, operators_dir)

    print("Generating documentation...")
    doc = render_doc(tool_registry, tool_sets, composed, inheritance)

    output_path.write_text(doc, encoding="utf-8")
    print(f"Generated {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
