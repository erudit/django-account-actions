# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import Http404
from django.test import RequestFactory
import pytest

from account_actions.action_base import AccountActionBase
from account_actions.action_pool import actions
from account_actions.test.factories import AccountActionTokenFactory
from account_actions.views.generic import AccountActionLandingView
from account_actions.views.generic import AccountActionConsumeView


class Action1(AccountActionBase):
    name = 'action-1'

    def execute(self, method):  # pragma: no cover
        pass


class Action2(AccountActionBase):
    name = 'action-2'
    landing_page_template_name = 'action-2.html'

    def execute(self, method):  # pragma: no cover
        pass


@pytest.mark.django_db
class TestAccountActionLandingView(object):
    @pytest.yield_fixture(autouse=True)
    def setup(self):
        self.factory = RequestFactory()
        yield
        actions.unregister_all()

    def test_return_an_http_404_error_if_the_token_cannot_be_found(self):
        # Setup
        view = AccountActionLandingView.as_view()
        request = self.factory.get('/')
        # Run & check
        with pytest.raises(Http404):
            view(request, key='dummy')

    def test_return_an_http_404_error_if_the_token_action_is_not_registered(self):
        # Setup
        token = AccountActionTokenFactory.create()
        view = AccountActionLandingView.as_view()
        request = self.factory.get('/')
        # Run & check
        with pytest.raises(Http404):
            view(request, key=token.key)

    def test_embeds_the_action_configuration_into_the_context(self):
        # Setup
        actions.register(Action1)
        token = AccountActionTokenFactory.create(action='action-1')

        user = User.objects.create_user(
            username='test', password='not_secret', email='test@exampe.com')
        request = self.factory.get('/')
        request.user = user

        view = AccountActionLandingView.as_view()

        # Run
        response = view(request, key=token.key)

        # Check
        assert response.status_code == 200
        assert isinstance(response.context_data['action'], Action1)

    def test_can_use_the_template_specified_in_the_action_configuration(self):
        # Setup
        actions.register(Action2)
        token = AccountActionTokenFactory.create(action='action-2')

        user = User.objects.create_user(
            username='test', password='not_secret', email='test@exampe.com')
        request = self.factory.get('/')
        request.user = user

        view = AccountActionLandingView.as_view()

        # Run
        response = view(request, key=token.key)

        # Check
        assert response.status_code == 200
        assert response.template_name == ['action-2.html', ]


@pytest.mark.django_db
class TestAccountActionConsumeView(object):
    @pytest.yield_fixture(autouse=True)
    def setup(self):
        self.factory = RequestFactory()
        yield
        actions.unregister_all()

    def test_return_an_http_403_error_if_the_user_is_not_authenticated(self):
        # Setup
        actions.register(Action1)
        token = AccountActionTokenFactory.create(action='action-1')

        request = self.factory.post('/')
        request.user = AnonymousUser()

        view = AccountActionConsumeView.as_view()

        # Run & check
        with pytest.raises(PermissionDenied):
            view(request, key=token.key)

    def test_return_an_http_403_error_if_the_action_cannot_be_consumed(self):
        # Setup
        actions.register(Action1)
        token = AccountActionTokenFactory.create(action='action-1')

        user = User.objects.create_user(
            username='test', password='not_secret', email='test@exampe.com')
        token.consume(user)

        request = self.factory.post('/')
        request.user = user

        view = AccountActionConsumeView.as_view()

        # Run & check
        with pytest.raises(PermissionDenied):
            view(request, key=token.key)

    def test_return_an_http_403_error_if_the_token_is_canceled(self):
        # Setup
        actions.register(Action1)
        token = AccountActionTokenFactory.create(action='action-1', is_canceled=True)

        user = User.objects.create_user(
            username='test', password='not_secret', email='test@exampe.com')

        request = self.factory.post('/')
        request.user = user

        view = AccountActionConsumeView.as_view()

        # Run & check
        with pytest.raises(PermissionDenied):
            view(request, key=token.key)

    def test_can_consume_an_action_token(self):
        # Setup
        actions.register(Action1)
        token = AccountActionTokenFactory.create(action='action-1')

        user = User.objects.create_user(
            username='test', password='not_secret', email='test@exampe.com')

        session_middleware = SessionMiddleware()
        message_middleware = MessageMiddleware()
        request = self.factory.post('/')
        session_middleware.process_request(request)
        message_middleware.process_request(request)
        request.user = user

        view = AccountActionConsumeView.as_view()

        # Run
        response = view(request, key=token.key)

        # Check
        assert response.status_code == 302
        token.refresh_from_db()
        assert token.is_consumed
