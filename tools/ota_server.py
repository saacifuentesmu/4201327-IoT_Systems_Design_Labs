from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/firmware/<version>')
def serve_firmware(version):
    filename = f"build/iot_lab_base_{version}_signed.bin"
    if os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    return "Firmware not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)