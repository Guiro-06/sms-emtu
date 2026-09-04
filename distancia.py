from geopy.distance import geodesic

ponto1 = (-23.685812, -46.527433)
ponto2 = (-23.686808, -46.528423)

distancia = geodesic(ponto1, ponto2).meters

print(f"Distância: {distancia:.1f} metros")