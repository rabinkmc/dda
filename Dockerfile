FROM python:3.13

WORKDIR /app

# build arg (default = dev)
ARG ENV=dev

COPY requirements/base.txt requirements/${ENV}.txt requirements/
RUN pip install -r requirements/${ENV}.txt

COPY . .
