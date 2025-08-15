import hashlib
import json
from pathlib import Path
from typing import List, Dict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def compute_file_hash(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def build_baseline(paths: List[str], baseline_file: Path):
    baseline = {}
    for p in paths:
        for file in Path(p).rglob("*"):
            if file.is_file():
                baseline[str(file)] = compute_file_hash(file)
    baseline_file.write_text(json.dumps(baseline, indent=2))
    print(f"Baseline written to {baseline_file} with {len(baseline)} entries")

def scan_and_diff(paths: List[str], baseline_file: Path) -> Dict[str, List[str]]:
    if not baseline_file.exists():
        return {p: [] for p in paths}

    baseline = json.loads(baseline_file.read_text())
    diffs = {p: [] for p in paths}

    for p in paths:
        for file in Path(p).rglob("*"):
            if file.is_file():
                file_hash = compute_file_hash(file)
                old_hash = baseline.get(str(file))
                if old_hash != file_hash:
                    diffs[p].append(str(file))
    return diffs

class FSHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_any_event(self, event):
        self.callback(event)

def watch(paths: List[str], on_change):
    observer = Observer()
    for p in paths:
        observer.schedule(FSHandler(on_change), p, recursive=True)
    observer.start()
    return observer
