#!/bin/bash
# Install git hooks that run pre-commit in Docker
# Usage: ./scripts/install-git-hooks.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
HOOKS_DIR="$PROJECT_DIR/.git/hooks"

echo "Installing Docker-based git hooks..."

# Create pre-commit hook
cat > "$HOOKS_DIR/pre-commit" << 'HOOK'
#!/bin/bash
# Pre-commit hook that runs pre-commit checks in Docker
# Installed by: ./scripts/install-git-hooks.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
IMAGE_NAME="neosetup-precommit"

cd "$PROJECT_DIR"

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker not found, falling back to local pre-commit..."
    exec pre-commit run --hook-stage pre-commit
fi

# Build image if needed (silently)
if [[ ! "$(docker images -q $IMAGE_NAME 2>/dev/null)" ]]; then
    echo "Building pre-commit Docker image (first time only)..."
    docker build -f Dockerfile.precommit -t "$IMAGE_NAME" . >/dev/null 2>&1
fi

# Run pre-commit in Docker on staged files
docker run --rm \
    -v "$PROJECT_DIR:/workspace" \
    -v "$PROJECT_DIR/.git:/workspace/.git" \
    -w /workspace \
    "$IMAGE_NAME" \
    run --hook-stage pre-commit
HOOK

chmod +x "$HOOKS_DIR/pre-commit"

echo "✅ Git pre-commit hook installed!"
echo ""
echo "Now when you run 'git commit', pre-commit will run inside Docker."
echo "To run manually: ./scripts/run-precommit.sh run --all-files"
