import tweepy
import requests
from bs4 import BeautifulSoup
import re
import webbrowser
import urllib.parse
import keys

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
dotd_image = urllib.parse.quote_plus(dotd_image)

## dotd_image contains the url for image ##

auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_SECRET)

api = tweepy.API(auth)

auth_url = auth.get_authorization_url()

webbrowser.open(auth_url)
print("Get the PIN from the window")

verifier = input("PIN: ").strip()
auth.get_access_token(verifier)

access_key = auth.access_token
access_secret = auth.access_token_secret

auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

api.send_direct_message(screen_name = 'veedhee_', text = 'PACKT BOOK OF THE DAY: '+ dotd_title)
api.send_direct_message(screen_name = 'veedhee_', text = dotd_summary)
api.send_direct_message(screen_name = 'veedhee_', text = dotd_image)
