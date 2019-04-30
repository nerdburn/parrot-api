from django.contrib.auth import get_user_model
from django.db import models

from apps.podcast.models import Podcast, Episode

class Moment(models.Model):
  user = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE,
      related_name='moments'
  )
  episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
  podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
  start_second = models.PositiveIntegerField() # does this accept 0? 
  end_second = models.PositiveIntegerField()
  short_code = models.SlugField()
  created_at = models.DateTimeField()
  rehypes_count = models.PositiveIntegerField() # best place to put this? 
  listen_count = models.PositiveIntegerField()
  like_count = models.PositiveIntegerField()