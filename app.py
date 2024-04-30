from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    product_data = scrape_product_data()
    return render_template('index.html', product_data=product_data)

def scrape_product_data():
    url = "https://www.amazon.com.br/gp/product/B0BZ7R2MPQ/"
    browser_header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
    }

    try:
        response = requests.get(url, headers=browser_header)
        response.raise_for_status() 
        soup = BeautifulSoup(response.content, 'html.parser')

        product_title = soup.select_one(".a-size-large .product-title-word-break")
        product_name = product_title.get_text(strip=True) if product_title else "Título do produto não encontrado."

        product_image_element = soup.select_one(".imgTagWrapper img")
        product_image_url = product_image_element.get("src") if product_image_element else ""

        product_price_element = soup.select_one(".a-price .a-offscreen")

        if product_price_element:
            product_price_text = product_price_element.get_text(strip=True)
            product_price = float(product_price_text.replace("R$", "").replace(".", "").replace(",", ".").strip())
        else:
            product_price = "Preço não encontrado"

        product_data = {
            "name": product_name,
            "image_url": product_image_url,
            "price": product_price
        }

        return product_data

    except requests.RequestException as e:
        print("Erro ao acessar a página:", e)
        return {"error": "Erro ao acessar a página."}

    except Exception as ex:
        print("Ocorreu um erro inesperado:", ex)
        return {"error": "Erro inesperado durante a raspagem de dados."}

if __name__ == "__main__":
    app.run(debug=True)
