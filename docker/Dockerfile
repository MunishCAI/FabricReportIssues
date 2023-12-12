FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt update && \
    apt install -y python3 python3-pip && \
    pip3 install --upgrade pip && \
    apt install -y unzip && \
    apt-get install -y ffmpeg libsm6 libxext6 && \
    apt-get install -y shellinabox nano && \
    apt-get install -y systemctl && \
    sed -i 's/SHELLINABOX_PORT=4200/SHELLINABOX_PORT=8500/g' /etc/default/shellinabox && \
    systemctl restart shellinabox && mkdir /install && mkdir /app

COPY requirements.txt /install
RUN pip3 install -r /install/requirements.txt

COPY ./main.zip /app
WORKDIR /app
RUN unzip main.zip

EXPOSE 8500

CMD ["python3", "temp.py"]


