import csv

id_escolhido = input('Digite o ID da parada: ')

with open("stop.txt", "r", encoding="utf-8") as arquivo:

    dados = csv.DictReader(arquivo)

    for parada in dados:

        if parada["stop_id"] == id_escolhido:

            print("Parada encontrada!")

            nome = parada["stop_name"]
            latitude = float(parada["stop_lat"])
            longitude = float(parada["stop_lon"])

            print("Nome:", nome)
            print("Latitude:", latitude)
            print("Longitude:", longitude)