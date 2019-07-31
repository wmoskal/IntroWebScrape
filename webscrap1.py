# example from Udemy course learn web scraping with python from scratch, coded by me.
from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://www.foxsports.com/nhl/stats?category=SCORING"
players = {}
player_no = 0
#while True:
    response = requests.get(url)

    # print(response)

    data = response.text

    # print(data)

    soup = BeautifulSoup(data, 'html.parser')

    #display all links from webpage url
    tags = soup.find_all('a')

    print(len(tags))
