#! /usr/bin/env python3
import configparser
import requests
from discord.ext import commands
import json
import asyncio
import time
from datetime import datetime
from dateutil import parser

latest_check = time.time()

config = configparser.ConfigParser()
config.read('config.ini')

fb_key2 = config['keys']['fb_token']
fb_test = config['keys']['fb_test']
token = config['keys']['discord']
chan = config['keys']['chan']
refresh_rate = int(config['keys']['refresh_rate'])

bot = commands.Bot(command_prefix='?', description='Jean Plancher')

def get_posts():
    r = requests.get("https://graph.facebook.com/v14.0/FlyingWhalesBDE/posts?access_token="+fb_test+"&format=json&method=get&pretty=0&suppress_http_code=1&transport=cors")
    return json.loads(r.text)["data"]
    #r = requests.get("https://graph.facebook.com/v14.0/LTUESymposium/posts?access_token="+fb_key2+"&format=json&method=get&pretty=0&suppress_http_code=1&transport=cors")
    #return json.loads(r.text)["data"]

def check_time(post):
    dt = parser.isoparse(post['created_time']).timestamp()
    return ("created_time" in post and latest_check < dt < latest_check + refresh_rate)

async def post_new_stuff(ctx = None):
    for post in get_posts():
        if ("message" in post and "id" in post and check_time(post)):
            if (ctx is not None):
                await ctx.channel.send(post['message'])
            else:
                await bot.get_channel(int(chan)).send(post['message'])
    latest_check = time.time()
    print("latest check set to : " + str(latest_check))

async def schedule(fn):
    while True:
        await asyncio.gather(
            asyncio.sleep(refresh_rate),
            fn(),
        )


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')
    await asyncio.create_task(schedule(post_new_stuff))

@bot.command(name='LTUE', pass_context='true')
async def LTUE(ctx):
    await post_new_stuff(ctx)

bot.run(token)