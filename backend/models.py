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

from django.db import models


class Stream(models.Model):
    name = models.CharField(max_length=255, blank=False)
    desc = models.TextField(blank=True)
    url = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name


class Device(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True)
    mac = models.CharField(max_length=17)
    configuration = models.CharField(max_length=255, default='')

    def __str__(self):
        name = self.name if self.name else self.mac
        if self.configuration != '':
            return "%s - %s" % (name, self.configuration)
        else:
            return name


class Group(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True)
    devices = models.ManyToManyField(Device)

    def __str__(self):
        return self.name
