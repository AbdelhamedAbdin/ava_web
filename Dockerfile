FROM python:3.7-slim-stretch

# Upgrade apt
RUN apt-get update -y

# Install curl
RUN apt-get install -y curl
RUN apt-get install -y software-properties-common
RUN apt-get install -y gpg-agent
RUN apt-get install -y ca-certificates
RUN add-apt-repository ppa:libreoffice/ppa
RUN apt-get install -y libreoffice || { rc=$?; [ "$rc" -eq 100 ] && exit 0; exit "$rc"; }
RUN apt-get install -y poppler-utils || { rc=$?; [ "$rc" -eq 100 ] && exit 0; exit "$rc"; }

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app/

RUN ["chmod", "+x", "./entrypoint.sh"]

ENTRYPOINT ["./entrypoint.sh"]
