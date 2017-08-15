from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from .models import sys_importdatei, user_verzeichniss, group_verzeichniss

admin.site.register(sys_importdatei)

class UserVerzeichnissInline(admin.StackedInline):
    model = user_verzeichniss
    extra = 0

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserVerzeichnissInline, )

class GroupVerzeichnissInline(admin.StackedInline):
    model = group_verzeichniss
    extra = 0

# Define a new User admin
class GroupAdmin(BaseGroupAdmin):
    inlines = (GroupVerzeichnissInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Re-register GroupAdmin
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
