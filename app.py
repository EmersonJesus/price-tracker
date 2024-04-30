from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    products = scrape_products()
    return render_template('index.html', products=products)

def scrape_products():
    url = "https://www.amazon.com.br/gp/product/B0BZ7R2MPQ/"
    browser_header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
    }

    response = requests.get(url, headers=browser_header)
    response.raise_for_status() 
    soup = BeautifulSoup(response.content, 'html.parser')

    product_title = soup.select_one(".a-size-large.product-title-word-break")
    product = product_title.get_text(strip=True) if product_title else "Título do produto não encontrado."

    return [product]

if __name__ == "__main__":
    app.run(debug=True)