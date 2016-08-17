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
from backend.models import Stream, Device, Group
from .forms import DeviceForm, GroupForm, SlideshowForm, StreamForm
from . import slideshow

@login_required()
def index(request):
    devices = len(Device.objects.all())
    groups = len(Group.objects.all())
    streams = len(Stream.objects.all())

    context = {
        'devices': devices,
        'streams': streams,
        'groups': groups,
    }
    return render(request, 'frontend/index.html', context)

@login_required()
def change(request):
    device_ids = request.POST.getlist('devices[]')  # device ids
    group_ids = request.POST.getlist('groups[]')  # group ids
    config = request.POST['config']  # config name

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
    streams = Stream.objects.order_by('name')
    slideshows = slideshow.list_slideshows()

    castable = len(devices) > 0 and (len(streams) > 0 or len(slideshows) > 0)

    context = {
        'devices': devices,
        'groups': groups,
        'streams': streams,
        'slideshows': slideshows,
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
            return render(request, 'frontend/devices.html')
    else:
        form = DeviceForm(instance=dev, label_suffix='')
        context = {
            'form': form,
        }
        return render(request, 'frontend/edit_device.html', context)
    return render(request, 'frontend/devices.html')

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


@login_required()
def slideshows(request):
    slides = slideshow.list_slideshows()
    context = {
        'slides': slides,
        'size': len(slides),
    }
    return render(request, 'frontend/slideshows.html', context)


@login_required()
def edit_slideshow(request, name):
    if request.method == 'POST':
        form = SlideshowForm(request.POST)
        if form.is_valid():
            slideshow.delete_slideshow(name)
            slideshow.create_slideshow(form.data['name'], form.data['desc'], form.data['url'])
            return HttpResponseRedirect('/frontend/slideshows')
    else:
        desc, url = slideshow.get_info(name)
        data = {
            'name': name,
            'url': url,
            'desc': desc,
            }
        form = SlideshowForm(data)
        context = {
            'form': form,
            'name': name,
        }
        return render(request, 'frontend/edit_slideshow.html', context)


@login_required()
def create_slideshow(request):
    if request.method == 'POST':
        form = SlideshowForm(request.POST)
        if form.is_valid():
            slideshow.create_slideshow(form.data['name'], form.data['desc'], form.data['url'])
            return HttpResponseRedirect('/frontend/slideshows')
    else:
        form = SlideshowForm()

    context = {
        'form': form,
    }
    return render(request, 'frontend/create_slideshow.html', context)


def get_slideshow(request, name):
    slides = slideshow.list_slides(name)
    slides = ['/static/frontend/web/%s/slides/%s' % (name, slide) for slide in slides]
    context = {
        'slides': slides,
    }
    return render(request, 'frontend/slideshow.html', context)

@login_required()
def delete_slideshow(request, name):
    slideshow.delete_slideshow(name)
    return HttpResponseRedirect('/frontend/slideshows')


@login_required()
def streams(request):
    streams = Stream.objects.order_by('name')
    context = {
        'streams': streams,
        'size': len(streams),
    }
    return render(request, 'frontend/streams.html', context)


@login_required()
def create_stream(request):
    if request.method == 'POST':
        form = StreamForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/frontend/streams')
    else:
        form = StreamForm(label_suffix='')

    context = {
        'form': form,
    }
    return render(request, 'frontend/create_stream.html', context)


@login_required()
def edit_stream(request, name):
    if request.method == 'POST':
        form = StreamForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/frontend/streams')
    else:
        stream = Stream.objects.get(name=name)
        form = StreamForm(instance=stream, label_suffix='')
        context = {
            'form': form,
            'name': name,
        }
        return render(request, 'frontend/edit_stream.html', context)


@login_required()
def delete_stream(request, name):
    stream = Stream.objects.get(name=name)
    stream.delete()
    return render(request, 'frontend/streams.html')

