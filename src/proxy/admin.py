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

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdmin_
from django.contrib.auth.models import User, Group as UserGroup
from django.utils.translation import ugettext_lazy as _

from .models import Target, Source, Group


class UserAdmin(UserAdmin_):

    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
                                       'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


class TargetAdmin(admin.ModelAdmin):

    list_display = ('name', 'url')
    fields = ('id', 'name', 'url')
    readonly_fields = ('id',)


class GroupAdmin(admin.ModelAdmin):

    list_display = ('name', 'default', 'targets_', 'number_of_sources')
    fields = ('id', 'name', 'default', 'targets', 'sources')
    readonly_fields = ('id',)
    filter_horizontal = ('targets', 'sources',)

    def targets_(self, obj):
        return obj.targets_str(limit=5)

    def number_of_sources(self, obj):
        return obj.sources.count()


class SourceAdmin(admin.ModelAdmin):

    readonly_fields = ('id',)
    fields = ('id', 'name')
    search_fields = ('id', 'name')


admin.site.unregister(UserGroup)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Target, TargetAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Group, GroupAdmin)
