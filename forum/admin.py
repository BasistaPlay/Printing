from django.contrib import admin
from .models import ForumCategory, Thread, Post

admin.site.register(ForumCategory)
admin.site.register(Thread)
admin.site.register(Post)