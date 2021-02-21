from django.contrib import admin

# Register your models here.

from .models import Resource, Tag, User

admin.site.register(Resource)
admin.site.register(Tag)
admin.site.register(User)
