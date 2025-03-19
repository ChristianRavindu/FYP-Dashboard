from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

# A list to store threat data (this will be updated dynamically)
threat_data = []

# Simulate adding data to the threat_data (you can replace this with real threat detection code)
def generate_fake_data():
    while True:
        time.sleep(5)
        threat_data.append({
            "ip": "8.8.8.8",  # Sample IP
            "status": "Malicious",
            "country": "United States",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        socketio.emit('new_threat', {"threat": threat_data[-1]}, broadcast=True)

@app.route('/')
def index():
    return render_template('index.html', threats=threat_data)

@app.route('/analyze_ip', methods=['POST'])
def analyze_ip():
    data = request.get_json()
    ip = data['ip']
    # Analyze IP here (e.g., call VirusTotal or your own logic)
    # For now, we assume it's malicious
    new_threat = {
        "ip": ip,
        "status": "Malicious",
        "country": "United States",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    threat_data.append(new_threat)
    socketio.emit('new_threat', {"threat": new_threat}, broadcast=True)
    return jsonify({"status": "Threat added", "data": new_threat})

# Running the background threat data generator
@app.before_request  # Use before_request instead of before_first_request
def start_thread():
    if not hasattr(app, 'background_thread'):
        thread = threading.Thread(target=generate_fake_data)
        thread.daemon = True
        app.background_thread = thread
        thread.start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
