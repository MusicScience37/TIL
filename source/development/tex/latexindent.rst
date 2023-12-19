TeX ファイルのフォーマッタ latexindent
==============================================

`latexindent <https://www.ctan.org/pkg/latexindent>`_
というツールで TeX ファイルのフォーマットを行うことができる。

使用例
------------

例えば、ファイル ``sample.tex`` をフォーマットしてファイルの内容を更新するのであれば、
以下のようなコマンドを実行する。

.. code-block:: console

    $ latexindent -w -s sample.tex

コマンドラインオプション
----------------------------

ヘルプで表示される latexindent コマンドの使用方法は以下の通り。

.. cspell: disable

.. code-block:: console

    $ latexindent --help
    latexindent.pl version 3.23.3, 2023-10-13
    usage: latexindent.pl [options] [file]
          -v, --version
              displays the version number and date of release
          -vv, --vversion
              displays verbose version details: the version number, date of release,
              and location details of latexindent.pl and defaultSettings.yaml
          -h, --help
              help (see the documentation for detailed instructions and examples)
          -sl, --screenlog
              log file will also be output to the screen
          -o, --outputfile=<name-of-output-file>
              output to another file; sample usage:
                    latexindent.pl -o outputfile.tex myfile.tex
                    latexindent.pl -o=outputfile.tex myfile.tex
          -w, --overwrite
              overwrite the current file; a backup will be made, but still be careful
          -wd, --overwriteIfDifferent
              overwrite the current file IF the indented text is different from original;
              a backup will be made, but still be careful
          -s, --silent
              silent mode: no output will be given to the terminal
          -t, --trace
              tracing mode: verbose information given to the log file
          -l, --local[=myyaml.yaml]
              use `localSettings.yaml`, `.localSettings.yaml`, `latexindent.yaml`,
              or `.latexindent.yaml` (assuming one of them exists in the directory of your file or in
              the current working directory); alternatively, use `myyaml.yaml`, if it exists;
              sample usage:
                    latexindent.pl -l some.yaml myfile.tex
                    latexindent.pl -l=another.yaml myfile.tex
                    latexindent.pl -l=some.yaml,another.yaml myfile.tex
          -y, --yaml=<yaml settings>
              specify YAML settings; sample usage:
                    latexindent.pl -y="defaultIndent:' '" myfile.tex
                    latexindent.pl -y="defaultIndent:' ',maximumIndentation:' '" myfile.tex
          -d, --onlydefault
              ONLY use defaultSettings.yaml, ignore ALL (yaml) user files
          -g, --logfile=<name of log file>
              used to specify the name of logfile (default is indent.log)
          -c, --cruft=<cruft directory>
              used to specify the location of backup files and indent.log
          -m, --modifylinebreaks
              modify linebreaks before, during, and at the end of code blocks;
              trailing comments and blank lines can also be added using this feature
          -r, --replacement
              replacement mode, allows you to replace strings and regular expressions
              verbatim blocks not respected
          -rv, --replacementrespectverb
              replacement mode, allows you to replace strings and regular expressions
              while respecting verbatim code blocks
          -rr, --onlyreplacement
              *only* replacement mode, no indentation;
              verbatim blocks not respected
          -k, --check mode
              will exit with 0 if document body unchanged, 1 if changed
          -kv, --check mode verbose
              as in check mode, but outputs diff to screen as well as to logfile
          -n, --lines=<MIN-MAX>
              only operate on selected lines; sample usage:
                    latexindent.pl --lines 3-5 myfile.tex
                    latexindent.pl --lines 3-5,7-10 myfile.tex
          --GCString
              loads the Unicode::GCString module for the align-at-ampersand routine
              Note: this requires the Unicode::GCString module to be installed on your system

.. cspell: enable

設定ファイル
-------------------

latexindent は ``.latexindent.yaml`` などのファイル名の YAML ファイルから設定を読み込む。
設定の内容については
`latexindent のドキュメント <https://latexindentpl.readthedocs.io/en/latest/sec-default-user-local.html>`_
を参照。
