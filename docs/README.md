Security Monitoring System

A real-time security monitoring tool for system integrity, processes, and memory on Windows/Linux.

Project Overview

This project is a Python-based Security Monitoring System designed to detect intrusions, system misconfigurations, and anomalous behavior in real time. It continuously monitors:

File integrity – detects modifications, deletions, or new files in critical directories.

Processes – flags suspicious processes with high CPU/memory usage.

Memory usage – identifies abnormal memory spikes that may indicate malware or misbehaving applications.

Alerts are printed in the terminal using rich tables and can be extended to email or webhook notifications.

Features

Real-time file, process, and memory monitoring

Configurable scan intervals and thresholds

Graceful shutdown handling

Python/Bash scripts for automation

Cross-platform support (Windows & Linux)

Easy to extend with email, Slack, or Teams alerts

Installation

Clone the repository:

git clone https://github.com/<your-username>/security-monitoring-system.git
cd security-monitoring-system


Create a virtual environment:

python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac


Install dependencies:

pip install -r requirements.txt

Usage

Run the main orchestrator:

python -m src.main


Modify or create files in monitored directories → see real-time alerts.

Suspicious processes and memory spikes are also detected automatically.

Configuration

Edit src/config.py to adjust:

Paths to monitor (CRITICAL_PATHS)

Scan intervals (SCAN_INTERVAL_SEC)

CPU/RSS thresholds (PROCESS_CPU_THRESHOLD, PROCESS_RSS_MB)

Memory spike threshold (MEM_SPIKE_GROWTH_MB)

Optional alert settings (SMTP, webhooks)

Folder Structure
security-monitoring-system/
├── src/         # Python source code
├── docs/        # Documentation and README
├── tests/       # Unit tests
├── requirements.txt
└── .gitignore

Future Enhancements

Email / Slack / Teams notifications

Web dashboard with Flask for real-time monitoring

SQLite or JSON database for baseline tracking

Linux-specific rootkit/malware detection hooks

Technologies & Tools

Python 3.x

psutil, watchdog, rich

Bash scripting (for Linux automation)

Windows/Linux system paths monitoring

Author

Saniya Pathan – Computer Engineering (Honors in Cybersecurity)
GitHub: https://github.com/saniyapathan1606