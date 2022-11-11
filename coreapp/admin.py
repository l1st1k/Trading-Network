from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


def debt_remove(modeladmin, request, queryset):
    queryset.update(debt=0)


debt_remove.short_description = 'Remove debt from Units'


class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'network', 'provider_link', 'unit_type', 'debt', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('unit_type', 'created_at', 'address__city', 'network')
    actions = (debt_remove,)

    def provider_link(self, obj):
        if obj.provider:
            return mark_safe(f'<a href="/admin/coreapp/unit/{obj.provider.id}/change/">{obj.provider.name}</a>')

    provider_link.short_description = 'provider'


class NetworkAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'release_date')
    search_fields = ('name', 'model')
    list_editable = ('release_date',)
    list_filter = ('release_date',)


class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'city', 'street', 'house_number')
    search_fields = ('country', 'city', 'street', 'house_number')
    list_filter = ('country',)


admin.site.register(Unit, UnitAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Network, NetworkAdmin)
