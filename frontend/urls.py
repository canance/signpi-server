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

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cast/', views.cast, name='cast'),
    url(r'^change/', views.change, name='change'),
    url(r'^create_device/', views.create_device, name="create_device"),
    url(r'^create_device_group', views.create_device_group, name='create_device_group'),
    url(r'^devices/', views.devices, name='devices'),
    url(r'^device_groups/', views.device_groups, name='device_groups'),
    url(r'^edit_device/(?P<dev>\d+)/$', views.edit_device, name='edit_device'),
    url(r'^edit_device_group/(?P<grp>\d+)/$', views.edit_device_group, name='edit_device_group'),
]
