import csv
from os import write
import time
from typing import Text
from googleapiclient.discovery import build
import requests
import sys
import configparser
import mysql.connector
import argparse

# print(config.sections())

mydba = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="mydatabase"
)


# print(db)
cursor = mydba.cursor()
cursor.execute("DROP TABLE IF EXISTS trend ")
sql = "CREATE TABLE trend (id INT AUTO_INCREMENT PRIMARY KEY,channelId VARCHAR(255),judul VARCHAR(255),channelName VARCHAR(255),publishedAt VARCHAR(255))"
cursor.execute(sql)

api_key = "AIzaSyD4XgHiLKFQRH2d9h-OBYQ0dskStxDwFwI"
#Ganti dengan api masing masing,kalo mau hehe
country_code = "ID"

snippet_features = ["title",
                    "publishedAt",
                    "channelId",
                    "channelTitle"]

unsafe_characters = ['\n', '"']

def prepare_feature(feature):
    for ch in unsafe_characters:
        feature = str(feature).replace(ch, "")
    return f'"{feature}"'


def api_req():
    url = f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet&chart=mostPopular&regionCode={country_code}&maxResults=50&key={api_key}"
    request = requests.get(url)
    if request.status_code == 429:
        print("Temp-Banned due to excess requests, please wait and continue later")
        sys.exit()
    return request.json()

# response = api_req()
# print(response)


def get_tags(tags_list):
    # Takes a list of tags, prepares each tag and joins them into a string by the pipe character
    return prepare_feature("|".join(tags_list))


# print(api_req)
video_data_page = api_req()
items = video_data_page.get('items', [])

# jalan = request.execute()
# print(jalan)

# print(items)

file = open('result/youtube_trending.csv', 'w', newline='', encoding='utf8')
writer = csv.writer(file)
head = ["channel id", "title","channel name",
        "waktu publish"]

lines = []
for video in items:
    comments_disabled = False
    ratings_disabled = False
    if "statistics" not in video:
        continue

    video_id = prepare_feature(video['id'])

    snippet = video['snippet']
    statistics = video['statistics']

    features = [prepare_feature(snippet.get(feature, ""))
                for feature in snippet_features]

    upload_date = snippet.get("publishedAt")
    channelid = snippet.get("channelId")
    channel = snippet.get("channelTitle")
    title = snippet.get("title")
    value = title.replace("'", "''")


    lines.append([channelid,title,channel,upload_date])

    mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="mydatabase"
)

    cursor = mydb.cursor()
    cursor.execute(f"INSERT INTO `trend`(`channelId`, `judul`, `channelName`, `publishedAt`) VALUES ('{channelid}','{value}','{channel}','{upload_date}')")

    mydb.commit()
    mydb.close()
    cursor.close()
    
writer.writerow(head)
for d in lines:
    writer.writerow(d)
file.close
# print(data)