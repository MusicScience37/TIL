HSL 色空間
================

HSL 色空間は

- Hue （色相）
- Saturation （彩度）
- Lightness （明度）

により色を表現する [Mozilla-color]_ 。

HSL 色空間は [Joblove1978]_ で定義されたものであり、
次のように HSL 色空間による表現 :math:`(h, s, l)` から
RGB 色空間による表現 :math:`(r, g, b)` を計算する。

.. math::

    r' &= \begin{cases}
        1 & \text{if $0 \le h \le 1/6$ or $5/6 \le h < 1$} \\
        2 - 6h & \text{if $1/6 \le h \le 2/6$} \\
        0 & \text{if $2/6 \le h \le 4/6$} \\
        6h - 4 & \text{if $4/6 \le h \le 5/6$}
    \end{cases}
    \\
    g' &= \begin{cases}
        6h & \text{if $0 \le h \le 1/6$} \\
        1 & \text{if $1/6 \le h \le 3/6$} \\
        4 - 6h & \text{if $3/6 \le h \le 4/6$} \\
        0 & \text{if $4/6 \le h < 1$}
    \end{cases}
    \\
    b' &= \begin{cases}
        0 & \text{if $0 \le h \le 2/6$} \\
        6h - 2 & \text{if $2/6 \le h \le 3/6$} \\
        1 & \text{if $3/6 \le h \le 5/6$} \\
        6 - 6h & \text{if $5/6 \le h < 1$}
    \end{cases}
    \\
    \begin{pmatrix} r \\ g \\ b \end{pmatrix} &=
    \begin{cases}
        \left(
            \begin{pmatrix} 0.5 \\ 0.5 \\ 0.5 \end{pmatrix}
            + s \left(
                \begin{pmatrix} r' \\ g' \\ b' \end{pmatrix}
                - \begin{pmatrix} 0.5 \\ 0.5 \\ 0.5 \end{pmatrix}
            \right)
        \right) \cdot 2i
        & \text{if $i \le 1/2$}
        \\
        \begin{pmatrix} 0.5 \\ 0.5 \\ 0.5 \end{pmatrix}
        + s \left(
            \begin{pmatrix} r' \\ g' \\ b' \end{pmatrix}
            - \begin{pmatrix} 0.5 \\ 0.5 \\ 0.5 \end{pmatrix}
        \right)
        + \left(
            \begin{pmatrix} 0.5 \\ 0.5 \\ 0.5 \end{pmatrix}
            - s \left(
                \begin{pmatrix} r' \\ g' \\ b' \end{pmatrix}
                - \begin{pmatrix} 0.5 \\ 0.5 \\ 0.5 \end{pmatrix}
            \right)
        \right) (2i - 1)
        & \text{if $i \ge 1/2$}
    \end{cases}

.. note::
    [Joblove1978]_ では最後が :math:`(2i - 1)` でなく :math:`(2 - 2i)` だったが、
    論文中の記述と矛盾するため :math:`(2i - 1)` とした。

HSL から RGB への変換については、
[W3C-color]_ に JavaScript による実装例があるが、
ここでは、Python で実装して挙動を確認する。

色相に対する RGB の変化
------------------------

まず、:math:`(r', g', b')` の計算式を実装する。

.. jupyter-execute::

    def hue2r(hue: float) -> float:
        """色相に対する RGB の R を計算する

        hue は [0, 1] の範囲にあるとする。
        """

        if (0.0 <= hue <= 1.0 / 6.0) or (5.0 / 6.0 <= hue):
            return 1.0
        elif 1.0 / 6.0 <= hue <= 2.0 / 6.0:
            return 2.0 - 6.0 * hue
        elif 2.0 / 6.0 <= hue <= 4.0 / 6.0:
            return 0.0
        else:
            return 6.0 * hue - 4.0

    def hue2g(hue: float) -> float:
        """色相に対する RGB の G を計算する

        hue は [0, 1] の範囲にあるとする。
        """

        if 0.0 <= hue <= 1.0 / 6.0:
            return 6 * hue
        elif 1.0 / 6.0 <= hue <= 3.0 / 6.0:
            return 1.0
        elif 3.0 / 6.0 <= hue <= 4.0 / 6.0:
            return 4.0 - 6.0 * hue
        else:
            return 0.0

    def hue2b(hue: float) -> float:
        """色相に対する RGB の B を計算する

        hue は [0, 1] の範囲にあるとする。
        """

        if 0.0 <= hue <= 2.0 / 6.0:
            return 0.0
        elif 2.0 / 6.0 <= hue <= 3.0 / 6.0:
            return 6.0 * hue - 2.0
        elif 3.0 / 6.0 <= hue <= 5.0 / 6.0:
            return 1.0
        else:
            return 6.0 - 6.0 * hue


.. jupyter-execute::

    import numpy as np
    import plotly.graph_objects as go

    h = np.linspace(0, 1, 61)
    r = np.vectorize(hue2r)(h)
    g = np.vectorize(hue2g)(h)
    b = np.vectorize(hue2b)(h)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=h, y=r,
                             mode='lines', name="r'",
                             line={'color': 'red'}))
    fig.add_trace(go.Scatter(x=h, y=g,
                             mode='lines', name="g'",
                             line={'color': 'green'}))
    fig.add_trace(go.Scatter(x=h, y=b,
                             mode='lines', name="b'",
                             line={'color': 'blue'}))

    fig.update_layout(
        title="色相に対する (r', g', b') の挙動",
        xaxis_title='色相',
        yaxis_title='RGB の値')

    fig

参考
--------

.. [Joblove1978]
    Joblove, G. and D. P. Greenberg. “Color spaces for computer graphics.” SIGGRAPH '78 (1978).
    (`Semantic Scholar <https://www.semanticscholar.org/paper/Color-spaces-for-computer-graphics-Joblove-Greenberg/042305fdca6fa3efa785c77bd1d72bf9cabbd993?sort=relevance&page=7>`_,
    `PDF <http://papers.cumincad.org/data/works/att/634c.content.pdf>`_)
.. [Mozilla-color] `\<color\> - CSS: カスケーディングスタイルシート | MDN <https://developer.mozilla.org/ja/docs/Web/CSS/color_value>`_
.. [W3C-color] `CSS Color Module Level 4 <https://drafts.csswg.org/css-color/#the-hsl-notation>`_
