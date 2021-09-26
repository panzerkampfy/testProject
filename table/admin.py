from django.contrib import admin

from .models import *

admin.site.register(Task)
admin.site.register(Column)
admin.site.register(Board)
admin.site.register(PermissionOnBoard)
admin.site.register(User)
