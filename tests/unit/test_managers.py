# -*- coding: utf-8 -*-

import datetime as dt

from django.contrib.auth.models import User
from django.utils import timezone
import pytest

from account_actions.models import AccountActionToken
from account_actions.test.factories import AccountActionTokenFactory


@pytest.mark.django_db
class TestPendingManager(object):
    def test_can_return_the_pending_account_actions(self):
        # Setup
        token_1 = AccountActionTokenFactory.create()
        token_2 = AccountActionTokenFactory.create()
        token_2._meta.get_field('created').auto_now_add = False
        token_2.created = timezone.now() - dt.timedelta(days=100)
        token_2.save()
        token_2._meta.get_field('created').auto_now_add = True
        # Run
        tokens = AccountActionToken.pending_objects.all()
        # Check
        assert list(tokens) == [token_1, ]

    def test_can_return_the_pending_account_actions_for_a_specific_object(self):
        # Setup
        user_1 = User.objects.create_user(
            username='test1', password='not_secret', email='test1@exampe.com')
        user_2 = User.objects.create_user(
            username='test2', password='not_secret', email='test2@exampe.com')
        token_1 = AccountActionTokenFactory.create(content_object=user_1)
        token_2 = AccountActionTokenFactory.create(content_object=user_1)
        token_2._meta.get_field('created').auto_now_add = False
        token_2.created = timezone.now() - dt.timedelta(days=100)
        token_2.save()
        token_2._meta.get_field('created').auto_now_add = True
        AccountActionTokenFactory.create(content_object=user_2)
        token_4 = AccountActionTokenFactory.create(content_object=user_2)
        token_4._meta.get_field('created').auto_now_add = False
        token_4.created = timezone.now() - dt.timedelta(days=100)
        token_4.save()
        token_4._meta.get_field('created').auto_now_add = True
        # Run
        tokens = AccountActionToken.pending_objects.get_for_object(user_1)
        # Check
        assert list(tokens) == [token_1, ]


@pytest.mark.django_db
class TestConsumedManager(object):
    def test_can_return_the_consumed_account_actions(self):
        # Setup
        user = User.objects.create_user(
            username='test1', password='not_secret', email='test1@exampe.com')
        token_1 = AccountActionTokenFactory.create()
        AccountActionTokenFactory.create()
        token_1.consume(user)
        # Run
        tokens = AccountActionToken.consumed_objects.all()
        # Check
        assert list(tokens) == [token_1, ]

    def test_can_return_the_consumed_account_actions_for_a_specific_object(self):
        # Setup
        user_1 = User.objects.create_user(
            username='test1', password='not_secret', email='test1@exampe.com')
        user_2 = User.objects.create_user(
            username='test2', password='not_secret', email='test2@exampe.com')
        token_1 = AccountActionTokenFactory.create(content_object=user_1)
        AccountActionTokenFactory.create(content_object=user_1)
        token_3 = AccountActionTokenFactory.create(content_object=user_2)
        AccountActionTokenFactory.create(content_object=user_2)
        token_1.consume(user_1)
        token_3.consume(user_2)
        # Run
        tokens = AccountActionToken.consumed_objects.get_for_object(user_1)
        # Check
        assert list(tokens) == [token_1, ]
