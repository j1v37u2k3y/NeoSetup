#!/usr/bin/env python3
"""
Package Installation Testing Script for NeoSetup
Tests package manager compatibility across different OS distributions
"""
# pylint: disable=duplicate-code  # Test utilities share common patterns

import subprocess  # nosec B404
import sys
import argparse


class PackageTester:
    """Test package manager compatibility across different OS distributions."""

    def __init__(self, os_name: str, pkg_mgr: str):
        self.os_name = os_name
        self.pkg_mgr = pkg_mgr

    def run_command(self, cmd: str, description: str, use_sudo: bool = False) -> bool:
        """Run a command with proper error handling"""
        if use_sudo:
            cmd = f"sudo {cmd}"

        print(f"🔍 {description}")
        print(f"Running: {cmd}")

        try:
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=300, check=False)  # nosec B603

            if result.returncode == 0:
                print(f"✅ {description} - PASSED")
                return True

            print(f"❌ {description} - FAILED (exit code: {result.returncode})")
            if result.stderr.strip():
                print(f"STDERR: {result.stderr.strip()}")
            return False

        except subprocess.TimeoutExpired:
            print(f"⏰ {description} - TIMEOUT")
            return False
        except (OSError, subprocess.SubprocessError) as e:
            print(f"💥 {description} - ERROR: {str(e)}")
            return False

    def update_package_cache(self) -> bool:
        """Update package manager cache"""
        if self.pkg_mgr == "apt":
            return self.run_command("apt-get update", "Update apt cache", use_sudo=True)
        # dnf/yum don't need explicit cache updates for our test
        return True

    def install_test_packages(self) -> bool:
        """Install common test packages"""
        packages = ["curl", "wget", "git", "vim", "htop", "tree"]

        if self.pkg_mgr == "apt":
            cmd = f"apt-get install -y {' '.join(packages)}"
        elif self.pkg_mgr == "dnf":
            cmd = f"dnf install -y {' '.join(packages)}"
        else:  # yum
            cmd = f"yum install -y {' '.join(packages)}"

        return self.run_command(cmd, f"Install test packages via {self.pkg_mgr}", use_sudo=True)

    def verify_installations(self) -> bool:
        """Verify installed packages work"""
        verifications = [
            ("curl --version", "Verify curl installation"),
            ("git --version", "Verify git installation"),
            ("vim --version", "Verify vim installation"),
        ]

        all_passed = True
        for cmd, description in verifications:
            # Only check first line of vim version to avoid huge output
            if "vim" in cmd:
                cmd += " | head -n1"

            if not self.run_command(cmd, description):
                all_passed = False

        return all_passed

    def run_all_tests(self) -> bool:
        """Run complete package testing suite"""
        print(f"📦 Testing package manager compatibility on {self.os_name}")
        print(f"Package manager: {self.pkg_mgr}")

        tests = [
            ("Update package cache", self.update_package_cache),
            ("Install test packages", self.install_test_packages),
            ("Verify installations", self.verify_installations),
        ]

        failed_tests = []

        for test_name, test_func in tests:
            print(f"\n{'=' * 50}")
            print(f"🧪 {test_name}")
            print(f"{'=' * 50}")

            if not test_func():
                failed_tests.append(test_name)
                print(f"❌ {test_name} FAILED")
                # Continue to get full picture
            else:
                print(f"✅ {test_name} PASSED")

        print(f"\n{'=' * 50}")
        print("📊 PACKAGE TEST SUMMARY")
        print(f"{'=' * 50}")
        print(f"OS: {self.os_name}")
        print(f"Package Manager: {self.pkg_mgr}")
        print(f"Total tests: {len(tests)}")
        print(f"Passed: {len(tests) - len(failed_tests)}")
        print(f"Failed: {len(failed_tests)}")

        if failed_tests:
            print("\n❌ Failed tests:")
            for test in failed_tests:
                print(f"  - {test}")
            return False

        print("\n✅ Package installation compatibility verified!")
        return True


def main():
    """Main function to test package manager compatibility."""
    parser = argparse.ArgumentParser(description="Test package manager compatibility")
    parser.add_argument("--os", required=True, help="Operating system name")
    parser.add_argument(
        "--pkg-mgr",
        required=True,
        choices=["apt", "dnf", "yum"],
        help="Package manager",
    )

    args = parser.parse_args()

    tester = PackageTester(args.os, args.pkg_mgr)
    success = tester.run_all_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
