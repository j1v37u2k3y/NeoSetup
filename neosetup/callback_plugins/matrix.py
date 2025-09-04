"""Matrix-themed Ansible callback plugin.

The red pill for your Ansible output - provides Matrix-style terminal animations
and color schemes for Ansible playbook execution.
"""

# pylint: disable=protected-access,super-with-arguments,invalid-name,import-error,too-many-locals,no-name-in-module
# Ansible callback plugins require protected access and have import constraints

from __future__ import absolute_import, division, print_function

import os
import time

from ansible.plugins.callback import CallbackBase

try:
    from ansible.color import C
except ImportError:
    # Fallback for different ansible versions
    from ansible import constants as C

__metaclass__ = type

DOCUMENTATION = """
    name: matrix
    type: stdout
    short_description: Matrix-themed Ansible output
    description:
        - This callback plugin formats Ansible output with a Matrix cyberpunk theme
        - Green colors for success, red for errors, with ASCII art banners
        - Custom messaging that fits the NeoSetup Matrix theme
    requirements:
        - Set as stdout in ansible.cfg or set ANSIBLE_STDOUT_CALLBACK=matrix
"""


class CallbackModule(CallbackBase):
    """
    Matrix-themed callback for Ansible output
    """

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = "stdout"
    CALLBACK_NAME = "matrix"

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.task_start_time = None
        self.play_start_time = None

    def _get_color(self, state):
        """Get appropriate color for different states"""
        colors = {
            "ok": C.COLOR_OK,  # Green
            "changed": C.COLOR_CHANGED,  # Yellow
            "error": C.COLOR_ERROR,  # Red
            "unreachable": C.COLOR_UNREACHABLE,  # Red
            "skipped": C.COLOR_SKIP,  # Cyan
            "matrix": "\033[92m",  # Bright green
            "matrix_dim": "\033[32m",  # Dim green
            "reset": "\033[0m",
        }
        return colors.get(state, "")

    def _print_banner(self, text, color="matrix"):
        """Print Matrix-styled banner"""
        color_code = self._get_color(color)
        reset = self._get_color("reset")

        banner = f"""
{color_code}╔══════════════════════════════════════════╗
║{text.center(42)}║
╚══════════════════════════════════════════╝{reset}
"""
        self._display.display(banner)

    def _print_matrix_line(self, text, color="matrix"):
        """Print a Matrix-styled line"""
        color_code = self._get_color(color)
        reset = self._get_color("reset")
        self._display.display(f"{color_code}🎭 {text}{reset}")

    def v2_playbook_on_start(self, playbook):
        """Called when a playbook starts"""
        self.play_start_time = time.time()

        banner_text = "Welcome to the Matrix, Neo"
        self._print_banner(banner_text)

        self._print_matrix_line("NeoSetup Ansible Edition - Initializing...")
        self._print_matrix_line(f"Playbook: {os.path.basename(playbook._file_name)}")
        self._display.display("")

    def v2_playbook_on_play_start(self, play):
        """Called when a play starts"""
        name = play.get_name().strip()
        if not name:
            name = "Unnamed Play"

        self._print_matrix_line(f"🎬 Starting Play: {name}")
        self._display.display("")

    def v2_playbook_on_task_start(self, task, _is_conditional):
        """Called when a task starts"""
        self.task_start_time = time.time()

        task_name = task.get_name().strip()
        if not task_name:
            task_name = str(task)

        # Add some Matrix flair to task names
        if "install" in task_name.lower():
            icon = "📦"
        elif "config" in task_name.lower():
            icon = "⚙️"
        elif "start" in task_name.lower():
            icon = "🚀"
        elif "copy" in task_name.lower() or "template" in task_name.lower():
            icon = "📝"
        elif "git" in task_name.lower():
            icon = "🔗"
        elif "check" in task_name.lower() or "stat" in task_name.lower():
            icon = "🔍"
        else:
            icon = "⚡"

        task_line = f"\n{self._get_color('matrix_dim')}{icon} TASK " f"[{task_name}]{self._get_color('reset')}"
        self._display.display(task_line)

    def v2_runner_on_ok(self, result):
        """Called when a task succeeds"""
        host = result._host.get_name()

        if result._result.get("changed", False):
            color = "changed"
            icon = "🔄"
        else:
            color = "ok"
            icon = "✅"

        self._display.display(f"{self._get_color(color)}{icon} ok: [{host}]{self._get_color('reset')}")

    def v2_runner_on_failed(self, result, ignore_errors=False):
        """Called when a task fails"""
        host = result._host.get_name()

        if ignore_errors:
            icon = "⚠️"
            color = "skipped"
        else:
            icon = "❌"
            color = "error"

        self._display.display(f"{self._get_color(color)}{icon} failed: [{host}]{self._get_color('reset')}")

        # Show error details
        if "msg" in result._result:
            self._display.display(f"    Error: {result._result['msg']}")

    def v2_runner_on_unreachable(self, result):
        """Called when a host is unreachable"""
        host = result._host.get_name()
        unreachable_line = f"{self._get_color('unreachable')}🔌 unreachable: " f"[{host}]{self._get_color('reset')}"
        self._display.display(unreachable_line)

    def v2_runner_on_skipped(self, result):
        """Called when a task is skipped"""
        host = result._host.get_name()
        skipped_line = f"{self._get_color('skipped')}⏭️  skipped: " f"[{host}]{self._get_color('reset')}"
        self._display.display(skipped_line)

    def v2_playbook_on_stats(self, stats):
        """Called when playbook execution is complete"""

        # Calculate total runtime
        if self.play_start_time:
            total_time = time.time() - self.play_start_time
            time_str = f"{total_time:.2f}s"
        else:
            time_str = "unknown"

        self._display.display("")
        self._print_banner("Mission Complete")

        # Show stats for each host
        hosts = sorted(stats.processed.keys())
        for host in hosts:
            summary = stats.summarize(host)

            ok = summary["ok"]
            changed = summary["changed"]
            unreachable = summary["unreachable"]
            failures = summary["failures"]
            skipped = summary["skipped"]

            # Matrix-themed summary
            if failures or unreachable:
                icon = "💥"
                status_color = "error"
                status_text = "RED PILL REJECTED"
            elif changed:
                icon = "🔄"
                status_color = "changed"
                status_text = "MATRIX MODIFIED"
            else:
                icon = "✅"
                status_color = "ok"
                status_text = "SIMULATION COMPLETE"

            status_line = f"{self._get_color(status_color)}{icon} {host}: " f"{status_text}{self._get_color('reset')}"
            self._display.display(status_line)
            stats_line = (
                f"    ok={ok} changed={changed} unreachable={unreachable} " f"failed={failures} skipped={skipped}"
            )
            self._display.display(stats_line)

        self._display.display("")
        self._print_matrix_line(f"⏱️  Total execution time: {time_str}")

        # Final Matrix message - red pill or blue pill outcome
        if any(stats.summarize(host)["failures"] for host in hosts):
            self._print_matrix_line("🔴 There is no spoon... but there were errors. Check the logs.")
        else:
            self._print_matrix_line("🟢 Welcome to the real world, Neo. Setup complete!")

        self._display.display("")

    def v2_playbook_on_no_hosts_matched(self):
        """Called when no hosts match"""
        self._print_matrix_line("⚠️  No hosts matched. Are you sure you took the red pill?")

    def v2_playbook_on_no_hosts_remaining(self):
        """Called when no hosts remain"""
        self._print_matrix_line("💀 All hosts have been disconnected from the Matrix.")
