FROM python:3.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY beacon_controller /usr/src/app/beacon_controller
COPY config /usr/src/app/config
COPY beacon /usr/src/app/beacon
COPY data/__init__.py /usr/src/app/data/__init__.py

COPY MANIFEST.in /usr/src/app/MANIFEST.in
COPY setup.py /usr/src/app/setup.py

# Install in edit mode so that we don't need to install the data files
# when the docker container is built. This way we can pass the data
# files in through a volume.
RUN pip install -e .

WORKDIR /usr/src/app/beacon

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]
