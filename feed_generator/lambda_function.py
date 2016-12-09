# coding=utf-8

import os
import urllib2
import boto3
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import hashlib

S3_DATA_BUCKET = os.environ["S3_DATA_BUCKET"]
RSS_FEED_URL = os.environ["RSS_FEED_URL"]
TEXT_TO_SPEECH_LAMBDA = os.environ["TEXT_TO_SPEECH_LAMBDA"]
FLASH_BRIEFING_FILE = "flash_briefing_ja.json"

s3 = boto3.resource("s3")
bucket = s3.Bucket(S3_DATA_BUCKET)


def raw_text(text):
    t = BeautifulSoup(text, "html.parser").get_text()
    return t.replace(u"\xa0", " ").replace(u"\u2019", "\'")

def load_feed():
    rss_feed = urllib2.urlopen(RSS_FEED_URL)
    rss_feed = BeautifulSoup(rss_feed, "html.parser")

    yesterday = datetime.now() + timedelta(days=-1)
    news = []
    for item in rss_feed.find_all("item"):
        pub_date = datetime.strptime(item.find("pubDate").string, "%a, %d %b %Y %H:%M:%S +0000")
        if pub_date < yesterday:
            continue
        uid = hashlib.sha1(item.find("guid").string).hexdigest()
        item = {
            "uid": uid,
            "updateDate": "{}.0Z".format(pub_date.strftime("%Y-%m-%dT%H:%M:%S")),
            "titleText": raw_text(item.find("title").get_text()),
            "mainText": raw_text(item.find("description").get_text()),
            "redirectionUrl": item.find("link").string,
            "streamUrl": "https://s3-ap-northeast-1.amazonaws.com/{}/{}.mp3".format(S3_DATA_BUCKET, uid)
        }
        news.append(item)

    return news

def export_news_data(items):
    obj = bucket.Object(FLASH_BRIEFING_FILE)
    response = obj.put(
        ACL="public-read",
        Body=json.dumps(items, ensure_ascii=False),
        ContentEncoding="utf-8",
        ContentType="application/json"
    )
    print(response)

def lambda_handler(event, context):
    news = load_feed()
    export_news_data(news)

    if len(news) > 0:
        client = boto3.client('lambda')
        response = client.invoke(
            FunctionName=TEXT_TO_SPEECH_LAMBDA,
            InvocationType='Event',
            Payload=json.dumps(news)
        )
