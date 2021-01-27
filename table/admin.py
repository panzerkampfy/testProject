from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Task)
admin.site.register(Column)# сменить на статус
admin.site.register(Board)
admin.site.register(PermissionOnBoard)