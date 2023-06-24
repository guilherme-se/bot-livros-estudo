import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Host': 'books.toscrape.com',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
}

pagina_atual = [str("https://books.toscrape.com/catalogue/page-{}.html").format(i) for i in range(1, 51)] 

product_link = []
product_name = []
product_price = []
product_stock = []

for link in pagina_atual:
    req = requests.get(link, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    products = soup.find_all(class_='product_pod')

    for product in products:
        product_path = (product.find('a'))['href']
        product_link.append(f"https://books.toscrape.com/catalogue/{product_path} ")

        h3find = product.find('h3')
        title_text = h3find.find('a')['title']
        product_name.append(title_text)

        price = product.find(class_='price_color')
        price_text = price.text.strip().replace("Â", "")  # removendo o caracter indesejado

        product_price.append(price_text)  # Mantém o preço como string
        
        stock = product.find(class_='instock availability')
        disponibilidade = stock.text.strip().replace('\n', '')  # removendo as quebras de linhas
        product_stock.append(disponibilidade)

# Criando DataFrame
df = pd.DataFrame({"Link": product_link, "Nome": product_name, "Preço": product_price, "Disponibilidade": product_stock}, columns=["Link", "Nome", "Preço", "Disponibilidade"])

# CSV
df.to_csv('livros.csv', index=False)

