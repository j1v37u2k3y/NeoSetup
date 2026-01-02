#!/usr/bin/env python3
"""
Binary Validation Script for NeoSetup
Validates that all expected tools are installed and executable for each operator.
"""

import argparse
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
}

# Platform-specific binary name overrides
PLATFORM_BINARY_MAP = {
    "debian": {"fd": "fdfind"},
    "ubuntu": {"fd": "fdfind"},
    # macOS and RHEL use 'fd' directly
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


def get_operator_tools(registry: dict, operator: str) -> set:
    """Get all tools for an operator including inherited tools."""
    operator_sets = registry.get("operator_tool_sets", {})

    # Base tools included with all operators
    base_tools = set(operator_sets.get("base", []))
    modern_cli = set(operator_sets.get("modern_cli", []))

    if operator == "base":
        return base_tools | modern_cli

    if operator == "matrix":
        matrix_tools = set(operator_sets.get("matrix", []))
        return base_tools | matrix_tools | modern_cli

    if operator == "jiveturkey":
        matrix_tools = set(operator_sets.get("matrix", []))
        jiveturkey_tools = set(operator_sets.get("jiveturkey", []))
        return base_tools | matrix_tools | jiveturkey_tools | modern_cli

    # Unknown operator - just return its tools
    return set(operator_sets.get(operator, []))


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
        result = subprocess.run(  # nosec B607 B602 - command -v requires shell
            f"command -v {binary_name}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
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
    registry: dict, operator: str, os_name: str, verbose: bool = False
) -> tuple[int, int, list]:
    """Validate all tools for an operator are installed."""
    tools = get_operator_tools(registry, operator)
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
        choices=["base", "matrix", "jiveturkey"],
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

    passed, failed, failures = validate_operator_tools(registry, args.operator, args.os, args.verbose)

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
