from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests

def Scrape():  

    retMessage = []

    url = 'https://dineoncampus.com/northwestern/whats-on-the-menu'

    driver = webdriver.Chrome()

    driver.get(url)

    time.sleep(15)

    content = driver.page_source

    with open('output.html', 'w', encoding='utf-8') as f:
        f.write(content)

    with open('output.html','r') as f:
        doc = BeautifulSoup(f, 'html.parser')

    tags = doc.find_all('strong')

    with open('/Users/joshprunty/Desktop/python shit/Webscraper/dishes.txt','w') as f:
        for tag in tags:
            f.write(tag.text)
            f.write('\n')

    for tag in tags:
        retMessage.append(tag.text)

    driver.quit()

    return retMessage

def send_message(message):
  resp = requests.post('http://textbelt.com/text', {
    'phone': '14403713543',
    'message': message,
    'key': 'textbelt'
  })
  print(resp.json())

greeting = "Good Morning! Here are today's dishes at Allison Dining Hall: \n\n"
dishes = ""
dshsList = Scrape()
for dish in dshsList[0:3]:
    dishes += dish
    dishes += "\n"
msg = greeting + dishes

send_message(msg)

