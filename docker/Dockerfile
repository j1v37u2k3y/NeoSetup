# Parameterized test container for NeoSetup's multi-distro verification matrix.
# One Dockerfile serves all nine distros via build-args, instead of nine
# near-identical siblings that drifted every time the install line changed.
#
# Build args:
#   BASE_IMAGE — e.g. ubuntu:24.04, debian:12, fedora:40, kalilinux/kali-rolling.
#   PKG_MGR    — apt | dnf. Selects the base-package install block.
#   USE_UV     — 0 | 1. When 1, bootstrap uv-managed CPython 3.12 for the
#                Ansible venv (needed on distros whose system python3 is older
#                than ansible >=14.2's floor: ubuntu-22.04, debian-12, and the
#                centos/rocky/almalinux 9 family). When 0, use the base image's
#                python3 directly (ubuntu-24.04, kali, parrot, fedora-40).

ARG BASE_IMAGE=debian:12
FROM ${BASE_IMAGE}

ARG PKG_MGR=apt
ARG USE_UV=0

# Install base packages. Debian family uses apt + python3-venv; RHEL family
# uses dnf (openssh-clients, not openssh-client).
RUN if [ "$PKG_MGR" = "apt" ]; then \
      apt-get update && \
      apt-get install -y --no-install-recommends python3 python3-pip python3-venv sudo curl wget git openssh-client && \
      apt-get clean && \
      rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*; \
    elif [ "$PKG_MGR" = "dnf" ]; then \
      dnf install -y --allowerasing python3 python3-pip sudo curl wget git tar gzip openssh-clients && \
      dnf clean all && \
      rm -rf /var/cache/dnf/*; \
    else \
      echo "Unsupported PKG_MGR: $PKG_MGR" >&2; exit 1; \
    fi

# Create test user
RUN useradd -m -s /bin/bash testuser && \
    echo 'testuser ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Copy requirements files
COPY neosetup/requirements-runtime.txt /tmp/requirements-runtime.txt
COPY neosetup/requirements.yml /tmp/requirements.yml

# Set up the Ansible venv.
# USE_UV=1: ansible >=14.2 needs Python >=3.12, which the older base distros
# ship older. uv provides a standalone CPython 3.12 uniformly across distros
# (test harness only). Store uv's managed CPython under /opt (world-readable)
# instead of the default /root, so the venv interpreter stays usable after we
# drop to testuser below.
ENV UV_PYTHON_INSTALL_DIR=/opt/uv-python
# venv first on PATH so python3/ansible/ansible-playbook resolve to it (has
# PyYAML + ansible) for the non-login `docker run ... python3 ...` test
# invocation.
ENV PATH="/opt/ansible-venv/bin:/root/.local/bin:${PATH}"
RUN if [ "$USE_UV" = "1" ]; then \
      curl -LsSf https://astral.sh/uv/install.sh | sh && \
      uv python install 3.12 && \
      uv venv --python 3.12 --seed /opt/ansible-venv && \
      /opt/ansible-venv/bin/pip install --no-cache-dir --upgrade pip && \
      /opt/ansible-venv/bin/pip install --no-cache-dir -r /tmp/requirements-runtime.txt && \
      rm -rf /root/.cache && \
      chmod -R a+rX /opt/uv-python /opt/ansible-venv; \
    else \
      python3 -m venv /opt/ansible-venv && \
      /opt/ansible-venv/bin/pip install --no-cache-dir --upgrade pip && \
      /opt/ansible-venv/bin/pip install --no-cache-dir -r /tmp/requirements-runtime.txt && \
      rm -rf /root/.cache/pip; \
    fi

# Install Ansible Galaxy collections and roles
RUN /opt/ansible-venv/bin/ansible-galaxy install -r /tmp/requirements.yml && \
    rm -f /tmp/requirements-runtime.txt /tmp/requirements.yml

# Add venv to PATH for all users (bashrc location differs between distros)
RUN if [ -f /etc/bash.bashrc ]; then \
      echo 'export PATH="/opt/ansible-venv/bin:$PATH"' >> /etc/bash.bashrc; \
    elif [ -f /etc/bashrc ]; then \
      echo 'export PATH="/opt/ansible-venv/bin:$PATH"' >> /etc/bashrc; \
    fi
RUN echo 'export PATH="/opt/ansible-venv/bin:$PATH"' >> /etc/profile

# Verify installation
RUN /opt/ansible-venv/bin/ansible --version && \
    /opt/ansible-venv/bin/python3 -c "import yaml; print('PyYAML available')"

# Set working directory
WORKDIR /neosetup

USER testuser
