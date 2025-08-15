from pathlib import Path

# Folders to monitor (adjust to your OS)
CRITICAL_PATHS = [
    r"C:\Temp\SecurityTest"  # Windows demo folder
]

# Baseline hash storage
BASELINE_FILE = Path(".baseline_hashes.json")

# Scan intervals (seconds)
SCAN_INTERVAL_SEC = 60
PROCESS_SCAN_INTERVAL_SEC = 30
MEMORY_SCAN_INTERVAL_SEC = 60

# Thresholds
PROCESS_CPU_THRESHOLD = 85.0
PROCESS_RSS_MB = 800
MEM_SPIKE_GROWTH_MB = 300

# Alert settings
ALERT_EMAIL = "your_email@example.com"  # optional
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "user"
SMTP_PASS = "password"
