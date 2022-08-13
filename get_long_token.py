#! /usr/bin/env python3
import configparser
import requests
import json

config = configparser.ConfigParser()
config.read('longtokenconfig.ini')

appid = config['fb']['appid']
csecret = config['fb']['clientsecret']
token = config['fb']['token']


r = requests.get("https://graph.facebook.com/v14.0/oauth/access_token?grant_type=fb_exchange_token&client_id="+appid+"&client_secret="+csecret+"&fb_exchange_token="+token)
print(json.loads(r.text)["access_token"])