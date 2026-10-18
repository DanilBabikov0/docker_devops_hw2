from flask import Flask, jsonify
import socket, os

app = Flask(__name__)

N = 2
PERSONAL_ID = "1E34A93D"
NAME = "Бабиков Данил"
DATA_FILE = "/data/backend_data.txt"

def ensure_file():
    os.makedirs("/data", exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.write("initial value\n")

@app.route("/")
def index():
    ensure_file()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
    return jsonify({
        "name": NAME,
        "variant": N,
        "id": PERSONAL_ID,
        "hostname": socket.gethostname(),
        "theme": "docker",
        "volume_content": content
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)