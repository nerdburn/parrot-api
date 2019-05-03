import requests
import pprint
import feedparser
from datetime import datetime
import time
from dateutil.parser import parse

from .models import Podcast, Category, Episode


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
        print('Found podcast: ', response.feed['title'])
        return response
    else: 
        print('An error has occurred.')
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
    
    # save the episodes
    try: 
        episodeList = rss.get('items', False) or rss.get('entries', False)
        if episodeList:
            print('Found episodes: ', len(episodeList))
            item = episodeList[1]
            save_episode(item, p)
        else: 
            print('No episode list found.')
    except Exception as error:
        print('error saving episode: ', error)


def extract_audio_link(episode):
    links = episode.get('links', False) or episode.get('media_content', False)
    print('links object:', links)
    url = None
    if links:
        for link in links:
            if 'type' in link.keys():
                if link['type'].startswith('audio'):
                    url = link['href']
    return url


def extract_episode_link(episode):
    link = episode.get('link', False)
    links = episode.get('links', False)
    content = episode.get('content', False)
    url = None
    if link:
        url = link
    elif links:
        for link in links:
            if 'type' in link.keys():
                if link['type'].startswith('text'):
                    url = link['href']
    if not url:
        url = content[0]['base']
    return url


def extract_duration_in_seconds(episode):
    # 'itunes_duration': '00:36:18'
    # 'itunes_duration': '841'
    itunes_duration = episode.get('itunes_duration', '')
    duration = ''
    if itunes_duration:
        duration = itunes_duration
    x = time.strptime(duration.split(',')[0],'%H:%M:%S')
    return datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()


def save_episode(episode, podcast):
    # handy - https://github.com/janw/podcast-archiver/blob/master/podcast_archiver.py
    print('-----------')
    print('attempting to save episode: ', episode['title'])
    pprint.pprint(episode)
    print('link:', extract_episode_link(episode))
    print('audio: ', extract_audio_link(episode))
    print('duration: ', extract_duration_in_seconds(episode))
    print('-----------')

    try: 
        e = Episode.objects.update_or_create(
            podcast = podcast,
            title = episode.get('title', False) or episode.get('ttl', None),
            content = episode.get('itunes_summary', False) or episode.get('summary', None),
            content_snippet = episode.get('itunes_summary', False) or episode.get('summary', None),
            published_date = parse(episode.get('published', None)),
            link = extract_episode_link(episode),
            audio_url = extract_audio_link(episode),
            duration_seconds = extract_duration_in_seconds(episode),
        )
        e.save()
    except Exception as e:
        print('error saving episode: ', e)
