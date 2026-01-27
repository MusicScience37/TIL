TLS のテスト用のサーバとクライアントの実行
=========================================================

..
    cspell:ignore servername Ciphersuite

OpenSSL のコマンドラインには
テスト用のサーバとクライアントを実行する機能がある。

サーバとクライアントの起動手順
---------------------------------

1. ファイルの準備

   .. uml::

       @startsalt
       {{T
       + test              | 作業ディレクトリ
       ++ ca-certificates  | 認証局の証明書用のディレクトリ
       +++ ca.crt          | 認証局の証明書
       ++ server           | サーバ用の作業ディレクトリ
       +++ server.crt      | サーバの証明書
       +++ server.key      | サーバの秘密鍵
       }}
       @endsalt

2. 認証局の証明書のハッシュの生成

   .. code:: console

       $ cd test
       $ openssl rehash ./ca-certificates
       $ ls ./ca-certificates/
       baf3acd5.0  ca.crt

   拡張子 .0 のシンボリックリンクが生成される。

3. サーバの起動

   .. code:: console

       $ cd server
       $ openssl s_server -accept 127.0.0.1:12345 -cert server.crt -key server.key --pass pass:test -CApath ../ca-certificates
       Using default temp DH parameters
       ACCEPT

4. クライアントの起動

   .. code:: console

       $ cd test
       $ openssl s_client -connect 127.0.0.1:12345 -CApath ./ca-certificates -brief -no_ign_eof < /dev/null
       Can't use SSL_get_servername
       CONNECTION ESTABLISHED
       Protocol version: TLSv1.3
       Ciphersuite: TLS_AES_256_GCM_SHA384
       Peer certificate: C = JP, L = Test, OU = Test, CN = 127.0.0.1, emailAddress = test@example.com
       Hash used: SHA256
       Signature type: RSA-PSS
       Verification: OK
       Server Temp Key: X25519, 253 bits
       DONE

   .. hint::
       途中にある以下を見ることで、認証できたことが確認できる。

       .. code:: none

           Verification: OK

5. Ctrl + C でサーバを終了させる。

TLS 相互認証
---------------

TLS の相互認証の検証は、以下のように行うことができる。

1. ファイルの準備

   .. uml::

       @startsalt
       {{T
       + test              | 作業ディレクトリ
       ++ ca-certificates  | 認証局の証明書用のディレクトリ
       +++ ca.crt          | 認証局の証明書
       ++ server           | サーバ用の作業ディレクトリ
       +++ server.crt      | サーバの証明書
       +++ server.key      | サーバの秘密鍵
       ++ client           | クライアント用の作業ディレクトリ
       +++ client.crt      | クライアントの証明書
       +++ client.key      | クライアントの秘密鍵
       }}
       @endsalt

2. 認証局の証明書のハッシュの生成

   .. code:: console

       $ cd test
       $ openssl rehash ./ca-certificates
       $ ls ./ca-certificates/
       baf3acd5.0  ca.crt

   拡張子 .0 のシンボリックリンクが生成される。

3. サーバの起動

   .. code:: console

       $ cd server
       $ openssl s_server -accept 127.0.0.1:12345 -cert server.crt -key server.key -CApath ../ca-certificates --pass pass:test -Verify 10
       verify depth is 10, must return a certificate
       Using default temp DH parameters
       ACCEPT

   .. note::
       -Verify オプションでクライアントの認証を求めるようにしている。

4. クライアントの起動

   .. code:: console

       $ cd test
       $ openssl s_client -connect 127.0.0.1:12345 -cert client.crt -key client.key --pass pass:test -CApath ../ca-certificates -brief -no_ign_eof < /dev/null
       Can't use SSL_get_servername
       CONNECTION ESTABLISHED
       Protocol version: TLSv1.3
       Ciphersuite: TLS_AES_256_GCM_SHA384
       Requested Signature Algorithms: ECDSA+SHA256:ECDSA+SHA384:ECDSA+SHA512:Ed25519:Ed448:RSA-PSS+SHA256:RSA-PSS+SHA384:RSA-PSS+SHA512:RSA-PSS+SHA256:RSA-PSS+SHA384:RSA-PSS+SHA512:RSA+SHA256:RSA+SHA384:RSA+SHA512:ECDSA+SHA224:RSA+SHA224
       Peer certificate: C = JP, L = Test, OU = Test, CN = 127.0.0.1, emailAddress = test@example.com
       Hash used: SHA256
       Signature type: RSA-PSS
       Verification: OK
       Server Temp Key: X25519, 253 bits
       DONE

5. Ctrl + C でサーバを終了させる。

参考
----------

- `/docs/man1.1.1/man1/openssl.html <https://www.openssl.org/docs/man1.1.1/man1/openssl.html>`_
- `/docs/man1.1.1/man1/rehash.html <https://www.openssl.org/docs/man1.1.1/man1/rehash.html>`_
- `/docs/man1.1.1/man1/s_server.html <https://www.openssl.org/docs/man1.1.1/man1/s_server.html>`_
- `/docs/man1.1.1/man1/s_client.html <https://www.openssl.org/docs/man1.1.1/man1/s_client.html>`_
