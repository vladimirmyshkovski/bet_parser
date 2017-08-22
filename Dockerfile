FROM ubuntu:latest 


MAINTAINER Narnik Gamarnik <narnikgamarnikus@gmail.com>

ADD run.py /

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  libcurl4-gnutls-dev libexpat1-dev gettext \
  libz-dev libssl-dev wget \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN apt-get update -y
RUN apt-get install bzip2 libfreetype6 libfontconfig1  -y
RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.8-linux-x86_64.tar.bz2
RUN tar -xvjf phantomjs-1.9.8-linux-x86_64.tar.bz2 && rm phantomjs-1.9.8-linux-x86_64.tar.bz2
RUN mv phantomjs-1.9.8-linux-x86_64 /usr/local/phantomjs-1.9.8-linux-x86_64
RUN ln -s /usr/local/phantomjs-1.9.8-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs

RUN pip3 install --no-cache-dir \
	'beautifulsoup4==4.6.0' \
	'bs4==0.0.1' \
	'lxml==3.8.0' \
	'selenium==3.5.0' \
	'idna==2.5'


CMD [ "python3", "./run.py" ]