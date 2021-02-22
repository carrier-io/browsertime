FROM sitespeedio/browsertime:11.3.0

RUN apt-get update -y
RUN apt-get install -y build-essential checkinstall
RUN apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
RUN cd /opt && wget https://www.python.org/ftp/python/3.8.7/Python-3.8.7.tgz && tar xzf Python-3.8.7.tgz
RUN cd /opt/Python-3.8.7 && ./configure --enable-optimizations && make altinstall && rm -f /opt/Python-3.8.7.tgz

COPY requirements.txt /browsertime/requirements.txt
COPY wrapper/start.py /browsertime/start.py

WORKDIR /browsertime

RUN pip install -r requirements.txt

ENTRYPOINT ["python3.8", "-u", "start.py"]