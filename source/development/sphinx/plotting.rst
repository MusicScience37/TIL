グラフのプロット
================

Python パッケージ
`Plotly <https://plotly.com/python/>`_
と
`jupyter-sphinx <https://jupyter-sphinx.readthedocs.io/en/latest/>`_
を組み合わせることで、
Sphinx ドキュメントにグラフを挿入する。

例えば、

.. code-block:: rst

    .. jupyter-execute::

        import numpy as np
        import plotly.express as px

        x = np.linspace(0, 1, 100)
        y = np.sin(x)

        fig = px.line(x=x, y=y)
        fig

で次の出力が得られる。

.. jupyter-execute::

    import numpy as np
    import plotly.express as px

    x = np.linspace(0, 1, 100)
    y = np.sin(x)

    fig = px.line(x=x, y=y)
    fig

なお、jupyter-sphinx 自体はソースコードのブロックを実行してくれるライブラリのため、
当然グラフでない計算結果の表示にも使用できる。
また、1 つの rst ファイル内では変数が共有される。

.. jupyter-execute::

    x
