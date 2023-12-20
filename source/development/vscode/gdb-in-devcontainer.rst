Devcontainer 内で GDB を使用する
======================================

VSCode の Devcontainer 上で GDB を使用すると、
普段は出ない警告やエラーが出るケースがある。

例えば、デッドロックや無限ループで止まってしまったプロセスに
GDB でアタッチしようとすると…

.. code-block:: console

    $ gdb ./build/Debug/bin/hash_tables_bench_maps 1188
    GNU gdb (Ubuntu 12.1-3ubuntu2) 12.1
    Copyright (C) 2022 Free Software Foundation, Inc.
    License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
    This is free software: you are free to change and redistribute it.
    There is NO WARRANTY, to the extent permitted by law.
    Type "show copying" and "show warranty" for details.
    This GDB was configured as "x86_64-linux-gnu".
    Type "show configuration" for configuration details.
    For bug reporting instructions, please see:
    <https://www.gnu.org/software/gdb/bugs/>.
    Find the GDB manual and other documentation resources online at:
        <http://www.gnu.org/software/gdb/documentation/>.

    For help, type "help".
    Type "apropos word" to search for commands related to "word"...
    Reading symbols from ./build/Debug/bin/hash_tables_bench_maps...
    Attaching to program: /workspaces/cpp-hash-tables/build/Debug/bin/hash_tables_bench_maps, process 1188
    Could not attach to process.  If your uid matches the uid of the target
    process, check the setting of /proc/sys/kernel/yama/ptrace_scope, or try
    again as the root user.  For more details, see /etc/sysctl.d/10-ptrace.conf
    ptrace: Operation not permitted.
    /workspaces/cpp-hash-tables/1188: No such file or directory.

ptrace の権限がないというエラーが発生する。

このような問題は ``devcontainer.json`` に以下の設定を加えることで解決する。

.. code-block:: json

    {
      "runArgs": ["--cap-add=SYS_PTRACE", "--security-opt", "seccomp=unconfined"],
    }

.. seealso::

    - `vscode-dev-containers/devcontainer.json at 5a084a93b0736ea86395ac99019a5b72a00b6341 · microsoft/vscode-dev-containers <https://github.com/microsoft/vscode-dev-containers/blob/5a084a93b0736ea86395ac99019a5b72a00b6341/container-templates/image/.devcontainer/devcontainer.json#L23>`_
    - `Docker上でgdbを動かす - 俺より凄いやつしかいない。 <https://www.cyamax.com/entry/2018/02/09/070000>`_
