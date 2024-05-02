from flask import Flask, render_template, request, redirect
from bs4 import BeautifulSoup
import requests
import random
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('tracked_products.json')
Product = Query()

def get_user_agent():
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
    ]
    return random.choice(user_agent_list)

def scrape_product_data(url):
    browser_header = {
        "User-Agent": get_user_agent()
    }

    try:
        response = requests.get(url, headers=browser_header)
        response.raise_for_status() 
        soup = BeautifulSoup(response.content, 'html.parser')

        product_title = soup.select_one("#productTitle")
        product_name = product_title.get_text(strip=True) if product_title else "Título do produto não encontrado."

        product_image_element = soup.select_one("#imgTagWrapperId img")
        product_image_url = product_image_element.get("src") if product_image_element else ""

        product_price_element = soup.select_one(".a-price .a-offscreen")
        product_price = product_price_element.get_text(strip=True) if product_price_element else "Preço não encontrado"

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

@app.route("/")
def home():
    products = db.all()
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    product_url = request.form['product_url']
    target_price = request.form['target_price']
    product_data = scrape_product_data(product_url)
    if not product_data.get('error'):
        db.insert({'name': product_data['name'], 'image_url': product_data['image_url'], 'price': product_data['price'], 'target_price': target_price})
    return redirect('/')

@app.route('/delete_product', methods=['POST'])
def delete_product():
    product_id = int(request.form['product_id'])
    db.remove(doc_ids=[product_id])
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)