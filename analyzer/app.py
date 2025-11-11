from flask import Flask, request, jsonify
from datetime import datetime
from collections import defaultdict
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%[ (asctime)s analyzer ]\t%(message)s'
)
logger = logging.getLogger("analyzer")

app = Flask(__name__)
daily_sessions = []

STATE = {
    "last_face_time": None,
    "session_start": None,
    "face_timeout_sec": 5.0,
    "daily_total": {},
    "min_session_sec": 2.0
}

def get_today():
    return datetime.now().strftime("%Y-%m-%d")

@app.route('/frame', methods=['POST'])
def receive_frame():
    try:
        data = request.get_json()
        if not data or 'frame_b64' not in data or 'timestamp' not in data or 'has_face' not in data:
            return jsonify({"error": "Invalid data"}), 400

        timestamp = data["timestamp"]
        has_face = data["has_face"]
        frame_b64 = data.get("frame_b64")

        now = datetime.fromtimestamp(timestamp)
        today = now.strftime("%Y-%m-%d")

        if today not in STATE["daily_total"]:
            STATE["daily_total"][today] = [0.0, []]

        if has_face:
            STATE["last_face_time"] = timestamp
            if STATE["session_start"] is None:
                STATE["session_start"] = timestamp
                logger.info("Session STARTED")
        elif STATE["last_face_time"] is not None:
            if timestamp - STATE["last_face_time"] > STATE["face_timeout_sec"]:
                if STATE["session_start"] is not None:
                    duration = timestamp - STATE["session_start"]
                    if duration >= STATE["min_session_sec"]:

                        STATE["daily_total"][today][0] += duration
                        STATE["daily_total"][today][1] += [{
                            "session_start": STATE["session_start"],
                            "session_end": timestamp
                        }]
                        mins = duration / 60
                        hours_today = STATE["daily_total"][today][0] / 3600
                        logger.info(f"Session ENDED | Duration: {mins:.1f} min | Total today: {hours_today:.2f} h")
                    STATE["session_start"] = None
    
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        logger.error(f"Error processing session: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/stats')
def stats():
    return jsonify({
        "daily_hours": {
            date: round(sec / 3600, 2) for (date, sec), _ in STATE["daily_total"].items()
        },
        "session_active": STATE["session_start"] is not None
    })

if __name__ == '__main__':
    logger.info("Analyzer started. Waiting for frames...")
    app.run(host='0.0.0.0', port=5000)