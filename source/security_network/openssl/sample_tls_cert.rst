TLS 証明書のサンプルを用意する
==============================

テスト用に TLS 証明書を用意したい。
本物の認証局に依頼すると費用がかかるため、
手元で代わりのものを作成する。

基本方針
----------

本物の認証局で行うことになる手順を openssl コマンドで再現する。

.. uml::

    participant ユーザ as User
    participant 認証局 as CA

    CA -> CA ++ : 認証局の自己署名証明書と秘密鍵を作成
    deactivate CA
    CA ->>] : 証明書を公開

    ... ...

    User -> User ++ : 秘密鍵を作成
    deactivate User
    User -> User ++ : 証明書署名要求\n(Certificate Signing Request, CSR)\nを作成
    deactivate User
    User -> CA ++ : 証明書署名要求を送付
    CA -> CA ++ : 認証局の署名付き証明書を作成
    deactivate CA
    CA --> User -- : 証明書を送付

    User -> User ++ : 証明書と秘密鍵を利用
    deactivate User

openssl コマンドによる証明書作成
-----------------------------------

ここでは、テスト用のサーバの証明書の作成を行うとした場合の手順を示す。
作業ディレクトリ（場所は問わない）には、
手順が成功すれば以下のファイルが生成される。

.. csv-table:: 作成するファイル一覧
    :header: "ファイル名", "内容"
    :widths: auto

    openssl-ca.cnf, 認証局の証明書発行用の設定ファイル
    ca.crt, 認証局の証明書
    ca.key, 認証局の秘密鍵
    ca.srl, 認証局が署名した証明書のシリアル番号
    openssl-server.cnf, サーバの証明書署名要求発行時の設定ファイル
    server.crt, サーバの証明書
    server.csr, サーバの証明書署名要求
    server.key, サーバの秘密鍵

.. note::
    ここで作成するのは勝手な「オレオレ証明書」のため、
    アプリケーションに認証局の証明書として登録しなければ使用できない。

.. note::
    複数の証明書を用意したい場合は 3. ユーザ側の設定ファイルの作成から始めること。

1. 認証局の設定ファイル作成

    認証局の証明書の発行に使用する設定ファイルを作成する。
    ここでは、以下のような内容の openssl-ca.cnf ファイルを作成する。

    .. code:: ini

        [ req ]
        default_bits           = 4096
        default_keyfile        = privkey.pem
        distinguished_name     = req_distinguished_name
        attributes             = req_attributes
        req_extensions         = v3_ca
        prompt                 = no
        output_password        = test

        dirstring_type = nobmp

        [ req_distinguished_name ]
        countryName                    = JP
        #countryName_default            = AU
        #countryName_min                = 2
        #countryName_max                = 2

        localityName                   = Test

        organizationalUnitName         = Test

        commonName                     = Test
        #commonName_max                 = 64

        emailAddress                   = test@example.com
        #emailAddress_max               = 40

        [ req_attributes ]
        challengePassword              = test
        #challengePassword_min          = 4
        #challengePassword_max          = 20

        [ v3_ca ]

        subjectKeyIdentifier=hash
        authorityKeyIdentifier=keyid:always,issuer:always
        basicConstraints = critical, CA:true

2. 認証局の自己署名証明書と秘密鍵の作成

    .. code:: console

        $ openssl req -config openssl-ca.cnf -new -x509 -days 3650 -keyout ca.key -out ca.crt
        Generating a RSA private key
        ..............................................................++++
        ............................++++
        writing new private key to 'ca.key'
        -----

    ca.crt, ca.key が生成される。

3. ユーザ側の設定ファイルの作成

    ユーザの証明書署名要求の生成に使用する設定ファイルを作成する。
    ここでは、以下のような内容の openssl-server.cnf ファイルを作成する。

    .. code:: ini

        [ req ]
        default_bits           = 4096
        default_keyfile        = privkey.pem
        distinguished_name     = req_distinguished_name
        attributes             = req_attributes
        req_extensions         = v3_ca
        prompt                 = no
        output_password        = test

        dirstring_type = nobmp

        [ req_distinguished_name ]
        countryName                    = JP
        #countryName_default            = AU
        #countryName_min                = 2
        #countryName_max                = 2

        localityName                   = Test

        organizationalUnitName         = Test

        commonName                     = 127.0.0.1
        #commonName_max                 = 64

        emailAddress                   = test@example.com
        #emailAddress_max               = 40

        [ req_attributes ]
        challengePassword              = test
        #challengePassword_min          = 4
        #challengePassword_max          = 20

        [ v3_ca ]

        subjectKeyIdentifier=hash

    .. note::
        commonName はサーバへアクセスする際の名前として使用されるもの。
        正しく入力しなければ認証に失敗する。

4. 証明書署名要求の作成

    .. code:: console

        $ openssl req -config openssl-server.cnf -new -keyout server.key -out server.csr

        Generating a RSA private key
        ......................++++
        ......................................................++++
        writing new private key to 'server.key'
        -----

    server.csr, server.key が生成される。

5. 証明書への署名

    .. code:: console

        $ openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 3650 -passin pass:test
        Signature ok
        subject=C = JP, L = Test, OU = Test, CN = 127.0.0.1, emailAddress = test@example.com
        Getting CA Private Key

    ca.srl, server.crt が生成される。
    （ca.srl は発行済み証明書のシリアル番号一覧となっている。）

    .. note::
        -passin オプションにある test は証明書のパスワード (output_password) として設定したもの。

6. 証明書のチェック

    .. code:: console

        $ openssl verify -CAfile ca.crt server.crt
        server.crt: OK

参考
-------

- `mosquitto-tls man page | Eclipse Mosquitto <https://mosquitto.org/man/mosquitto-tls-7.html>`_
- `/docs/man1.1.1/man1/req.html <https://www.openssl.org/docs/man1.1.1/man1/req.html>`_
- `/docs/man1.1.1/man1/x509.html <https://www.openssl.org/docs/man1.1.1/man1/x509.html>`_
- `/docs/man1.1.1/man1/openssl.html <https://www.openssl.org/docs/man1.1.1/man1/openssl.html>`_
