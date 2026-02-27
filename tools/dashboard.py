"""
IoT Systems Design - Lab Dashboard
Application and Service Domain (ASD) Server bridging to a Thread/CoAP Edge Node
"""

from flask import Flask, render_template_string, request, jsonify
import subprocess
import json
import logging

app = Flask(__name__)

# Suppress default Flask logging to keep the console clean for CoAP debug output
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# --- Network Configuration (Interface Capability) ---
# Configure the IPv6 address of the Thread node (obtain via 'ipaddr' in the ESP CLI)
NODE_IP = "fd11:22:33:0:0:0:0:1"  
COAP_PORT = 5683

# --- CoAP Subprocess Handlers ---

def get_sensor_data():
    """
    Sensing Capability: Polls the edge node via CoAP GET.
    """
    try:
        print(f"[CoAP GET] Requesting /sensor from {NODE_IP}...")
        result = subprocess.run([
            "python", "tools/coap_client.py",
            "--host", NODE_IP, "get", "/sensor"
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            # Attempt to parse the stdout as JSON
            try:
                data = json.loads(result.stdout.strip())
                return data
            except json.JSONDecodeError:
                # Fallback if the CoAP client returns raw text instead of JSON
                return {"raw_value": result.stdout.strip()}
        else:
            print(f"[ERROR] CoAP GET Failed: {result.stderr}")
            return {"error": "Node unreachable"}
            
    except subprocess.TimeoutExpired:
        print("[ERROR] CoAP GET Timeout. Is the Thread node active?")
        return {"error": "Timeout"}
    except Exception as e:
        print(f"[ERROR] Subprocess error: {e}")
        return {"error": "Internal Error"}

def control_light(state):
    """
    Actuating Capability: Sends a command to the edge node via CoAP PUT.
    """
    try:
        print(f"[CoAP PUT] Sending /light -> {state} to {NODE_IP}...")
        result = subprocess.run([
            "python", "tools/coap_client.py",
            "--host", NODE_IP, "put", "/light", str(state)
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            return True
        else:
            print(f"[ERROR] CoAP PUT Failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("[ERROR] CoAP PUT Timeout.")
        return False
    except Exception as e:
        print(f"[ERROR] Subprocess error: {e}")
        return False

# --- Frontend User Domain (UD) ---

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IoT Lab: Thread & CoAP Dashboard</title>
    <style>
        body { font-family: system-ui, -apple-system, sans-serif; background-color: #f4f4f9; color: #333; padding: 2rem; max-width: 600px; margin: 0 auto; }
        .card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 1.5rem; }
        h1 { font-size: 1.25rem; border-bottom: 2px solid #0056b3; padding-bottom: 0.5rem; margin-top: 0; }
        .data-point { font-size: 2rem; font-weight: bold; color: #0056b3; margin: 0.5rem 0; font-family: monospace; }
        .btn-group { display: flex; gap: 1rem; }
        .btn { flex: 1; padding: 0.75rem; font-size: 1rem; border: none; border-radius: 4px; cursor: pointer; color: white; transition: opacity 0.2s; }
        .btn:hover { opacity: 0.9; }
        .btn-on { background-color: #28a745; }
        .btn-off { background-color: #dc3545; }
        .badge { background: #e9ecef; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem; font-family: monospace; }
    </style>
</head>
<body>
    <h2>IoT Systems Design Lab</h2>
    <p>Target Node: <span class="badge">{{ node_ip }}</span> (Thread/IPv6)</p>

    <div class="card">
        <h1>Sensing Capability (CoAP GET /sensor)</h1>
        <div class="data-point" id="sensor-data">Loading...</div>
        <p style="font-size: 0.8rem; color: #666;" id="status-text">Initializing connection...</p>
    </div>

    <div class="card">
        <h1>Actuating Capability (CoAP PUT /light)</h1>
        <div class="btn-group">
            <button class="btn btn-on" onclick="controlLight(1)">Turn ON (1)</button>
            <button class="btn btn-off" onclick="controlLight(0)">Turn OFF (0)</button>
        </div>
    </div>

    <script>
        // Asynchronous polling to replace <meta refresh>
        function fetchSensorData() {
            fetch('/api/sensor')
                .then(response => response.json())
                .then(data => {
                    const display = document.getElementById('sensor-data');
                    const status = document.getElementById('status-text');
                    
                    if (data.error) {
                        display.innerText = "ERR";
                        status.innerText = "Error: " + data.error;
                        status.style.color = "red";
                    } else {
                        // Formats the JSON payload for display
                        display.innerText = JSON.stringify(data);
                        status.innerText = "Connected. Live data stream active.";
                        status.style.color = "green";
                    }
                })
                .catch(err => console.error("Polling error:", err));
        }

        // Send actuation command asynchronously
        function controlLight(state) {
            fetch('/api/control', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({state: state})
            })
            .then(response => response.json())
            .then(data => {
                if(data.status !== 'ok') {
                    alert("Failed to route command to Thread node.");
                }
            });
        }

        // Start polling every 2 seconds
        setInterval(fetchSensorData, 2000);
        fetchSensorData(); // Initial fetch
    </script>
</body>
</html>
'''

# --- Flask Routes ---

@app.route('/')
def dashboard():
    """Serves the frontend UI."""
    return render_template_string(HTML_TEMPLATE, node_ip=NODE_IP)

@app.route('/api/sensor', methods=['GET'])
def api_get_sensor():
    """Endpoint for the frontend to retrieve cached/live sensor data."""
    data = get_sensor_data()
    return jsonify(data)

@app.route('/api/control', methods=['POST'])
def api_control_light():
    """Endpoint for the frontend to send actuation commands."""
    payload = request.get_json()
    state = payload.get('state', 0)
    
    success = control_light(state)
    if success:
        return jsonify({'status': 'ok'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'CoAP PUT failed'}), 502

if __name__ == '__main__':
    print("===================================================")
    print(" Thread/CoAP Dashboard Initialized")
    print(f" Target Edge Node IP: {NODE_IP}")
    print(f" Listening on: http://0.0.0.0:5000/")
    print("===================================================\n")
    app.run(host='0.0.0.0', port=5000, debug=True)