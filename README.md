# face-presence-tracker

```
docker compose --profile webui up webui
```
```
docker compose up --build
```

# Face Presence Tracker

A local tool that tracks how much time you spend in front of your laptop using your webcam. It detects your face, counts active time, and shows live stats in a web browser.

All processing happens on your computer — no data is sent anywhere.

## How it works
- **Processor**: Reads video from your webcam and detects faces.
- **Analyzer**: Decides when you are present or away, and counts total time.
- **Web UI** (optional): Shows live video, status, and daily stats. Protected by password.

## Use cases
- Track your screen time
- Improve focus and reduce distractions
- Monitor work hours (for personal use)
- Privacy-friendly alternative to cloud-based trackers
