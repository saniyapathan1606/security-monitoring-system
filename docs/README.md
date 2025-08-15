# Security Monitoring System

Real-time monitoring of **files**, **processes**, and **memory** to detect intrusions or system misconfigurations. Cross-platform (Windows/Linux), built with Python.

## Features
- File Integrity Monitoring (hash-based + filesystem events)
- Process anomaly detection (elevated user, no parent, high CPU/RSS)
- Memory RSS spike detection
- Alerting via **Email (SMTP)** and **Webhook**
- Simple configuration in `src/main.py`

## Quick Start
```bash
pip install -r requirements.txt
python -m src.main
