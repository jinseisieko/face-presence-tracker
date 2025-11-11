from flask import Flask, render_template_string

app = Flask(__name__)
UPDATE_INTERVAL = 14
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Face Presence Live View</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 20px; background: #f0f0f0; }
        #frame { max-width: 100%; max-height: 70vh; border: 2px solid #ccc; border-radius: 8px; background: #000; }
        #status { margin-top: 15px; font-size: 1.2em; }
        .face { color: #2e7d32; font-weight: bold; }
        .no-face { color: #d32f2f; }
        .info { margin-top: 10px; color: #555; }
    </style>
</head>
<body>
    <h1>Face Presence Tracker — Live View</h1>
    <div id="status">Loading...</div>
    <img id="frame" src="" alt="Live feed">
    <script>
        async function fetchLatest() {
            try {
                const response = await fetch('/latest');
                if (!response.ok) throw new Error("No data");
                const data = await response.json();

                // Показать изображение
                document.getElementById('frame').src = 'data:image/jpeg;base64,' + data.frame_b64;

                // Обновить статус
                const statusEl = document.getElementById('status');
                const time = new Date(data.timestamp * 1000).toLocaleTimeString();
                if (data.has_face) {
                    statusEl.innerHTML = `Face detected | ${time}`;
                    statusEl.className = 'face';
                } else {
                    statusEl.innerHTML = `No face | ${time}`;
                    statusEl.className = 'no-face';
                }
            } catch (e) {
                document.getElementById('status').innerHTML = 'Waiting for data...';
            }
        }
        fetchLatest();
''' + f'''
        setInterval(fetchLatest, UPDATE_INTERVAL_WM);
    </script>
</body>
</html>
'''

HTML = HTML.replace("UPDATE_INTERVAL_WM", str(int(UPDATE_INTERVAL*1000)))

@app.route('/')
def index():
    return HTML

@app.route('/latest')
def proxy_latest():
    import requests
    try:
        resp = requests.get("http://analyzer:5000/latest", timeout=3)
        return resp.json(), resp.status_code
    except:
        return {"error": "Analyzer unavailable"}, 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)