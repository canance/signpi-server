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
from .forms import DeviceForm, GroupForm


@login_required()
def index(request):
    devices = len(Device.objects.all())
    groups = len(Group.objects.all())
    configs = len(Configuration.objects.all())


    context = {
        'devices': devices,
        'configs': configs,
        'groups': groups,
    }
    return render(request, 'frontend/index.html', context)


@login_required()
def change(request):
    device_ids = request.POST.getlist('devices[]')  # device ids
    group_ids = request.POST.getlist('groups[]')  # group ids
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

    return HttpResponseRedirect('/frontend/')


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


@login_required()
def device_groups(request):
    groups = Group.objects.order_by('name')

    context = {
        'groups': groups,
        'size': len(groups),
    }
    return render(request, 'frontend/device_groups.html', context)


@login_required()
def create_device_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, label_suffix='')
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/frontend/device_groups')
    else:
        form = GroupForm(label_suffix='')

    context = {
        'form': form,
    }
    return render(request, 'frontend/create_device_group.html', context)


@login_required()
def edit_device_group(request, grp):
    group = Group.objects.get(pk=grp)

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/frontend/device_groups')
    else:
        form = GroupForm(instance=group, label_suffix='')
        context = {
            'form': form,
        }
        return render(request, 'frontend/edit_device_group.html', context)


@login_required()
def devices(request):
    devs = Device.objects.order_by('name')
    context = {
        'devices': devs,
        'size': len(devs),
    }
    return render(request, 'frontend/devices.html', context)


@login_required()
def edit_device(request, dev):
    dev = Device.objects.get(pk=dev)

    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=dev)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/frontend/devices')
    else:
        form = DeviceForm(instance=dev, label_suffix='')
        context = {
            'form': form,
        }
        return render(request, 'frontend/edit_device.html', context)


@login_required()
def create_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST, label_suffix='')
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/frontend/devices')
    else:
        form = DeviceForm(label_suffix='')

    context = {
        'form': form,
    }
    return render(request, 'frontend/create_device.html', context)