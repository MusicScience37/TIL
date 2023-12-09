テストページ
=================

本文

ヘッダ2
-----------------

ヘッダ3
..................

ヘッダ4
```````````````````

ヘッダ5
''''''''''''''''''

ヘッダ 6
^^^^^^^^^^^^^

本文

段落を分けた本文

Inline markup
--------------------

- 標準 standard
- *強調* *emphasis*
- **さらに強調** **strong emphasis**
- ``コード`` ``code``

リスト
--------------

- テスト
- テスト

  - テスト

    - テスト

      - テスト

- テスト

1. テスト
2. テスト

   1. テスト

      1. テスト

term
    definition

単語
    説明

    もう少し説明

引用
------------

.. cspell:disable

自動生成の適当なテキスト：

    Eirmod invidunt sadipscing est vel ea tation consetetur consetetur ut consequat dolore. At vero labore lorem eirmod tempor dolor facilisis dolor consetetur dolore takimata et clita. Ex sed soluta magna voluptua molestie. Aliquyam vero nostrud delenit dolores velit takimata diam sit. Placerat sadipscing labore voluptua.

.. cspell:enable

表
-------------

.. csv-table:: 単純な表
    :widths: auto
    :header-rows: 1

    列1,列2,列3
    テスト,テスト,テスト

.. csv-table:: 極端な表
    :widths: auto
    :header-rows: 1

    長い列,タイトルが長いだけの列
    長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章 長い文章,2

リンク
------------------

- `reStructuredText Primer <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_

各種メッセージ
-------------------

.. attention:: attention のテスト

.. caution:: caution のテスト

.. danger:: danger のテスト

.. error:: error のテスト

.. hint:: hint のテスト

.. important:: important のテスト

.. note:: note のテスト

.. tip:: tip のテスト

.. warning:: warning のテスト

.. todo:: todo のテスト

.. versionadded:: 1.2.3
    versionadded のテスト

.. versionchanged:: 1.2.3
    versionchanged のテスト

.. deprecated:: 1.2.3
    deprecated のテスト

.. seealso:: seealso のテスト

ソースコード
--------------------

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

参考文献
-----------------

- :footcite:t:`Joblove1978`
- :footcite:p:`MozillaColor`

.. footbibliography::

数式
-------------

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

PlantUML
----------------

.. uml::

    activate クライアント
    クライアント -> サーバ ++ : リクエスト
    return レスポンス
