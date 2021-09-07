import csv
from os import write
import time
from googleapiclient.discovery import build
import requests
import sys

api_key = "AIzaSyD4XgHiLKFQRH2d9h-OBYQ0dskStxDwFwI"

country_code = "ID"

snippet_features = ["title",
                    "publishedAt",
                    "channelId",
                    "channelTitle",
                    "categoryId"]

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
    channel_id = snippet.get("channelId")
    channel = snippet.get("channelTitle")
    title = snippet.get("title")


    lines.append([channel_id,                                                             # 
                 title,channel,upload_date,"-"])
    # lines = [video_id, ]
    # line = [video_id] + features + [prepare_feature(x) for x in [trending_date, tags, view_count, likes, dislikes,
    #                                                              comment_count, thumbnail_link, comments_disabled,
    #                                                              ratings_disabled, description]]
    # lines.append(",".join(line))

    print(snippet)
writer.writerow(head)
for d in lines:
    writer.writerow(d)
file.close
# print(data)