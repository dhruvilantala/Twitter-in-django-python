from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import *

# Register your models here.

admin.site.unregister(Group)

# mix profile info in to user info
class ProfileInline(admin.StackedInline):
    model = Profile


# extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    # just display username fields on admin page
    fields = ['username']
    inlines = [ProfileInline] 

# unregister initial user
admin.site.unregister(User)
# register user
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)
admin.site.register(Meep)
admin.site.register(Comment)