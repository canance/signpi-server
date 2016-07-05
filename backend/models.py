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


class App(models.Model):
    value = models.TextField()

    def __str__(self):
        return self.value


class URL(models.Model):
    value = models.TextField()

    def __str__(self):
        return self.value


class Args(models.Model):
    value = models.TextField()

    def __str__(self):
        return self.value


class Configuration(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True)
    app_id = models.ForeignKey(App, models.SET_NULL, blank=True, null=True)
    url_id = models.ForeignKey(URL, models.SET_NULL, blank=True, null=True)
    args_id = models.ForeignKey(Args, models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Device(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True)
    mac = models.CharField(max_length=17)
    configuration = models.ForeignKey(Configuration, models.SET_NULL, blank=True, null=True)

    def __str__(self):
        config = self.configuration if self.configuration else "N/A"
        name = self.name if self.name  else self.mac
        return "%s - %s" % (name, config)


class Group(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True)
    devices = models.ManyToManyField(Device)

    def __str__(self):
        return self.name
