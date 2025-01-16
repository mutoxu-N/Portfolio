---
# description: ""
showTableOfContents: true
tags: ["Docker", "Let's Encrypt","nginx","oauth"]
title: "自鯖に外部からHTTPSアクセスするためのリバースプロキシ"
type: "post"
date: 2024-04-04
---

## 要約
[TV録画サーバー](/Portfolio/posts/tv_rec/)を外部からアクセスできるようにしたかった。


しかし、TV放送には著作権があるので、安易にWeb上に公開することはできない。
これに対処するために必要な処置は以下の２つである。(ポート開放はできる前提)
- HTTPSによる暗号化
- ログイン認証によるアクセス制限

## nginxの設定
HTTPS化やログイン認証にはサーバーが必要なので、
最低限のnginxサーバーを構築する。
この段階ではリバースプロキシの機能は持っておらず、
証明書発行やログインページの表示などに使用する。

このnginxはDockerを用いて起動することができる。


## HTTPSによる暗号化
HTTPSの証明書は[Let's Encrypt](https://letsencrypt.org/ja/)を使って発行した。
便利なことに、これもDockerイメージがあるので `certbot/certbot` を使って証明書の発行と自動更新を行っている。

## ログイン認証
### OAuth2
限られたユーザーのみがTV録画を閲覧できるように、Googleアカウントによる認証を追加した。
これには、[OAuth2 Proxy](https://oauth2-proxy.github.io/oauth2-proxy/)を使用した。
OAuth2 ProxyもDocker上で動作するため、`quay.io/oauth2-proxy/oauth2-proxy` を使用して実行した。

OAuth2とGoogleの連携は多くの人が解説している通りに行った。

### ホワイトリスト
残念ながら、OAuth2を設定しただけでは、
どんなGoogleアカウントを使用してもアクセスできてしまうため、登録されたメールアドレスだけを許容するように設定する。

以下のような `allowmails` というファイルを作成し, 
OAuth2のオプションに `--authenticated-emails-file="allowmails"` を追加することで、
そのメールアドレスのGoogleアカウントでログインしたときのみ閲覧することができる設定になる。
```
taro@example.com
jiro@example.com
saburo@example.com
```

## リバースプロキシ
nginxにリバースプロキシ機能を追加する。
これに関してはネット上に情報が溢れているので各自調べてほしいが、
TV録画サーバーにプロキシする際に `auth_request /oauth2/auth;` を忘れると一般公開されるので注意しよう。

このリバースプロキシは汎用的なものなので、TV録画サーバー以外でAPIを公開したいときなどにも使用することができる。
