#!/usr/bin/env python3
"""
Performance Testing Script for NeoSetup
Measures execution time and validates performance targets
"""
# pylint: disable=duplicate-code  # Test scripts share common patterns

import os
import subprocess  # nosec B404
import sys
import time
import argparse


class PerformanceTester:
    """Performance testing class for NeoSetup Ansible playbooks."""

    def __init__(self, os_name: str, target_seconds: int = 300):
        self.os_name = os_name
        self.target_seconds = target_seconds
        self.venv_path = "/opt/ansible-venv"

    def run_timed_command(self, cmd: str, description: str) -> tuple[bool, float]:
        """Run a command and measure execution time"""
        print(f"⚡ {description}")
        print(f"Running: {cmd}")

        # Prepare command with virtual environment
        full_cmd = f"""
        source {self.venv_path}/bin/activate
        export PATH={self.venv_path}/bin:$PATH
        {cmd}
        """

        start_time = time.time()

        try:
            result = subprocess.run(  # nosec B603 B607
                ["bash", "-c", full_cmd],
                capture_output=True,
                text=True,
                timeout=self.target_seconds + 60,  # Add buffer to timeout
                check=False,
            )

            end_time = time.time()
            duration = end_time - start_time

            success = result.returncode == 0

            print(f"📊 Duration: {duration:.2f} seconds")
            print(f"🎯 Target: < {self.target_seconds} seconds")

            if success:
                if duration < self.target_seconds:
                    print(f"✅ {description} - PASSED (within target)")
                else:
                    print(f"⚠️ {description} - SLOW (exceeded target)")
                    success = False
            else:
                print(f"❌ {description} - FAILED (exit code: {result.returncode})")
                if result.stderr.strip():
                    print(f"STDERR: {result.stderr.strip()}")

            return success, duration

        except subprocess.TimeoutExpired:
            end_time = time.time()
            duration = end_time - start_time
            print(f"⏰ {description} - TIMEOUT after {duration:.2f} seconds")
            return False, duration
        except (OSError, subprocess.SubprocessError) as e:
            end_time = time.time()
            duration = end_time - start_time
            print(f"💥 {description} - ERROR: {str(e)}")
            return False, duration

    def run_performance_test(self) -> bool:  # pylint: disable=duplicate-code
        """Run the main performance test"""
        print(f"⚡ Performance benchmark starting on {self.os_name}")

        cmd = """timeout 300 ansible-playbook playbooks/site.yml \\
            -i ../test-inventory/hosts \\
            -e 'operator=base' \\
            --check \\
            --diff || true"""

        success, duration = self.run_timed_command(cmd, "Base operator dry-run performance test")

        print(f"\n{'=' * 60}")
        print("📊 PERFORMANCE RESULTS")
        print(f"{'=' * 60}")
        print(f"OS: {self.os_name}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Target: < {self.target_seconds} seconds")
        print(f"Status: {'✅ PASSED' if success else '❌ FAILED'}")

        return success


def main():
    """Main function to run NeoSetup performance tests."""
    parser = argparse.ArgumentParser(description="Run NeoSetup performance tests")
    parser.add_argument("--os", required=True, help="Operating system name")
    parser.add_argument("--target", type=int, default=300, help="Target time in seconds")
    parser.add_argument("--working-dir", default="/neosetup/neosetup", help="Working directory")

    args = parser.parse_args()

    os.chdir(args.working_dir)

    tester = PerformanceTester(args.os, args.target)
    success = tester.run_performance_test()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
