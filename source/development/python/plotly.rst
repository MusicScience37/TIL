.. _development-python-plotly:

Plotly の Python ライブラリでグラフをプロット
=============================================

Python パッケージ
`Plotly <https://plotly.com/python/>`_
はグラフをプロットするライブラリである。
Plotly 自体は Python 以外に R や Javascript にも対応しており、
グラフを表示する機能は Javascript で書かれている。

機能
----------

- インタラクティブに値を見たり拡大・縮小したりできる
  HTML 形式のグラフを生成できる。
  （下記の例を参照）

- 様々なグラフに対応している。

  - ギャラリーを参照：`Plotly Express | Python | Plotly <https://plotly.com/python/plotly-express/#gallery>`_

- PNG, JPEG, SVG, PDF といった画像の出力もできる。

  - 古いバージョンでは画像出力用に別途バイナリをインストール必要があったものの、
    現在は pip によるインストールのみで画像出力まで対応できる。

インストール
------------------

.. code-block:: bash

    pip install plotly
    pip install pandas # Plotly Express の機能を利用する場合は必要
    pip install kaleido # 画像ファイルの出力を行う場合は必要

プロットの例
--------------------

以下にプロットの例を示す。
Sphinx へのグラフの表示方法については
:ref:`development-sphinx-plotting`
を参照。

.. jupyter-execute::

    import numpy as np
    import plotly.express as px

    x = np.linspace(0, 6.28, 100)
    y = np.sin(x)

    fig = px.line(x=x, y=y)
    fig

プロットの HTML 出力
--------------------------------

上記の例のようにインタラクティブなグラフは
次のようにして HTML ファイルへ出力できる
（`Interactive HTML Export | Python | Plotly <https://plotly.com/python/interactive-html-export/>`_）。

.. code-block:: python3

    fig.write_html('path_to_output.html')

プロットの画像ファイル出力
---------------------------

静的な画像ファイルも出力できる。
PNG, JPEG, SVG, PDF などに対応しているという
（`Static Image Export | Python | Plotly <https://plotly.com/python/static-image-export/>`_）。

.. code-block:: python3

    fig.write_image('path_to_output.png')
