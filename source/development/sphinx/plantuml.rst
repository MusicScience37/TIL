PlantUML の利用
==================

Sphinx の文書に PlantUML の図を挿入するためには、次のようにする。

1. `PlantUML のホームページ <https://plantuml.com/>`_ から
   plantuml.jar をダウンロードする。
2. 拡張機能をインストールする。

.. code:: console

    $ pip3 install sphinxcontrib-plantuml

3. conf.py に設定を追加する。

.. code:: python

    extensions += ['sphinxcontrib.plantuml']
    plantuml='java -jar $PLANTUML_JAR_PATH'
    plantuml_output_format = 'svg'
    plantuml_syntax_error_image = True

4. 本文中に図を挿入する。

.. code:: rst

    .. uml::

        A -> B: request
        return response

.. uml::

    A -> B: request
    return response
