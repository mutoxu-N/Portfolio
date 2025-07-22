---
# description: ""
showTableOfContents: true
tags: ["Linux", "Python"]
title: "お名前.com のDDNSクライアントを自作"
type: "post"
date: 2025-07-22
---

## 背景

お名前ドットコムの DDNS クライアンをは Windows のみに対応している。
{{< linkcard "https://help.onamae.com/answer/7920" >}}

自宅サーバーは Ubuntu なので、
Python で動く DDNS クライアントを作成した。

## 機能

-   お名前ドットコムで管理している DNS の A レコードを現在の IP で更新する
-   複数のホスト名に対応
-   更新不要なときは API をたたかない

## 仕組み

1. 現在の IP を取得
2. FQDN 　に対応するアドレス取得
3. IP アドレスが違っていたら API を叩いて更新

## インストール

リポジトリでは `pipenv` を使用している。\
`Pipfile` には Python3.11.9 と記載してあるが、バージョンが多少異なっていても問題は無いだろう。

使用しているパッケージは以下の 2 つなので、 \
`pipenv` を使わなくても `pip install` でインストールできる。

-   requests
-   dnspython

## 設定

### config.json

設定は `config.json` で行う。\
(リポジトリの `config.json.copy` を編集・名前変更して使用してください。)

-   `config.json` の例

```json
{
    "user_id": "01234567",
    "password": "p@s5w0rd",
    "FQDNs": [
        {
            "host": "abc",
            "domain": "example.com"
        },
        {
            "host": "def",
            "domain": "example.com"
        }
    ]
}
```

### crontab

このプログラムは実行時に 1 度だけ処理が行われる。\
従って, crontab に登録して定期実行する使い方が良いだろう。

-   設定例(一時間ごとに実行)

```
0 * * * * cd ~/OnamaeDdnsClient && pipenv run python3 update.py
```

カレントディレクトリにログが書き出されるので `cd` しておくと良い。

-   ログの例

```
[2025-07-22 13:00:01] NOT UPDATED (IP:aaa.bbb.ccc.ddd)
[2025-07-22 14:00:02] NOT UPDATED (IP:aaa.bbb.ccc.ddd)
[2025-07-22 15:00:02] NOT UPDATED (IP:aaa.bbb.ccc.ddd)
[2025-07-22 16:00:02] NOT UPDATED (IP:aaa.bbb.ccc.ddd)
[2025-07-22 17:00:01] UPDATE: abc.example.com aaa.bbb.ccc.ddd -> eee.fff.ggg.hhh
[2025-07-22 17:00:01] UPDATE: def.example.com aaa.bbb.ccc.ddd -> eee.fff.ggg.hhh
```

## ソースコード

ソースコード: [GitHub](https://github.com/suzukicloud/onamae-ddns-client)
{{< linkcard "https://github.com/mutoxu-N/OnamaeDdnsClient" >}}
