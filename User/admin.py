from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active')
    search_fields = ('email', 'username')
    list_editable = ('is_active',)
    list_filter = ('is_active',)


admin.site.register(User, UserAdmin)
