#!/usr/bin/env python3
"""
Binary Validation Script for NeoSetup
Validates that all expected tools are installed and executable for each operator.
"""

import argparse
import os
import subprocess  # nosec B404
import sys
from pathlib import Path

import yaml

# Mapping of tool names to their actual binary names
# Some packages install binaries with different names
BINARY_NAME_MAP = {
    "ripgrep": "rg",
    "httpie": "http",
    "netcat": "nc",
    "mc": "mc",  # midnight-commander on macOS installs as mc
    "pre-commit": "pre-commit",
    "docker-compose": "docker-compose",
    "build-essential": "gcc",  # Check for gcc as indicator
    "python3-pip": "pip3",
    "awscli": "aws",
    "azure-cli": "az",
    "impacket": "smbserver.py",  # pipx/pip expose impacket examples by their real names
}

# Platform-specific binary name overrides
PLATFORM_BINARY_MAP = {
    # Debian/Ubuntu rename these binaries to avoid package collisions.
    "debian": {"fd": "fdfind", "bat": "batcat"},
    "ubuntu": {"fd": "fdfind", "bat": "batcat"},
    # macOS and RHEL use 'fd' / 'bat' directly
}

# Tools that require special handling or should be skipped in container tests
SKIP_IN_CONTAINER = {
    # macOS-only tools
    "duti",
    "mas",
    "mackup",
    "stats",
    "rectangle",
    # WSL-only tools
    "wslu",
    "powershell",
    # GUI or special tools
    "jupyter",  # Requires display
}

# Custom installation tools that may not be in PATH without shell init
CUSTOM_INSTALL_TOOLS = {
    "pyenv",
    "poetry",
    "kubectl",
    "helm",
    "azure-cli",
    "act",
}


def load_tool_registry(registry_path: Path) -> dict:
    """Load the tool registry YAML file."""
    with open(registry_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_binary_name(tool_name: str, platform: str = "") -> str:
    """Get the actual binary name for a tool, considering platform-specific overrides."""
    # Check platform-specific overrides first
    if platform in PLATFORM_BINARY_MAP:
        if tool_name in PLATFORM_BINARY_MAP[platform]:
            return PLATFORM_BINARY_MAP[platform][tool_name]
    # Fall back to general mapping
    return BINARY_NAME_MAP.get(tool_name, tool_name)


def get_operator_tools(
    registry: dict,
    operator: str,
    group_vars_path: Path | None = None,
    operators_dir: Path | None = None,
) -> set:
    """Compose an operator's expected tools exactly like install_tools_unified.yml:
    modern_cli + operator_tool_sets across the inheritance spine + tool_categories
    (via tool_sets) + tools_config.additional_tools. Reads inheritance from
    group_vars and the operator's own vars so it stays correct as operators change."""
    operator_sets = registry.get("operator_tool_sets", {})
    tool_sets = registry.get("tool_sets", {})

    tools = set(operator_sets.get("modern_cli", []))

    # Inheritance spine (dynamic, from group_vars) + the operator itself.
    inheritance = {}
    if group_vars_path and group_vars_path.exists():
        with open(group_vars_path, encoding="utf-8") as f:
            gv = yaml.safe_load(f) or {}
        inheritance = gv.get("operator_inheritance", {}) or {}
    for op in (inheritance.get(operator, []) or []) + [operator]:
        tools |= set(operator_sets.get(op, []))

    # The operator's opted-in categories + additional_tools (from its vars.yml).
    if operators_dir:
        op_vars_path = operators_dir / operator / "vars.yml"
        if op_vars_path.exists():
            with open(op_vars_path, encoding="utf-8") as f:
                ov = yaml.safe_load(f) or {}
            for category in ov.get("tool_categories", []) or []:
                tools |= set(tool_sets.get(category, []))
            tools |= set((ov.get("tools_config") or {}).get("additional_tools") or [])

    return tools


def get_platform(os_name: str) -> str:
    """Map OS name to registry platform."""
    platform_map = {
        "ubuntu-22.04": "ubuntu",
        "ubuntu-24.04": "ubuntu",
        "debian-12": "debian",
        "kali-rolling": "debian",
        "parrot-security": "debian",
        "centos-stream-9": "redhat",
        "rocky-9": "redhat",
        "almalinux-9": "redhat",
        "fedora-40": "redhat",
    }
    return platform_map.get(os_name, os_name)


def check_binary(binary_name: str) -> tuple[bool, str]:
    """Check if a binary is available in PATH."""
    try:
        env = {**os.environ, "PATH": os.environ.get("PATH", "") + ":/usr/games:/usr/local/games"}
        result = subprocess.run(  # nosec B607 B602 - command -v requires shell
            f"command -v {binary_name}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
            env=env,
        )
        if result.returncode == 0:
            path = result.stdout.strip()
            return True, path
        return False, ""
    except (subprocess.TimeoutExpired, OSError) as e:
        return False, str(e)


def should_skip_tool(tool: str, packages: dict, platform: str) -> str | None:
    """Check if a tool should be skipped. Returns skip reason or None."""
    if tool in SKIP_IN_CONTAINER:
        return "platform-specific"
    if not packages and tool not in CUSTOM_INSTALL_TOOLS:
        return f"no package for {platform}"
    has_platform_pkg = platform in packages or "pip" in packages
    if not has_platform_pkg and tool not in CUSTOM_INSTALL_TOOLS:
        return f"not available on {platform}"
    return None


def validate_single_tool(tool: str, platform: str, tool_registry: dict, verbose: bool) -> str:
    """Validate a single tool. Returns 'pass', 'fail', 'skip', or 'custom'."""
    tool_info = tool_registry.get(tool, {})
    packages = tool_info.get("packages", {})

    skip_reason = should_skip_tool(tool, packages, platform)
    if skip_reason:
        if verbose:
            print(f"⏭️  {tool}: Skipped ({skip_reason})")
        return "skip"

    binary = get_binary_name(tool, platform)
    found, path = check_binary(binary)

    if found:
        print(f"✅ {tool} ({binary}): {path}" if verbose else f"✅ {tool}")
        return "pass"

    if tool in CUSTOM_INSTALL_TOOLS:
        if verbose:
            print(f"⚠️  {tool} ({binary}): Not in PATH (custom install)")
        return "custom"

    print(f"❌ {tool} ({binary}): NOT FOUND")
    return "fail"


def validate_operator_tools(
    registry: dict,
    operator: str,
    os_name: str,
    verbose: bool = False,
    source_paths: tuple[Path | None, Path | None] = (None, None),
) -> tuple[int, int, list]:
    """Validate all tools for an operator are installed."""
    group_vars_path, operators_dir = source_paths
    tools = get_operator_tools(registry, operator, group_vars_path, operators_dir)
    tool_registry = registry.get("tool_registry", {})
    platform = get_platform(os_name)

    print(f"\n{'=' * 60}")
    print(f"Validating {operator} operator ({len(tools)} tools)")
    print(f"{'=' * 60}\n")

    passed, failed, failures = 0, 0, []
    for tool in sorted(tools):
        result = validate_single_tool(tool, platform, tool_registry, verbose)
        if result == "pass":
            passed += 1
        elif result == "fail":
            failed += 1
            failures.append(tool)

    return passed, failed, failures


def main():
    """Main function to validate operator tool installations."""
    parser = argparse.ArgumentParser(description="Validate NeoSetup operator tool installations")
    parser.add_argument(
        "--operator",
        required=True,
        choices=["base", "matrix", "jiveturkey", "macos", "windows_wsl", "python_dev", "nodejs_dev", "go_dev"],
        help="Operator to validate",
    )
    parser.add_argument(
        "--os",
        required=True,
        help="OS name (e.g., ubuntu-22.04, debian-12)",
    )
    parser.add_argument(
        "--registry",
        default=None,
        help="Path to tool_registry.yml",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output",
    )

    args = parser.parse_args()

    # Find registry file
    if args.registry:
        registry_path = Path(args.registry)
    else:
        # Try common locations
        possible_paths = [
            Path("neosetup/roles/tools/vars/tool_registry.yml"),
            Path("/neosetup/neosetup/roles/tools/vars/tool_registry.yml"),
            Path(__file__).parent.parent.parent / "neosetup/roles/tools/vars/tool_registry.yml",
        ]
        registry_path = None
        for p in possible_paths:
            if p.exists():
                registry_path = p
                break

        if not registry_path:
            print("❌ Could not find tool_registry.yml")
            sys.exit(1)

    print(f"📋 Loading registry from {registry_path}")
    registry = load_tool_registry(registry_path)

    # Derive group_vars + operators dir from the registry location
    # (.../neosetup/roles/tools/vars/tool_registry.yml -> neosetup root is parents[3]).
    neosetup_root = registry_path.resolve().parents[3]
    group_vars_path = neosetup_root / "group_vars" / "all" / "operators.yml"
    operators_dir = neosetup_root / "operators"

    passed, failed, failures = validate_operator_tools(
        registry, args.operator, args.os, args.verbose, (group_vars_path, operators_dir)
    )

    # Summary
    print(f"\n{'=' * 60}")
    print("VALIDATION SUMMARY")
    print(f"{'=' * 60}")
    print(f"Operator: {args.operator}")
    print(f"OS: {args.os}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failures:
        print(f"\nMissing tools: {', '.join(failures)}")
        sys.exit(1)

    print("\n✅ All expected tools validated successfully!")
    sys.exit(0)


if __name__ == "__main__":
    main()
