import requests

topico = "gui-emtu-047-9x82k"

mensagem = "🚍 TESTE: sua notificação do projeto EMTU funcionou!"

resposta = requests.post(
    f"https://ntfy.sh/{topico}",
    data=mensagem.encode("utf-8")
)

print("Status:", resposta.status_code)
print("Mensagem enviada!")