.. _development-cpp-approval-catch2-v3:

Approval Tests を Catch2 v3 で使用する
=========================================

`Approval Tests for C++ <https://github.com/approvals/ApprovalTests.cpp>`_
を
`Catch2 <https://github.com/catchorg/Catch2>`_
のバージョン 3 で使用する場合に、
2022/2/13 の最新版では少し調整が必要になったため、
ここにメモを残しておく。

使用したライブラリのバージョン
-----------------------------------

- Approval Tests for C++ 10.12.1
- Catch2 v3.0.0-preview4

問題点
-------------

- Approval Tests が ``catch2/catch.hpp`` ファイルを使用するが、
  Catch2 v3 にはそのようなヘッダがない。
- Approval Tests が ``Catch::TestEventListenerBase`` というクラスを使用するが、
  Catch2 v3 では ``Catch::EventListenerBase`` という名前に変更されている。

調整内容
--------------

インクルードディレクトリに ``catch2/catch.hpp`` ファイルを追加し、
以下のように記載しておくと、
ビルドができるようになる。

.. code-block:: cpp

    #include <catch2/catch_test_case_info.hpp>
    #include <catch2/catch_test_macros.hpp>
    #include <catch2/reporters/catch_reporter_event_listener.hpp>
    #include <catch2/reporters/catch_reporter_registrars.hpp>

    namespace Catch {

    struct TestEventListenerBase : public EventListenerBase {
        using EventListenerBase::EventListenerBase;
    };

    }  // namespace Catch
