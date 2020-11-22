import requests
from bs4 import BeautifulSoup


def get_bs_obj(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text)
