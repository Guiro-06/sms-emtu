from flask import Flask
import subprocess
import sys

app = Flask(__name__)

monitor = subprocess.Popen([sys.executable, "monitor.py"])


@app.route("/")
def inicio():
    return "Monitor EMTU funcionando!"


@app.route("/status")
def status():
    if monitor.poll() is None:
        return "Monitor EMTU está rodando!"
    return "Monitor EMTU parou."


if __name__ == "__main__":
    import os

    porta = int(os.environ.get("PORT", 3000))

    app.run(
        host="0.0.0.0",
        port=porta
    )