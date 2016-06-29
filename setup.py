# -*- coding: utf-8 -*-

from os.path import abspath
from os.path import dirname
from os.path import join
from setuptools import find_packages
from setuptools import setup
import codecs

import account_actions


def read_relative_file(filename):
    """
    Returns contents of the given file, whose path is supposed relative
    to this module.
    """
    with codecs.open(join(dirname(abspath(__file__)), filename), encoding='utf-8') as f:
        return f.read()


setup(
    name='django-account-actions',
    version=account_actions.__version__,
    author='Érudit Consortium',
    author_email='tech@erudit.org',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/erudit/django-account-actions',
    license='GPLv3',
    description='A Django application to define account-related actions in a standardized way',
    long_description=read_relative_file('README.rst'),
    zip_safe=False,
    install_requires=[
        'django>=1.8',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
