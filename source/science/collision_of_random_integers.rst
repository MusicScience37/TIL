ランダムな整数の衝突
========================

UUID バージョン 4 :footcite:p:`Leach2005` のようにランダムで十分長い整数は、
同じ整数が選択される（以降、「衝突する」）確率が十分低いため、
単一のプロセスでなく複数のプロセスやコンピュータ上で生成される ID などで
使用されることがある。
ここでは、そのような乱数が衝突する確率が実際どの程度になるのか計算してみる。

衝突する確率
----------------

まず、衝突する確率の計算式を考える。
整数を 0 から :math:`m-1` までの :math:`m` 個の中から
:math:`n` 回選択する場合、
衝突しない確率は、

.. math::

    p(m, n) = 1 -
        \frac{m    }{m} \cdot
        \frac{m-1  }{m} \cdot
        \frac{m-2  }{m} \cdot
        \frac{m-3  }{m} \cdot \cdots \cdot
        \frac{m-n+1}{m}

のように書ける。
（あとのため 2 種類の表記をしておく。）

選択する整数の数が少ない場合
----------------------------------

選択する整数の数 :math:`n` が少ない場合はコンピュータで比較的容易に計算できる。
ただし、そのままの計算式では :math:`m` が大きい場合に
浮動小数点数の打ち切り誤差で正しく計算できなくなるため、
計算式を変形しておく。

.. math::

    p(m, n) &= 1 -
        \frac{m    }{m} \cdot
        \frac{m-1  }{m} \cdot
        \frac{m-2  }{m} \cdot
        \frac{m-3  }{m} \cdot \cdots \cdot
        \frac{m-n+1}{m}
    \\
        &= 1 - \prod_{i=0}^{n-1} \frac{m - i}{m}
    \\
        &= 1 - \prod_{i=0}^{n-1} \left(1 - \frac{i}{m} \right)
    \\
        &= 1 - \exp\left(\sum_{i=0}^{n-1} \log\left(1 - \frac{i}{m} \right) \right)

.. jupyter-execute::

    import math
    import plotly.express as px


    def calc_random_number_collision_rate(
        num_selectable_numbers: int, num_selected_numbers: int
    ) -> float:
        """ランダムな整数が衝突する確率を計算する。

        Args:
            num_selectable_numbers (int): 選択肢の数。
            num_selected_numbers (int): 選択する数。

        Returns:
            float: 衝突する確率。
        """

        log_sum = 0.0
        for i in range(num_selected_numbers):
            log_sum = log_sum + math.log1p(-float(i) / float(num_selectable_numbers))
        return -math.expm1(log_sum)


    num_bits_vec = []
    num_selected_numbers_vec = []
    rate_vec = []
    for num_bits in [8, 16, 32, 64, 128]:
        for num_selected_numbers in [2, 5, 10, 20, 50, 100, 200, 500, 1000]:
            num_selectable_numbers = 2**num_bits
            if num_selected_numbers > num_selectable_numbers:
                continue

            rate = calc_random_number_collision_rate(
                num_selectable_numbers=num_selectable_numbers,
                num_selected_numbers=num_selected_numbers,
            )

            num_bits_vec.append(num_bits)
            num_selected_numbers_vec.append(num_selected_numbers)
            rate_vec.append(rate)

    fig = px.line(
        x=num_selected_numbers_vec,
        y=rate_vec,
        color=num_bits_vec,
        log_x=True,
        log_y=True,
        markers=True,
    )
    fig.update_layout(
        legend_title_text="選択する整数のビット数",
        xaxis_title="選択した整数の数",
        yaxis_title="確率",
        title="ランダムに選択した整数が衝突する確率",
        yaxis={
            "exponentformat": "power",
        },
    )
    fig

近似式
-------------

選択する整数の数 :math:`n` が小さくない場合も考える。
:math:`m \gg n \gg 1` とし、
マクローリン展開

.. math::

    \log(1 - x) = - \sum_{k=1}^\infty \frac{x^k}{k} \approx -x

を用いると、

.. math::

    \sum_{i=0}^{n-1} \log\left(1 - \frac{i}{m} \right) & \approx
        - \sum_{i=0}^{n-1} \frac{i}{m}
    \\
        & = - \frac{n(n-1)}{2m}
    \\
        & \approx - \frac{n^2}{2m}

となるから、

.. math::

    p(m, n) \approx 1 - \exp\left(- \frac{n^2}{2m} \right)

のように近似できる。

.. jupyter-execute::

    import math
    import plotly.express as px


    def calc_random_number_collision_rate_approx(
        num_selectable_numbers: int, num_selected_numbers: int
    ) -> float:
        """ランダムな整数が衝突する確率を近似計算する。

        Args:
            num_selectable_numbers (int): 選択肢の数。
            num_selected_numbers (int): 選択する数。

        Returns:
            float: 衝突する確率。
        """

        return -math.expm1(-0.5 * float(num_selected_numbers) * float(num_selected_numbers) / float(num_selectable_numbers))


    num_bits_vec = []
    num_selected_numbers_vec = []
    rate_vec = []
    for num_bits in [8, 16, 32, 64, 128]:
        for num_selected_numbers in [
            2, 5, 10,
            20, 50, 100,
            200, 500, 1000,
            2000, 5000, 10000,
            20000, 50000, 100000,
            200000, 500000, 1000000,
            2000000, 5000000, 10000000,
            20000000, 50000000, 100000000,
            200000000, 500000000, 1000000000,
            2000000000, 5000000000, 10000000000,
            20000000000, 50000000000, 100000000000,
            200000000000, 500000000000, 1000000000000,
            2000000000000, 5000000000000, 10000000000000,
        ]:
            num_selectable_numbers = 2**num_bits
            # num_selectable_numbers >> num_selected_numbers >> 1 が 1000 倍以上の差で成り立つ場合だけ計算することにする。
            if num_selectable_numbers < num_selected_numbers * 1000 or num_selected_numbers < 1000:
                continue

            rate = calc_random_number_collision_rate_approx(
                num_selectable_numbers=num_selectable_numbers,
                num_selected_numbers=num_selected_numbers,
            )

            num_bits_vec.append(num_bits)
            num_selected_numbers_vec.append(num_selected_numbers)
            rate_vec.append(rate)

    fig = px.line(
        x=num_selected_numbers_vec,
        y=rate_vec,
        color=num_bits_vec,
        log_x=True,
        log_y=True,
        markers=True,
    )
    fig.update_layout(
        legend_title_text="選択する整数のビット数",
        xaxis_title="選択した整数の数",
        yaxis_title="確率",
        title="ランダムに選択した整数が衝突する確率",
        xaxis={
            "exponentformat": "power",
        },
        yaxis={
            "exponentformat": "power",
        },
    )
    fig

まとめ
----------

ランダムな整数が衝突する確率を計算してグラフにすることができた。
ランダムな整数で ID などを決定する際に参考にしたい。

参考
---------

.. footbibliography::
