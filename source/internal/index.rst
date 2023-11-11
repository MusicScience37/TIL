Internal
===============

ここは本ページの作成者が確認するページです。

ルール
---------

- ビルドが通る状態で master にコミットする。
- Sphinx の設定は一旦ブランチを切って作業を行い、CI で結果を確認してからマージする。

TODO リスト
-----------

.. todolist::

各種設定のテスト
---------------------

ノート
..............

.. note:: これはノートです。

ソースコード
....................

.. code-block:: c++
    :caption: 色々な要素を含んだ C++ コード

    #include <iostream>

    template <typename T>
    class Example {
    public:
        /*!
         * \brief Construct.
         *
         * \param[in] var var.
         */
        Example(T var) : var_(var) {}

        /*!
         * \brief Get var.
         *
         * \return var.
         */
        [[nodiscard]] const T& var() const { return var_; }

    private:
        //! var.
        T var_;
    };

    int main() {
        Example<int> ex(5);
        int res = ex.var();
        return 0;
    }

.. code-block:: python
    :caption: 色々な要素を含んだ Python コード

    """Test of a code block."""

    import pathlib
    import typing

    THIS_DIR = pathlib.Path(__file__).absolute().parent


    class Example:
        """A class for test of a code block."""

        def __init__(self, value: typing.Optional[int] = None) -> None:
            if value is None:
                value = 12345
            self._value = value

        @property
        def value(self) -> int:
            """Get the value."""
            return self._value


    if __name__ == "__main__":
        main()

数式
....................

- 基本的な記号

  .. math::

      \sum_{n=1}^\infty \frac{1}{n^2}
      = \frac{1}{1^2} + \frac{1}{2^2} + \frac{1}{3^2} + \ldots
      = \frac{\pi^2}{6}

- ``\bm`` によるベクトル表記

  .. math::

      \bm{a} = \begin{pmatrix} a_1 \\ a_2 \\ a_3 \end{pmatrix}

- 横に長い数式

  .. math::

      1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10
      + 11 + 12 + 13 + 14 + 15 + 16 + 17 + 18 + 19 + 20
      + 21 + 22 + 23 + 24 + 25 + 26 + 27 + 38 + 29 + 30

- 等号の位置揃え

  .. math::

      a &= 1 \\
      b &= 12345 \\
      \bm{c} &= \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{pmatrix}

表
........

.. csv-table::
    :widths: auto
    :header-rows: 1

    長い列,タイトルが長いだけの列
    長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章,2

jupyter-execute with Plotly
....................................

.. jupyter-execute::

    import numpy as np
    import plotly.express as px

    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    fig = px.line(x=x, y=y)
    fig

PlantUML
.................

.. uml::

    activate クライアント
    クライアント -> サーバ ++ : リクエスト
    return レスポンス

nbsphinx
.................

.. toctree::
    :caption: About
    :maxdepth: 1

    test-nbsphinx
