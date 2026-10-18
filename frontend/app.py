from flask import Flask, Response
import os, requests

app = Flask(__name__)

BACKEND_HOST = os.environ.get("BACKEND_HOST", "backend")
BACKEND_PORT = os.environ.get("BACKEND_PORT", "5000")

@app.route("/")
def index():
    return "<h1>Фронтэнд Вариант 2</h1><p><a href='/api'>/api</a></p>"

@app.route("/api")
def api():
    try:
        r = requests.get(f"http://{BACKEND_HOST}:{BACKEND_PORT}/", timeout=3)
        return Response(r.content, status=r.status_code, mimetype="application/json")
    except requests.RequestException as e:
        return {"error": str(e), "backend_host": BACKEND_HOST}, 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)