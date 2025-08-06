FROM python:3.10-slim 

RUN apt-get update \ 
&& apt-get install -y --no-install-recommends \
    build-essential \ 
    default-libmysqlclient-dev \
    libjpeg-dev \ 
    zlib1g-dev \
    pkg-config \ 
    && rm -rf /var/lib/apt/lists/*
    
RUN pip3 install pillow 

WORKDIR /app 

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

ENV DJANGO_SETTINGS_MODULE=netalith0django.settings 

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]