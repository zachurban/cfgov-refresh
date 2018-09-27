#!/bin/bash

# ==========================================================================
# Setup script for installing project dependencies.
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

ENVVAR=.env
if [ ! -f $ENVVAR ]; then
  echo 'Creating default environment variables...'
  cp "$ENVVAR"_SAMPLE $ENVVAR
fi

if [ "$1" != "docker" ]; then
  ./frontend.sh $1
fi

./backend.sh $1

if [[ ! -z "$CFGOV_SPEAK_TO_ME" ]]; then
  say "Set up has finished."
fi
