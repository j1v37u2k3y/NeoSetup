# 🎭 NeoSetup Ansible Edition Makefile
# Welcome to the Matrix - convenient commands for the development environment

.PHONY: help install shell tmux tools docker test lint clean deps

# Default operator
OPERATOR ?= jiveturkey
INVENTORY ?= inventories/local/hosts.yml
PLAYBOOK_DIR = playbooks
ANSIBLE_FLAGS ?= -v

# Help target - shows available commands
help:
	@echo "🎭 NeoSetup Ansible Edition - The Matrix has you..."
	@echo ""
	@echo "Available commands:"
	@echo "  make install OPERATOR=jiveturkey  - Full installation with operator"
	@echo "  make shell OPERATOR=matrix        - Configure shell only"
	@echo "  make tmux OPERATOR=base          - Configure tmux only"
	@echo "  make tools                       - Install CLI tools"
	@echo "  make docker                      - Install Docker"
	@echo "  make test-docker                 - Test Docker installation"
	@echo "  make test                        - Run molecule tests"
	@echo "  make lint                        - Run ansible-lint"
	@echo "  make dry-run                     - Show what would change"
	@echo "  make deps                        - Install dependencies"
	@echo "  make dev-setup                   - Setup development environment"
	@echo "  make precommit                   - Run pre-commit in Docker"
	@echo "  make precommit-staged            - Run pre-commit on staged files"
	@echo "  make clean                       - Clean cache files"
	@echo ""
	@echo "Operators: base, matrix, jiveturkey"
	@echo "Example: make install OPERATOR=matrix"

# Full installation with selected operator
install: deps
	@echo "🚀 Installing NeoSetup with $(OPERATOR) operator..."
	ansible-playbook -i $(INVENTORY) $(PLAYBOOK_DIR)/site.yml \
		-e "neosetup_operator=$(OPERATOR)" --ask-become-pass $(ANSIBLE_FLAGS)

# Configure shell only
shell: deps
	@echo "🐚 Configuring shell with $(OPERATOR) operator..."
	ansible-playbook -i $(INVENTORY) $(PLAYBOOK_DIR)/site.yml \
		-e "neosetup_operator=$(OPERATOR)" \
		--tags "shell" --become --ask-become-pass $(ANSIBLE_FLAGS)

# Configure tmux only
tmux: deps
	@echo "🖥️ Configuring tmux with $(OPERATOR) operator..."
	ansible-playbook -i $(INVENTORY) $(PLAYBOOK_DIR)/site.yml \
		-e "neosetup_operator=$(OPERATOR)" \
		--tags "tmux" --ask-become-pass $(ANSIBLE_FLAGS)

# Install tools only
tools: deps
	@echo "🔧 Installing tools with $(OPERATOR) operator..."
	ansible-playbook -i $(INVENTORY) $(PLAYBOOK_DIR)/site.yml \
		-e "neosetup_operator=$(OPERATOR)" \
		--tags "tools" --ask-become-pass $(ANSIBLE_FLAGS)

# Install Docker
docker: deps
	@echo "🐳 Installing Docker..."
	ansible-playbook -i $(INVENTORY) $(PLAYBOOK_DIR)/site.yml \
		--tags "docker" --ask-become-pass $(ANSIBLE_FLAGS)

# Dry run - show what would change
dry-run: deps
	@echo "🔍 Dry run - showing what would change with $(OPERATOR) operator..."
	ansible-playbook -i $(INVENTORY) $(PLAYBOOK_DIR)/site.yml \
		-e "neosetup_operator=$(OPERATOR)" \
		--check --diff $(ANSIBLE_FLAGS)

# Test Docker installation
test-docker: deps
	@echo "🐳 Testing Docker installation..."
	ansible-playbook -i $(INVENTORY) test-docker.yml $(ANSIBLE_FLAGS)

# Install Ansible dependencies
deps:
	@echo "📦 Installing Ansible dependencies..."
	@if command -v ansible-galaxy >/dev/null 2>&1; then \
		ansible-galaxy install -r requirements.yml --force; \
	else \
		echo "❌ ansible-galaxy not found. Please install Ansible first:"; \
		echo "   sudo apt install ansible  # Debian/Ubuntu/Kali"; \
		echo "   pip3 install ansible     # Via Python pip"; \
		exit 1; \
	fi

# Skip dependencies (for troubleshooting)
no-deps:
	@echo "⚠️ Skipping dependency installation"

# Direct Ansible commands (bypass deps)
ansible-dry-run:
	@echo "🔍 Direct Ansible dry run (no deps)..."
	ansible-playbook -i $(INVENTORY) $(PLAYBOOK_DIR)/site.yml \
		-e "neosetup_operator=$(OPERATOR)" --check --diff $(ANSIBLE_FLAGS)

ansible-install:
	@echo "🚀 Direct Ansible install (no deps)..."
	ansible-playbook -i $(INVENTORY) $(PLAYBOOK_DIR)/site.yml \
		-e "neosetup_operator=$(OPERATOR)" --ask-become-pass $(ANSIBLE_FLAGS)

ansible-shell:
	@echo "🐚 Direct Ansible shell config (no deps)..."
	ansible-playbook -i $(INVENTORY) $(PLAYBOOK_DIR)/site.yml \
		-e "neosetup_operator=$(OPERATOR)" --tags "shell" $(ANSIBLE_FLAGS)

# Run tests with molecule
test:
	@echo "🧪 Running molecule tests..."
	molecule test

# Lint playbooks and roles
lint:
	@echo "🔍 Linting Ansible code..."
	ansible-lint $(PLAYBOOK_DIR)/*.yml
	yamllint .

# Run pre-commit checks in Docker (consistent environment)
precommit:
	@echo "🐳 Running pre-commit in Docker..."
	../scripts/run-precommit.sh run --all-files

# Run pre-commit on staged files only
precommit-staged:
	@echo "🐳 Running pre-commit on staged files..."
	../scripts/run-precommit.sh run

# Build pre-commit Docker image
precommit-build:
	@echo "🐳 Building pre-commit Docker image..."
	cd .. && docker build -f Dockerfile.precommit -t neosetup-precommit .

# Clean cache and temp files
clean:
	@echo "🧹 Cleaning cache files..."
	find . -name "*.retry" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete

# Quick status check
status:
	@echo "📊 NeoSetup Ansible Status:"
	@echo "  Inventory: $(INVENTORY)"
	@echo "  Default Operator: $(OPERATOR)"
	@echo "  Ansible Version: $$(ansible --version | head -n1)"
	@echo "  Python Version: $$(python3 --version)"

# Development commands
dev-setup: deps
	@echo "🛠️ Setting up development environment..."
	@echo "📦 Creating virtual environment..."
	python3 -m venv ../.venv
	@echo "📦 Installing dependencies in .venv..."
	../.venv/bin/pip install --upgrade pip
	../.venv/bin/pip install -r requirements-runtime.txt
	../.venv/bin/pip install -r ../requirements.txt
	ansible-galaxy install -r requirements.yml
	@echo "🪝 Installing Docker-based pre-commit hooks..."
	git config core.hooksPath ../.githooks
	@echo ""
	@echo "✅ Development environment ready!"
	@echo "   Activate venv: source ../.venv/bin/activate"
	@echo "   Run pre-commit: ./scripts/run-precommit.sh run --all-files"

# Show operator information
operator-info:
	@echo "🎭 Available Operators:"
	@grep -A5 "operators:" group_vars/all/operators.yml | tail -n +2
