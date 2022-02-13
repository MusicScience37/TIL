Catch2 でモックテスト
===========================

`Catch2 <https://github.com/catchorg/Catch2>`_
でモックテストをする方法の調査記録。

今のところ :ref:`development_cpp_catch2_with_mocking_trompeloeil` が有力。

gMock
-----------

gMock は `Google Test <https://github.com/google/googletest>`_ に含まれる
モックテストフレームワークで、
C++ mock test で Google 検索するとほとんどこれしか出てこない程度には
スタンダードになっている。
しかし、Google Test で使用することを前提としており、
Google Test の関数を内部で呼び出している。

一応、Catch2 と一緒に使用するための設定例が
`catch2-with-gmock <https://github.com/matepek/catch2-with-gmock>`_
にあるが、
Google Test と Catch2 の内部の関数に依存しているうえに、
大してメンテナンスされていない。

FakeIt
----------------

`FakeIt <https://github.com/eranpeer/FakeIt>`_ は
複数のテストフレームワークに対応したモックテストフレームワーク。

残念ながら、master ブランチは 2019/11/30 で止まっており、
最新の Catch2 では動作しないという
`Issue 197 <https://github.com/eranpeer/FakeIt/issues/197>`_
と修正の
`Pull Request 201 <https://github.com/eranpeer/FakeIt/pull/201>`_
は放置されている
（2020/12/16 現在）。
開発が終了しているようだ。

.. _development_cpp_catch2_with_mocking_trompeloeil:

Trompeloeil
----------------

`Trompeloeil <https://github.com/rollbear/trompeloeil>`_ は
複数のテストフレームワークに対応したモックテストフレームワーク。

`最新リリースにおける Catch2 対応ヘッダ <https://github.com/rollbear/trompeloeil/blob/v39/include/catch2/trompeloeil.hpp>`_
を見る限り、使用している Catch2 の機能は以下の通り。

- ``CATCH_VERSION_MAJOR`` マクロ
- ``FAIL`` マクロ
- ``CAPTURE`` マクロ
- ``CHECK`` マクロ
- ``REQUIRE`` マクロ

これらは、2020/12/16 現在進んでいるメジャーバージョンアップの
Catch2 v3.0.0-preview3 でも存在している基本的なマクロである。

公式の
`Cook Book <https://github.com/rollbear/trompeloeil/blob/master/docs/CookBook.md>`_
に大量のドキュメントがある。

使用例
~~~~~~~~~

`Test Catch2 Trompeloeil <https://gitlab.com/MusicScience37/test-catch2-trompeloeil>`_
より引用。

ソースコード：

.. code-block:: cpp

    #include <catch2/catch_test_macros.hpp>
    #include <catch2/catch_version_macros.hpp>
    #include <catch2/trompeloeil.hpp>

    class IAdder {
    public:
        virtual int add(int x, int y) = 0;
    };

    class MockAdder : public IAdder {
    public:
        MAKE_MOCK2(add, int(int, int), override);
    };

    TEST_CASE("IAdder::add") {
        SECTION("success case") {
            MockAdder adder;

            int x = 0;
            int y = 0;
            REQUIRE_CALL(adder, add(ANY(int), ANY(int)))
                .LR_SIDE_EFFECT(x = _1)
                .LR_SIDE_EFFECT(y = _2)
                .RETURN(_1 + _2)
                .TIMES(1);

            REQUIRE(adder.add(2, 3) == 5);
            REQUIRE(x == 2);
            REQUIRE(y == 3);
        }

        SECTION("fail case") {
            MockAdder adder;

            using trompeloeil::eq;

            REQUIRE_CALL(adder, add(eq(2), ANY(int))).RETURN(_1 + _2).TIMES(1);

            REQUIRE(adder.add(1, 2) == 3);
        }
    }

実行例：

.. code-block:: console

    $ ./build/Debug/bin/test_mocking

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    test_mocking is a Catch v3.0.0-preview.3 host application.
    Run with -? for options

    -------------------------------------------------------------------------------
    IAdder::add
      fail case
    -------------------------------------------------------------------------------
    ../../test/test_mocking.cpp:32
    ...............................................................................

    ../../extern/Trompeloeil/include/catch2/trompeloeil.hpp:40: FAILED:
    explicitly with message:
      No match for call of add with signature int(int, int) with.
        param  _1 == 1
        param  _2 == 2

    Tried adder.add(eq(2), ANY(int)) at ../../test/test_mocking.cpp:37
        Expected  _1 == 2

    ../../test/test_mocking.cpp:39: FAILED:
      REQUIRE( adder.add(1, 2) == 3 )
    due to unexpected exception with message:
      Exception translation was disabled by CATCH_CONFIG_FAST_COMPILE

    ===============================================================================
    test cases: 1 | 1 failed
    assertions: 6 | 4 passed | 2 failed

Mockitopp
--------------

`Mockitopp <https://github.com/tpounds/mockitopp>`_ は
モックテストフレームワーク。
特にテストフレームワークへの依存はなく、
テストの失敗時は例外を投げることでそれを伝えるようになっている模様。

大してドキュメントがなく、更新も 2019/7/17 で止まっているため、
これ以上は調べていない。
