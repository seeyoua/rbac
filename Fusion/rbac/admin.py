from django.contrib import admin

# Register your models here.
from .models import UserInfo, Menu, Permission, Role

admin.site.register(UserInfo)
admin.site.register(Menu)
admin.site.register(Permission)
admin.site.register(Role)