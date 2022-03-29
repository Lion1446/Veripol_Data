from bs4 import BeautifulSoup   ##pip3 install beautifulsoup4
import os
import requests                 ##pip3 install requests

f = open('House of Representatives.html', 'r')
html_string = f.read()
f.close()
soup = BeautifulSoup(html_string, "html.parser")
headers = soup.find_all(class_="panel-heading")
bodies = soup.find_all(class_="panel-body")
downloadables = []

for body in bodies:
    body_soup = BeautifulSoup(str(body), "html.parser")
    classes = body_soup.find_all(class_="m-0 p-0")
    for this_class in classes:
        print(this_class.text)




