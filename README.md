まずdockerコンテナを立ち上げる

`docker compose up -d --build`

次のコマンドでコンテナへ接続（コンテナの中の環境に入ってその環境下でコマンドを打てるように）します。python3というのはdocker-compose.ymlで指定したコンテナの名前です。

`docker-compose exec python3 bash`

これで次からターミナルで打つコマンドはコンテナ内の環境下で実行されるようになります。

