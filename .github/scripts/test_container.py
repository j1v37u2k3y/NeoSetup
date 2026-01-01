#!/usr/bin/env python3
"""
Container Testing Script for NeoSetup
Runs comprehensive tests inside Docker containers with proper error handling
"""

import os
import sys
import subprocess  # nosec B404
import argparse


class ContainerTester:
    """Test NeoSetup functionality inside Docker containers."""

    def __init__(self, os_name: str, operator: str):
        self.os_name = os_name
        self.operator = operator
        self.venv_path = "/opt/ansible-venv"

    def run_command(self, cmd: str, description: str) -> bool:
        """Run a command with proper error handling and logging"""
        print(f"🔍 {description}")
        print(f"Running: {cmd}")

        try:
            # Activate virtual environment for all commands
            full_cmd = f"""
            set -e
            source {self.venv_path}/bin/activate
            export PATH={self.venv_path}/bin:$PATH
            {cmd}
            """

            result = subprocess.run(
                ["bash", "-c", full_cmd], capture_output=True, text=True, timeout=300, check=False
            )  # nosec B603 B607

            if result.returncode == 0:
                print(f"✅ {description} - PASSED")
                if result.stdout.strip():
                    print(f"Output: {result.stdout.strip()}")
                return True

            print(f"❌ {description} - FAILED")
            print(f"Exit code: {result.returncode}")
            if result.stdout.strip():
                print(f"STDOUT: {result.stdout.strip()}")
            if result.stderr.strip():
                print(f"STDERR: {result.stderr.strip()}")
            return False

        except subprocess.TimeoutExpired:
            print(f"⏰ {description} - TIMEOUT (300s)")
            return False
        except (OSError, subprocess.SubprocessError) as e:
            print(f"💥 {description} - ERROR: {str(e)}")
            return False

    def verify_environment(self) -> bool:
        """Verify the test environment is properly set up"""
        print(f"🟢 Starting NeoSetup test on {self.os_name} with operator {self.operator}")

        # Check virtual environment (use 'command -v' instead of 'which' for RHEL compatibility)
        if not self.run_command("command -v ansible-playbook", "Verify ansible-playbook is available"):
            return False

        if not self.run_command("ansible --version", "Check Ansible version"):
            return False

        if not self.run_command(
            "python3 -c 'import yaml; print(\"PyYAML available\")'",
            "Verify PyYAML module",
        ):
            return False

        return True

    def run_syntax_check(self) -> bool:
        """Run Ansible syntax check"""
        return self.run_command("ansible-playbook playbooks/site.yml --syntax-check", "Ansible syntax check")

    def run_operator_validation(self) -> bool:
        """Run operator validation"""
        return self.run_command(
            f"python3 scripts/validate_operator.py {self.operator}",
            f"Operator validation for {self.operator}",
        )

    def run_dry_run_test(self) -> bool:
        """Run Ansible integration test with safe tags only"""
        # Match the actual installation pattern from Makefile
        # Run shell and tmux configuration which are safe in containers
        cmd = f"""ansible-playbook playbooks/site.yml \\
            -i inventories/local/hosts.yml \\
            -e 'neosetup_operator={self.operator}' \\
            -e 'container_test=true' \\
            --tags 'shell,tmux' \\
            --skip-tags 'tools,docker' \\
            -v"""

        return self.run_command(cmd, f"Ansible integration test for {self.operator}")

    def run_all_tests(self) -> bool:
        """Run all tests in sequence"""
        tests = [
            ("Environment verification", self.verify_environment),
            ("Syntax check", self.run_syntax_check),
            ("Operator validation", self.run_operator_validation),
            ("Dry-run test", self.run_dry_run_test),
        ]

        failed_tests = []

        for test_name, test_func in tests:
            print(f"\n{'=' * 60}")
            print(f"🧪 Running: {test_name}")
            print(f"{'=' * 60}")

            if not test_func():
                failed_tests.append(test_name)
                print(f"❌ {test_name} FAILED")
                # Continue with other tests to get full picture
            else:
                print(f"✅ {test_name} PASSED")

        print(f"\n{'=' * 60}")
        print("📊 TEST SUMMARY")
        print(f"{'=' * 60}")
        print(f"OS: {self.os_name}")
        print(f"Operator: {self.operator}")
        print(f"Total tests: {len(tests)}")
        print(f"Passed: {len(tests) - len(failed_tests)}")
        print(f"Failed: {len(failed_tests)}")

        if failed_tests:
            print("\n❌ Failed tests:")
            for test in failed_tests:
                print(f"  - {test}")
            return False

        print("\n🎉 All tests passed!")
        return True


def main():
    """Main function to run container tests."""
    parser = argparse.ArgumentParser(description="Run NeoSetup container tests")
    parser.add_argument("--os", required=True, help="Operating system name")
    parser.add_argument("--operator", required=True, help="Operator to test")
    parser.add_argument("--working-dir", default="/neosetup/neosetup", help="Working directory")

    args = parser.parse_args()

    # Change to working directory
    os.chdir(args.working_dir)

    # Run tests
    tester = ContainerTester(args.os, args.operator)
    success = tester.run_all_tests()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
