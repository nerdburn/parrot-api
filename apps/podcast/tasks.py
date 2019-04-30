import requests
import pprint

def fetch_itunes_podcast(query):
    URL = "http://itunes.apple.com/search"
    OPTIONS = {
        'country': 'us',
        'media': 'podcast',
        'entity': 'podcast',
        'term': query,
        'limit': 20
    }
    response = requests.get(url = URL, params = OPTIONS)

    if response: 
        data = response.json()
        pprint.pprint(data['results'][0])
    else: 
        print('An error has occurred.')
    # data = r.json()
    # pprint.pprint(data['results'][0])


def fetch_rss_podcast(feedUrl):
    print('Fetching RSS feed: ', feedUrl)