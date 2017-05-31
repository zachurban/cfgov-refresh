#!/usr/bin/env bash

# Fail if any command fails.
set -e

echo "running $RUNTEST tests"
if [ "$RUNTEST" == "frontend" ]; then
    ./frontend.sh test

    gulp "test:unit"
    gulp "test:coveralls"
elif [ "$RUNTEST" == "backend" ]; then
    pip install -r requirements/test.txt
    PYTHONPATH=cfgov DJANGO_SETTINGS_MODULE=cfgov.settings.test python cfgov/manage.py test
    flake8
    coveralls
elif [ "$RUNTEST" == "acceptance" ]; then
    ./frontend.sh test

    export DISPLAY=:99.0
    sh -e /etc/init.d/xvfb start &
    sleep 3
    export HEADLESS_CHROME_BINARY=/usr/bin/google-chrome-beta

    gulp test:acceptance
fi
