import requests
import pprint
import feedparser
import time
import datetime
import json

from apps.podcast.fixtures import titles
from dateutil.parser import parse
from .models import Podcast, Category, Episode

def fetch_top_100_podcasts():
    if titles:
        print(titles)
        for title in titles:
            try:
                print(title)
                #find_and_save_podcast(title.title)
            except Exception as e:
                print('------------------------------------------')
                print('Find and save podcast failed: ', e)
                print('------------------------------------------')
    return False


def fetch_itunes_podcast_by_title(query):
    if query:
        print('------------------------------------------------------')
        print('Fetching itunes podcast by title: ', query)
        print('------------------------------------------------------')
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
        print('------------------------------------------------------')
        print('Found podcast: ', response.feed['title'])
        print('------------------------------------------------------')
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
        p, created = Podcast.objects.update_or_create(
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
    episodeList = rss.get('items', False) or rss.get('entries', False)
    if episodeList:
        print('Found episodes: ', len(episodeList))
        for episode in episodeList:
            try: 
                save_episode(episode, p)
            except Exception as error:
                print('error saving episode: ', str(error))
    else: 
        print('No episode list found.')

    return p


def extract_audio_link(episode):
    links = episode.get('links', False) or episode.get('media_content', False)
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
        if ':' in itunes_duration:
            timestr = '00:04:23'
            ftr = [3600,60,1]
            res = sum([a*b for a,b in zip(ftr, [int(i) for i in timestr.split(":")])])
            return res
        else: 
            return int(itunes_duration)
    else:
        return 0



def save_episode(episode, podcast):
    # handy - https://github.com/janw/podcast-archiver/blob/master/podcast_archiver.py
    try: 
        e, created = Episode.objects.update_or_create(
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
