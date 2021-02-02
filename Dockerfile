FROM sitespeedio/browsertime:11.3.0

COPY requirements.txt /browsertime/requirements.txt
COPY wrapper/start.py /browsertime/start.py

WORKDIR /browsertime

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-u", "start.py"]