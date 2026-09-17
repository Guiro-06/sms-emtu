#  Monitoramento EMTU

Sistema desenvolvido em Python para monitorar a linha 047 da EMTU
em tempo real e enviar notificações para o celular quando o ônibus
chega ao ponto de referência.

##  Como funciona

O sistema consulta a API da EMTU a cada 15 segundos, identifica os
ônibus no sentido Vila Palmares e acompanha sua localização.

Quando o ônibus chega ao ponto de alerta 91795, uma notificação é
enviada para o iPhone através do ntfy.

##  Tecnologias

- Python
- Requests
- Geopy
- Flask
- API REST
- Git/GitHub
- ntfy
- Belmo

##  Estrutura

- `monitor.py` — monitoramento dos ônibus
- `app.py` — aplicação Flask e inicialização do monitor
- `notificacao.py` — envio de notificações
- `stop.txt` — dados das paradas
- `requirements.txt` — dependências do projeto

##   Objetivo

Automatizar o acompanhamento do ônibus e avisar o usuário no momento
certo para sair da estação e caminhar até o ponto de embarque.