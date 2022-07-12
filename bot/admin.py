from django.contrib import admin

# Register your models here.
from .models import User, Post, Video

admin.site.site_header = "Kozimxon To'rayev"
print(admin.site.actions)
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Video)