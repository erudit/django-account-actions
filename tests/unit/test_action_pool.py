# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
import pytest

from account_actions.action_base import AccountActionBase
from account_actions.action_pool import actions
from account_actions.exceptions import ActionAlreadyRegistered


class SimpleAction(AccountActionBase):
    name = 'simpleaction'

    def execute(self, method):  # pragma: no cover
        pass


@pytest.mark.django_db
class TestAccountActionPool(object):
    @pytest.yield_fixture(autouse=True)
    def setup(self):
        yield
        actions.unregister_all()

    def test_can_register_simple_actions(self):
        # Setup
        actions_count_before = len(actions.get_actions())
        # Run
        actions.register(SimpleAction)
        # Check
        assert len(actions.get_actions()) == actions_count_before + 1
        assert SimpleAction.name in actions._registry
        assert isinstance(actions._registry[SimpleAction.name], SimpleAction)

    def test_should_raise_if_an_action_is_registered_twice(self):
        # Setup
        actions_count_before = len(actions.get_actions())
        actions.register(SimpleAction)
        # Run & check
        with pytest.raises(ActionAlreadyRegistered):
            actions.register(SimpleAction)
        actions.unregister_all()
        actions_count_after = len(actions.get_actions())
        assert actions_count_before == actions_count_after

    def test_cannot_register_a_class_which_is_not_an_action(self):
        # Setup
        actions_count_before = len(actions.get_actions())
        # Run & check
        with pytest.raises(ImproperlyConfigured):
            actions.register(type('BadClass'))
        assert len(actions.get_actions()) == actions_count_before

    def test_cannot_register_erroneous_actions(self):
        # Setup
        actions_count_before = len(actions.get_actions())
        # Run & check
        with pytest.raises(ImproperlyConfigured):
            class ErrnoneousAction1(AccountActionBase):
                pass
        with pytest.raises(ImproperlyConfigured):
            class ErrnoneousAction2(AccountActionBase):
                name = 'test'
        actions_count_after = len(actions.get_actions())
        assert actions_count_before == actions_count_after
