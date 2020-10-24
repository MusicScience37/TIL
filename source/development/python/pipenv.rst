pipenv
=========

pipenv は Python の仮想環境を作成するコマンド。
Python のバージョンとパッケージを隔離することができる。

インストール
-------------------

Python のバージョンを選択したい場合、pyenv をインストールしておく。

.. code:: console

    $ pip install --user pipx
    $ pipx install pipenv

使用例
------------------

2020/10/24 時点の本リポジトリで試した。

プロジェクトのディレクトリに移動して初期化を行う。

.. code:: console

    $ pipenv --three
    Creating a virtualenv for this project…
    Pipfile: /home/kenta/projects/doc/til/Pipfile
    Using /home/kenta/.pyenv/versions/3.9.0/bin/python3.9 (3.9.0) to create virtualenv…
    ⠸ Creating virtual environment...created virtual environment CPython3.9.0.final.0-64 in 236ms
      creator CPython3Posix(dest=/home/kenta/projects/doc/til/.venv, clear=False, global=False)
      seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/home/kenta/.local/share/virtualenv)
        added seed packages: pip==20.2.3, setuptools==50.3.1, wheel==0.35.1
      activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator
    
    ✔ Successfully created virtual environment! 
    Virtualenv location: /home/kenta/projects/doc/til/.venv
    Creating a Pipfile for this project…

パッケージを追加する。

.. code:: console

    $ pipenv install sphinx~=3.2.1
    Installing sphinx~=3.2.1…
    Adding sphinx to Pipfile's [packages]…
    ✔ Installation Succeeded 
    Pipfile.lock not found, creating…
    Locking [dev-packages] dependencies…
    Locking [packages] dependencies…
    Building requirements...
    Resolving dependencies...
    ✔ Success! 
    Updated Pipfile.lock (165e96)!
    Installing dependencies from Pipfile.lock (165e96)…
      🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 0/0 — 00:00:00
    To activate this project's virtualenv, run pipenv shell.
    Alternatively, run a command inside the virtualenv with pipenv run.

パッケージを更新する。

.. code:: console

    $ pipenv update
    Building requirements...
    Resolving dependencies...
    ✔ Success! 
    Skipped Update of Package watchdog: 0.10.3 installed,, 0.10.3 available.
    Skipped Update of Package urllib3: 1.25.11 installed,, 1.25.11 available.
    Skipped Update of Package tornado: 6.0.4 installed,, 6.0.4 available.
    Skipped Update of Package sphinxcontrib-serializinghtml: 1.1.4 installed,, 1.1.4 available.
    Skipped Update of Package sphinxcontrib-qthelp: 1.0.3 installed,, 1.0.3 available.
    Skipped Update of Package sphinxcontrib-plantuml: 0.18.1 installed, 0.18.1 required (~=0.18 set in Pipfile), 0.18.1 available.
    Skipped Update of Package sphinxcontrib-jsmath: 1.0.1 installed,, 1.0.1 available.
    Skipped Update of Package sphinxcontrib-htmlhelp: 1.0.3 installed,, 1.0.3 available.
    Skipped Update of Package sphinxcontrib-devhelp: 1.0.2 installed,, 1.0.2 available.
    Skipped Update of Package sphinxcontrib-applehelp: 1.0.2 installed,, 1.0.2 available.
    Skipped Update of Package Sphinx: 3.2.1 installed, Any required (~=3.2.1 set in Pipfile), 3.2.1 available.
    Skipped Update of Package sphinx-rtd-theme: 0.5.0 installed, 0.5.0 required (~=0.5.0 set in Pipfile), 0.5.0 available.
    Skipped Update of Package sphinx-autobuild: 0.7.1 installed, 0.7.1 required (~=0.7.1 set in Pipfile), 2020.9.1 available.
    Skipped Update of Package snowballstemmer: 2.0.0 installed,, 2.0.0 available.
    Skipped Update of Package six: 1.15.0 installed,, 1.15.0 available.
    Skipped Update of Package requests: 2.24.0 installed,, 2.24.0 available.
    Skipped Update of Package PyYAML: 5.3.1 installed,, 5.3.1 available.
    Skipped Update of Package pytz: 2020.1 installed,, 2020.1 available.
    Skipped Update of Package pyparsing: 2.4.7 installed,, 2.4.7 available.
    Skipped Update of Package Pygments: 2.7.1 installed,, 2.7.1 available.
    Skipped Update of Package port-for: 0.3.1 installed,, 0.4 available.
    Skipped Update of Package pathtools: 0.1.2 installed,, 0.1.2 available.
    Skipped Update of Package packaging: 20.4 installed,, 20.4 available.
    Skipped Update of Package MarkupSafe: 1.1.1 installed,, 1.1.1 available.
    Skipped Update of Package livereload: 2.6.3 installed,, 2.6.3 available.
    Skipped Update of Package Jinja2: 2.11.2 installed,, 2.11.2 available.
    Skipped Update of Package imagesize: 1.2.0 installed,, 1.2.0 available.
    Skipped Update of Package idna: 2.10 installed,, 2.10 available.
    Skipped Update of Package docutils: 0.16 installed,, 0.16 available.
    Skipped Update of Package chardet: 3.0.4 installed,, 3.0.4 available.
    Skipped Update of Package certifi: 2020.6.20 installed,, 2020.6.20 available.
    Skipped Update of Package breathe: 4.20.0 installed, 4.20.0 required (~=4.20.0 set in Pipfile), 4.23.0 available.
    Skipped Update of Package Babel: 2.8.0 installed,, 2.8.0 available.
    Skipped Update of Package argh: 0.26.2 installed,, 0.26.2 available.
    Skipped Update of Package alabaster: 0.7.12 installed,, 0.7.12 available.
    All packages are up to date!

インストールされたパッケージを使用する。

.. code:: console

    $ pipenv shell

参考
-------

`Pipenv: Python Dev Workflow for Humans — pipenv 2020.8.13.dev0 documentation <https://pipenv.pypa.io/en/latest/>`_
