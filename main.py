import requests
from bs4 import BeautifulSoup

# URL do produto desejado
url = 'https://www.amazon.com.br/gp/product/B0BZ7R2MPQ/'

# Preço-alvo
preco_alvo = 1000.00

# User agent
browser_header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
}

# Realiza a solicitação HTTP
pagina = requests.get(url, headers=browser_header)
soup = BeautifulSoup(pagina.content, 'html.parser')
titulo_do_produto = soup.select_one("#productTitle")

if titulo_do_produto:
    produto = titulo_do_produto.get_text(strip=True)
else:
    produto = "Título do produto não encontrado."

# Encontre o elemento de preço atual
preco_atual_element = soup.select_one(".a-price .a-offscreen")

if preco_atual_element:
    # Se o elemento existe, obtenha o texto
    texto_do_preco = preco_atual_element.get_text(strip=True)
    preco_atual =  texto_do_preco.replace("R$", "").replace(".", "").replace(",", ".").strip()
    preco_atual = float(preco_atual)
else:
    # Se o elemento não existe, defina um preço padrão ou trate de outra forma
    preco_atual = None  # Ou qualquer outro valor padrão que você deseje

# Verifica se o preço atual é menor do que o preço-alvo
if preco_atual is not None and preco_atual < preco_alvo:
    print(f' Produto: {produto}, Preço Atual: R${preco_atual:.2f}')
else:
    print(f'Preço do produto "{produto}" não atingiu o preço-alvo.')
