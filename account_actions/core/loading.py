# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from importlib import import_module
from importlib.machinery import PathFinder

from django.conf import settings


def load(modname):
    """ Loads all the modules that are named 'modname' from all the installed applications. """

    def _get_module(app, modname):
        # Find out the app's __path__
        try:
            app_path = import_module(app).__path__
        except AttributeError:  # pragma: no cover
            return

        # Use importlib's PathFinder().find_spec() to find the app's modname.py
        if PathFinder().find_spec(modname, app_path) is None:
            return

        # Import the app's module file
        import_module('{}.{}'.format(app, modname))

    for app in settings.INSTALLED_APPS:
        _get_module(app, modname)
