# -*- coding: utf-8 -*-
import datetime as dt

from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .conf import settings as account_actions_settings
from .models import AccountActionToken


class IsExpiredFilter(admin.SimpleListFilter):
    title = _('Expired')
    parameter_name = 'is_expired'

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('Yes')),
            ('No', _('No')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        dt_limit = timezone.now() - dt.timedelta(
            days=account_actions_settings.ACTION_TOKEN_VALIDITY_DURATION)
        if value == 'Yes':
            return queryset.filter(created__lt=dt_limit)
        elif value == 'No':
            return queryset.exclude(created__lt=dt_limit)
        return queryset


class IsConsumedFilter(admin.SimpleListFilter):
    title = _('Consumed')
    parameter_name = 'is_consumed'

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('Yes')),
            ('No', _('No')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(consumption_date__isnull=False, user__isnull=False)
        elif value == 'No':
            return queryset.exclude(consumption_date__isnull=False, user__isnull=False)
        return queryset


class AccountActionTokenAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'key', 'email', 'first_name', 'last_name', 'action', 'expiration_date',
        'is_canceled', 'is_expired', 'is_consumed', )
    list_display_links = ('id', 'key', 'email', )
    list_filter = ('action', 'is_canceled', IsExpiredFilter, IsConsumedFilter, )
    search_fields = ('email', 'first_name', 'last_name', )
    actions = ('cancel', 'uncancel', )

    def is_expired(self, obj):
        return obj.is_expired
    is_expired.boolean = True
    is_expired.short_description = _('Expired')

    def is_consumed(self, obj):
        return obj.is_consumed
    is_consumed.boolean = True
    is_consumed.short_description = _('Consumed')

    def cancel(self, request, queryset):
        queryset.update(is_canceled=True)
    cancel.short_description = _('Cancel selected %(verbose_name_plural)s')

    def uncancel(self, request, queryset):
        queryset.update(is_canceled=False)
    uncancel.short_description = _('Uncancel selected %(verbose_name_plural)s')


admin.site.register(AccountActionToken, AccountActionTokenAdmin)
