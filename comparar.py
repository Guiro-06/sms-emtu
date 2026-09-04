import csv
import requests
from geopy.distance import geodesic

# Pergunta qual parada o usuário quer
id_escolhido = input("Digite o ID da parada: ")

# Procura a parada no arquivo stop.txt
with open("stop.txt", "r", encoding="utf-8") as arquivo:

    dados = csv.DictReader(arquivo)

    for parada in dados:

        if parada["stop_id"] == id_escolhido:

            nome = parada["stop_name"]
            latitude_parada = float(parada["stop_lat"])
            longitude_parada = float(parada["stop_lon"])

            print("\nParada encontrada!")
            print("Nome:", nome)
            print("Latitude:", latitude_parada)
            print("Longitude:", longitude_parada)

            # Consulta a API da EMTU
            url = "https://rest-emtu.noxxonsat.com.br/rest/lineDetails"

            parametros = {
                "linha": "047"
            }

            resposta = requests.get(
                url,
                params=parametros,
                verify=False
            )

            dados_api = resposta.json()

            linha = dados_api["linhas"][0]
            veiculos = linha["veiculos"]

            print("\nDistância dos ônibus indo para Vila Palmares:\n")

            # Calcula a distância somente dos ônibus no sentido VOLTA
            for onibus in veiculos:

                if onibus["sentidoLinha"] != "volta":
                    continue

                latitude_onibus = onibus["latitude"]
                longitude_onibus = onibus["longitude"]

                ponto_parada = (
                    latitude_parada,
                    longitude_parada
                )

                ponto_onibus = (
                    latitude_onibus,
                    longitude_onibus
                )

                distancia = geodesic(
                    ponto_parada,
                    ponto_onibus
                ).meters

                # Mostra em metros ou quilômetros
                if distancia >= 1000:
                    distancia_formatada = f"{distancia / 1000:.1f} km"
                else:
                    distancia_formatada = f"{distancia:.1f} metros"

                print(
                    f"Ônibus {onibus['prefixo']} → "
                    f"{distancia_formatada}"
                )

            break