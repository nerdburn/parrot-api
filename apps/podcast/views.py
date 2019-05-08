from django.http import HttpResponse
from rest_framework import generics, permissions
from django.conf import settings
from . import tasks
from django.utils.http import urlunquote, urlquote


class FetchView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        #query = urlunquote(request.GET['query'])
        #tasks.fetch_itunes_podcast('american life')
        #tasks.fetch_rss_podcast('http://wakingup.libsyn.com/rss')
        #tasks.find_and_save_podcast(query)
        tasks.fetch_top_100_podcasts()
        return HttpResponse('Done')