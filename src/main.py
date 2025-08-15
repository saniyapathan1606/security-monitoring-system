"""
Main Orchestrator:
- Builds/loads baseline
- Runs scheduled scans
- Watches file changes
- Sends alerts when anomalies detected
"""

import os
import signal
import threading
import time
from pathlib import Path
from typing import List

from rich import print, box
from rich.table import Table

# --- Use relative imports to avoid ModuleNotFoundError ---
from .config import *
from .file_integrity_monitor import build_baseline, scan_and_diff, watch
from .process_monitor import snapshot, find_suspicious
from .memory_analyzer import find_rss_spikes
from .alert_system import alert

# ...rest of your main.py code remains the same

# ---- Configuration (edit quickly here or load from .env) ----
CRITICAL_PATHS = [r"C:\Temp\SecurityTest"]

BASELINE_FILE = Path(".baseline_hashes.json")
SCAN_INTERVAL_SEC = 60  # periodic scan
PROCESS_CPU_THRESHOLD = 85.0
PROCESS_RSS_MB = 800
MEM_SPIKE_GROWTH_MB = 300
# --------------------------------------------------------------


def table_from_list(title: str, rows: List[List[str]], headers: List[str]):
    t = Table(title=title, show_lines=False, box=box.SIMPLE)
    for h in headers:
        t.add_column(h)
    for r in rows:
        t.add_row(*[str(x) for x in r])
    print(t)


def on_fs_event(event):
    msg = f"Filesystem change detected: {event.event_type} -> {event.src_path}"
    print(f"[magenta]{msg}[/magenta]")
    alert("FIM Event", msg)


def periodic_scanner(stop_evt: threading.Event):
    while not stop_evt.is_set():
        diffs = scan_and_diff(CRITICAL_PATHS, BASELINE_FILE)
        any_changes = any(diffs.values())
        if any_changes:
            body = []
            for k, items in diffs.items():
                if items:
                    body.append(f"{k.upper()}:\n" + "\n".join(items[:50]))
            body_text = "\n\n".join(body)
            print("[red]Integrity changes detected![/red]")
            alert("File Integrity Changes Detected", body_text)
        time.sleep(SCAN_INTERVAL_SEC)


def process_watchdog(stop_evt: threading.Event):
    while not stop_evt.is_set():
        procs = snapshot()
        sus = find_suspicious(procs, rss_mb_threshold=PROCESS_RSS_MB, cpu_threshold=PROCESS_CPU_THRESHOLD)
        if sus:
            rows = [[p["pid"], p["name"], p["user"], ",".join(p["reasons"])] for p in sus]
            table_from_list("Suspicious Processes", rows, ["PID", "Name", "User", "Reasons"])
            alert("Suspicious Processes Detected", "\n".join([str(r) for r in rows]))
        time.sleep(30)


def memory_watchdog(stop_evt: threading.Event):
    while not stop_evt.is_set():
        spikes = find_rss_spikes(interval_sec=5, growth_mb=MEM_SPIKE_GROWTH_MB)
        if spikes:
            rows = [[s["pid"], s["name"], s.get("user"), s["growth_mb"]] for s in spikes]
            table_from_list("Memory RSS Spikes", rows, ["PID", "Name", "User", "Growth(MB)"])
            alert("Memory RSS Spike Detected", "\n".join([str(r) for r in rows]))
        time.sleep(60)


def main():
    print("[bold cyan]Security Monitoring System[/bold cyan]")

    # Ensure baseline (create if missing)
    if not BASELINE_FILE.exists():
        print("[yellow]No baseline found; building one now...[/yellow]")
        build_baseline(CRITICAL_PATHS, BASELINE_FILE)

    # Start watchdog on filesystem
    observer = watch(CRITICAL_PATHS, on_change=on_fs_event)

    # Start periodic threads
    stop_evt = threading.Event()
    threads = [
        threading.Thread(target=periodic_scanner, args=(stop_evt,), daemon=True),
        threading.Thread(target=process_watchdog, args=(stop_evt,), daemon=True),
        threading.Thread(target=memory_watchdog, args=(stop_evt,), daemon=True),
    ]
    for t in threads:
        t.start()

    # Graceful shutdown
    def shutdown(*_):
        print("[yellow]Shutting down...[/yellow]")
        stop_evt.set()
        observer.stop()
        observer.join(timeout=3)
        raise SystemExit(0)

    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, shutdown)

    # Keep alive
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
