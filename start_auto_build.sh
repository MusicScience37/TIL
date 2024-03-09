#!/bin/bash

set -eu

cd $(dirname $0)
mkdir -p build/html
if [ ! -f build/html/favicon.ico ]; then
    wget -nv https://kicon.musicscience37.com/KIcon.ico -O build/html/favicon.ico
fi
PYDEVD_DISABLE_FILE_VALIDATION=1 sphinx-autobuild source build/html --host 0 --port 3737
