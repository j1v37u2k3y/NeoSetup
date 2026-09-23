#!/usr/bin/env python3
"""
Test suite for operator validation system
Tests various validation scenarios and error conditions

The negative cases assert on the *specific* offending field and severity per
injected fault (one fault per assertion). The boolean / integer-range /
array-item-enum / nested-object cases exercise behavior the validator silently
ignored before enforcement was added -- they detect nothing against the old
validator and produce a targeted error against the current one.
"""

# pylint: disable=wrong-import-position,wrong-import-order,consider-using-with,import-error
# pylint: disable=too-many-public-methods,protected-access
# Test files need flexible imports, file handling and direct helper access.

import copy
import os
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

# Add the scripts directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
try:
    from validate_operator import OperatorValidator, ValidationLevel  # noqa: E402
except ImportError:
    # Fallback for different environments
    ValidationLevel = None
    OperatorValidator = None


def errors_of(results):
    """Return only the ERROR-level results."""
    return [r for r in results if r.level == ValidationLevel.ERROR]


def warnings_of(results):
    """Return only the WARNING-level results."""
    return [r for r in results if r.level == ValidationLevel.WARNING]


def errors_for(results, field):
    """Return ERROR-level results for an exact field name."""
    return [r for r in errors_of(results) if r.field == field]


def errors_matching(results, prefix):
    """Return ERROR-level results whose field starts with the given prefix."""
    return [r for r in errors_of(results) if r.field.startswith(prefix)]


class TestOperatorValidation(unittest.TestCase):
    """Test operator validation functionality"""

    def setUp(self):
        """Set up test environment"""
        # Path to the schema file
        self.schema_path = Path(__file__).parent.parent / "schema" / "operator_schema.yml"
        self.validator = OperatorValidator(str(self.schema_path))

        # Base valid operator for testing
        self.valid_operator = {
            "operator_name": "test",
            "operator_version": "1.0.0",
            "operator_description": "Test operator",
            "shell_config": {
                "preferred_shell": "zsh",
                "oh_my_zsh_plugins": ["git", "docker"],
            },
        }

    def base_operator(self):
        """Return a fresh, deep-copied minimal valid operator."""
        return copy.deepcopy(self.valid_operator)

    def create_temp_operator(self, operator_data):
        """Create a temporary operator file for testing"""
        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False)
        yaml.dump(operator_data, temp_file)
        temp_file.close()
        return temp_file.name

    def validate(self, operator_data):
        """Write operator_data to a temp file, validate it and return results."""
        temp_file = self.create_temp_operator(operator_data)
        try:
            return self.validator.validate_operator(temp_file)
        finally:
            os.unlink(temp_file)

    def test_valid_operator(self):
        """Test validation of a valid operator"""
        results = self.validate(self.valid_operator)
        self.assertEqual(len(results), 0, "Valid operator should have no validation errors")

    def test_missing_required_fields(self):
        """Test validation with missing required fields"""
        results = self.validate({"shell_config": {"preferred_shell": "zsh"}})
        # Each required field is reported individually as its own error.
        self.assertEqual(len(errors_for(results, "operator_name")), 1)
        self.assertEqual(len(errors_for(results, "operator_version")), 1)
        self.assertEqual(len(errors_for(results, "operator_description")), 1)

    def test_invalid_field_types(self):
        """Test validation with invalid field types reports the offending field"""
        invalid_operator = self.base_operator()
        invalid_operator["operator_name"] = 123  # Should be a string

        results = self.validate(invalid_operator)
        name_errors = errors_for(results, "operator_name")
        self.assertEqual(len(name_errors), 1, "operator_name (int) should be a type error")
        self.assertIn("must be a string", name_errors[0].message)

    def test_array_type_enforced(self):
        """A string where an array is expected is flagged on that field"""
        invalid_operator = self.base_operator()
        invalid_operator["shell_config"]["oh_my_zsh_plugins"] = "not-an-array"

        results = self.validate(invalid_operator)
        plugin_errors = errors_for(results, "shell_config.oh_my_zsh_plugins")
        self.assertEqual(len(plugin_errors), 1, "oh_my_zsh_plugins (str) should be an array-type error")
        self.assertIn("must be an array", plugin_errors[0].message)

    def test_pattern_validation(self):
        """Test pattern validation for operator name"""
        invalid_operator = self.base_operator()
        invalid_operator["operator_name"] = "Invalid-Name!"  # Doesn't match pattern

        results = self.validate(invalid_operator)
        name_errors = errors_for(results, "operator_name")
        self.assertEqual(len(name_errors), 1)
        self.assertIn("pattern", name_errors[0].message.lower())

    def test_version_pattern(self):
        """Test version pattern validation"""
        test_cases = [
            ("1.0.0", True),  # Valid semver
            ("1.0.0-beta", True),  # Valid with prerelease
            ("1.0", False),  # Invalid - missing patch
            ("v1.0.0", False),  # Invalid - has 'v' prefix
            ("1.0.0.0", False),  # Invalid - too many parts
        ]

        for version, should_be_valid in test_cases:
            with self.subTest(version=version):
                test_operator = self.base_operator()
                test_operator["operator_version"] = version
                results = self.validate(test_operator)
                version_errors = errors_for(results, "operator_version")

                if should_be_valid:
                    self.assertEqual(len(version_errors), 0, f"Version {version} should be valid")
                else:
                    self.assertGreater(len(version_errors), 0, f"Version {version} should be invalid")

    def test_shell_config_validation(self):
        """Test shell configuration validation (enum error + plugin-count warning)"""
        test_operator = self.base_operator()
        test_operator["shell_config"] = {
            "preferred_shell": "invalid_shell",  # Not in enum
            "oh_my_zsh_plugins": ["git"] * 25,  # Too many plugins (warning)
        }

        results = self.validate(test_operator)
        # Specific enum error on preferred_shell
        shell_errors = errors_for(results, "shell_config.preferred_shell")
        self.assertEqual(len(shell_errors), 1, "invalid_shell should be an enum error")
        self.assertIn("not in allowed values", shell_errors[0].message)

        # Warning (not error) for too many plugins
        plugin_warnings = [r for r in warnings_of(results) if "plugins" in r.message.lower()]
        self.assertGreater(len(plugin_warnings), 0, "Should warn for too many plugins")

    def test_boolean_type_enforced(self):
        """A non-boolean tmux mouse setting is flagged on tmux_config.settings.mouse"""
        test_operator = self.base_operator()
        test_operator["tmux_config"] = {"settings": {"mouse": "yes"}}

        results = self.validate(test_operator)
        mouse_errors = errors_for(results, "tmux_config.settings.mouse")
        self.assertEqual(len(mouse_errors), 1, "mouse='yes' should be a boolean-type error")
        self.assertIn("must be a boolean", mouse_errors[0].message)

    def test_boolean_true_accepted(self):
        """A genuine boolean tmux mouse setting produces no error"""
        test_operator = self.base_operator()
        test_operator["tmux_config"] = {"settings": {"mouse": True}}

        results = self.validate(test_operator)
        self.assertEqual(len(errors_for(results, "tmux_config.settings.mouse")), 0)

    def test_integer_below_minimum_enforced(self):
        """An out-of-range (too low) integer setting is flagged on its field"""
        test_operator = self.base_operator()
        test_operator["tmux_config"] = {"settings": {"base_index": -1}}

        results = self.validate(test_operator)
        index_errors = errors_for(results, "tmux_config.settings.base_index")
        self.assertEqual(len(index_errors), 1, "base_index=-1 should be a minimum-bound error")
        self.assertIn("below minimum", index_errors[0].message)

    def test_integer_above_maximum_enforced(self):
        """An out-of-range (too high) integer setting is flagged on its field"""
        test_operator = self.base_operator()
        test_operator["tmux_config"] = {"settings": {"base_index": 999}}

        results = self.validate(test_operator)
        index_errors = errors_for(results, "tmux_config.settings.base_index")
        self.assertEqual(len(index_errors), 1, "base_index=999 should be a maximum-bound error")
        self.assertIn("above maximum", index_errors[0].message)

    def test_integer_in_range_accepted(self):
        """An in-range integer setting produces no error"""
        test_operator = self.base_operator()
        test_operator["tmux_config"] = {"settings": {"base_index": 1, "history_limit": 10000}}

        results = self.validate(test_operator)
        self.assertEqual(len(errors_matching(results, "tmux_config.settings")), 0)

    def test_operator_tags_are_free_form(self):
        """operator_tags is free-form (no enum): any string tags validate.

        Item-level enum enforcement is covered by test_nested_object_property_enum
        (networks[].driver) and test_tmux_config_validation (theme).
        """
        test_operator = self.base_operator()
        test_operator["operator_tags"] = ["development", "python", "go", "not_a_real_tag"]

        results = self.validate(test_operator)
        self.assertEqual(len(errors_matching(results, "operator_tags")), 0)

    def test_array_item_pattern_enforced(self):
        """A shell path element that violates the item pattern is flagged.

        Spaces and $(...) are allowed (real-world Windows / nvm paths); ';' is not.
        """
        test_operator = self.base_operator()
        test_operator["shell_config"]["paths"] = ["$HOME/bin", "/bad;path"]

        results = self.validate(test_operator)
        self.assertEqual(len(errors_for(results, "shell_config.paths[0]")), 0)
        path_errors = errors_for(results, "shell_config.paths[1]")
        self.assertEqual(len(path_errors), 1, "path with an illegal character should be an item-pattern error")
        self.assertIn("pattern", path_errors[0].message.lower())

    def test_nested_object_missing_required(self):
        """A docker network entry missing its required 'name' is flagged on that entry"""
        test_operator = self.base_operator()
        test_operator["docker_config"] = {"networks": [{"driver": "bridge"}]}

        results = self.validate(test_operator)
        network_errors = errors_for(results, "docker_config.networks[0]")
        self.assertEqual(len(network_errors), 1, "network missing 'name' should be a required-field error")
        self.assertIn("name", network_errors[0].message)

    def test_nested_object_property_enum(self):
        """A bad driver on a docker network entry is flagged on the nested property"""
        test_operator = self.base_operator()
        test_operator["docker_config"] = {"networks": [{"name": "valid_net", "driver": "not_a_driver"}]}

        results = self.validate(test_operator)
        driver_errors = errors_for(results, "docker_config.networks[0].driver")
        self.assertEqual(len(driver_errors), 1, "bad driver should be a nested-property enum error")
        self.assertIn("not in allowed values", driver_errors[0].message)

    def test_nested_object_property_pattern(self):
        """A bad network name is flagged on the nested name property via its pattern"""
        test_operator = self.base_operator()
        test_operator["docker_config"] = {"networks": [{"name": "Bad-Name"}]}

        results = self.validate(test_operator)
        name_errors = errors_for(results, "docker_config.networks[0].name")
        self.assertEqual(len(name_errors), 1, "bad network name should be a nested-property pattern error")
        self.assertIn("pattern", name_errors[0].message.lower())

    def test_nested_object_valid_network(self):
        """A well-formed docker network entry produces no error"""
        test_operator = self.base_operator()
        test_operator["docker_config"] = {"networks": [{"name": "matrix_net", "driver": "bridge"}]}

        results = self.validate(test_operator)
        self.assertEqual(len(errors_matching(results, "docker_config.networks")), 0)

    def test_tmux_config_validation(self):
        """Test tmux configuration validation reports each specific fault"""
        test_operator = self.base_operator()
        test_operator["tmux_config"] = {
            "theme": "invalid_theme",  # Not in enum
            "prefix": "Invalid",  # Doesn't match pattern
            "settings": {
                "mouse": "yes",  # Should be boolean
                "base_index": -1,  # Below minimum
            },
        }

        results = self.validate(test_operator)
        self.assertEqual(len(errors_for(results, "tmux_config.theme")), 1, "theme enum error")
        self.assertEqual(len(errors_for(results, "tmux_config.prefix")), 1, "prefix pattern error")
        self.assertEqual(len(errors_for(results, "tmux_config.settings.mouse")), 1, "mouse boolean error")
        self.assertEqual(len(errors_for(results, "tmux_config.settings.base_index")), 1, "base_index min error")

    def test_docker_config_validation(self):
        """Test docker configuration validation reports each specific fault"""
        test_operator = self.base_operator()
        test_operator["docker_config"] = {
            "install_compose": "yes",  # Should be boolean
            "compose_version": "v3",  # Not in enum
            "networks": [
                {
                    "name": "Invalid-Name",  # Doesn't match pattern
                    "driver": "invalid",  # Not in enum
                }
            ],
        }

        results = self.validate(test_operator)
        self.assertEqual(len(errors_for(results, "docker_config.install_compose")), 1, "install_compose bool error")
        self.assertEqual(len(errors_for(results, "docker_config.compose_version")), 1, "compose_version enum error")
        self.assertEqual(len(errors_for(results, "docker_config.networks[0].name")), 1, "network name pattern error")
        self.assertEqual(len(errors_for(results, "docker_config.networks[0].driver")), 1, "network driver enum error")

    def test_unknown_declared_type_errors(self):
        """A schema rule with an unrecognized type raises an error (does not pass silently)"""
        self.validator.results = []
        self.validator._validate_field("custom_field", "value", {"type": "strng"})
        type_errors = errors_for(self.validator.results, "custom_field")
        self.assertEqual(len(type_errors), 1, "unknown declared type should raise an error")
        self.assertIn("unknown type", type_errors[0].message.lower())

    def test_registered_tools_flag_unregistered(self):
        """additional_tools not present in the tool registry are flagged as errors"""
        test_operator = self.base_operator()
        test_operator["operator_name"] = "registry_probe"
        test_operator["tools_config"] = {"additional_tools": ["jq", "definitely_not_a_registered_tool"]}

        results = self.validate(test_operator)
        registry_errors = errors_for(results, "tools_config.additional_tools")
        self.assertEqual(len(registry_errors), 1, "only the unregistered tool should be flagged")
        self.assertIn("definitely_not_a_registered_tool", registry_errors[0].message)
        self.assertIn("not registered", registry_errors[0].message)

    def test_registered_tools_accept_known(self):
        """additional_tools that exist in the tool registry produce no error"""
        test_operator = self.base_operator()
        test_operator["operator_name"] = "registry_probe"
        test_operator["tools_config"] = {"additional_tools": ["jq", "htop", "ripgrep"]}

        results = self.validate(test_operator)
        self.assertEqual(len(errors_for(results, "tools_config.additional_tools")), 0)

    def test_inheritance_validation(self):
        """Test operator inheritance validation"""
        test_operator = self.base_operator()
        test_operator["extends"] = "base"  # valid enum member; parent does not exist on disk here

        results = self.validate(test_operator)
        inheritance_errors = errors_for(results, "extends")
        self.assertGreater(len(inheritance_errors), 0, "Should have inheritance validation error")

    def test_invalid_yaml_file(self):
        """Test validation of invalid YAML file"""
        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False)
        temp_file.write("invalid: yaml: content: [")  # Malformed YAML
        temp_file.close()

        try:
            results = self.validator.validate_operator(temp_file.name)
            file_errors = errors_for(results, "file")
            self.assertGreater(len(file_errors), 0, "Should have file parsing error")
        finally:
            os.unlink(temp_file.name)

    def test_validation_result_suggestions(self):
        """Test that validation results include helpful suggestions"""
        results = self.validate({"shell_config": {"preferred_shell": "zsh"}})
        results_with_suggestions = [r for r in errors_of(results) if r.suggestion is not None]
        self.assertGreater(len(results_with_suggestions), 0, "Should provide helpful suggestions")


class TestValidationIntegration(unittest.TestCase):
    """Integration tests for operator validation"""

    def setUp(self):
        """Set up test environment"""
        self.schema_path = Path(__file__).parent.parent / "schema" / "operator_schema.yml"
        self.validator = OperatorValidator(str(self.schema_path))
        self.operators_dir = Path(__file__).parent.parent / "operators"

    def test_existing_operators_valid(self):
        """Test that the core operators validate cleanly"""
        operators_to_test = ["base", "matrix", "jiveturkey"]

        for operator_name in operators_to_test:
            with self.subTest(operator=operator_name):
                operator_file = self.operators_dir / operator_name / "vars.yml"

                if operator_file.exists():
                    results = self.validator.validate_operator(str(operator_file))
                    error_results = errors_of(results)
                    self.assertEqual(
                        len(error_results),
                        0,
                        f"Operator {operator_name} should be valid. Errors: {[r.message for r in error_results]}",
                    )
                else:
                    self.fail(f"Operator file not found: {operator_file}")


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)
