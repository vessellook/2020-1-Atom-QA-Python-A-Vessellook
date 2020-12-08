FROM jenkins/jenkins:lts

USER root
ENV TZ=Europe/Moscow

RUN apt update
RUN apt install -y build-essential zlib1g-dev libncurses5-dev \
	libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev

RUN mkdir -p /opt/python38
RUN cd /opt/python38
RUN wget https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tar.xz
RUN tar -xf Python-3.8.2.tar.xz && cd Python-3.8.2 && ./configure --enable-optimizations && make altinstall

RUN rm -rf /opt/python38

RUN apt-get -y update && \
    apt-get -y install apt-transport-https ca-certificates curl gnupg-agent software-properties-common && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") $(lsb_release -cs) stable" && \
    apt-get update && \
    apt-get -y install docker-ce docker-ce-cli containerd.io
RUN curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose && \
    ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
    
ARG HOST_UID=1004
ARG HOST_GID=999

RUN pip3.8 install --upgrade pip
RUN pip3.8 install pytest allure-pytest pytest filelock pymysql sqlalchemy pytest-xdist \
                   pytest-check allure-pytest requests selenium webdriver_manager bs4 python-dotenv


