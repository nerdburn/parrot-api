import requests
import pprint
import feedparser

from apps.podcast.models import Podcast, Category


def fetch_itunes_podcast_by_title(query):
    if query:
        print('Fetching itunes podcast by title: ', query)
    else:
        print('Missing title.')
        return False

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
        return data['results'][0]
    else: 
        print('No podcast found.')
        return False


def fetch_rss_podcast_by_feed_url(feedUrl):
    # https://www.tutorialspoint.com/python/python_reading_rss_feed.htm
    print('Fetching RSS feed: ', feedUrl)
    response = feedparser.parse(feedUrl)
    if response:
        if (len(response.entries) > 0):
            print('Entries found:', len(response.entries))
        return response
    else: 
        print('An error has occurred.')
        return False


def save_podcast(iTunesPodcast):

    if not iTunesPodcast:
        print('Must include iTunes podcast to save, aborting.')
        return False

    try:
        response = fetch_rss_podcast_by_feed_url(iTunesPodcast['feedUrl'])
        rssPodcast = response.feed
    except Exception as e: 
        print('e: ', e)
        return False

    try:

        c = Category.objects.update_or_create(name=iTunesPodcast['primaryGenreName'])
        podcast = Podcast(
            artwork_url = iTunesPodcast['artworkUrl600'],
            feed_url = iTunesPodcast['feedUrl'],
            link = rssPodcast['link'],
            title = rssPodcast['title'],
            description = rssPodcast['description'],
            category = c[0]
        )
        podcast.save()
    except Exception as e: 
        print('Failed to save: ', e)
        return False


def find_and_save_podcast(title):
    
    # Find podcast on iTunes
    iTunesPodcast = fetch_itunes_podcast_by_title(title)
    if not iTunesPodcast:
        return False
    else:
        print('------------------')
        pprint.pprint(iTunesPodcast)
        print('------------------')

    return save_podcast(iTunesPodcast)
