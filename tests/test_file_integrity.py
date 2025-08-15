import os
from pathlib import Path
from src.file_integrity_monitor import build_baseline, scan_and_diff

def test_baseline_and_diff(tmp_path: Path):
    f = tmp_path / "test.txt"
    f.write_text("hello")
    paths = [str(tmp_path)]
    baseline_file = tmp_path / ".baseline.json"

    build_baseline(paths, baseline_file)
    diffs = scan_and_diff(paths, baseline_file)
    # No changes after immediate scan
    assert not any(diffs.values())

    # Modify file
    f.write_text("changed")
    diffs2 = scan_and_diff(paths, baseline_file)
    assert "modified" in diffs2 and len(diffs2["modified"]) >= 1
