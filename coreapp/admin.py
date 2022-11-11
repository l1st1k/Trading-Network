from django.contrib import admin

from .models import *


class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'provider', 'unit_type', 'debt', 'created_at')
    search_fields = ('name', 'email')
    list_editable = ('email',)
    list_filter = ('name', 'email', 'unit_type', 'created_at')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'release_date')
    search_fields = ('name', 'model')
    list_editable = ('release_date',)
    list_filter = ('name', 'release_date')


class AddressAdmin(admin.ModelAdmin):
    list_display = ('country', 'city', 'street', 'house_number')
    search_fields = ('country', 'city', 'street', 'house_number')
    list_editable = ('house_number',)
    list_filter = ('country', 'city')


admin.site.register(Unit, UnitAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Address, AddressAdmin)
