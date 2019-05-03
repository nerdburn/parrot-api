import requests
import pprint
import feedparser
from datetime import datetime
from dateutil.parser import parse

from .models import Podcast, Category


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

    # fetch RSS feed for podcast details
    try: 
        rss = fetch_rss_podcast_by_feed_url(iTunesPodcast['feedUrl'])
        rssPodcast = rss.feed
    except Exception as e:
        print('Error getting RSS feed:', e)
        return False

    # save the podcast genre from iTunes and associate it with podcast
    '''
    try:
        c = Category.objects.update_or_create(name=iTunesPodcast['primaryGenreName'])
        p = Podcast(
            artwork_url = iTunesPodcast['artworkUrl600'],
            feed_url = iTunesPodcast['feedUrl'],
            link = rssPodcast['link'],
            title = rssPodcast['title'],
            description = rssPodcast['description'],
            category = c[0]
        )
        p.save()
    except Exception as e: 
        print('Failed to save: ', e)
    '''

    try: 
        item = rss.entries[1]
        save_episode(item)
    except Exception as error:
        print('error saving episode: ', error)

    '''
    # save podcast episodes (but only if they don't exist)
    for item in rss.entries:
        try:
            e = Episode.objects.update_or_create(
                podcast = p
                title = models.CharField(max_length=100)
                slug = models.SlugField(unique=True)
                content = models.TextField()
                content_snippet = models.CharField(max_length=200)
                published_date = models.DateTimeField()
                link = models.URLField()
                audio_url = models.URLField()
                duration_seconds = models.DurationField()
            )
            e.save()
        except Exception as e:
            print('e: ', e)
    '''
        

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


def save_episode(episode):
    print('-----------')
    print('attempting to save episode: ', episode['title'])
    pprint.pprint(episode)
    print('-----------')
    print('link?', episode.get('link', episode['content'][0]['base']))
    content = episode.get('content', [{}])[0]
    print('content: ', content)
    get_date_obj = parse(episode.get('published', None))
    print('date:', get_date_obj)
    media = episode.get('media_content', [])
    print('media content: ', media)

    '''
    e = Episode.objects.update_or_create(
        podcast = p,
        title = episode.get('title', None),
        content = episode.get('itunes:subtitle', None),
        content_snippet = episode.get('itunes:summary', None)
        published_date = parse(episode.get('published', None))
        link = episode.get('link', episode['content'][0]['base'])
        audio_url = media[0]['url']
        duration_seconds = episode.get('itunes_duration', 0)
    )
    e.save()
    '''

    '''
    def to_seconds(data):
        a = data.split(':')
        seconds = 0
        multiplier = 1

        while(len(a) > 0):
            time = a.pop()
            seconds += (time * multiplier)
            multiplier *= 60
    return seconds

    def toString(totalsecs):
        sec_num = parseInt(totalsecs, 10)
        hours   = Math.floor(sec_num / 3600)
        minutes = Math.floor((sec_num - (hours * 3600)) / 60)
        seconds = sec_num - (hours * 3600) - (minutes * 60)
        if (hours   < 10) {hours   = "0"+hours; }
        if (minutes < 10) {minutes = "0"+minutes;}
        if (seconds < 10) {seconds = "0"+seconds;}
        var time = hours+':'+minutes+':'+seconds
        return time
    '''