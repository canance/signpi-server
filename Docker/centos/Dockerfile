FROM centos:latest
MAINTAINER Cory Nance <canance@coastal.edu>

RUN yum install -y centos-release-scl
RUN yum install -y ghostscript git ImageMagick rh-python35-python vim wget
RUN echo #!/bin/bash > /etc/profile.d/enablepython35.sh
RUN echo source /opt/rh/rh-python35/enable >> /etc/profile.d/enablepython35.sh
RUN echo export X_SCLS="`scl enable rh-python35 'echo $X_SCLS'`" >> /etc/profile.d/enablepython35.sh
RUN source /etc/profile.d/enablepython35.sh && pip install gunicorn django==1.9
RUN git clone https://github.com/canance/signpi-server.git
RUN source /etc/profile.d/enablepython35.sh && python /signpi-server/manage.py migrate
RUN source /etc/profile.d/enablepython35.sh && echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'csci1234')" | python /signpi-server/manage.py shell
EXPOSE 8000
VOLUME /signpi-server
CMD source /etc/profile.d/enablepython35.sh && /signpi-server/manage.py runserver 0.0.0.0:8000

