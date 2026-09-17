from flask import Flask
import subprocess
import sys
import os
import requests
import urllib3

app = Flask(__name__)

ARQUIVO_STATUS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "monitor_status.txt"
)

inicio_monitor = None

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

                    ultima_consulta = arquivo.read().strip()

                return (
                    "Monitor EMTU está rodando!<br>"
                    f"PID: {monitor.pid}<br>"
                    f"Última consulta à EMTU: {ultima_consulta}"
                )

            except Exception as erro:

                return (
                    "Monitor EMTU está rodando!<br>"
                    f"PID: {monitor.pid}<br>"
                    f"Erro ao ler status: {erro}"
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


@app.route("/emtu-test")
def emtu_test():

    urllib3.disable_warnings(
        urllib3.exceptions.InsecureRequestWarning
    )

    try:

        resposta = requests.get(
            "https://rest-emtu.noxxonsat.com.br/rest/lineDetails",
            params={
                "linha": "047"
            },
            verify=False,
            timeout=15
        )

        return (
            f"Conexão com EMTU funcionando!<br>"
            f"Status HTTP: {resposta.status_code}<br>"
            f"Tamanho da resposta: {len(resposta.content)} bytes"
        )

    except Exception as erro:

        return (
            "ERRO AO ACESSAR A API DA EMTU!<br>"
            f"Tipo: {type(erro).__name__}<br>"
            f"Erro: {erro}"
        )


if __name__ == "__main__":

    porta = int(
        os.environ.get("PORT", 3000)
    )

    app.run(
        host="0.0.0.0",
        port=porta
    )