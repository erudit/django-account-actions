# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountActionToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Update date')),
                ('active', models.BooleanField(default=True, verbose_name='Is active')),
                ('consumption_date', models.DateTimeField(null=True, blank=True, verbose_name='Consumption date')),
                ('key', models.CharField(unique=True, max_length=40)),
                ('first_name', models.CharField(null=True, blank=True, max_length=30, verbose_name='First name')),
                ('last_name', models.CharField(null=True, blank=True, max_length=30, verbose_name='Last name')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail address')),
                ('action', models.CharField(max_length=100, verbose_name='Action')),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('content_type', models.ForeignKey(null=True, blank=True, verbose_name='Type', to='contenttypes.ContentType')),
                ('user', models.ForeignKey(null=True, blank=True, verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Account action tokens',
                'verbose_name': 'Account action token',
            },
        ),
    ]
