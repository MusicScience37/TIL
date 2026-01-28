#!/bin/bash

set -e

cd $(dirname $0)
g++ -std=c++20 -O2 -o test_num_seeds test_num_seeds.cpp
./test_num_seeds
