# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import AccountActionToken


class AccountActionTokenAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'key', 'email', 'first_name', 'last_name', 'action', 'is_canceled', 'expiration_date',
        'is_expired', 'is_consumed', )
    list_display_links = ('id', 'key', 'email', )
    list_filter = ('action', 'is_canceled', )
    search_fields = ('email', 'first_name', 'last_name', )


admin.site.register(AccountActionToken, AccountActionTokenAdmin)
