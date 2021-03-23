# multi stage builder for image optimization

# BUILDER 

FROM python:3.8.1-slim-buster as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

RUN pip install --upgrade pip
RUN pip install flake8
COPY . /usr/src/app/
RUN flake8 --ignore=E501,F401 .

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


# FINAL IMAGE

FROM python:3.8.1-slim-buster

RUN mkdir -p /home/app

RUN addgroup -S app && adduser -S app -G app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Get dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# Get production entrypoint script
COPY ./entrypoint.prod.sh $APP_HOME

# Copy project to home folder
COPY . $APP_HOME

# chown of project to the app user
RUN chown -R app:app $APP_HOME

# Switch to app user
USER app

# Run production entrypoint.prod.sh
ENTRYPOINT ["/home/app/web/entrypoint.prod.sh"]