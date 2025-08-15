import psutil
import time

_previous = {}

def find_rss_spikes(interval_sec=5, growth_mb=300):
    global _previous
    spikes = []
    for p in psutil.process_iter(["pid", "name", "username", "memory_info"]):
        info = p.info
        rss_mb = info["memory_info"].rss / (1024*1024)
        prev = _previous.get(info["pid"], rss_mb)
        if rss_mb - prev >= growth_mb:
            spikes.append({
                "pid": info["pid"],
                "name": info["name"],
                "user": info["username"],
                "growth_mb": rss_mb - prev
            })
        _previous[info["pid"]] = rss_mb
    return spikes
