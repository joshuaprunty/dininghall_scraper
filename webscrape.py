from bs4 import BeautifulSoup
import webbrowser
import os
from selenium import webdriver
import time

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

with open('/Users/joshprunty/Desktop/python shit/dishes.txt','w') as f:
    for tag in tags:
        f.write(tag.text)
        f.write('\n')

driver.quit()




