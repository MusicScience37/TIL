.. _development-cpp-approval-num-anal:

数値計算への Approval Tests の適用
===========================================

.. _development-cpp-approval-num-anal-intro:

背景
----------

数値計算の実装を試験するのに通常のテストフレームワークのアサーションを使用するには、
計算結果などの数値が一定の範囲に入っていることをチェックするような書き方をする。
例えば、
C++ のコンパイル時に平方根を計算する
``num_collect::constants::sqrt`` 関数（``std::sqrt`` の ``constexpr`` 版）の単体試験を行う
`あるソースコード <https://gitlab.com/MusicScience37/numerical-collection-cpp/-/blob/abcf85d2529893741ee171536d9244fb77f3adb6/test/units/constants/sqrt_test.cpp#L46>`_
では、次のように書いている。

.. code-block:: cpp

    constexpr auto true_val = static_cast<TestType>(1.234);
    constexpr TestType x = true_val * true_val;
    constexpr TestType val = num_collect::constants::sqrt(x);
    REQUIRE_THAT(val, Catch::Matchers::WithinRel(true_val));

ここでは、
:math:`x = \sqrt{x} \cdot \sqrt{x}` が成り立っていることを確認している。
``Catch::Matchers::WithinRel`` は相対誤差がオプション引数で指定可能な許容量の範囲内かどうかをチェックしており、
ここではデフォルトの値を用いている。

上記のようにデフォルトの許容量で試験ができれば良いが、
一般的には許容量の値を適切に調整する必要がある上に、
あるアルゴリズムである問題を解いた際の誤差がどの程度になるかを
あらかじめ算出しておくことができない場合が多い。
例えば、「古典的 Runge-Kutta 法」と呼ばれるアルゴリズムには、
誤差が
:math:`A h^5`
（:math:`h` はステップ幅と呼ばれるパラメータで、:math:`A` は問題に応じた係数）
になるという理論はあるが、
係数 :math:`A` の計算が容易でないため、
ある問題における具体的な誤差の値を推定することができない。
その結果、
「大きすぎない範囲で試験が通る適当な許容量を探索する」というヒューリスティックで
許容量を決定することになってしまい、
次の C++ のソースコード
（ `引用元 <https://gitlab.com/MusicScience37/numerical-collection-cpp/-/blob/abcf85d2529893741ee171536d9244fb77f3adb6/test/units/ode/runge_kutta/rk4_formula_test.cpp#L110>`_ ）
のように試験ケースごとの固有の定数として許容量を記載しておく必要がある。

.. code-block:: cpp

    constexpr double tol = 1e-10;  // この試験ケースにおける許容量
    REQUIRE_THAT(solver.variable(), eigen_approx(reference, tol));  // 誤差が許容量の範囲に入っているかチェック

このようなアサーションによる試験が容易でない場合において、
一度目視で確認された過去の処理結果との比較により処理結果のチェックを行う
`Approval Tests <https://approvaltests.com/>`_
というテストフレームワークが存在する。
ここでは、Approval Tests を数値計算に適用する。

.. note::
    Approval Tests は Java, C#, C++, php, Python, ... と様々な言語で使用できる。
    対応する言語については
    `公式ホームページ <https://approvaltests.com/>`_
    を参照。

Approval Tests を用いた試験の流れ
------------------------------------------

ここで、
`Approval Tests 公式ホームページ <https://approvaltests.com/>`_
の内容をもとに試験の流れをまとめる。

まず、試験を追加する際には次のようにする。

1. 試験を実装する。
2. 試験を実行する。確認済みの処理結果のファイルはないため、試験失敗となる。
3. 試験実行時に生成される処理結果のファイルを確認し、問題がなければ確認済みの処理結果として保存する。
4. 再度試験を実行し、試験が通ることを確認する。

その後、実装や試験の変更により処理結果が変更になった場合は次のようにする。

1. 試験を実行する。試験が失敗する。
2. 試験実行時に生成される処理結果のファイルを確認し、問題がなければ確認済みの処理結果として保存する。
3. 再度試験を実行し、試験が通ることを確認する。

処理結果の変動の要因
-------------------------

処理結果は次のような要因により変化する可能性がある。

1. ソースコード（アルゴリズムの実装または試験）の変更

   - 性能向上やバグにより処理結果が変化する。

2. コンパイラの変更

   - コンパイラやそのオプションの変更により細かい浮動小数点数演算の命令が変化し、
     丸め誤差が変化する可能性がある。

3. 乱数による変動

   - 乱数にもとづいて処理を行うアルゴリズムでは、
     乱数のシード値やアルゴリズムにより処理結果が変化する。
     しかし、ソースコード上で乱数のシード値やアルゴリズムを固定して試験を行うことにより回避できる。
     （例：遺伝的アルゴリズム。）

ここで、ソースコードの変更による処理結果の変化はしっかり確認する必要がある。
しかし、コンパイラの変更による処理結果の変化は考慮に入れないようにしたい。
そのため、使用する浮動小数点数の桁数よりも少なめの桁数までの値を用いて処理結果の比較を行うようにする。
桁数は適宜調整を行う必要があるが、アルゴリズムに依存しない定数として共有できる。

実験
-----------------------

ここでは、
:ref:`development-cpp-approval-num-anal-intro`
で触れた ``num_collect::constants::sqrt`` 関数を対象として試験を実装した。
``num_collect::constants::sqrt`` 関数は
`numerical-collection-cpp ライブラリ <https://gitlab.com/MusicScience37/numerical-collection-cpp>`_
の一部である。

C++ の関数を試験するため、
Approval Tests の C++ 版である
`Approval Tests for C++ <https://github.com/approvals/ApprovalTests.cpp>`_
を使用する。
Approval Tests for C++ は既存のテストフレームワークをベースに動作するものであり、
Boost.Test, Catch2, Google Tests, ... といった様々なテストフレームワークで使用できるが、
ここでは
`Catch2 <https://github.com/catchorg/Catch2>`_
を使用した。

ライブラリのバージョンは以下の通りである。

- Approval Tests for C++ 10.12.1

- Catch2 v3.0.0-preview4

  - 参考：:ref:`development-cpp-approval-catch2-v3`

- numerical-collection-cpp 0.3.0

- `fmt <https://github.com/fmtlib/fmt>`_ 8.1.1

  - 数値のフォーマットに使用した。

Approval Tests for C++ にはソースコード上で指定する様々なオプションがあるが、
ここでは以下のように設定した。

.. code-block:: cpp

    #include <memory>

    #define APPROVALS_CATCH
    #include <ApprovalTests.hpp>

    // ソースコードのディレクトリの approvals サブディレクトリに
    // Approval Tests における処理結果のファイルを配置する。
    static const auto directory_config =
        ApprovalTests::Approvals::useApprovalsSubdirectory("approvals");

    // 試験を CMake で自動化するにあたって、
    // 実行時にインタラクティブに処理結果の確認をするというデフォルト設定が不便だったため、
    // 自動で承認済みの処理結果のファイルを上書きする設定を使用した。
    // 処理結果のファイルを Git で管理し、
    // 変更を確認できるようにしておくという前提のもとでは問題ない。
    static const auto default_options =
        ApprovalTests::Approvals::useAsDefaultReporter(
            std::make_shared<ApprovalTests::AutoApproveReporter>());

試験コードは次のようにした。

.. code-block:: cpp

    #include <ApprovalTests.hpp>
    #include <catch2/catch_test_macros.hpp>
    #include <fmt/format.h>
    #include <num_collect/constants/sqrt.h>

    TEST_CASE("sqrt") {
        // 平方根の計算を行う対象の値の一覧
        const auto inputs = std::vector<double>{0.0, 0.5, 1.0, 2.0, 123.456};

        ApprovalTests::CombinationApprovals::verifyAllCombinations(
            "sqrt",
            [](double input) {
                // 本来はコンパイル時定数で使用するための関数だが、
                // ここでは簡略化のため実行時に使用している。
                const double my_sqrt = num_collect::constants::sqrt(input);
                const double std_sqrt = std::sqrt(input);
                const int precision = 10;  // 処理結果として出力する桁数

                return fmt::format(
                    "Input: {1:.{0}e}\n"
                    "my_sqrt:  {2:.{0}e}\n"
                    "std_sqrt: {3:.{0}e}",
                    precision, input, my_sqrt, std_sqrt);
            },
            inputs);
    }

ここで、ソースコード上にある定数 ``precision`` は
``double`` 型の精度（10 進数で 15 桁程度）を踏まえて選択したものである。

上記のソースコードにより処理結果としては以下のような内容のファイルが生成される。

.. code-block:: none

    sqrt


    (0) => Input: 0.0000000000e+00
    my_sqrt:  0.0000000000e+00
    std_sqrt: 0.0000000000e+00
    (0.5) => Input: 5.0000000000e-01
    my_sqrt:  7.0710678119e-01
    std_sqrt: 7.0710678119e-01
    (1) => Input: 1.0000000000e+00
    my_sqrt:  1.0000000000e+00
    std_sqrt: 1.0000000000e+00
    (2) => Input: 2.0000000000e+00
    my_sqrt:  1.4142135624e+00
    std_sqrt: 1.4142135624e+00
    (123.456) => Input: 1.2345600000e+02
    my_sqrt:  1.1111075555e+01
    std_sqrt: 1.1111075555e+01

上記の試験コードは
`exp-approval-num-anal リポジトリ <https://gitlab.com/MusicScience37/exp-approval-num-anal>`_
に保存している。
