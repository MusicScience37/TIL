pybind11 でインタプリタを埋め込んだときに rdynamic フラグが必要？（未解決）
===========================================================================

pybind11 を使用してインタプリタを埋め込んだ際に、
``-rdynamic`` フラグをリンク時に使用しなければ
実行時に undefined symbol が出るという事態に陥った。

.. todo:: 結局原因がよく分かっていない。

参考
-------

`Problem with embedded Python in combination with CMake 3.4+ · Issue #1662 · pybind/pybind11 · GitHub <https://github.com/pybind/pybind11/issues/1662>`_
