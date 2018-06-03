 FROM python:3
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /pulse
 WORKDIR /pulse
 ADD requirements.txt /pulse/
 RUN pip install -r requirements.txt
 ADD . /pulse/
