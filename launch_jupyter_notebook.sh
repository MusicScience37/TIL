#!/bin/bash

# jupyter lab は plotly のグラフが正常に表示できなかったため、
# 現状は jupyter notebook にする。

set -e

jupyter notebook --allow-root --no-browser --NotebookApp.token='' --port=8765
