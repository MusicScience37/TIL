数式の追加
===================

設定
------------------

``extensions`` に
`MathJax <https://www.mathjax.org/>`_
を用いた拡張機能 ``sphinx.ext.mathjax`` を追加し、
``mathjax3_config`` で
`MathJax 公式ドキュメント <https://docs.mathjax.org/en/latest/options/input/tex.html>`_
にて示されているような設定を追加する。

.. hint::

    本サイトでは以下のような設定をしている。

    .. code-block:: python

        # setting of MathJax
        # Extension for MathJax is already enabled by myst_nb.
        # MathJax URL working with Plotly was written in https://www.npmjs.com/package/plotly.js/v/2.16.4#mathjax.
        mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"
        mathjax3_config = {
            "tex": {
                "macros": {
                    "bm": ["{\\boldsymbol{#1}}", 1],
                },
            },
        }

    Jupyter Notebook を表示できる ``myst_nb`` という拡張機能を導入すると
    自動で拡張機能 ``sphinx.ext.mathjax`` が有効化されるため、
    MathJax の追加の設定のみ行っている。

    また、Jupyter Notebook で数式込みの Plotly ライブラリのグラフを表示するために、
    使用する MathJax の URL を変更する必要があった。

rst ファイル
------------------

.. code-block:: rst

    .. math::

        \sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}


詳しい使い方は
`リファレンス <http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#math>`_
を参照。

出力
------------------

.. math::

    \sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}

    \bm{a} = \begin{pmatrix} a_1 \\ a_2 \\ a_3 \end{pmatrix}
