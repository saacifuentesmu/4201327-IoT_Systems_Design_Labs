from flask import Flask, render_template_string, request
import requests
import time

app = Flask(__name__)

# Configurar IPv6 del nodo Thread (obtener con ipaddr en CLI)
NODE_IP = "fd11:22:33:0:0:0:0:1"  # Reemplazar con IP real del nodo
COAP_PORT = 5683

def get_sensor_data():
    try:
        # Usar CoAP client para obtener datos
        import subprocess
        result = subprocess.run([
            "python", "tools/coap_client.py",
            "--host", NODE_IP, "get", "/sensor"
        ], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            # Parsear JSON (simplificado)
            data = result.stdout.strip()
            return data
        return "{}"
    except:
        return "{}"

def control_light(state):
    try:
        import subprocess
        result = subprocess.run([
            "python", "tools/coap_client.py",
            "--host", NODE_IP, "put", "/light", str(state)
        ], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

@app.route('/')
def dashboard():
    sensor_data = get_sensor_data()
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>IoT Lab Dashboard</title>
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        <h1>IoT Sensor Dashboard</h1>
        <div id="sensor-data">{{ sensor_data }}</div>
        <h2>Control Luz</h2>
        <button onclick="controlLight(1)">Encender</button>
        <button onclick="controlLight(0)">Apagar</button>
        <script>
        function controlLight(state) {
            fetch('/control_light', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({state: state})
            });
        }
        </script>
    </body>
    </html>
    ''', sensor_data=sensor_data)

@app.route('/control_light', methods=['POST'])
def control_light_endpoint():
    data = request.get_json()
    state = data.get('state', 0)
    control_light(state)
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)