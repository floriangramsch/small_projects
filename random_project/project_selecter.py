from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import random
import webbrowser

url = 'https://nevonprojects.com/project-ideas/software-project-ideas/'

# open connection, grabbing page
uClient = urlopen(url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")
projects = page_soup.find("ul", {"class": "press"}).findAll("a")
webbrowser.open(random.choices(projects)[0]["href"])