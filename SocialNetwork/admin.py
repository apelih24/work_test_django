from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'post_text', 'pub_date', 'likes', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['post_text']


admin.site.register(Post, PostAdmin)
