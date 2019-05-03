from django.contrib import admin
from .models import Podcast, Episode, Category

admin.site.register(Episode)

@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ('title', 'last_synced_date',)
    list_display_links = ('title',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)