======================
django-account-actions
======================

.. image:: http://img.shields.io/travis/erudit/django-account-actions.svg?style=flat-square
    :target: http://travis-ci.org/erudit/django-account-actions
    :alt: Build status

.. image:: https://img.shields.io/codecov/c/github/erudit/django-account-actions.svg?style=flat-square
    :target: https://codecov.io/github/erudit/django-account-actions
    :alt: Codecov status

*A Django application to define account-related actions in a standardized way.*

.. contents::

Requirements
------------

* Python 2.7+ or 3.3+
* Django 1.8+

Installation
------------

Just run:

.. code-block:: shell

  pip install git+git://github.com/erudit/django-account-actions.git

Once installed you just need to add ``account_actions`` to ``INSTALLED_APPS`` in your project's settings module:

.. code-block:: python

  INSTALLED_APPS = (
      # other apps
      'account_actions',
  )

Then install the models:

::

    python manage.py migrate account_actions

*Congrats! You’re in!*

Usage
-----

*Django-account-actions* allows you to define account-related actions that comply with the following workflow:

* You want to give a user (identified by an e-mail address) the ability to perform an action (eg. join a team on a specific service)
* You create an action token for this user
* The user can choose to consume the token either by logging in or by creating a new account

*Django-account-actions* gives you the ability to define such actions by using a registration pattern and a well defined interface.

Defining actions
~~~~~~~~~~~~~~~~

In order to define actions you will have to write a subclass of ``account_actions.action_base.AccountActionBase`` for any action you want to create. These class-based actions must be defined inside an ``account_actions`` Python module in your Django application (just add a file called ``account_actions.py`` to an existing Django application). Finally your class-based action must be registered to the ``account_actions.action_pool.actions`` object by using its ``register`` method to be available to the global actions pool.

Each of these actions must provide a ``name`` and must define an ``execute`` method:

* The ``name`` attribute is used to identify your action in the global action pool
* The ``execute`` method is used to execute the action. For example it can add the user who consumed the action to a specific group

Let’s write a simple example. Consider we are trying to write an action that will add users to a specific Django ``Group`` instance. We could write:

.. code-block:: python

    # -*- coding utf-8 -*-

    from account_actions.action_base import AccountActionBase
    from account_actions.action_pool import actions
    from django.contrib.auth.models import Group


    class AddToDummyGroupAction(AccountActionBase):
        name = 'add-to-dummy-group'

        def execute(self, token):
            group = Group.objects.get(name='Dummy group')
            token.user.groups.add(group)


    actions.register(AddToDummyGroupAction)

The ``account_actions.action_base.AccountActionBase`` class lets you define precisely the way your action behaves (see https://github.com/erudit/django-account-actions/blob/master/account_actions/action_base.py#L41):

* you can define a landing page template that will be displayed when a user try to consume the action
* you can override ``send_notification_email`` method in order to send a notification e-mail when the action is created
* ...

Consuming actions
~~~~~~~~~~~~~~~~~

*Django-account-actions* does not provide fully functional views and templates to consume actions. Instead you have to implement your own views using the generic views provided by the ``account_actions.views.generic`` module to define how your actions can be consumed by your users.

Basically you just have to add two views to your URLs:

* a "landing" page that will display informations related to the considered action to the user before he choose to consume it (or not). This can be achieved by subclassing the ``account_actions.views.generic.AccountActionLandingView`` generic view
* a view to consume the action (see the ``account_actions.views.generic.AccountActionConsumeView`` generic view)

Authors
-------

Érudit Consortium <tech@erudit.org> and contributors_

.. _contributors: https://github.com/erudit/django-account-actions/graphs/contributors

License
-------

GNU General Public License v3 (GPLv3). See ``LICENSE`` for more details.
