# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 21:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0005_lookupuserinfo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lookupuserinfo',
            old_name='timezone',
            new_name='timeZone',
        ),
    ]
