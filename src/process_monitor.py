import psutil

def snapshot():
    procs = []
    for p in psutil.process_iter(["pid", "name", "username", "cpu_percent", "memory_info"]):
        info = p.info
        procs.append({
            "pid": info["pid"],
            "name": info["name"],
            "user": info["username"],
            "cpu": info["cpu_percent"],
            "rss": info["memory_info"].rss / (1024*1024)  # MB
        })
    return procs

def find_suspicious(processes, rss_mb_threshold=800, cpu_threshold=85):
    suspicious = []
    for p in processes:
        reasons = []
        if p["rss"] > rss_mb_threshold:
            reasons.append(f"High RSS {p['rss']:.1f} MB")
        if p["cpu"] > cpu_threshold:
            reasons.append(f"High CPU {p['cpu']:.1f}%")
        if reasons:
            p["reasons"] = reasons
            suspicious.append(p)
    return suspicious
