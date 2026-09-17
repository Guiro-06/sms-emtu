from flask import Flask
import subprocess
import sys
import os
from datetime import datetime, timezone


app = Flask(__name__)


ARQUIVO_STATUS = "monitor_status.txt"


inicio_monitor = datetime.now(timezone.utc)


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

        if os.path.exists(ARQUIVO_STATUS):

            try:

                with open(
                    ARQUIVO_STATUS,
                    "r",
                    encoding="utf-8"
                ) as arquivo:

                    ultima_consulta = datetime.fromisoformat(
                        arquivo.read().strip()
                    )


                agora = datetime.now(timezone.utc)


                tempo_desde_consulta = (
                    agora - ultima_consulta
                )


                return (
                    "Monitor EMTU está rodando!<br>"
                    f"PID: {monitor.pid}<br>"
                    f"Iniciado em: "
                    f"{inicio_monitor.strftime('%d/%m/%Y %H:%M:%S')} UTC<br>"
                    f"Última consulta à EMTU: "
                    f"{ultima_consulta.strftime('%d/%m/%Y %H:%M:%S')} UTC<br>"
                    f"Tempo desde a última consulta: "
                    f"{tempo_desde_consulta}"
                )


            except Exception as erro:

                return (
                    "Monitor EMTU está rodando!<br>"
                    f"PID: {monitor.pid}<br>"
                    f"Não foi possível ler o status: {erro}"
                )


        return (
            "Monitor EMTU está rodando!<br>"
            f"PID: {monitor.pid}<br>"
            "Ainda não foi registrada uma consulta à EMTU."
        )


    return (
        "Monitor EMTU parou.<br>"
        f"Código de saída: {monitor.returncode}"
    )


if __name__ == "__main__":

    porta = int(
        os.environ.get("PORT", 3000)
    )


    app.run(
        host="0.0.0.0",
        port=porta
    )