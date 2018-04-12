from slackclient import SlackClient
from bs4 import BeautifulSoup
import re
import urllib.parse
import key
from time import strftime
import requests

url = 'https://www.packtpub.com/packt/offers/free-learning'
headers = {'user-agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion'}

r = requests.get(url, headers=headers)
r2 = str(r.content)

soup = BeautifulSoup(r2, 'html.parser')
dotd = soup.find('div', {'class': 'dotd-main-book-summary'})
dotd_title = dotd.find('div', {'class': 'dotd-title'})
dotd_title = dotd_title.get_text()
dotd_title = re.sub(r"\\n", "", dotd_title)
dotd_title = re.sub(r"\\t", "", dotd_title)

## dotd_title contains the title ##
print(dotd_title)

dotd_summary = dotd.find_all("div")
desc1 = dotd_summary[2]
desc2 = dotd_summary[3]

desc1 = desc1.get_text()
desc2 = desc2.get_text()

desc1 = re.sub(r"\\t", "", desc1)
desc1 = re.sub(r"\\n", "", desc1)
desc1 = re.sub(r"\\r", "\n", desc1)

desc2 = re.sub(r"\\t", "", desc2)
desc2 = re.sub(r"\\n", "", desc2)
desc2 = re.sub(r"\\r", "\n", desc2)

dotd_summary = desc1 + "\n" + desc2

## dotd_summary contains the book summary ##
print(dotd_summary)

dotd_image = soup.find('div', {'class': 'dotd-main-book-image'})
im = dotd_image.find('img')['src']
dotd_image = 'http:'+im
print(dotd_image)

## dotd_image contains the url for image ##

#sending slack notification

channel = 'packt-tracer'
token = key.token
sc = SlackClient(token)

image_url = dotd_image
attachments = attachments = [{"title": dotd_title,
                              "image_url": image_url}]
date = str(strftime("%A, %d %b %Y"))
date = "[{}] {}".format(date, dotd_title)
link = "Click to download: "+url
message = date + '\n\n' + dotd_summary + '\n' + link

sc.api_call('chat.postMessage', channel=channel, text=message, username='Packt Bot', icon_emoji=':robot_face:', attachments=attachments)

print('Success!')
