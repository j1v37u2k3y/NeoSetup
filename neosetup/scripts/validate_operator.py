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

    def _load_schema(self, schema_path: str) -> Dict:
        """Load validation schema from YAML file."""
        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except (OSError, yaml.YAMLError) as e:
            print(f"Error loading schema: {e}")
            sys.exit(1)

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
        """Validate individual field against rules."""
        # Type validation
        expected_type = rules.get("type")
        if expected_type == "string" and not isinstance(value, str):
            self.results.append(
                ValidationResult(
                    ValidationLevel.ERROR,
                    field_name,
                    f"Field '{field_name}' must be a string, got {type(value).__name__}",
                )
            )
            return

        if expected_type == "array" and not isinstance(value, list):
            self.results.append(
                ValidationResult(
                    ValidationLevel.ERROR,
                    field_name,
                    f"Field '{field_name}' must be an array, got {type(value).__name__}",
                )
            )
            return

        # Pattern validation for strings
        if isinstance(value, str) and "pattern" in rules:
            if not re.match(rules["pattern"], value):
                self.results.append(
                    ValidationResult(
                        ValidationLevel.ERROR,
                        field_name,
                        f"Field '{field_name}' value '{value}' doesn't match required pattern",
                        f"Pattern: {rules['pattern']}",
                    )
                )

        # Length validation
        if isinstance(value, str) and "max_length" in rules:
            if len(value) > rules["max_length"]:
                self.results.append(
                    ValidationResult(
                        ValidationLevel.WARNING,
                        field_name,
                        f"Field '{field_name}' exceeds maximum length of {rules['max_length']}",
                    )
                )

        # Enum validation
        if "enum" in rules and value not in rules["enum"]:
            self.results.append(
                ValidationResult(
                    ValidationLevel.ERROR,
                    field_name,
                    f"Field '{field_name}' value '{value}' not in allowed values: {rules['enum']}",
                )
            )

        # Array validation
        if isinstance(value, list) and "max_items" in rules:
            if len(value) > rules["max_items"]:
                self.results.append(
                    ValidationResult(
                        ValidationLevel.WARNING,
                        field_name,
                        f"Field '{field_name}' has {len(value)} items, recommended maximum: {rules['max_items']}",
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

        # Return non-zero exit code if there are errors
        if errors:
            sys.exit(1)


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
        validator.validate_operator(str(operator_path))
        validator.print_results(args.info)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
