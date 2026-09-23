#!/usr/bin/env python3
"""
NeoSetup Operator Validator

Validates operator configurations against the schema and inheritance rules.
Usage: python3 validate_operator.py [operator_name] [--strict] [--fix]
"""

import argparse
import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Any, Optional

import yaml

# Schema "type" values this validator understands. Any declared type outside
# this set is treated as an error rather than silently passing.
KNOWN_TYPES = ("string", "boolean", "integer", "number", "array", "object")

_TYPE_LABELS = {
    "string": "a string",
    "boolean": "a boolean",
    "integer": "an integer",
    "number": "a number",
    "array": "an array",
    "object": "an object",
}

# Type predicates. ``bool`` is deliberately excluded from ``integer``/``number``
# because in Python ``bool`` is a subclass of ``int`` (``isinstance(True, int)``
# is True), so a boolean must not satisfy a numeric type check.
_TYPE_CHECKS = {
    "string": lambda v: isinstance(v, str),
    "boolean": lambda v: isinstance(v, bool),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "array": lambda v: isinstance(v, list),
    "object": lambda v: isinstance(v, dict),
}


def _type_matches(expected_type: str, value: Any) -> bool:
    """Return True when value matches the given schema type."""
    checker = _TYPE_CHECKS.get(expected_type)
    return bool(checker(value)) if checker else False


def _type_label(expected_type: str) -> str:
    """Return a human-readable label for a schema type."""
    return _TYPE_LABELS.get(expected_type, expected_type)


class ValidationLevel(Enum):
    """Enumeration for validation severity levels."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationResult:
    """Data class representing a single validation result."""

    level: ValidationLevel
    field: str
    message: str
    suggestion: Optional[str] = None


class OperatorValidator:
    """Validator for NeoSetup operator configurations."""

    def __init__(self, schema_path: str):
        """Initialize validator with schema file."""
        self.schema = self._load_schema(schema_path)
        self.results: List[ValidationResult] = []
        self.tool_registry_keys, self.operator_tool_sets = self._load_tool_registry(schema_path)

    def _load_schema(self, schema_path: str) -> Dict:
        """Load validation schema from YAML file."""
        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except (OSError, yaml.YAMLError) as e:
            print(f"Error loading schema: {e}")
            sys.exit(1)

    def _load_tool_registry(self, schema_path: str):
        """Load registered tool names and operator tool-sets from the registry.

        The registry lives at ``roles/tools/vars/tool_registry.yml`` relative to
        the neosetup root (the schema's grandparent directory). If it cannot be
        read, registry-membership checks are skipped rather than failing hard.
        """
        registry_path = Path(schema_path).parent.parent / "roles" / "tools" / "vars" / "tool_registry.yml"
        try:
            with open(registry_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except (OSError, yaml.YAMLError):
            return set(), {}
        registry = data.get("tool_registry") or {}
        tool_sets = data.get("operator_tool_sets") or {}
        return set(registry.keys()), tool_sets

    def validate_operator(self, operator_path: str) -> List[ValidationResult]:
        """Validate a single operator configuration."""
        self.results = []

        # Load operator configuration
        try:
            with open(operator_path, "r", encoding="utf-8") as f:
                operator = yaml.safe_load(f)
        except (OSError, yaml.YAMLError) as e:
            self.results.append(ValidationResult(ValidationLevel.ERROR, "file", f"Failed to load operator file: {e}"))
            return self.results

        # Validate metadata
        self._validate_metadata(operator)

        # Validate shell configuration
        if "shell_config" in operator:
            self._validate_shell_config(operator["shell_config"])

        # Validate tmux configuration
        if "tmux_config" in operator:
            self._validate_tmux_config(operator["tmux_config"])

        # Validate tools configuration
        if "tools_config" in operator:
            self._validate_tools_config(operator["tools_config"])

        # Validate that referenced tools are registered in the tool registry
        self._validate_registered_tools(operator)

        # Validate docker configuration
        if "docker_config" in operator:
            self._validate_docker_config(operator["docker_config"])

        # Validate inheritance
        self._validate_inheritance(operator, operator_path)

        return self.results

    def _validate_metadata(self, operator: Dict) -> None:
        """Validate operator metadata fields."""
        schema = self.schema["operator_metadata"]

        # Check required fields
        for field in schema["required_fields"]:
            if field not in operator:
                self.results.append(
                    ValidationResult(
                        ValidationLevel.ERROR,
                        field,
                        f"Required field '{field}' is missing",
                        f"Add '{field}: <value>' to your operator configuration",
                    )
                )

        # Validate field types and patterns
        for field, rules in schema["field_types"].items():
            if field in operator:
                self._validate_field(field, operator[field], rules)

    def _validate_field(self, field_name: str, value: Any, rules: Dict) -> None:
        """Validate an individual field value against its schema rules.

        Honors the full schema vocabulary: string/boolean/integer/number/array/
        object types, string pattern/min_length/max_length, scalar enum,
        integer/number minimum/maximum, array max_items and per-item rules
        (element enum/pattern and nested-object required/properties), and object
        max_properties with nested property recursion.
        """
        if not self._validate_field_type(field_name, value, rules):
            return
        self._validate_string_constraints(field_name, value, rules)
        self._validate_enum(field_name, value, rules)
        self._validate_numeric_constraints(field_name, value, rules)
        self._validate_array_constraints(field_name, value, rules)
        self._validate_object_constraints(field_name, value, rules)

    def _validate_field_type(self, field_name: str, value: Any, rules: Dict) -> bool:
        """Check a field's declared type.

        Returns False (stop further checks) on a type mismatch or an unknown
        declared type; True when the value's type is acceptable.
        """
        expected_type = rules.get("type")
        if expected_type is None:
            return True

        if expected_type not in KNOWN_TYPES:
            self.results.append(
                ValidationResult(
                    ValidationLevel.ERROR,
                    field_name,
                    f"Field '{field_name}' declares unknown type '{expected_type}' in schema",
                    f"Use one of: {', '.join(KNOWN_TYPES)}",
                )
            )
            return False

        # The schema declares some list-valued fields (e.g. tmux plugins) as
        # objects; tolerate the list form rather than emit a false positive.
        if expected_type == "object" and isinstance(value, list):
            return False

        if not _type_matches(expected_type, value):
            self.results.append(
                ValidationResult(
                    ValidationLevel.ERROR,
                    field_name,
                    f"Field '{field_name}' must be {_type_label(expected_type)}, got {type(value).__name__}",
                )
            )
            return False
        return True

    def _validate_string_constraints(self, field_name: str, value: Any, rules: Dict) -> None:
        """Validate string-specific rules: pattern, min_length and max_length."""
        if not isinstance(value, str):
            return

        pattern = rules.get("pattern")
        if pattern and not re.match(pattern, value):
            self.results.append(
                ValidationResult(
                    ValidationLevel.ERROR,
                    field_name,
                    f"Field '{field_name}' value '{value}' doesn't match required pattern",
                    f"Pattern: {pattern}",
                )
            )

        min_length = rules.get("min_length")
        if min_length is not None and len(value) < min_length:
            self.results.append(
                ValidationResult(
                    ValidationLevel.ERROR,
                    field_name,
                    f"Field '{field_name}' is shorter than minimum length of {min_length}",
                )
            )

        max_length = rules.get("max_length")
        if max_length is not None and len(value) > max_length:
            self.results.append(
                ValidationResult(
                    ValidationLevel.WARNING,
                    field_name,
                    f"Field '{field_name}' exceeds maximum length of {max_length}",
                )
            )

    def _validate_enum(self, field_name: str, value: Any, rules: Dict) -> None:
        """Validate an enum constraint on a scalar value."""
        if "enum" not in rules or isinstance(value, (list, dict)):
            return
        if value not in rules["enum"]:
            self.results.append(
                ValidationResult(
                    ValidationLevel.ERROR,
                    field_name,
                    f"Field '{field_name}' value '{value}' not in allowed values: {rules['enum']}",
                )
            )

    def _validate_numeric_constraints(self, field_name: str, value: Any, rules: Dict) -> None:
        """Validate integer/number minimum and maximum bounds."""
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return

        minimum = rules.get("minimum")
        if minimum is not None and value < minimum:
            self.results.append(
                ValidationResult(
                    ValidationLevel.ERROR,
                    field_name,
                    f"Field '{field_name}' value {value} is below minimum of {minimum}",
                )
            )

        maximum = rules.get("maximum")
        if maximum is not None and value > maximum:
            self.results.append(
                ValidationResult(
                    ValidationLevel.ERROR,
                    field_name,
                    f"Field '{field_name}' value {value} is above maximum of {maximum}",
                )
            )

    def _validate_array_constraints(self, field_name: str, value: Any, rules: Dict) -> None:
        """Validate array max_items and recurse into per-item rules."""
        if not isinstance(value, list):
            return

        max_items = rules.get("max_items")
        if max_items is not None and len(value) > max_items:
            self.results.append(
                ValidationResult(
                    ValidationLevel.WARNING,
                    field_name,
                    f"Field '{field_name}' has {len(value)} items, recommended maximum: {max_items}",
                )
            )

        item_rules = rules.get("items")
        if isinstance(item_rules, dict):
            for index, item in enumerate(value):
                self._validate_array_item(field_name, index, item, item_rules)

    def _validate_array_item(self, field_name: str, index: int, item: Any, item_rules: Dict) -> None:
        """Validate a single array element against the schema's item rules.

        Enforces element enum and pattern, and for nested objects the required
        fields and declared properties.
        """
        item_field = f"{field_name}[{index}]"

        if "enum" in item_rules and item not in item_rules["enum"]:
            self.results.append(
                ValidationResult(
                    ValidationLevel.ERROR,
                    item_field,
                    f"Value '{item}' not in allowed values: {item_rules['enum']}",
                )
            )

        pattern = item_rules.get("pattern")
        if pattern and isinstance(item, str) and not re.match(pattern, item):
            self.results.append(
                ValidationResult(
                    ValidationLevel.ERROR,
                    item_field,
                    f"Value '{item}' doesn't match required pattern",
                    f"Pattern: {pattern}",
                )
            )

        if item_rules.get("type") == "object" and isinstance(item, dict):
            for required_field in item_rules.get("required") or []:
                if required_field not in item:
                    self.results.append(
                        ValidationResult(
                            ValidationLevel.ERROR,
                            item_field,
                            f"Missing required field '{required_field}'",
                            f"Add '{required_field}' to this entry",
                        )
                    )
            for prop_name, prop_rules in (item_rules.get("properties") or {}).items():
                if prop_name in item:
                    self._validate_field(f"{item_field}.{prop_name}", item[prop_name], prop_rules)

    def _validate_object_constraints(self, field_name: str, value: Any, rules: Dict) -> None:
        """Validate object max_properties and recurse into declared properties."""
        if not isinstance(value, dict):
            return

        max_properties = rules.get("max_properties")
        if max_properties is not None and len(value) > max_properties:
            self.results.append(
                ValidationResult(
                    ValidationLevel.WARNING,
                    field_name,
                    f"Field '{field_name}' has {len(value)} properties, recommended maximum: {max_properties}",
                )
            )

        for prop_name, prop_rules in (rules.get("properties") or {}).items():
            if prop_name in value:
                self._validate_field(f"{field_name}.{prop_name}", value[prop_name], prop_rules)

    def _validate_registered_tools(self, operator: Dict) -> None:
        """Flag tools referenced by an operator that are not in the tool registry.

        Every name in ``tools_config.additional_tools`` (and, when the operator
        name maps to an ``operator_tool_sets`` entry, the members of that set)
        must be a key in ``roles/tools/vars/tool_registry.yml`` -- otherwise the
        installer silently skips it (``when: item in tool_registry``).
        """
        if not self.tool_registry_keys:
            return

        tools_config = operator.get("tools_config") or {}
        additional_tools = tools_config.get("additional_tools") or []
        if isinstance(additional_tools, list):
            for tool in additional_tools:
                if isinstance(tool, str) and tool not in self.tool_registry_keys:
                    self.results.append(
                        ValidationResult(
                            ValidationLevel.ERROR,
                            "tools_config.additional_tools",
                            f"Tool '{tool}' is not registered in roles/tools/vars/tool_registry.yml",
                            f"Add '{tool}' to the tool registry or remove it from additional_tools",
                        )
                    )

        operator_name = operator.get("operator_name")
        members = self.operator_tool_sets.get(operator_name) if operator_name else None
        for tool in members or []:
            if isinstance(tool, str) and tool not in self.tool_registry_keys:
                self.results.append(
                    ValidationResult(
                        ValidationLevel.ERROR,
                        f"operator_tool_sets.{operator_name}",
                        f"Tool '{tool}' in operator_tool_sets['{operator_name}'] is not registered",
                        f"Add '{tool}' to the tool registry or remove it from the tool set",
                    )
                )

    def _validate_shell_config(self, shell_config: Dict) -> None:
        """Validate shell configuration section."""
        schema = self.schema["shell_config"]

        for field, value in shell_config.items():
            if field in schema["field_types"]:
                self._validate_field(f"shell_config.{field}", value, schema["field_types"][field])

        # Custom validations
        if "oh_my_zsh_plugins" in shell_config:
            plugins = shell_config["oh_my_zsh_plugins"]
            if len(plugins) > 15:
                self.results.append(
                    ValidationResult(
                        ValidationLevel.WARNING,
                        "shell_config.oh_my_zsh_plugins",
                        f"Large number of plugins ({len(plugins)}) may slow shell startup",
                        "Consider removing unused plugins",
                    )
                )

    def _validate_tmux_config(self, tmux_config: Dict) -> None:
        """Validate tmux configuration section."""
        schema = self.schema["tmux_config"]

        for field, value in tmux_config.items():
            if field in schema["field_types"]:
                if field == "settings" and isinstance(value, dict):
                    # Validate nested settings
                    for setting, setting_value in value.items():
                        setting_rules = schema["field_types"]["settings"]["properties"].get(setting, {})
                        if setting_rules:
                            self._validate_field(
                                f"tmux_config.settings.{setting}",
                                setting_value,
                                setting_rules,
                            )
                else:
                    self._validate_field(f"tmux_config.{field}", value, schema["field_types"][field])

    def _validate_tools_config(self, tools_config: Dict) -> None:
        """Validate tools configuration section."""
        schema = self.schema["tools_config"]

        for field, value in tools_config.items():
            if field in schema["field_types"]:
                self._validate_field(f"tools_config.{field}", value, schema["field_types"][field])

    def _validate_docker_config(self, docker_config: Dict) -> None:
        """Validate docker configuration section."""
        schema = self.schema["docker_config"]

        for field, value in docker_config.items():
            if field in schema["field_types"]:
                self._validate_field(f"docker_config.{field}", value, schema["field_types"][field])

    def _validate_inheritance(self, operator: Dict, operator_path: str) -> None:
        """Validate operator inheritance rules."""
        if "extends" not in operator:
            return

        parent_name = operator["extends"]

        # Check if parent exists
        parent_path = Path(operator_path).parent.parent / parent_name / "vars.yml"
        if not parent_path.exists():
            self.results.append(
                ValidationResult(
                    ValidationLevel.ERROR,
                    "extends",
                    f"Parent operator '{parent_name}' not found at {parent_path}",
                    "Create the parent operator or fix the 'extends' field",
                )
            )
            return

        # Check for circular dependencies (simplified)
        try:
            with open(parent_path, "r", encoding="utf-8") as f:
                parent_operator = yaml.safe_load(f)

            if parent_operator.get("extends") == operator.get("operator_name"):
                self.results.append(
                    ValidationResult(
                        ValidationLevel.ERROR,
                        "extends",
                        f"Circular dependency detected with parent '{parent_name}'",
                    )
                )
        except (OSError, yaml.YAMLError) as e:
            self.results.append(
                ValidationResult(
                    ValidationLevel.WARNING,
                    "extends",
                    f"Could not validate parent operator: {e}",
                )
            )

    def print_results(self, show_info: bool = False) -> None:
        """Print validation results in a formatted way."""
        if not self.results:
            print("✅ Operator validation passed!")
            return

        errors = [r for r in self.results if r.level == ValidationLevel.ERROR]
        warnings = [r for r in self.results if r.level == ValidationLevel.WARNING]
        info = [r for r in self.results if r.level == ValidationLevel.INFO]

        if errors:
            print(f"\n❌ {len(errors)} Error(s):")
            for result in errors:
                print(f"  • {result.field}: {result.message}")
                if result.suggestion:
                    print(f"    💡 {result.suggestion}")

        if warnings:
            print(f"\n⚠️  {len(warnings)} Warning(s):")
            for result in warnings:
                print(f"  • {result.field}: {result.message}")
                if result.suggestion:
                    print(f"    💡 {result.suggestion}")

        if info and show_info:
            print(f"\nℹ️  {len(info)} Info:")
            for result in info:
                print(f"  • {result.field}: {result.message}")


def main():  # pylint: disable=too-many-branches
    """Main function to validate NeoSetup operator configurations."""
    parser = argparse.ArgumentParser(description="Validate NeoSetup operator configuration")
    parser.add_argument("operator", nargs="?", help="Operator name or path to validate")
    parser.add_argument("--all", action="store_true", help="Validate all operators")
    parser.add_argument("--info", action="store_true", help="Show info-level messages")
    parser.add_argument("--schema", help="Path to schema file", default="schema/operator_schema.yml")

    args = parser.parse_args()

    # Find script directory and schema
    script_dir = Path(__file__).parent
    schema_path = script_dir.parent / args.schema

    if not schema_path.exists():
        print(f"Schema file not found: {schema_path}")
        sys.exit(1)

    validator = OperatorValidator(str(schema_path))

    if args.all:
        # Validate all operators
        operators_dir = script_dir.parent / "operators"
        if not operators_dir.exists():
            print("Operators directory not found")
            sys.exit(1)

        all_passed = True
        for operator_dir in operators_dir.iterdir():
            if operator_dir.is_dir():
                vars_file = operator_dir / "vars.yml"
                if vars_file.exists():
                    print(f"\n🔍 Validating operator: {operator_dir.name}")
                    results = validator.validate_operator(str(vars_file))
                    validator.print_results(args.info)
                    if any(r.level == ValidationLevel.ERROR for r in results):
                        all_passed = False

        if all_passed:
            print("\n🎉 All operators validated successfully!")
        else:
            print("\n❌ Some operators have validation errors")
            sys.exit(1)

    elif args.operator:
        # Validate specific operator
        if "/" in args.operator:
            operator_path = args.operator
        else:
            operators_dir = script_dir.parent / "operators"
            operator_path = operators_dir / args.operator / "vars.yml"

        if not Path(operator_path).exists():
            print(f"Operator file not found: {operator_path}")
            sys.exit(1)

        print(f"🔍 Validating operator: {Path(operator_path).parent.name}")
        results = validator.validate_operator(str(operator_path))
        validator.print_results(args.info)
        if any(r.level == ValidationLevel.ERROR for r in results):
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
