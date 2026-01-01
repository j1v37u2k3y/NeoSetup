#!/bin/bash
# Run pre-commit checks in Docker container
# Usage: ./scripts/run-precommit.sh [pre-commit args]
#
# Examples:
#   ./scripts/run-precommit.sh                    # Run on all files
#   ./scripts/run-precommit.sh run --all-files    # Same as above
#   ./scripts/run-precommit.sh run                # Run on staged files only
#   ./scripts/run-precommit.sh run yamllint       # Run specific hook

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
IMAGE_NAME="neosetup-precommit"

cd "$PROJECT_DIR"

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in PATH"
    exit 1
fi

# Build the image if it doesn't exist or if Dockerfile changed
if [[ ! "$(docker images -q $IMAGE_NAME 2>/dev/null)" ]] || \
   [[ "Dockerfile.precommit" -nt "$(docker inspect -f '{{.Created}}' $IMAGE_NAME 2>/dev/null || echo '1970-01-01')" ]]; then
    echo "Building pre-commit Docker image..."
    docker build -f Dockerfile.precommit -t "$IMAGE_NAME" .
fi

echo "Running pre-commit in Docker..."
echo "================================"

# Run pre-commit in container
# Mount the project directory and preserve git state
docker run --rm \
    -v "$PROJECT_DIR:/workspace" \
    -v "$PROJECT_DIR/.git:/workspace/.git" \
    -w /workspace \
    "$IMAGE_NAME" \
    "$@"

echo ""
echo "Pre-commit checks complete!"
