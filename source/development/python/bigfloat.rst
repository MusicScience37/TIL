.. _development-python-bigfloat:

任意精度演算ライブラリ bigfloat
=================================

C 言語で書かれた任意精度浮動小数点演算のライブラリ
`GNU MPFR Library <https://www.mpfr.org/>`_
を Python から使用できるライブラリの 1 つに
`bigfloat <https://bigfloat.readthedocs.io/en/latest/index.html>`_
パッケージがある。

Ubuntu へのインストール
-------------------------

bigfloat パッケージのインストールには
MPFR ライブラリが必要なため注意。

.. code-block:: console

    $ sudo apt install libmpfr-dev
    $ pip install bigfloat

使用例
--------------

.. code-block:: python

    >>> from bigfloat import BigFloat
    >>> BigFloat(2)
    BigFloat.exact('2.00000000000000000000000000000000000', precision=113)
    >>> BigFloat.fromhex('0x1.8p+0')
    BigFloat.exact('1.50000000000000000000000000000000000', precision=113)
    >>> '{:a}'.format(BigFloat.fromhex('0x1.8p+0'))
    '0x1.8p+0'
    >>> '{:a}'.format(BigFloat.fromhex('0x1.fb15fa86d92b228b6596fdb93fp+0') + BigFloat.fromhex('0x1.22738c56c3ecf61e3f58931ec2p+0'))
    '0x3.1d8986dd9d1818a9a4ef90d801p+0'
    >>> '{:a}'.format(BigFloat.fromhex('0x1.fb15fa86d92b228b6596fdb93fp+0') - BigFloat.fromhex('0x1.22738c56c3ecf61e3f58931ec2p+0'))
    '0xd.8a26e30153e2c6d263e6a9a7dp-4'
    >>> '{:a}'.format(BigFloat.fromhex('0x1.fb15fa86d92b228b6596fdb93fp+0') * BigFloat.fromhex('0x1.22738c56c3ecf61e3f58931ec2p+0'))
    '0x2.3f53c6a82f11712dad9c5fd34db6p+0'
    >>> '{:a}'.format(BigFloat.fromhex('0x1.fb15fa86d92b228b6596fdb93fp+0') / BigFloat.fromhex('0x1.22738c56c3ecf61e3f58931ec2p+0'))
    '0x1.bef0545a14fda729d96fa6624b59p+0'
