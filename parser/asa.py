import requests
from aiogram import Bot, types
from sqlalchemy import exists
from data.maping import channels
from model.engine import insert_image, session
from model.models import Replay, Topic


def check_exists_url(url: str):
    is_exists = session.query(exists().where(Replay.url == url)).scalar()
    return is_exists


def get_download_content(channel):
    for key, data in channels[channel].items():
        print(channel, data)
        for tag in data:
            print(tag)
            payload = {
                "query": " query SubredditQuery( $url: String! $filter: SubredditPostFilter $iterator: String ) { getSubreddit(url: $url) { children( limit: 20 iterator: $iterator filter: $filter disabledHosts: null ) { iterator items { __typename id url title subredditId subredditTitle subredditUrl redditPath isNsfw albumUrl hasAudio fullLengthSource gfycatSource redgifsSource ownerAvatar username displayName isPaid tags isFavorite mediaSources { url width height isOptimized } blurredMediaSources { url width height isOptimized } } } } } ",
                "variables": {
                    "url": f"{tag}",
                    "filter": None,
                    "hostsDown": None
                },
                "authorization": None}

            r = requests.post(
                'https://api.scrolller.com/api/v2/graphql', json=payload)
            
            try:
                all_objects = r.json().get("data").get(
                    "getSubreddit").get("children").get("items")
                for data in all_objects:
                    print(data.get("id"))
                    print(data.get("mediaSources")[-1])
                    url = data.get("mediaSources")[-1].get("url") 
                    content_type = requests.get(url)
                    content_type = content_type.headers.get(
                        "Content-Type")
                    if not check_exists_url(url=url):
                        insert_image(
                            url=url, content_type=content_type,
                            model=Topic, chanel_id=channel
                        )
            except:
                continue


if __name__ == "__main__":
    for chanel in channels:
        get_download_content(chanel)
