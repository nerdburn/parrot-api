from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    def __str__(self):
       return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

  
class Podcast(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)
    artwork_url = models.URLField()
    feed_url = models.URLField()
    link = models.URLField()
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    last_synced_date = models.DateTimeField(default=now(), blank=True)

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Podcast.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
    
    def __str__(self):
       return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Episode(models.Model): 
    podcast = models.ForeignKey('Podcast', null=False, blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    content_snippet = models.TextField()
    published_date = models.DateTimeField()
    link = models.URLField()
    audio_url = models.URLField()
    duration_seconds = models.DurationField()

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Episode.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
    
    def __str__(self):
       return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
