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

import redis
import requests

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import (QueryDict, HttpResponse, HttpResponseBadRequest,
                         Http404, HttpResponseForbidden)
from django.template.defaultfilters import filesizeformat
from django.utils.decorators import method_decorator
from django.views.generic.base import View, TemplateView


from .utils import (update_input_counters, get_io_counters,
                    get_url_responsiveness)
from .models import Target, Source, Group
from .parsers import all_parsers
from .tasks import resend, resend_low

url_validator = URLValidator()
capitalize = lambda s: s[0].upper() + s[1:]


class DashboardView(TemplateView):

    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['targets'] = Target.objects.all()
        context['sources'] = Source.objects.all()
        context['groups'] = Group.objects.all()
        source_id = self.request.GET.get('source')
        if source_id:
            try:
                context['source_found'] = Source.objects.get(id=source_id)
            except Source.DoesNotExist:
                context['source_not_found'] = source_id
        return context

    def head(self, request, *args, **kwargs):
        response = HttpResponse()
        response['AmigoProxy'] = 'yes'  # Avoid loops
        return response

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(DashboardView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        for Parser in all_parsers:
            source_id = Parser().get_id(request.body)
            if source_id:
                break
        else:  # Didn't break
            return HttpResponse('Invalid')
        source, _ = Source.objects.get_or_create(name=source_id)
        r = redis.Redis()
        update_input_counters(len(request.body), r)
        all_targets = set()
        for group in source.all_groups():
            for target in group.targets.all():
                all_targets.add(target)
        for target in all_targets:
            responsiveness = get_url_responsiveness(target.url, r)
            if responsiveness < -settings.EXPECTED_CONCURRENCY:
                resend_low.delay(target.url, request.body)
            else:
                resend.delay(target.url, request.body)
        return HttpResponse('Ok')


pluralize = lambda r: '1 POST' if str(r) == '1' else '%s POSTs' % r


def io_counters(request, *args, **kwargs):
    (s_data_in, s_count_in, s_data_out, s_count_out,
     m_data_in, m_count_in, m_data_out, m_count_out) = get_io_counters()
    return HttpResponse(','.join((
        filesizeformat(s_data_in), pluralize(s_count_in),
        filesizeformat(s_data_out), pluralize(s_count_out),
        filesizeformat(m_data_in), pluralize(m_count_in),
        filesizeformat(m_data_out), pluralize(m_count_out),
    )))


class BaseView(View):

    model = None

    def get_object(self, id, strict=True):
        try:
            return self.model.objects.get(id=id)
        except self.model.DoesNotExist:
            if strict:
                raise Http404('Not found')
            return None


class DeleteMixin():

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden('Not authenticated')
        DELETE = QueryDict(request.body)
        id = DELETE.get('id')
        if not id:
            return HttpResponseBadRequest('id not found in request')
        self.get_object(id).delete()
        return HttpResponse('Ok')


class TargetsView(DeleteMixin, BaseView):

    model = Target

    def post(self, request, *args, **kwargs):
        if request.POST.get('method') == 'DELETE':
            return self.delete(request, *args, **kwargs)
        if not request.user.is_authenticated():
            return HttpResponseForbidden('Not authenticated.')
        id = request.POST.get('id')
        name, url = request.POST.get('name'), request.POST.get('url')
        if not id:  # New target
            if not name or not url:
                return HttpResponseBadRequest('Both name and URL are required')
            target = Target()
        else:
            target = self.get_object(id)
        if name:
            target.name = capitalize(name)
        if url:
            if not url.startswith('http'):
                url = 'http://%s' % url
            try:
                url_validator(url)
                response = requests.head(url)
            except ValidationError:
                return HttpResponseBadRequest('This is not a valid URL')
            except requests.exceptions.RequestException:
                return HttpResponseBadRequest('This URL is not accessible')
            if response.headers.get('AmigoProxy') == 'yes':
                return HttpResponseBadRequest('AmigoProxy cannot be a target')
            target.url = url
        target.save()
        return HttpResponse('Ok')


class SourcesView(BaseView):

    model = Source

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden('Not authenticated.')
        id, group_id = request.POST.get('id'), request.POST.get('group_id')
        if not id or not group_id:
            return HttpResponseBadRequest('Both id and group_id are required')
        source = self.get_object(id)
        if request.POST.get('method') == 'DELETE':
            source.groups.remove(group_id)
        else:
            source.groups.add(group_id)
        return HttpResponse('Ok')


class GroupsView(DeleteMixin, BaseView):

    model = Group

    def post(self, request, *args, **kwargs):
        if request.POST.get('method') == 'DELETE':
            return self.delete(request, *args, **kwargs)
        if not request.user.is_authenticated():
            return HttpResponseForbidden('Not authenticated.')
        id = request.POST.get('id')
        name, targets = request.POST.get('name'), request.POST.get('targets')
        default = request.POST.get('default')
        if not id:  # New group
            if not name:
                return HttpResponseBadRequest('Group name cannot be empty')
            group = Group()
        else:
            group = self.get_object(id)
        if name or default != group.default:
            if name:
                group.name = capitalize(name)
            group.default = bool(default)
            group.save()
        if targets is not None:
            group.targets.clear()
            if targets:
                group.targets.add(*targets.split(','))
        return HttpResponse('Ok')
