#!/bin/bash

base_dir=$(dirname $0)
mkdir -p $base_dir/build/auto_build
PYDEVD_DISABLE_FILE_VALIDATION=1 sphinx-autobuild $base_dir/source $base_dir/build/auto_build --host 0 --port 3737
