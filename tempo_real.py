import requests
import urllib3

# Esconde o aviso do certificado
urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


# ==========================================
# CONFIGURAÇÕES
# ==========================================

url = "https://rest-emtu.noxxonsat.com.br/rest/lineDetails"

parametros = {
    "linha": "047"
}


# ==========================================
# CONSULTAR API
# ==========================================

resposta = requests.get(
    url,
    params=parametros,
    verify=False,
    timeout=10
)

dados = resposta.json()

linha = dados["linhas"][0]

veiculos = linha["veiculos"]


# ==========================================
# MOSTRAR SEQUÊNCIA DOS ÔNIBUS
# ==========================================

print("\nÔNIBUS NO SENTIDO VOLTA:\n")


for onibus in veiculos:

    if onibus["sentidoLinha"] != "volta":
        continue

    print(
        f"Ônibus: {onibus['prefixo']} "
        f"| seqPonto: {onibus['seqPonto']} "
        f"| Latitude: {onibus['latitude']} "
        f"| Longitude: {onibus['longitude']}"
    )