from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from coreapp.models import *
from coreapp.tasks import celery_remove_debt


def debt_remove(modeladmin, request, queryset):
    if len(queryset) > 20:
        pks = queryset.values_list('pk', flat=True)
        # TODO add .delay (celery)
        # Should be with '.delay', as below, but for now it removed for test needs.
        # p.s. haven't separated celery worker
        # celery_remove_debt.delay(pks)
        celery_remove_debt(pks)
    else:
        queryset.update(debt=0)


debt_remove.short_description = 'Remove debt from Units'


class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'network', 'provider_link', 'unit_type', 'debt', 'created_at')
    # list_display = ('name', 'email_link', 'network', 'provider_link', 'unit_type', 'debt', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('unit_type', 'created_at', 'address__city', 'network')
    actions = (debt_remove,)

    # class Media:
    #     js = ("js/script.js",)
    #
    # def email_link(self, obj):
    #     html_for_email_button = \
    #         """
    #             <html>
    #                 <head>
    #                     <meta charset="utf-8">
    #                     <base href="/">
    #                     <script src=coreapp/static/js/script.js></script>
    #                 </head>
    #                 <body>
    #                     <button onclick={{()=>copyContent('{}');}}>{}</button>
    #                 </body>
    #             </html>
    #         """
    #     return format_html(html_for_email_button, obj.email, obj.email)
    #
    # email_link.short_description = 'email'

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
