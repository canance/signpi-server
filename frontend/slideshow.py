# Author:   Cory Nance <canance@coastal.edu>
# Revision: 29 June 2016
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

import os
import shutil
import subprocess

#SLIDESHOW_PATH = '/slideshows'
#FETCH_SLIDES_PATH = '/usr/bin/fetch_slides'
SLIDESHOW_PATH = '/home/cory/PycharmProjects/signage'
FETCH_SLIDES_PATH = '/home/cory/PycharmProjects/signage/bin/fetch_slides'
CONF_PATH = os.path.join(SLIDESHOW_PATH, "signage/conf.d")
# set to frontend/static/frontend/web
WEB_PATH = os.path.join('/home/cory/PycharmProjects/signpi-server/frontend/static/frontend', "web")


def list_slides(name):
    path = os.path.join(WEB_PATH, name + "/slides")
    return [slide for slide in os.listdir(path)]


def list_slideshows():
    return [conf[:-5] for conf in os.listdir(CONF_PATH)]


def create_slideshow(name, desc, url):
    if name in list_slideshows():
        raise Exception("The name [%s] is already taken!" % name)

    web_path = os.path.join(WEB_PATH, name)
    conf_path = os.path.join(CONF_PATH, name + '.conf')

    # create conf file
    conf = '#/bin/bash\n'
    conf += '#\n'
    conf += '# %s\n'
    conf += '#\n\n'
    conf += 'SLIDESHOW_PDF="%s"\n'
    conf += 'SLIDESHOW_OUTPUT="%s"\n'
    conf = conf % (desc, url, web_path)

    # write to file
    f = open(conf_path, 'w')
    f.write(conf)
    f.flush()
    f.close()

    # call fetch_slides script
    if os.path.exists(web_path):
        shutil.rmtree(web_path)
    os.mkdir(web_path)
    os.chdir(web_path)
    completed_process = subprocess.run([FETCH_SLIDES_PATH, conf_path])
    return completed_process.returncode == 0
