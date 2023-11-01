import requests
from bs4 import BeautifulSoup

url = "https://www.amazon.com.br/Celular-Xiaomi-Redmi-Note-12/dp/B0BZ7R2MPQ/"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Accept-Language": "pt-BR",
}

resposta = requests.get(url, headers=headers)
soup = BeautifulSoup(resposta.text, 'html.parser')

# Encontre o título do produto usando o seletor CSS apropriado
titulo_do_produto = soup.select_one("#productTitle")

if titulo_do_produto:
    texto_do_titulo = titulo_do_produto.get_text(strip=True)
    print(f"{texto_do_titulo}")
else:
    print("Título do produto não encontrado.")

# Encontre o preço do produto usando um seletor CSS mais específico
preco = soup.select_one(".a-price .a-offscreen")

if preco:
    texto_do_preco = preco.get_text(strip=True)
    print(f"{texto_do_preco}")
else:
    print("Preço do produto não encontrado.")
