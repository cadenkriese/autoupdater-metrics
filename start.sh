#!/usr/bin/env bash

mkdir -p /var/log/autoupdater-metrics/

pipenv update --bare
pipenv run -- uwsgi uwsgi.ini
