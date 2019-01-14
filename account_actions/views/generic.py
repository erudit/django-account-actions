# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.http import HttpResponseRedirect
from django.utils.functional import cached_property
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin

from ..action_pool import actions
from ..models import AccountActionToken

logger = logging.getLogger(__name__)


class AccountActionTokenMixin(SingleObjectMixin):
    context_object_name = 'token'
    key_url_kwargs = 'key'
    model = AccountActionToken

    def get_context_data(self, **kwargs):
        context = super(AccountActionTokenMixin, self).get_context_data(**kwargs)
        context['action'] = self.action
        context.update(self.action.get_extra_context(self.object, self.request.user))
        return context

    def get_action(self):
        """ Returns the action associated with the current token.

        If no actions can be found, an HTTP 404 error is returned.
        """
        action = actions.get_action(self.get_object().action)
        if not action:
            logger.error(
                'Unable to find the following action: {}'.format(self.object.action),
                exc_info=True, extra={'request': self.request, })
            # If the action is not configured, we should raise an HTTP 404 error because no action
            # can be executed for the current token.
            raise Http404
        return action

    def get_object(self, queryset=None):
        if queryset is None:  # pragma: no cover
            queryset = self.get_queryset()

        key = self.kwargs.get(self.key_url_kwargs)
        queryset = queryset.filter(key=key)

        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404

        return obj

    def get_token(self):
        return self.get_object()

    action = cached_property(get_action)
    token = cached_property(get_token)


class AccountActionLandingView(AccountActionTokenMixin, SingleObjectTemplateResponseMixin, View):
    """
    This views provides a "landing" page in order to consume an action.
    """
    http_method_names = ['get', ]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_template_names(self):
        if self.action.landing_page_template_name:
            return [self.action.landing_page_template_name, ]
        return super(AccountActionLandingView, self).get_template_names()


class AccountActionConsumeView(AccountActionTokenMixin, View):
    """
    This views can be used to "consume" an account action token. It will associate the token with
    the current user and execute the proper operations related to the considered action.
    """
    http_method_names = ['post', ]

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            raise PermissionDenied
        return super(AccountActionConsumeView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self):
        messages.success(
            self.request, self.action.get_consumption_success_message(self.object))
        return self.action.get_consumption_redirect_url(self.object)

    def has_permission(self):
        return self.request.user.is_authenticated \
            and self.action.can_be_consumed(self.get_object(), self.request.user)

    def post(self, request, *args, **kwargs):
        self.request = request
        self.object = self.get_object()
        self.object.consume(request.user)
        return HttpResponseRedirect(self.get_redirect_url())
