import requests

payload = {
    "query":" query SubredditQuery( $url: String! $filter: SubredditPostFilter $iterator: String ) { getSubreddit(url: $url) { children( limit: 50 iterator: $iterator filter: $filter disabledHosts: null ) { iterator items { __typename id url title subredditId subredditTitle subredditUrl redditPath isNsfw albumUrl hasAudio fullLengthSource gfycatSource redgifsSource ownerAvatar username displayName isPaid tags isFavorite mediaSources { url width height isOptimized } blurredMediaSources { url width height isOptimized } } } } } ",
    "variables":{"url":"/r/WhatsWrongWithYourDog","filter":None,"hostsDown":None},
    "authorization":None}

r = requests.post('https://api.scrolller.com/api/v2/graphql', json=payload)

all_objects = r.json().get("data").get("getSubreddit").get("children").get("items")
for data in all_objects:
    data.get("id")
    data.get("mediaSources")[-1]