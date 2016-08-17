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

from .models import Device, Stream
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import frontend.slideshow

import json


def configuration(request):
    if 'dev' not in request.GET:
        return HttpResponse('Invalid request!')

    mac_address = request.GET['dev']

    try:
        device = Device.objects.get(mac__iexact=mac_address)
    except ObjectDoesNotExist:
        device = Device()
        device.mac = mac_address
        device.save()
    else:
        if device.configuration[:7] == 'stream:':
            intent = 'stream'
            stream = Stream.objects.get(name=device.configuration[7:])
            url = stream.url

        elif device.configuration[:10] == 'slideshow:':
            intent = 'slideshow'
            _, url = frontend.slideshow.get_info(device.configuration[10:])
        else:
            url = ''
            intent = 'error'
        configuration_data = {
            'intent': intent,
            'url': url,
        }
        return HttpResponse(json.dumps(configuration_data, sort_keys=True, indent=4, separators=(',', ':')))

    return HttpResponse('{}')

