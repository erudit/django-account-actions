# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
import pytest

from account_actions.action_base import AccountActionBase
from account_actions.action_pool import actions
from account_actions.test.factories import AccountActionTokenFactory


email_sent = False
execute_called = False


class TestEmailNotificationAction(AccountActionBase):
    name = 'test-email-notification'

    def execute(self, method):  # pragma: no cover
        pass

    def send_notification_email(self, token):
        global email_sent
        email_sent = True


class TestExecuteAction(AccountActionBase):
    name = 'test-execute'

    def execute(self, method):
        pass

    def send_notification_email(self, token):
        global execute_called
        execute_called = True


@pytest.mark.django_db
class TestSendCreationNotificationEmailReceiver(object):
    @pytest.yield_fixture(autouse=True)
    def setup(self):
        yield
        actions.unregister_all()

    def test_can_send_a_notification_on_token_creation(self):
        # Setup
        actions.register(TestEmailNotificationAction)
        # Run & check
        AccountActionTokenFactory.create(action='test-email-notification')
        assert email_sent


@pytest.mark.django_db
class TestExecuteActionReceiver(object):
    @pytest.yield_fixture(autouse=True)
    def setup(self):
        yield
        actions.unregister_all()

    def test_can_execute_the_action_after_consumption(self):
        # Setup
        actions.register(TestExecuteAction)
        token = AccountActionTokenFactory.create(action='test-execute')
        user = User.objects.create_user(
            username='test', password='not_secret', email='test@exampe.com')
        # Run & check
        token.consume(user)
        assert execute_called
