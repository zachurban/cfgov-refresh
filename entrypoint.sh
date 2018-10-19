cp -r ../static_built ./cfgov/static_built

ENVVAR=.env
if [ ! -f $ENVVAR ]; then
  echo 'Creating default environment variables...'
  cp "$ENVVAR"_SAMPLE $ENVVAR
fi

# Build satellites
for d in /usr/src/app/develop-apps/*/ ; do
    if [ -d "$d" ]; then
      export PYTHONPATH=$d:$PYTHONPATH
      if [ ! -d "$d/node_modules" ]; then
        echo "Building frontend for: $d"
        "$d/frontend.sh"
      fi
    fi
done

source $ENVVAR
python cfgov/manage.py runserver 0.0.0.0:8000
