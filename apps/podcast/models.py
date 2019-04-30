from django.contrib.auth import get_user_model
from django.db import models

class Category(models.Model): 
  title = models.CharField(max_length=30)
  slug = models.SlugField()
  
class Podcast(models.Model):
  category = models.ManyToManyField(Category)
  artwork_url = models.URLField()
  feed_url = models.URLField()
  link = models.URLField()
  title = models.CharField(max_length=100)
  slug = models.SlugField()
  description = models.TextField()
  last_synced_date = models.DateTimeField()

class Episode(models.Model): 
  podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
  title = models.CharField(max_length=100)
  slug = models.SlugField()
  content = models.TextField()
  content_snippet = models.CharField(max_length=200)
  published_date = models.DateTimeField()
  link =  models.URLField()
  audio_url = models.URLField()
  duration_seconds = models.DurationField()