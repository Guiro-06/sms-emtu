import csv
import time
import requests
import urllib3
from geopy.distance import geodesic


# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

LINHA = "047"

# Ponto onde quero receber o alerta
ID_ALERTA = "91795"

# Ponto onde vou pegar o ônibus
ID_EMBARQUE = "8254"

# Distância para considerar que o ônibus chegou ao 91795
RAIO_ALERTA = 100

# Tópico do ntfy
TOPICO = "gui-emtu-047-9x82k"

# API da EMTU
URL_API = "https://rest-emtu.noxxonsat.com.br/rest/lineDetails"

# Remove aviso do certificado expirado
urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


# ==========================================================
# FUNÇÃO - NOTIFICAÇÃO
# ==========================================================

def enviar_notificacao(prefixo):

    mensagem = (
        f"🚍 Ônibus {prefixo} chegou ao ponto {ID_ALERTA}!\n\n"
        f"🏃 Saia agora da estação para pegar o ônibus.\n\n"
        f"🚌 Embarque: ponto {ID_EMBARQUE}"
    )

    try:

        resposta = requests.post(
            f"https://ntfy.sh/{TOPICO}",
            data=mensagem.encode("utf-8"),
            timeout=10
        )

        if resposta.status_code == 200:

            print("📱 Notificação enviada para o iPhone!")

        else:

            print(
                "Erro ao enviar notificação:",
                resposta.status_code
            )

    except requests.RequestException as erro:

        print(
            "Erro ao enviar notificação:",
            erro
        )


# ==========================================================
# FUNÇÃO - LER STOP
# ==========================================================

def buscar_stop(arquivo, stop_id):

    arquivo.seek(0)

    dados = csv.DictReader(arquivo)

    for parada in dados:

        if parada["stop_id"] == stop_id:

            return {
                "nome": parada["stop_name"],
                "latitude": float(parada["stop_lat"]),
                "longitude": float(parada["stop_lon"])
            }

    return None


# ==========================================================
# 1. PEGAR OS DOIS PONTOS
# ==========================================================

with open(
    "stop.txt",
    "r",
    encoding="utf-8"
) as arquivo:

    parada_alerta = buscar_stop(
        arquivo,
        ID_ALERTA
    )

    parada_embarque = buscar_stop(
        arquivo,
        ID_EMBARQUE
    )


if parada_alerta is None:

    print(
        f"O ponto {ID_ALERTA} não foi encontrado."
    )

    exit()


if parada_embarque is None:

    print(
        f"O ponto {ID_EMBARQUE} não foi encontrado."
    )

    exit()


latitude_alerta = parada_alerta["latitude"]
longitude_alerta = parada_alerta["longitude"]

latitude_embarque = parada_embarque["latitude"]
longitude_embarque = parada_embarque["longitude"]

nome_alerta = parada_alerta["nome"]
nome_embarque = parada_embarque["nome"]


# ==========================================================
# 2. FUNÇÃO PARA SABER DE QUE LADO DO 91795 O ÔNIBUS ESTÁ
# ==========================================================

def calcular_posicao_relativa(latitude, longitude):

    # Transformamos latitude/longitude em uma coordenada
    # aproximada em metros.

    fator_latitude = 111320

    fator_longitude = (
        111320
        * __import__("math").cos(
            __import__("math").radians(latitude_alerta)
        )
    )

    # Vetor: 91795 → 8254
    vetor_x = (
        (longitude_embarque - longitude_alerta)
        * fator_longitude
    )

    vetor_y = (
        (latitude_embarque - latitude_alerta)
        * fator_latitude
    )

    # Vetor: 91795 → ônibus
    onibus_x = (
        (longitude - longitude_alerta)
        * fator_longitude
    )

    onibus_y = (
        (latitude - latitude_alerta)
        * fator_latitude
    )

    tamanho_vetor = (
        vetor_x * vetor_x
        + vetor_y * vetor_y
    )

    if tamanho_vetor == 0:

        return 0

    # Projeção do ônibus sobre a direção 91795 → 8254
    posicao = (
        (onibus_x * vetor_x)
        + (onibus_y * vetor_y)
    ) / tamanho_vetor

    return posicao


# ==========================================================
# 3. MOSTRAR CONFIGURAÇÃO
# ==========================================================

print("=" * 60)
print("        MONITORAMENTO DA LINHA 047")
print("        DESTINO: VILA PALMARES")
print("=" * 60)

print("\n📍 ALERTA")
print("ID:", ID_ALERTA)
print("Nome:", nome_alerta)

print("\n🚌 EMBARQUE")
print("ID:", ID_EMBARQUE)
print("Nome:", nome_embarque)

print("\nSentido monitorado: VOLTA")
print("\nPressione Ctrl + C para parar.")


# ==========================================================
# 4. MEMÓRIA
# ==========================================================

# Guarda a posição relativa anterior do ônibus
posicao_anterior = {}

# Guarda quais ônibus já foram avisados
notificados = set()


# ==========================================================
# 5. MONITORAMENTO
# ==========================================================

while True:

    try:

        resposta = requests.get(
            URL_API,
            params={
                "linha": LINHA
            },
            verify=False,
            timeout=10
        )

        resposta.raise_for_status()

        dados_api = resposta.json()

        linha = dados_api["linhas"][0]

        veiculos = linha["veiculos"]


        # Limpa tela
        print("\033[2J\033[H", end="")


        print("=" * 60)
        print("        MONITORAMENTO DA LINHA 047")
        print("        DESTINO: VILA PALMARES")
        print("=" * 60)

        print(f"\n📍 Alerta: {ID_ALERTA}")
        print(f"🚌 Embarque: {ID_EMBARQUE}\n")


        encontrou_onibus = False


        # ==================================================
        # ANALISAR CADA ÔNIBUS
        # ==================================================

        for onibus in veiculos:

            # ------------------------------------------------
            # SÓ QUEREMOS VOLTA
            # ------------------------------------------------

            if onibus["sentidoLinha"] != "volta":

                continue


            prefixo = onibus["prefixo"]

            latitude = float(
                onibus["latitude"]
            )

            longitude = float(
                onibus["longitude"]
            )


            # =================================================
            # POSIÇÃO DO ÔNIBUS EM RELAÇÃO AO TRECHO
            # =================================================

            posicao_atual = calcular_posicao_relativa(
                latitude,
                longitude
            )


            # =================================================
            # DISTÂNCIA ATÉ 91795
            # =================================================

            distancia = geodesic(
                (
                    latitude_alerta,
                    longitude_alerta
                ),
                (
                    latitude,
                    longitude
                )
            ).meters


            # =================================================
            # SE JÁ FOI NOTIFICADO
            # =================================================

            if prefixo in notificados:

                continue


            # =================================================
            # PRIMEIRA VEZ QUE VEMOS O ÔNIBUS
            # =================================================

            if prefixo not in posicao_anterior:

                posicao_anterior[prefixo] = posicao_atual

                # ------------------------------------------------
                # SE ELE JÁ ESTÁ DEPOIS DO 91795:
                # IGNORA
                # ------------------------------------------------

                if posicao_atual > 0:

                    continue

                # Ainda antes do 91795
                continue


            posicao_antiga = posicao_anterior[prefixo]


            # =================================================
            # DETECTAR CRUZAMENTO DO 91795
            # =================================================

            cruzou_alerta = (
                posicao_antiga < 0
                and posicao_atual >= 0
            )


            # =================================================
            # NOTIFICAÇÃO
            # =================================================

            if cruzou_alerta:

                print(
                    f"\n🚨 ÔNIBUS {prefixo} "
                    f"CHEGOU AO PONTO {ID_ALERTA}!"
                )

                print(
                    f"📍 {nome_alerta}"
                )

                print(
                    "🏃 Saia agora para pegar o ônibus!"
                )


                enviar_notificacao(
                    prefixo
                )


                # Marca que já avisamos
                notificados.add(prefixo)


                # Atualiza posição
                posicao_anterior[prefixo] = posicao_atual

                continue


            # =================================================
            # SE JÁ PASSOU
            # =================================================

            if posicao_atual >= 0:

                # Se já está depois do ponto,
                # não mostramos.
                posicao_anterior[prefixo] = posicao_atual

                continue


            # =================================================
            # CALCULAR STATUS
            # =================================================

            encontrou_onibus = True


            if distancia <= RAIO_ALERTA:

                status = "ESTÁ PRÓXIMO"

                simbolo = "🟡"

            elif posicao_atual > posicao_antiga:

                status = "ESTÁ INDO"

                simbolo = "🟢"

            else:

                status = "ESTÁ INDO"

                simbolo = "🟢"


            # =================================================
            # DISTÂNCIA FORMATADA
            # =================================================

            if distancia >= 1000:

                distancia_formatada = (
                    f"{distancia / 1000:.1f} km"
                )

            else:

                distancia_formatada = (
                    f"{distancia:.1f} metros"
                )


            # =================================================
            # MOSTRAR
            # =================================================

            print(
                f"{simbolo} Ônibus {prefixo}"
            )

            print(
                f"   Status: {status}"
            )

            print(
                f"   Distância até {ID_ALERTA}: "
                f"{distancia_formatada}"
            )

            print()


            # Atualiza posição
            posicao_anterior[prefixo] = posicao_atual


        # ==================================================
        # NENHUM ÔNIBUS
        # ==================================================

        if not encontrou_onibus:

            print(
                "Nenhum ônibus ainda a caminho "
                "do ponto de alerta."
            )


        print("-" * 60)

        print(
            "Atualizando a cada 15 segundos..."
        )


        time.sleep(15)


    # ======================================================
    # ERROS
    # ======================================================

    except requests.RequestException as erro:

        print(
            "Erro ao consultar a API:",
            erro
        )

        time.sleep(15)


    except (
        KeyError,
        IndexError,
        ValueError
    ) as erro:

        print(
            "Erro ao interpretar os dados:",
            erro
        )

        time.sleep(15)


    except KeyboardInterrupt:

        print(
            "\nMonitoramento encerrado."
        )

        break