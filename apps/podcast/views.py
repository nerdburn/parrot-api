from django.http import HttpResponse
from rest_framework import generics, permissions
from django.conf import settings


class FetchView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        from apps.podcast import tasks
        tasks.fetch_itunes_podcast('american life')
        return HttpResponse('Done')