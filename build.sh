#!/bin/bash

set -eu

cd $(dirname $0)
mkdir -p build
if [ ! -f build/favicon.ico ]; then
    wget -nv https://kicon.musicscience37.com/KIcon.ico -O build/favicon.ico
fi
PYDEVD_DISABLE_FILE_VALIDATION=1 sphinx-build -M html source build
