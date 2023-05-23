FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y adduser gcc make && \
    pip install --upgrade setuptools pip poetry

# add the appropriate user
RUN adduser --system --home /app --uid 1000 --group appuser

# add all current files, install dependencies (including dev) and build package
COPY . /app/
RUN chown -R appuser:appuser /app/
#COPY --chown=appuser:appuser .pip.conf /etc/pip.conf

# Run everything as the appuser
USER appuser

# NOTE: This will create a virtual env and install the application there, so to interact with
# python packages you should either enable the environment, or use `poetry run`.
RUN poetry install

ENTRYPOINT ["/usr/bin/make", "tests"]
