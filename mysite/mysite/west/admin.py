# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import Character,Contact,Tag

# Register your models here.

admin.site.register([Character,Contact,Tag])

