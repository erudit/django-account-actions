# -*- coding: utf-8 -*-

import datetime as dt
import factory
from faker import Factory
from django.utils import timezone

from ..core.key import gen_action_key
from ..models import AccountActionToken
from ..conf.settings import ACTION_TOKEN_VALIDITY_DURATION

faker = Factory.create()


class AccountActionTokenFactory(factory.django.DjangoModelFactory):
    key = factory.Sequence(lambda n: gen_action_key())

    email = faker.email()
    first_name = faker.first_name()
    last_name = faker.last_name()

    action = factory.Sequence(lambda n: 'action-{}'.format(n))

    class Meta:
        model = AccountActionToken


class ExpiredAccountActionTokenFactory(AccountActionTokenFactory):

    @factory.post_generation
    def post(obj, create, extracted, **kwargs):
        obj._meta.get_field('created').auto_now_add = False
        obj.created = timezone.now() - dt.timedelta(days=ACTION_TOKEN_VALIDITY_DURATION + 1)
        obj.save()
        obj._meta.get_field('created').auto_now_add = True
