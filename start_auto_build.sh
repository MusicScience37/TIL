#!/bin/bash

base_dir=$(dirname $0)
mkdir -p build
if [ ! -f build/favicon.ico ]; then
    wget -nv https://kicon.musicscience37.com/KIcon.ico -O build/favicon.ico
fi
PYDEVD_DISABLE_FILE_VALIDATION=1 sphinx-autobuild $base_dir/source $base_dir/build --host 0 --port 3737
