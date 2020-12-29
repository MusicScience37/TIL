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
[W3C-color]_ に JavaScript による実装例がある。

参考
--------

.. [Joblove1978]
    Joblove, G. and D. P. Greenberg. “Color spaces for computer graphics.” SIGGRAPH '78 (1978).
    (`Semantic Scholar <https://www.semanticscholar.org/paper/Color-spaces-for-computer-graphics-Joblove-Greenberg/042305fdca6fa3efa785c77bd1d72bf9cabbd993?sort=relevance&page=7>`_,
    `PDF <http://papers.cumincad.org/data/works/att/634c.content.pdf>`_)
.. [Mozilla-color] `\<color\> - CSS: カスケーディングスタイルシート | MDN <https://developer.mozilla.org/ja/docs/Web/CSS/color_value>`_
.. [W3C-color] `CSS Color Module Level 4 <https://drafts.csswg.org/css-color/#the-hsl-notation>`_
