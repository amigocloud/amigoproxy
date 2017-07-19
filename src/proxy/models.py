# AmigoProxy
#
# Copyright (c) 2011-2015 AmigoCloud Inc., All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this library.

import uuid

from django.db import models
from django.db.models import Q

generate_id = lambda: uuid.uuid4().hex[1:-1:3]


class Target(models.Model):

    id = models.CharField(primary_key=True, editable=False, max_length=10,
                          default=generate_id)
    name = models.CharField(max_length=100)
    url = models.URLField()
    reverse = models.BooleanField(default=True)
    response_format = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Source(models.Model):

    id = models.CharField(primary_key=True, editable=False, max_length=10,
                          default=generate_id)
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

    def all_groups(self):
        return Group.objects.filter(Q(sources=self) | Q(default=True))


class Group(models.Model):

    id = models.CharField(primary_key=True, editable=False, max_length=10,
                          default=generate_id)
    name = models.CharField(max_length=100)
    default = models.BooleanField(default=False)
    targets = models.ManyToManyField(Target, related_name='groups')
    sources = models.ManyToManyField(Source, related_name='groups')

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def targets_str(self, limit=10):
        targets = self.targets.order_by('name').values_list('name', flat=True)
        count = self.targets.count()
        if not count:
            return 'No targets'
        if count > limit:
            return ', '.join(targets[:count]) + ', ...'
        return ', '.join(targets)
