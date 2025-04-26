import requests
from bs4 import BeautifulSoup



url  = "https://fr.klimas.com/boulons-dancrage-mecanique-vis-a-beton-systeme-dancrage-chimique/wdbls/"
html =  requests.get(url)
soup =  BeautifulSoup(html.text)


img = soup.select_one('.entered.lazyloaded')
print(img)
