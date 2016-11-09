from django.contrib import admin

# Register your models here.

# import the posts to the admin view 
from .models import Post

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "timestamp", "updated"]
    list_display_links = ["title", "updated"]
    list_filter = ["title", "timestamp"]
    search_fields = ["title"]
    
    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)