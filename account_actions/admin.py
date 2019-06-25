# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .models import AccountActionToken


class AccountActionTokenAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'key', 'email', 'first_name', 'last_name', 'action', 'is_canceled', 'expiration_date',
        'is_expired', 'is_consumed', )
    list_display_links = ('id', 'key', 'email', )
    list_filter = ('action', 'is_canceled', )
    search_fields = ('email', 'first_name', 'last_name', )
    actions = ('cancel', 'uncancel', )

    def cancel(self, request, queryset):
        queryset.update(is_canceled=True)
    cancel.short_description = _('Cancel selected %(verbose_name_plural)s')

    def uncancel(self, request, queryset):
        queryset.update(is_canceled=False)
    uncancel.short_description = _('Uncancel selected %(verbose_name_plural)s')


admin.site.register(AccountActionToken, AccountActionTokenAdmin)
