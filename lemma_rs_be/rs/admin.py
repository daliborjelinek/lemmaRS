from django.contrib import admin

# Register your models here.

from .models import Resource, Tag, User, Project, ProjectGroup

admin.site.register(Resource)
admin.site.register(Tag)
admin.site.register(User)
admin.site.register(Project)
admin.site.register(ProjectGroup)
