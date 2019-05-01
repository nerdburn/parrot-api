import requests
import pprint
import feedparser


def fetch_itunes_podcast(query):
    print('Fetching iTunes podcast: ', query)

    URL = "http://itunes.apple.com/search"
    OPTIONS = {
        'country': 'us',
        'media': 'podcast',
        'entity': 'podcast',
        'term': query,
        'limit': 1
    }

    response = requests.get(url = URL, params = OPTIONS)

    if response: 
        data = response.json()
        pprint.pprint(data['results'][0])
    else: 
        print('An error has occurred.')

    return data['results'][0]


def fetch_rss_podcast(feedUrl):
    # https://www.tutorialspoint.com/python/python_reading_rss_feed.htm
    print('Fetching RSS feed: ', feedUrl)

    response = feedparser.parse(feedUrl)

    if response: 
        pprint.pprint(response)
    else: 
        print('An error has occurred.')
