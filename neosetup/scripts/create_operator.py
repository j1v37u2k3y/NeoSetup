#!/usr/bin/env python3
"""
NeoSetup Operator Generator

Creates new operators from templates with proper validation and structure.
Usage: python3 create_operator.py <operator_name> [--parent <parent_name>] [--interactive]
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

import yaml


class OperatorGenerator:
    """Generates new NeoSetup operators"""

    def __init__(self):
        """Initialize the generator"""
        self.script_dir = Path(__file__).parent
        self.neosetup_dir = self.script_dir.parent
        self.operators_dir = self.neosetup_dir / "operators"
        self.schema_path = self.neosetup_dir / "schema" / "operator_schema.yml"

        # Load schema for validation
        self.schema = self._load_schema()

        # Default templates
        self.templates = {
            "minimal": self._get_minimal_template(),
            "standard": self._get_standard_template(),
            "advanced": self._get_advanced_template(),
        }

    def _load_schema(self) -> Dict:
        """Load the operator schema"""
        try:
            with open(self.schema_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except (OSError, yaml.YAMLError) as e:
            print(f"Error loading schema: {e}")
            sys.exit(1)

    def _get_minimal_template(self) -> Dict:
        """Get minimal operator template"""
        return {
            "# Operator metadata": None,
            "operator_name": "",
            "operator_version": "1.0.0",
            "operator_description": "",
            "": None,
            "# Shell configuration": None,
            "shell_config": {
                "preferred_shell": "zsh",
                "oh_my_zsh_theme": "robbyrussell",
                "oh_my_zsh_plugins": ["git", "docker"],
                "aliases": {"ll": "ls -alF", "la": "ls -A", "gs": "git status"},
                "environment": {"EDITOR": "vim", "PAGER": "less"},
            },
        }

    def _get_standard_template(self) -> Dict:
        """Get standard operator template"""
        return {
            "# Operator metadata": None,
            "operator_name": "",
            "operator_version": "1.0.0",
            "operator_description": "",
            "": None,
            "# Shell configuration": None,
            "shell_config": {
                "preferred_shell": "zsh",
                "oh_my_zsh_theme": "robbyrussell",
                "oh_my_zsh_plugins": [
                    "git",
                    "docker",
                    "zsh-autosuggestions",
                    "zsh-syntax-highlighting",
                ],
                "aliases": {
                    "..": "cd ..",
                    "...": "cd ../..",
                    "ll": "ls -alF",
                    "la": "ls -A",
                    "gs": "git status",
                    "ga": "git add",
                    "gc": "git commit",
                    "gp": "git push",
                    "d": "docker",
                    "dc": "docker compose",
                },
                "environment": {
                    "EDITOR": "vim",
                    "PAGER": "less",
                    "LANG": "en_US.UTF-8",
                },
            },
            " ": None,
            "# Tmux configuration": None,
            "tmux_config": {
                "prefix": "C-a",
                "settings": {"base_index": 1, "history_limit": 10000, "mouse": True},
                "plugins": {"enabled": True, "sensible": True, "resurrect": True},
            },
            "  ": None,
            "# Tools configuration": None,
            "tools_config": {
                "essential_tools": [
                    {"name": "fd", "description": "Better find"},
                    {"name": "ripgrep", "description": "Better grep"},
                    {"name": "fzf", "description": "Fuzzy finder"},
                    {"name": "tree", "description": "Directory tree"},
                    {"name": "htop", "description": "Process viewer"},
                ]
            },
        }

    def _get_advanced_template(self) -> Dict:
        """Get advanced operator template with all sections"""
        return {
            "# Operator metadata": None,
            "operator_name": "",
            "operator_version": "1.0.0",
            "operator_description": "",
            "operator_author": "",
            "operator_tags": ["development"],
            "": None,
            "# Shell configuration": None,
            "shell_config": {
                "preferred_shell": "zsh",
                "framework": "oh-my-zsh",
                "oh_my_zsh_theme": "powerlevel10k/powerlevel10k",
                "oh_my_zsh_plugins": [
                    "git",
                    "docker",
                    "kubectl",
                    "zsh-autosuggestions",
                    "zsh-syntax-highlighting",
                    "colored-man-pages",
                ],
                "aliases": {
                    "..": "cd ..",
                    "...": "cd ../..",
                    "ll": "ls -alF",
                    "la": "ls -A",
                    "gs": "git status",
                    "ga": "git add",
                    "gc": "git commit",
                    "gp": "git push",
                    "gl": "git pull",
                    "gd": "git diff",
                    "d": "docker",
                    "dc": "docker compose",
                    "k": "kubectl",
                },
                "environment": {
                    "EDITOR": "vim",
                    "VISUAL": "vim",
                    "PAGER": "less",
                    "LANG": "en_US.UTF-8",
                    "HISTSIZE": "10000",
                },
                "paths": ["$HOME/.local/bin", "$HOME/bin"],
            },
            " ": None,
            "# Tmux configuration": None,
            "tmux_config": {
                "theme": "matrix",
                "prefix": "C-a",
                "terminal": "tmux-256color",
                "settings": {
                    "base_index": 1,
                    "pane_base_index": 1,
                    "history_limit": 50000,
                    "mouse": True,
                },
                "timing": {"escape_time": 0, "repeat_time": 600},
                "plugins": {
                    "enabled": True,
                    "sensible": True,
                    "resurrect": True,
                    "continuum": True,
                    "yank": True,
                },
                "status_bar": {"position": "bottom", "justify": "left", "interval": 5},
            },
            "  ": None,
            "# Tools configuration": None,
            "tools_config": {
                "essential_tools": [
                    {"name": "fd", "description": "Better find"},
                    {"name": "ripgrep", "description": "Better grep"},
                    {"name": "fzf", "description": "Fuzzy finder"},
                    {"name": "tree", "description": "Directory tree"},
                    {"name": "htop", "description": "Process viewer"},
                ],
                "modern_cli_tools": [
                    {"name": "eza", "description": "Better ls"},
                    {"name": "bat", "description": "Better cat"},
                    {"name": "delta", "description": "Better git diff"},
                ],
                "development_tools": [
                    {"name": "jq", "description": "JSON processor"},
                    {"name": "yq", "description": "YAML processor"},
                    {"name": "httpie", "description": "HTTP client"},
                ],
            },
            "   ": None,
            "# Docker configuration": None,
            "docker_config": {
                "install_compose": True,
                "compose_version": "v2",
                "install_buildx": True,
                "enable_buildkit": True,
                "security": {"userns_remap": False},
            },
        }

    def validate_operator_name(self, name: str) -> bool:
        """Validate operator name according to schema"""
        pattern = self.schema["operator_metadata"]["field_types"]["operator_name"]["pattern"]
        return bool(re.match(pattern, name))

    def check_operator_exists(self, name: str) -> bool:
        """Check if operator already exists"""
        return (self.operators_dir / name / "vars.yml").exists()

    def get_available_parents(self) -> List[str]:
        """Get list of available parent operators"""
        parents = []
        if not self.operators_dir.exists():
            return parents

        for operator_dir in self.operators_dir.iterdir():
            if operator_dir.is_dir() and (operator_dir / "vars.yml").exists():
                parents.append(operator_dir.name)
        return parents

    def create_operator_interactive(self) -> Dict:
        """Create operator configuration interactively"""
        print("🎯 Creating a new NeoSetup operator")
        print("=" * 40)

        # Get operator name
        while True:
            name = input("Operator name (lowercase, alphanumeric + underscore): ").strip()
            if not name:
                print("❌ Operator name is required")
                continue
            if not self.validate_operator_name(name):
                print("❌ Invalid name format. Use lowercase letters, numbers, and underscores only")
                continue
            if self.check_operator_exists(name):
                print(f"❌ Operator '{name}' already exists")
                continue
            break

        # Get version
        version = input("Version (default: 1.0.0): ").strip() or "1.0.0"

        # Get description
        while True:
            description = input("Description: ").strip()
            if description:
                break
            print("❌ Description is required")

        # Get author
        author = input("Author (optional): ").strip()

        # Get parent operator
        parents = self.get_available_parents()
        parent = None
        if parents:
            print(f"\\nAvailable parent operators: {', '.join(parents)}")
            parent_input = input("Parent operator (optional): ").strip()
            if parent_input and parent_input in parents:
                parent = parent_input
            elif parent_input:
                print(f"⚠️  Parent '{parent_input}' not found, creating standalone operator")

        # Get template type
        print("\\nChoose template:")
        print("1. Minimal - Basic shell configuration only")
        print("2. Standard - Shell + Tmux + Essential tools")
        print("3. Advanced - Full configuration with all sections")

        while True:
            choice = input("Template (1-3, default: 2): ").strip() or "2"
            if choice in ["1", "2", "3"]:
                break
            print("❌ Please choose 1, 2, or 3")

        template_map = {"1": "minimal", "2": "standard", "3": "advanced"}
        template_name = template_map[choice]

        # Get tags
        print(
            "\\nAvailable tags:",
            ", ".join(self.schema["operator_metadata"]["field_types"]["operator_tags"]["items"]["enum"]),
        )
        tags_input = input("Tags (comma-separated, optional): ").strip()
        tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else ["development"]

        return {
            "name": name,
            "version": version,
            "description": description,
            "author": author,
            "parent": parent,
            "template": template_name,
            "tags": tags,
        }

    def generate_operator_config(self, config: Dict) -> Dict:
        """Generate operator configuration from parameters"""
        # Start with template
        operator_config = self.templates[config["template"]].copy()

        # Remove comment keys (they're just for readability in templates)
        operator_config = {k: v for k, v in operator_config.items() if not k.startswith("#") and k.strip()}

        # Set metadata
        operator_config["operator_name"] = config["name"]
        operator_config["operator_version"] = config["version"]
        operator_config["operator_description"] = config["description"]

        if config.get("author"):
            operator_config["operator_author"] = config["author"]

        if config.get("parent"):
            operator_config["extends"] = config["parent"]

        if config.get("tags"):
            operator_config["operator_tags"] = config["tags"]

        return operator_config

    def create_operator_directory(self, name: str, config: Dict) -> Path:
        """Create operator directory structure"""
        operator_dir = self.operators_dir / name
        operator_dir.mkdir(parents=True, exist_ok=True)

        # Create vars.yml
        vars_file = operator_dir / "vars.yml"

        # Create YAML content with proper formatting
        yaml_content = self._format_yaml_with_comments(config)

        with open(vars_file, "w", encoding="utf-8") as f:
            f.write(yaml_content)

        # Create README.md
        readme_content = f"""# {config['operator_name'].title()} Operator

{config['operator_description']}

## Version
{config['operator_version']}

## Usage

```bash
cd neosetup
make install OPERATOR={config['operator_name']}
```

## Configuration

This operator includes:

- **Shell Configuration**: {"Custom shell setup" if 'shell_config' in config else "Inherits from parent"}
- **Tmux Configuration**: {"Custom tmux setup" if 'tmux_config' in config else "Inherits from parent"}
- **Tools**: {"Custom tool selection" if 'tools_config' in config else "Inherits from parent"}
- **Docker**: {"Custom Docker configuration" if 'docker_config' in config else "Inherits from parent"}

## Customization

Edit `vars.yml` to customize this operator's behavior.

## Validation

Validate this operator configuration:

```bash
cd neosetup
python3 scripts/validate_operator.py {config['operator_name']}
```
"""

        readme_file = operator_dir / "README.md"
        with open(readme_file, "w", encoding="utf-8") as f:
            f.write(readme_content)

        return operator_dir

    def _format_yaml_with_comments(self, config: Dict) -> str:
        """Format YAML with proper comments and structure"""
        # Use YAML dump with proper formatting
        yaml_str = yaml.dump(config, default_flow_style=False, sort_keys=False, width=120)

        # Add header comments
        lines = []
        lines.append("---")
        lines.append(f"# {config['operator_name'].title()} Operator Configuration")

        if config.get("extends"):
            lines.append(f"# Extends: {config['extends']}")

        lines.append("")

        # Add the YAML content
        lines.append(yaml_str.rstrip())

        return "\n".join(lines) + "\n"

    def create_operator(
        self,
        name: str,
        parent: Optional[str] = None,
        template: str = "standard",
        interactive: bool = False,
        **kwargs,
    ) -> Path:
        """Create a new operator"""
        if interactive:
            config = self.create_operator_interactive()
        else:
            # Validate inputs
            if not self.validate_operator_name(name):
                raise ValueError(f"Invalid operator name: {name}")

            if self.check_operator_exists(name):
                raise ValueError(f"Operator already exists: {name}")

            if parent and parent not in self.get_available_parents():
                raise ValueError(f"Parent operator not found: {parent}")

            if template not in self.templates:
                raise ValueError(f"Invalid template: {template}")

            config = {
                "name": name,
                "version": kwargs.get("version", "1.0.0"),
                "description": kwargs.get("description", f"{name.title()} operator configuration"),
                "author": kwargs.get("author"),
                "parent": parent,
                "template": template,
                "tags": kwargs.get("tags", ["development"]),
            }

        # Generate configuration
        operator_config = self.generate_operator_config(config)

        # Create operator directory
        operator_dir = self.create_operator_directory(config["name"], operator_config)

        return operator_dir

    def list_templates(self):
        """List available templates"""
        print("Available templates:")
        for name, template in self.templates.items():
            sections = [k for k in template if k.endswith("_config")]
            print(f"  {name}: {', '.join(sections)}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Create new NeoSetup operator")
    parser.add_argument("name", nargs="?", help="Operator name")
    parser.add_argument("--parent", help="Parent operator to extend")
    parser.add_argument(
        "--template",
        choices=["minimal", "standard", "advanced"],
        default="standard",
        help="Template type",
    )
    parser.add_argument("--version", default="1.0.0", help="Operator version")
    parser.add_argument("--description", help="Operator description")
    parser.add_argument("--author", help="Operator author")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--list-templates", action="store_true", help="List available templates")
    parser.add_argument("--list-parents", action="store_true", help="List available parent operators")

    args = parser.parse_args()

    generator = OperatorGenerator()

    if args.list_templates:
        generator.list_templates()
        return

    if args.list_parents:
        parents = generator.get_available_parents()
        if parents:
            print("Available parent operators:")
            for parent in parents:
                print(f"  {parent}")
        else:
            print("No parent operators found")
        return

    if not args.name and not args.interactive:
        parser.print_help()
        return

    try:
        # Parse tags
        tags = []
        if args.tags:
            tags = [tag.strip() for tag in args.tags.split(",")]

        # Create operator
        operator_dir = generator.create_operator(
            name=args.name,
            parent=args.parent,
            template=args.template,
            interactive=args.interactive,
            version=args.version,
            description=args.description,
            author=args.author,
            tags=tags,
        )

        print("\\n✅ Operator created successfully!")
        print(f"📁 Location: {operator_dir}")
        print(f"\\n🔍 Validate with: python3 scripts/validate_operator.py {operator_dir.name}")
        print(f"🚀 Install with: make install OPERATOR={operator_dir.name}")

    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except (OSError, yaml.YAMLError) as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
