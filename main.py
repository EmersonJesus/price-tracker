import requests
from bs4 import BeautifulSoup

url = 'https://www.amazon.com.br/gp/product/B0BZ7R2MPQ/'

preco_alvo = 1000.00

browser_header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
}

try:
    pagina = requests.get(url, headers=browser_header)
    pagina.raise_for_status() 
    soup = BeautifulSoup(pagina.content, 'html.parser')

    titulo_do_produto = soup.select_one("#productTitle")
    produto = titulo_do_produto.get_text(strip=True) if titulo_do_produto else "Título do produto não encontrado."


    preco_atual_element = soup.select_one(".a-price .a-offscreen")

    if preco_atual_element:
        texto_do_preco = preco_atual_element.get_text(strip=True)
        preco_atual = float(texto_do_preco.replace("R$", "").replace(".", "").replace(",", ".").strip())
    else:
        preco_atual = None

    if preco_atual is not None and preco_atual < preco_alvo:
        print(f' Produto: {produto}, Preço Atual: R${preco_atual:.2f}')
    else:
        print(f'Preço do produto "{produto}" não atingiu o preço-alvo.\nPreço Atual: R${preco_atual:.2f}')

except requests.RequestException as e:
    print("Erro ao acessar a página:", e)
except Exception as ex:
    print("Ocorreu um erro inesperado:", ex)
