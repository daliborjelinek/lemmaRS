from django.contrib import admin

# Register your models here.

from .models import Resource, Tag, User, Project, ProjectGroup, PermissionLevel, PermissionRequest, ReservedResource, \
    Reservation


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'fullname', 'role', 'email')


admin.site.register(Resource)
admin.site.register(Tag)
admin.site.register(User, UserAdmin)
admin.site.register(Project)
admin.site.register(ProjectGroup)
admin.site.register(PermissionLevel)
admin.site.register(PermissionRequest)
admin.site.register(ReservedResource)
admin.site.register(Reservation)
