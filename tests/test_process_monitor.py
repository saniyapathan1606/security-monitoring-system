from src.process_monitor import snapshot, find_suspicious

def test_snapshot_runs():
    procs = snapshot()
    assert isinstance(procs, list)

def test_find_suspicious_thresholds():
    procs = [{"pid":1,"ppid":0,"name":"init","user":"root","cpu":0.0,"rss":900*1024*1024}]
    sus = find_suspicious(procs, rss_mb_threshold=800, cpu_threshold=90.0)
    assert sus and "elevated_user" in sus[0]["reasons"]
