from flask import Flask
import subprocess
import sys
import os
from datetime import datetime

app = Flask(__name__)

inicio_monitor = datetime.now()

monitor = subprocess.Popen([
    sys.executable,
    "monitor.py"
])


@app.route("/")
def inicio():
    return "Monitor EMTU funcionando!"


@app.route("/status")
def status():
    if monitor.poll() is None:
        tempo = datetime.now() - inicio_monitor

        return (
            "Monitor EMTU está rodando!<br>"
            f"PID: {monitor.pid}<br>"
            f"Iniciado em: {inicio_monitor.strftime('%d/%m/%Y %H:%M:%S')}<br>"
            f"Tempo rodando: {tempo}"
        )

    return (
        f"Monitor EMTU parou.<br>"
        f"Código de saída: {monitor.returncode}"
    )


if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 3000))

    app.run(
        host="0.0.0.0",
        port=porta
    )