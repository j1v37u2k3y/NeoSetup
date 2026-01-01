#!/usr/bin/env python3
"""
Generate TOOLS.md documentation from tool_registry.yml

This script reads the tool registry and generates a markdown document
showing all tools available for each operator with descriptions.
"""

import sys
from pathlib import Path

import yaml


def load_tool_registry(registry_path: Path) -> dict:
    """Load the tool registry YAML file."""
    with open(registry_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def calculate_operator_counts(operator_sets: dict) -> dict:
    """Calculate tool counts including inheritance for each operator."""
    base = set(operator_sets.get("base", []))
    matrix = set(operator_sets.get("matrix", []))
    jiveturkey = set(operator_sets.get("jiveturkey", []))
    modern_cli = set(operator_sets.get("modern_cli", []))

    return {
        "base_count": len(base),
        "matrix_count": len(matrix),
        "jiveturkey_count": len(jiveturkey),
        "modern_cli_count": len(modern_cli),
        "matrix_total": len(base | matrix | modern_cli),
        "jiveturkey_total": len(base | matrix | jiveturkey | modern_cli),
    }


def generate_tools_doc(registry: dict) -> str:  # pylint: disable=too-many-locals
    """Generate markdown documentation from the tool registry."""
    tool_registry = registry.get("tool_registry", {})
    operator_sets = registry.get("operator_tool_sets", {})
    counts = calculate_operator_counts(operator_sets)

    doc = """# NeoSetup Tools Reference

> **Auto-generated** - Do not edit manually. Run `python3 neosetup/scripts/generate_tools_doc.py` to regenerate.

This document lists all tools installed by each NeoSetup operator.

## Operator Inheritance

```
base (essential tools)
  └── matrix (base + matrix-themed tools)
        └── jiveturkey (base + matrix + power-user tools)
```

## Quick Reference

| Operator | Inherits From | Unique Tools | Total Tools |
|----------|---------------|--------------|-------------|
| `base` | - | {base_count} | {base_count} |
| `matrix` | base | {matrix_count} | {matrix_total} |
| `jiveturkey` | base + matrix | {jiveturkey_count} | {jiveturkey_total} |

> **Note**: All operators also include `modern_cli` tools ({modern_cli_count} tools) for enhanced terminal experience.

---

"""
    doc = doc.format(**counts)

    # Document each operator set
    operator_descriptions = {
        "base": "Essential development tools included with every installation.",
        "matrix": "Matrix-themed tools for the cyberpunk aesthetic.",
        "jiveturkey": "Power-user tools for advanced workflows.",
        "modern_cli": "Modern replacements for classic Unix tools.",
        "macos_tools": "macOS-specific utilities for system integration.",
        "windows_wsl": "Tools for Windows Subsystem for Linux integration.",
        "python_dev": "Python development toolchain.",
        "cloud_tools": "Cloud and DevOps tools for AWS, Kubernetes, etc.",
    }

    for operator, tools in operator_sets.items():
        description = operator_descriptions.get(operator, "")
        doc += f"## {operator.replace('_', ' ').title()}\n\n"

        if description:
            doc += f"{description}\n\n"

        doc += "| Tool | Description | Category |\n"
        doc += "|------|-------------|----------|\n"

        for tool_name in sorted(tools):
            tool_info = tool_registry.get(tool_name, {})
            tool_desc = tool_info.get("description", "No description available")
            category = tool_info.get("category", "general")
            doc += f"| `{tool_name}` | {tool_desc} | {category} |\n"

        doc += "\n---\n\n"

    # Add full tool reference
    doc += """## Full Tool Registry

Complete list of all tools available in NeoSetup.

| Tool | Description | Category | Platforms |
|------|-------------|----------|-----------|
"""

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

# Install with matrix operator (includes base + matrix tools)
make install OPERATOR=matrix

# Install with jiveturkey operator (includes base + matrix + power-user tools)
make install OPERATOR=jiveturkey
```

## Adding Custom Tools

To request a new tool, open an issue with the `operator` label or submit a PR adding it to:
- `neosetup/roles/tools/vars/tool_registry.yml`

---

*Generated from `neosetup/roles/tools/vars/tool_registry.yml`*
"""

    return doc


def main():
    """Main function to generate tools documentation."""
    # Determine paths
    script_dir = Path(__file__).parent
    registry_path = script_dir.parent / "roles" / "tools" / "vars" / "tool_registry.yml"
    output_path = script_dir.parent.parent / "TOOLS.md"

    # Allow custom output path
    if len(sys.argv) > 1:
        output_path = Path(sys.argv[1])

    # Check registry exists
    if not registry_path.exists():
        print(f"Error: Tool registry not found at {registry_path}")
        sys.exit(1)

    # Load and generate
    print(f"Loading tool registry from {registry_path}")
    registry = load_tool_registry(registry_path)

    print("Generating documentation...")
    doc = generate_tools_doc(registry)

    # Write output
    output_path.write_text(doc, encoding="utf-8")
    print(f"Generated {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
