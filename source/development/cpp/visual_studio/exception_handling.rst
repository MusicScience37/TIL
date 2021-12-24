「アンワインド セマンティクスは有効にはなりません。」
=========================================================

Visual Studio で次のような警告が表示された。

.. code:: console

    warning C4530: C++ 例外処理を使っていますが、アンワインド セマンティクスは有効にはなりません。/EHsc を指定してください。

メッセージだけ読んでも何のことか分からないが、
``/EHsc`` を検索すると、
Visual Studio 公式ドキュメントの
`/EH (Exception handling model) | Microsoft Docs <https://docs.microsoft.com/en-us/cpp/build/reference/eh-exception-handling-model?view=msvc-170>`_
がヒットした。

これによると、C++ 標準の通りに例外を動作させるために
``/EHsc`` というコンパイルオプションが必要らしい。

Visual Studio における「C++」は Visual C++ であって C++ ではないため、
デフォルトでは例外を正しく扱えないのかもしれない。
