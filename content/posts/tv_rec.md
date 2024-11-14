---
# description: ""
showTableOfContents: true
tags: ["Docker","MySQL"]
title: "TV録画サーバーを作った話"
type: "post"
date: 2024-11-14
---

## 概要
TVを録画するためのサーバーを作成したときの手順と、
暗号化が解除されず、解決に1週間以上かかった話。
<!--more-->


## サーバー機のスペック
- OS: Ubuntu Server 24.04.1 LTS
- CPU: Intel N100
- チューナー: PX-MLT5PE

### チューナーのドライバ
今回使用したチューナーは、Linux用のドライバは用意されていない。
有志で非公式ドライバを公開してくださっているのでこれを利用した。
{{< linkcard "https://github.com/nns779/px4_drv" >}}


## TV録画
### 必要なソフト
TV録画には以下のソフトウェアが必要である。
- Mirakurun: チューナーの電波を解析する。(B-CASカードが有効なら暗号化を解除する。)
- EPGStation: 録画設定を管理し、録画データを動画ファイルとして保存・エンコードする。
- MySQL: 録画設定を管理するデータベース。

これらのソフトは、すべてDocker上で構築することができる。
{{< linkcard "https://github.com/l3tnun/docker-mirakurun-epgstation" >}}


### スクランブル解除ができない
手順通りにDockerコンテナを立ち上げても、テレビの暗号化が解除されなかった。
ホストマシンで `pcsc_scan` を行うと、ICカードリーダーとB-CASカードが認識されており、
`docker-compose.yml` でコンテナ内でも使えるようになっていた。

しかし、コンテナ内で `pcsc_scan` を実行してもICカードリーダーが認識されておらず、
暗号化解除が行われていなかった。
よく見ると、`pcsc_scan`のバージョンがホストマシンのものと異なっていた。
ホストマシンとコンテナ内で互換性の無いカードリーダードライバを使っていたために、不具合が生じていたようだ。

以上より、単純に `pcscd` の新しいものをインストールすれば良いと考えていたが、
問題のあるMirakurunは [`chinachu/mirakurun`](https://hub.docker.com/r/chinachu/mirakurun) という
`Debian`ベースのDockerイメージを使用しており、
ホストマシン(Ubuntu)と同じバージョンはインストールすることができなかった。
(アップデートが行われていなかった。)

そこで、Mirakurunを起動できる他のDockerイメージを探したところ、
`Alpine`ベースの
[`collelog/mirakurun`](https://hub.docker.com/r/collelog/mirakurun) を見つけることができた。
このDockerイメージを使用すると、暗号化を解除することができた。

