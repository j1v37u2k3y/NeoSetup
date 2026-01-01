#!/usr/bin/env python3
"""
Generate Dockerfile for NeoSetup testing containers.
"""
# pylint: disable=duplicate-code  # Test utilities share common patterns

import sys
import argparse
from pathlib import Path


def generate_dockerfile(os_name: str, _ansible_version: str) -> str:
    """Generate Dockerfile content for the specified OS."""

    # OS to Docker image mapping
    images = {
        "ubuntu-22.04": "ubuntu:22.04",
        "ubuntu-24.04": "ubuntu:24.04",
        "debian-12": "debian:12",
        "kali-rolling": "kalilinux/kali-rolling",
        "parrot-security": "parrotsec/security",
        "centos-stream-9": "quay.io/centos/centos:stream9",
        "rocky-9": "rockylinux:9",
        "almalinux-9": "almalinux:9",
        "fedora-40": "fedora:40",
    }

    base_image = images.get(os_name, os_name)

    # Use template substitution instead of f-strings to avoid false security warnings
    dockerfile_template = """# Test container for {os_name}
FROM {base_image}

# Install base packages including python3-venv
RUN if [ -f /etc/debian_version ]; then \\
  apt-get update && \\
  apt-get install -y python3 python3-pip python3-venv sudo curl wget git openssh-client && \\
  apt-get clean; \\
elif [ -f /etc/redhat-release ]; then \\
  if command -v dnf; then \\
    dnf install -y --allowerasing python3 python3-pip sudo curl wget git tar gzip openssh-clients || \\
    (dnf install -y --allowerasing python3 sudo curl wget git tar gzip openssh-clients && \\
     curl -sS https://bootstrap.pypa.io/get-pip.py | python3); \\
  else \\
    yum install -y epel-release && \\
    yum install -y python3 python3-pip sudo curl wget git tar gzip openssh-clients \\
      gcc python3-devel libffi-devel openssl-devel rust cargo || \\
    (yum install -y python3 sudo curl wget git tar gzip openssh-clients && \\
     curl -sS https://bootstrap.pypa.io/get-pip.py | python3); \\
  fi; \\
fi

# Create test user
RUN useradd -m -s /bin/bash testuser && \\
    echo 'testuser ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Copy requirements files
COPY neosetup/requirements-runtime.txt /tmp/requirements-runtime.txt
COPY neosetup/requirements.yml /tmp/requirements.yml

# Create virtual environment and install from requirements
RUN python3 -m venv /opt/ansible-venv
RUN /opt/ansible-venv/bin/pip install --upgrade pip
RUN /opt/ansible-venv/bin/pip install -r /tmp/requirements-runtime.txt

# Install Ansible Galaxy collections and roles
RUN /opt/ansible-venv/bin/ansible-galaxy install -r /tmp/requirements.yml

# Add venv to PATH for all users (bashrc location differs between distros)
RUN if [ -f /etc/bash.bashrc ]; then \\
      echo 'export PATH="/opt/ansible-venv/bin:$PATH"' >> /etc/bash.bashrc; \\
    elif [ -f /etc/bashrc ]; then \\
      echo 'export PATH="/opt/ansible-venv/bin:$PATH"' >> /etc/bashrc; \\
    fi
RUN echo 'export PATH="/opt/ansible-venv/bin:$PATH"' >> /etc/profile

# Verify installation
RUN /opt/ansible-venv/bin/ansible --version && \\
    /opt/ansible-venv/bin/python3 -c "import yaml; print('PyYAML available')"

# Set working directory
WORKDIR /neosetup

USER testuser
"""

    return dockerfile_template.format(os_name=os_name, base_image=base_image)


def main():
    """Main function to generate Dockerfile for NeoSetup testing."""
    parser = argparse.ArgumentParser(description="Generate Dockerfile for NeoSetup testing")
    parser.add_argument("--os-name", required=True, help="Operating system name (e.g., ubuntu-22.04)")
    parser.add_argument("--ansible-version", default=">=4.0", help="Ansible version constraint")
    parser.add_argument("--output", "-o", help="Output file path (default: Dockerfile.{os_name})")

    args = parser.parse_args()

    if not args.output:
        args.output = f"Dockerfile.{args.os_name}"

    dockerfile_content = generate_dockerfile(args.os_name, args.ansible_version)

    # Write to file
    output_path = Path(args.output)
    output_path.write_text(dockerfile_content, encoding="utf-8")

    print(f"Generated Dockerfile: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
