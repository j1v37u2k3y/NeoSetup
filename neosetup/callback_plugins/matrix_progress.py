"""Matrix-themed Ansible callback plugin with real-time progress tracking.

Enhanced version of the Matrix callback that provides:
- Per-role progress bars
- Task completion indicators
- Estimated time remaining
- Real-time progress updates
"""

# pylint: disable=protected-access
# Ansible callback plugins require access to protected members like _result, _host, _role

from __future__ import absolute_import, division, print_function

import os
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field

from ansible.plugins.callback import CallbackBase

DOCUMENTATION = """
    name: matrix_progress
    type: stdout
    short_description: Matrix-themed Ansible output with real-time progress
    description:
        - Enhanced Matrix callback with progress bars and time estimates
        - Shows per-role progress tracking
        - Provides real-time task completion indicators
        - Estimates remaining installation time
    requirements:
        - Set as stdout in ansible.cfg or set ANSIBLE_STDOUT_CALLBACK=matrix_progress
"""

# Known NeoSetup roles for progress tracking
NEOSETUP_ROLES = ["common", "shell", "tmux", "tools", "docker"]

# ANSI color codes for terminal output
COLORS = {
    "ok": "\033[92m",  # Bright green
    "changed": "\033[93m",  # Yellow
    "error": "\033[91m",  # Red
    "unreachable": "\033[91m",  # Red
    "skipped": "\033[96m",  # Cyan
    "matrix": "\033[92m",  # Bright green
    "matrix_dim": "\033[32m",  # Dim green
    "cyan": "\033[96m",
    "yellow": "\033[93m",
    "reset": "\033[0m",
    "bold": "\033[1m",
}


def render_progress_bar(progress, width=25, label="", show_percent=True):
    """Render an ASCII progress bar.

    Args:
        progress: Float between 0 and 1
        width: Width of the progress bar in characters
        label: Optional label to show before the bar
        show_percent: Whether to show percentage

    Returns:
        Formatted progress bar string
    """
    progress = max(0, min(1, progress))
    filled = int(width * progress)
    empty = width - filled

    bar_str = "█" * filled + "░" * empty
    pct = str(int(progress * 100)).rjust(3)
    percent_str = f" {pct}%" if show_percent else ""

    if label:
        return f"{label}: [{bar_str}]{percent_str}"
    return f"[{bar_str}]{percent_str}"


def format_time(seconds):
    """Format seconds into human-readable string."""
    if seconds < 60:
        rounded = round(seconds, 1)
        return f"{rounded}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}m {secs}s"


def get_color(state):
    """Get ANSI color code for a given state."""
    return COLORS.get(state, "")


@dataclass
class TaskStats:
    """Container for task statistics."""

    total: int = 0
    completed: int = 0
    failed: int = 0
    skipped: int = 0
    changed: int = 0


@dataclass
class TimingInfo:
    """Container for timing information."""

    playbook_start: float = 0.0
    task_start: float = 0.0
    task_times: list = field(default_factory=list)

    def record_task_duration(self):
        """Record the duration of the current task."""
        if self.task_start:
            duration = time.time() - self.task_start
            self.task_times.append(duration)
            # Keep only last 50 for rolling average
            self.task_times = self.task_times[-50:]

    def estimate_remaining(self, remaining_tasks):
        """Estimate remaining time based on task durations."""
        if not self.task_times or remaining_tasks <= 0:
            return None
        avg_time = sum(self.task_times[-20:]) / len(self.task_times[-20:])
        return avg_time * remaining_tasks


@dataclass
class RoleTracking:
    """Container for role tracking information."""

    current: str = None
    tasks: dict = field(default_factory=lambda: defaultdict(int))
    completed: dict = field(default_factory=lambda: defaultdict(int))
    order: list = field(default_factory=list)


class CallbackModule(CallbackBase):
    """Matrix-themed callback with real-time progress tracking."""

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = "stdout"
    CALLBACK_NAME = "matrix_progress"

    def __init__(self):
        super().__init__()
        self.stats = TaskStats()
        self.timing = TimingInfo()
        self.roles = RoleTracking()
        self.last_display_lines = 0
        self.is_tty = sys.stdout.isatty()

    def _clear_lines(self, count):
        """Clear previous output lines for in-place updates."""
        if self.is_tty and count > 0:
            sys.stdout.write(f"\033[{count}A")
            sys.stdout.write("\033[J")
            sys.stdout.flush()

    def _get_role_from_task(self, task):
        """Extract role name from task."""
        if hasattr(task, "_role") and task._role:
            return task._role.get_name()
        task_path = getattr(task, "_ds", {}).get("__file__", "") if hasattr(task, "_ds") else ""
        for role in NEOSETUP_ROLES:
            if f"/roles/{role}/" in task_path:
                return role
        return None

    def _print_header(self):
        """Print Matrix-styled header."""
        c = get_color
        header = f"""
{c('matrix')}╔══════════════════════════════════════════════════════════════╗
║{c('bold')}              🔴 Welcome to the Matrix, Neo 🔴                  {c('reset')}{c('matrix')}║
║                  NeoSetup Installation Progress                  ║
╚══════════════════════════════════════════════════════════════════╝{c('reset')}
"""
        self._display.display(header)

    def _build_progress_lines(self):
        """Build the lines for the progress display."""
        c = get_color
        lines = []

        # Task counter (no percentage - we don't know total upfront)
        lines.append(f"{c('matrix')}📦 Tasks completed: {self.stats.completed}{c('reset')}")

        # Time info
        elapsed = time.time() - self.timing.playbook_start if self.timing.playbook_start else 0
        elapsed_str = format_time(elapsed)
        lines.append(f"{c('cyan')}⏱️  Elapsed: {elapsed_str}{c('reset')}")

        return lines

    def _build_role_progress_lines(self):
        """Build the lines for per-role progress."""
        c = get_color
        lines = []

        if not self.roles.order:
            return lines

        lines.append(f"\n{c('matrix_dim')}Roles: {c('reset')}")
        for role in self.roles.order:
            completed = self.roles.completed[role]
            is_current = role == self.roles.current

            if is_current:
                icon, color = "▶", c("yellow")
                status = f"({completed} tasks)"
            else:
                icon, color = "✓", c("ok")
                status = f"({completed} tasks)"

            lines.append(f"  {color}{icon} {role} {status}{c('reset')}")

        return lines

    def _build_stats_line(self):
        """Build the statistics line."""
        c = get_color
        parts = []
        if self.stats.changed > 0:
            parts.append(f"{c('changed')}changed={self.stats.changed}{c('reset')}")
        if self.stats.failed > 0:
            parts.append(f"{c('error')}failed={self.stats.failed}{c('reset')}")
        if self.stats.skipped > 0:
            parts.append(f"{c('skipped')}skipped={self.stats.skipped}{c('reset')}")
        return f"\n{' | '.join(parts)}" if parts else ""

    def _print_progress_display(self, task_name=""):
        """Print the real-time progress display."""
        c = get_color
        lines = self._build_progress_lines()
        lines.extend(self._build_role_progress_lines())

        # Current task
        if task_name:
            display_name = task_name[:47] + "..." if len(task_name) > 50 else task_name
            lines.append(f"\n{c('matrix_dim')}⚡ {display_name}{c('reset')}")

        stats_line = self._build_stats_line()
        if stats_line:
            lines.append(stats_line)

        self._clear_lines(self.last_display_lines)
        self._display.display("\n".join(lines))
        self.last_display_lines = len(lines)

    def _print_completion_banner(self):
        """Print the completion banner."""
        c = get_color
        if self.stats.failed > 0:
            banner_color, banner_text, icon = "error", "Installation Encountered Errors", "💥"
        else:
            banner_color, banner_text, icon = "matrix", "Installation Complete", "✅"

        banner = f"""
{c(banner_color)}╔══════════════════════════════════════════════════════════════╗
║{c('bold')}            {icon} {banner_text.center(42)} {icon}            {c('reset')}{c(banner_color)}║
╚══════════════════════════════════════════════════════════════════╝{c('reset')}
"""
        self._display.display(banner)

    def _print_summary_stats(self, total_time):
        """Print the summary statistics."""
        c = get_color
        self._display.display(f"{c('matrix')}📊 Installation Summary{c('reset')}")
        self._display.display(f"   ⏱️  Total time: {format_time(total_time)}")
        self._display.display(f"   📦 Tasks: {self.stats.completed} total")

        ok_count = self.stats.completed - self.stats.changed - self.stats.failed - self.stats.skipped
        self._display.display(f"   {c('ok')}✓  OK: {ok_count}{c('reset')}")

        if self.stats.changed > 0:
            self._display.display(f"   {c('changed')}🔄 Changed: {self.stats.changed}{c('reset')}")
        if self.stats.failed > 0:
            self._display.display(f"   {c('error')}❌ Failed: {self.stats.failed}{c('reset')}")
        if self.stats.skipped > 0:
            self._display.display(f"   {c('skipped')}⏭️  Skipped: {self.stats.skipped}{c('reset')}")

    def _print_role_breakdown(self):
        """Print the role breakdown."""
        c = get_color
        if not self.roles.order:
            return

        self._display.display(f"\n{c('matrix')}📋 Role Breakdown{c('reset')}")
        for role in self.roles.order:
            completed = self.roles.completed[role]
            total = self.roles.tasks[role]
            if total > 0:
                self._display.display(f"   • {role}: {completed}/{total} tasks")

    def _print_host_summary(self, stats):
        """Print the host summary."""
        c = get_color
        self._display.display(f"\n{c('matrix')}🖥️  Host Summary{c('reset')}")

        for host in sorted(stats.processed.keys()):
            summary = stats.summarize(host)
            if summary["failures"] or summary["unreachable"]:
                status_icon, status_color = "❌", c("error")
            elif summary["changed"]:
                status_icon, status_color = "🔄", c("changed")
            else:
                status_icon, status_color = "✅", c("ok")

            self._display.display(
                f"   {status_color}{status_icon} {host}: "
                f"ok={summary['ok']} changed={summary['changed']} "
                f"failed={summary['failures']} skipped={summary['skipped']}{c('reset')}"
            )

    def v2_playbook_on_start(self, playbook):
        """Called when a playbook starts."""
        self.timing.playbook_start = time.time()
        self._print_header()

        playbook_name = os.path.basename(playbook._file_name)
        self._display.display(f"{get_color('matrix_dim')}📂 Playbook: {playbook_name}{get_color('reset')}")
        self._display.display("")

    def v2_playbook_on_play_start(self, play):
        """Called when a play starts."""
        name = play.get_name().strip() or "Unnamed Play"
        self._display.display(f"\n{get_color('matrix')}🎬 {name}{get_color('reset')}")
        self._display.display("")

    def v2_playbook_on_task_start(self, task, is_conditional=None):
        """Called when a task starts."""
        self.timing.task_start = time.time()
        self.stats.total += 1

        role = self._get_role_from_task(task)
        if role:
            if role != self.roles.current:
                self.roles.current = role
                if role not in self.roles.order:
                    self.roles.order.append(role)
            self.roles.tasks[role] += 1

        task_name = task.get_name().strip() or str(task)
        self._print_progress_display(task_name)

    def v2_runner_on_ok(self, result):
        """Called when a task succeeds."""
        self.timing.record_task_duration()
        self.stats.completed += 1

        if result._result.get("changed", False):
            self.stats.changed += 1

        if self.roles.current:
            self.roles.completed[self.roles.current] += 1

    def v2_runner_on_failed(self, result, ignore_errors=False):
        """Called when a task fails."""
        self.timing.record_task_duration()
        self.stats.completed += 1
        self.stats.failed += 1

        if self.roles.current:
            self.roles.completed[self.roles.current] += 1

        host = result._host.get_name()
        c = get_color
        self._display.display(f"\n{c('error')}❌ FAILED: [{host}]{c('reset')}")
        if "msg" in result._result:
            self._display.display(f"   {c('error')}{result._result['msg']}{c('reset')}")

    def v2_runner_on_unreachable(self, result):
        """Called when a host is unreachable."""
        self.timing.record_task_duration()
        self.stats.completed += 1
        self.stats.failed += 1

        host = result._host.get_name()
        self._display.display(f"\n{get_color('unreachable')}🔌 UNREACHABLE: [{host}]{get_color('reset')}")

    def v2_runner_on_skipped(self, result):
        """Called when a task is skipped."""
        self.timing.record_task_duration()
        self.stats.completed += 1
        self.stats.skipped += 1

        if self.roles.current:
            self.roles.completed[self.roles.current] += 1

    def v2_playbook_on_stats(self, stats):
        """Called when playbook execution is complete."""
        c = get_color
        self._clear_lines(self.last_display_lines)

        total_time = time.time() - self.timing.playbook_start if self.timing.playbook_start else 0

        self._display.display("")
        self._print_completion_banner()
        self._print_summary_stats(total_time)
        self._print_role_breakdown()
        self._print_host_summary(stats)

        self._display.display("")
        if self.stats.failed > 0:
            self._display.display(f"{c('error')}🔴 There is no spoon... but there were errors.{c('reset')}")
        else:
            self._display.display(f"{c('matrix')}🟢 Welcome to the real world, Neo. Your setup is complete!{c('reset')}")
            self._display.display(f"{c('matrix_dim')}💡 Restart your shell or run: source ~/.zshrc{c('reset')}")
        self._display.display("")

    def v2_playbook_on_no_hosts_matched(self):
        """Called when no hosts match."""
        self._display.display(
            f"{get_color('error')}⚠️  No hosts matched. Are you sure you took the red pill?{get_color('reset')}"
        )

    def v2_playbook_on_no_hosts_remaining(self):
        """Called when no hosts remain."""
        self._display.display(
            f"{get_color('error')}💀 All hosts have been disconnected from the Matrix.{get_color('reset')}"
        )
