
from bs4 import BeautifulSoup

import requests

url = 'http://www.randomwordgenerator.org/random-sentence-generator'

num_requests = 1000 

while (num_requests>0):
    r  = requests.get(url)
    data = r.text

    soup = BeautifulSoup(data, 'html.parser')
    for item in soup.find_all('p', {'class':'result '}):
        print(item.b.text)

    num_requests = num_requests - 1

