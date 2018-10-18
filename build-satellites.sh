for d in /usr/src/app/develop-apps/*/ ; do
    export PYTHONPATH=$d:$PYTHONPATH
    if [ ! -d "$d/node_modules" ]; then
      echo "Building frontend for: $d"
      "$d/frontend.sh"
    fi
done
