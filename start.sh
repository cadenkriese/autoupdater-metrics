#!/usr/bin/env bash
# NOTE: pipenv must be created by the user executing this file.

PYTHON37='/usr/local/bin/python3.7'

mkdir -p /var/log/autoupdater-metrics/
cd /opt/flogic/autoupdater-metrics/

${PYTHON37} -m pipenv run -- uwsgi uwsgi.ini
