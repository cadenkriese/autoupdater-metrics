#!/usr/bin/env bash

PYTHON37='/usr/local/bin/python3.7'

printf "%s\n" "FLASK_ENV='production'" "FLASK_DEBUG='false'" >.env

${PYTHON37} -m pipenv --rm
${PYTHON37} -m pipenv --python ${PYTHON37}

${PYTHON37} -m pipenv update
