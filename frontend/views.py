# Author:   Cory Nance <canance@coastal.edu>
# Revision: 6 February 2016
#
# Copyright 2016 Coastal Carolina University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from backend.models import Configuration, Device, Group


@login_required()
def index(request):
    devices = Device.objects.exclude(name__isnull=True).order_by('name')
    configs = Configuration.objects.order_by('name')

    context = {
        'devices': devices,
        'configs': configs,
    }

    return render(request, 'frontend/index.html', context)


@login_required()
def change(request):
    device_ids = request.POST.getlist('devices[]')  # device ids
    group_ids = request.POST.getlist('groups[]') # group ids
    config_id = request.POST['config']  # config id

    # make sure config is a valid id
    config = get_object_or_404(Configuration, pk=config_id)

    for device_id in device_ids:
        device = get_object_or_404(Device, pk=device_id)
        device.configuration = config
        device.save()

    for group_id in group_ids:
        group = get_object_or_404(Group, pk=group_id)
        for device in group.devices.all():
            device.configuration = config
            device.save()

    return HttpResponseRedirect(reverse('frontend:index'))


@login_required()
def cast(request):
    devices = Device.objects.order_by('name')
    groups = Group.objects.order_by('name')
    configs = Configuration.objects.order_by('name')

    castable = True if len(configs) != 0 and len(devices) != 0 else False

    context = {
        'devices': devices,
        'groups': groups,
        'configs': configs,
        'castable': castable,
    }

    return render(request, 'frontend/cast.html', context)
