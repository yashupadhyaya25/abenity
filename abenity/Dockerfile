# Pulling Ubuntu image
FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
# Updating packages and installing cron
RUN apt-get update && apt-get install cron -y 
RUN apt-get install python3 -y
RUN apt-get -y install python3-pip
RUN apt-get install wget -y
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable
RUN apt-get install -f
RUN apt-get install -yqq unzip curl
RUN pip install selenium

RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/117.0.5938.92/linux64/chromedriver-linux64.zip
RUN unzip chromedriver-linux64.zip 
RUN mkdir -p /member_export
RUN chmod -R 777 /member_export

ADD ./abenity.py .
ADD ./main.py .
RUN pip install flask
RUN pip install azure-storage-blob

ENTRYPOINT [ "python3" ]
CMD ["-d","./main.py"]
