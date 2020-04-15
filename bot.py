#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import requests
import logging
import subprocess
import urllib.request
import time
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    username = update.message.chat.username
    update.message.reply_text('Hi master %s,  I\'m here to serve you!' % (username))
    logger.info("Command /start from %s" % (username))

def conferencias(update, context):
	reader = open('/home/pi/Scripts/Bots/HackerOpsBot/conferencias.txt','r')
	try:
		update.message.reply_text(reader.read())
	finally:
		reader.close()
	username = update.message.chat.username
	logger.info("Command /conferencias from %s" % (username))

def thehackernews(update, context):
	url = 'https://thehackernews.com/'
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	tags = soup.findAll('a',{"class": "story-link"})

	for tag in tags[:3]:
		update.message.reply_text(tag.get("href"))
	username = update.message.chat.username
	logger.info("Command /noticias from %s" % (username))

def threatpost(update, context):
	NewsFeed = feedparser.parse("https://threatpost.com/feed/")
	username = update.message.chat.username
	for entry in NewsFeed.entries[:3]:
		update.message.reply_text(entry.link)

def SANSInternetStormCenter(update, context):
	NewsFeed = feedparser.parse("https://isc.sans.edu/rssfeed_full.xml")
	username = update.message.chat.username
	for entry in NewsFeed.entries[:3]:
		update.message.reply_text(entry.link)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater("<API_KEY>", use_context=True)

    logger.info("Bot encendido")

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("conferencias", conferencias))
    dp.add_handler(CommandHandler("thehackernews", thehackernews))
    dp.add_handler(CommandHandler("threatpost", threatpost))
    dp.add_handler(CommandHandler("internetStormCenter", SANSInternetStormCenter))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
