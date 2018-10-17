cd /usr/src/app

cp -r ../static_built ./cfgov/static_built

ENVVAR=.env
if [ ! -f $ENVVAR ]; then
  echo 'Creating default environment variables...'
  cp "$ENVVAR"_SAMPLE $ENVVAR
fi

source $ENVVAR
python cfgov/manage.py runserver 0.0.0.0:8000
