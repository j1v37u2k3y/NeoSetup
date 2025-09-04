#!/usr/bin/env python3
"""
Test suite for operator validation system
Tests various validation scenarios and error conditions
"""
# pylint: disable=wrong-import-position,wrong-import-order,consider-using-with,import-error
# Test files need flexible imports and file handling

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

    def create_temp_operator(self, operator_data):
        """Create a temporary operator file for testing"""
        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False)
        yaml.dump(operator_data, temp_file)
        temp_file.close()
        return temp_file.name

    def test_valid_operator(self):
        """Test validation of a valid operator"""
        temp_file = self.create_temp_operator(self.valid_operator)
        try:
            results = self.validator.validate_operator(temp_file)
            self.assertEqual(len(results), 0, "Valid operator should have no validation errors")
        finally:
            os.unlink(temp_file)

    def test_missing_required_fields(self):
        """Test validation with missing required fields"""
        invalid_operator = {"shell_config": {"preferred_shell": "zsh"}}
        temp_file = self.create_temp_operator(invalid_operator)
        try:
            results = self.validator.validate_operator(temp_file)
            error_results = [r for r in results if r.level == ValidationLevel.ERROR]
            self.assertGreater(
                len(error_results),
                0,
                "Should have validation errors for missing required fields",
            )

            # Check that all required fields are reported as missing
            missing_fields = [r.field for r in error_results]
            self.assertIn("operator_name", missing_fields)
            self.assertIn("operator_version", missing_fields)
            self.assertIn("operator_description", missing_fields)
        finally:
            os.unlink(temp_file)

    def test_invalid_field_types(self):
        """Test validation with invalid field types"""
        invalid_operator = self.valid_operator.copy()
        invalid_operator["operator_name"] = 123  # Should be string
        invalid_operator["oh_my_zsh_plugins"] = "not-an-array"  # Should be array

        temp_file = self.create_temp_operator(invalid_operator)
        try:
            results = self.validator.validate_operator(temp_file)
            error_results = [r for r in results if r.level == ValidationLevel.ERROR]
            self.assertGreater(
                len(error_results),
                0,
                "Should have validation errors for invalid field types",
            )
        finally:
            os.unlink(temp_file)

    def test_pattern_validation(self):
        """Test pattern validation for operator name"""
        invalid_operator = self.valid_operator.copy()
        invalid_operator["operator_name"] = "Invalid-Name!"  # Doesn't match pattern

        temp_file = self.create_temp_operator(invalid_operator)
        try:
            results = self.validator.validate_operator(temp_file)
            error_results = [r for r in results if r.level == ValidationLevel.ERROR]
            pattern_errors = [r for r in error_results if "pattern" in r.message.lower()]
            self.assertGreater(len(pattern_errors), 0, "Should have pattern validation error")
        finally:
            os.unlink(temp_file)

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
                test_operator = self.valid_operator.copy()
                test_operator["operator_version"] = version

                temp_file = self.create_temp_operator(test_operator)
                try:
                    results = self.validator.validate_operator(temp_file)
                    error_results = [r for r in results if r.level == ValidationLevel.ERROR]
                    version_errors = [r for r in error_results if r.field == "operator_version"]

                    if should_be_valid:
                        self.assertEqual(len(version_errors), 0, f"Version {version} should be valid")
                    else:
                        self.assertGreater(
                            len(version_errors),
                            0,
                            f"Version {version} should be invalid",
                        )
                finally:
                    os.unlink(temp_file)

    def test_shell_config_validation(self):
        """Test shell configuration validation"""
        test_operator = self.valid_operator.copy()
        test_operator["shell_config"] = {
            "preferred_shell": "invalid_shell",  # Not in enum
            "oh_my_zsh_plugins": ["git"] * 25,  # Too many plugins (warning)
        }

        temp_file = self.create_temp_operator(test_operator)
        try:
            results = self.validator.validate_operator(temp_file)
            error_results = [r for r in results if r.level == ValidationLevel.ERROR]
            warning_results = [r for r in results if r.level == ValidationLevel.WARNING]

            # Should have error for invalid shell
            shell_errors = [r for r in error_results if "shell_config.preferred_shell" in r.field]
            self.assertGreater(len(shell_errors), 0, "Should have error for invalid shell")

            # Should have warning for too many plugins
            plugin_warnings = [r for r in warning_results if "plugins" in r.message.lower()]
            self.assertGreater(len(plugin_warnings), 0, "Should have warning for too many plugins")
        finally:
            os.unlink(temp_file)

    def test_tmux_config_validation(self):
        """Test tmux configuration validation"""
        test_operator = self.valid_operator.copy()
        test_operator["tmux_config"] = {
            "theme": "invalid_theme",  # Not in enum
            "prefix": "Invalid",  # Doesn't match pattern
            "settings": {
                "mouse": "yes",  # Should be boolean
                "base_index": -1,  # Below minimum
            },
        }

        temp_file = self.create_temp_operator(test_operator)
        try:
            results = self.validator.validate_operator(temp_file)
            error_results = [r for r in results if r.level == ValidationLevel.ERROR]

            # Check for various tmux validation errors
            self.assertGreater(len(error_results), 0, "Should have tmux validation errors")

            # Check specific field errors
            field_errors = [r.field for r in error_results]
            self.assertTrue(any("tmux_config" in field for field in field_errors))
        finally:
            os.unlink(temp_file)

    def test_inheritance_validation(self):
        """Test operator inheritance validation"""
        test_operator = self.valid_operator.copy()
        test_operator["extends"] = "nonexistent_operator"

        temp_file = self.create_temp_operator(test_operator)
        try:
            results = self.validator.validate_operator(temp_file)
            error_results = [r for r in results if r.level == ValidationLevel.ERROR]
            inheritance_errors = [r for r in error_results if r.field == "extends"]

            self.assertGreater(len(inheritance_errors), 0, "Should have inheritance validation error")
        finally:
            os.unlink(temp_file)

    def test_docker_config_validation(self):
        """Test docker configuration validation"""
        test_operator = self.valid_operator.copy()
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

        temp_file = self.create_temp_operator(test_operator)
        try:
            results = self.validator.validate_operator(temp_file)
            error_results = [r for r in results if r.level == ValidationLevel.ERROR]

            # Should have multiple docker config errors
            docker_errors = [r for r in error_results if "docker_config" in r.field]
            self.assertGreater(len(docker_errors), 0, "Should have docker validation errors")
        finally:
            os.unlink(temp_file)

    def test_invalid_yaml_file(self):
        """Test validation of invalid YAML file"""
        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False)
        temp_file.write("invalid: yaml: content: [")  # Malformed YAML
        temp_file.close()

        try:
            results = self.validator.validate_operator(temp_file.name)
            error_results = [r for r in results if r.level == ValidationLevel.ERROR]
            file_errors = [r for r in error_results if r.field == "file"]

            self.assertGreater(len(file_errors), 0, "Should have file parsing error")
        finally:
            os.unlink(temp_file.name)

    def test_validation_result_suggestions(self):
        """Test that validation results include helpful suggestions"""
        invalid_operator = {"shell_config": {"preferred_shell": "zsh"}}
        temp_file = self.create_temp_operator(invalid_operator)

        try:
            results = self.validator.validate_operator(temp_file)
            error_results = [r for r in results if r.level == ValidationLevel.ERROR]

            # Check that suggestions are provided
            results_with_suggestions = [r for r in error_results if r.suggestion is not None]
            self.assertGreater(len(results_with_suggestions), 0, "Should provide helpful suggestions")
        finally:
            os.unlink(temp_file)


class TestValidationIntegration(unittest.TestCase):
    """Integration tests for operator validation"""

    def setUp(self):
        """Set up test environment"""
        self.schema_path = Path(__file__).parent.parent / "schema" / "operator_schema.yml"
        self.validator = OperatorValidator(str(self.schema_path))
        self.operators_dir = Path(__file__).parent.parent / "operators"

    def test_existing_operators_valid(self):
        """Test that all existing operators are valid"""
        operators_to_test = ["base", "matrix", "jiveturkey"]

        for operator_name in operators_to_test:
            with self.subTest(operator=operator_name):
                operator_file = self.operators_dir / operator_name / "vars.yml"

                if operator_file.exists():
                    results = self.validator.validate_operator(str(operator_file))
                    error_results = [r for r in results if r.level == ValidationLevel.ERROR]

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
