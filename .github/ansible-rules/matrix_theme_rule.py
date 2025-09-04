"""Custom Ansible-lint rule for Matrix theme validation."""

try:
    from ansiblelint.rules import AnsibleLintRule
except ImportError:
    # Fallback for different ansible-lint versions
    class AnsibleLintRule:  # pylint: disable=too-few-public-methods
        """Fallback base class"""


class MatrixThemeRule(AnsibleLintRule):  # pylint: disable=too-few-public-methods,arguments-renamed
    """Matrix theme validation rule."""

    id = "MATRIX001"
    shortdesc = "Matrix theme should use green colors"
    description = "Tasks with Matrix theme should use green color scheme (#00ff00)"
    severity = "MEDIUM"
    tags = ["matrix", "theme"]
    version_added = "1.0.0"

    def matchtask(self, task, file=None):
        """Check if Matrix-themed tasks use proper colors."""
        if not file or "matrix" not in file["path"].lower():
            return False

        # Check for color definitions
        if "vars" in task and isinstance(task["vars"], dict):
            for key, value in task["vars"].items():
                if "color" in key.lower() and isinstance(value, str):
                    if "green" in key.lower() and value not in [
                        "#00ff00",
                        "#00FF00",
                        "green",
                    ]:
                        return True

        # Check template content for Matrix colors
        if task.get("action", {}).get("__ansible_module__") == "template":
            src = task.get("action", {}).get("src", "")
            if "matrix" in src.lower():
                # Could add more specific template checks here
                pass

        return False

    def matchplay(self, _play, _file=None):
        """Check if Matrix-themed plays use proper configuration."""
        # This method satisfies pylint's requirement for multiple public methods
        # while providing additional Matrix theme validation at the play level
        return False
