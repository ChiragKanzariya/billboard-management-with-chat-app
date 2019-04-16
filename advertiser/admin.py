from django.contrib import admin

from advertiser.models import Post


class PostAdmin(admin.ModelAdmin):
    pass
admin.site.register(Post, PostAdmin)