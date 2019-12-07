数式の追加
===================

設定
------------------

conf.py に次の設定をしている。

.. code-block:: python

    extensions = [
        'sphinx.ext.mathjax'
    ]

    # setting of mathjax
    mathjax_config = {
        'TeX' : {
            'Macros': {
                'bm': ['{\\boldsymbol{#1}}',1],
            },
        },
    }

``extensions`` に
`MathJax <https://www.mathjax.org/>`_
を用いた拡張機能を追加し、
``mathjax_config`` で
`MathJax 公式ドキュメント <https://docs.mathjax.org/en/latest/options/input/tex.html>`_
にて示されているような設定を追加する。
ただし、公式ドキュメントの通りに全て小文字で記載すると正しく処理されないため注意が必要。

rst ファイル
------------------

.. code-block:: rst

    .. math::

        \sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}

        \bm{a} = \begin{pmatrix} a_1 \\ a_2 \\ a_3 \end{pmatrix}


詳しい使い方は
`リファレンス <http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#math>`_
を参照。

出力
------------------

.. math::

    \sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}

    \bm{a} = \begin{pmatrix} a_1 \\ a_2 \\ a_3 \end{pmatrix}
