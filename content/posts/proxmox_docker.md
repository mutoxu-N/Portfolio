---
# description: ""
showTableOfContents: true
tags: ["Server", "Docker", "Proxmox", "Self Hosting"]
title: "ProxmoxでDockerホストを準備する備忘録"
type: "post"
date: 2025-08-07
---

## やりたいこと

Proxmox で Docker を使いたい。\
公式ドキュメントでは、Docker 用の VM を作成することが推奨されている。
{{< linkcard "https://pve.proxmox.com/pve-docs/pve-admin-guide.html#chapter_pct" >}}

しかし、単一目的の VM を多数起動するのはリソースを食うので、 \
**出来るだけ軽量なもの** を選択し、設定する方法を備忘録として残したい。

## VM の作成

今回は Docker のホストをするだけの VM を作成するため、\
軽量な Linux ディストリビューションの [DietPi](https://www.dietpi.com/) を使用する。

DietPi の公式サイトには Proxmox 用のファイルが用意されている。
![DietPiの公式サイト](/Portfolio/images/posts/proxmox_docker/dietpi_proxmox.png)

Proxmox へのインストール方法はドキュメントに記載されている。
{{< linkcard "https://dietpi.com/docs/install/#how-to-install-dietpi-proxmox" >}}

VM の起動後はコンソールの指示に従って、セットアップを行う。

## DietPi のセットアップ

インストールを完了するために、root ログインを行う。 \
DietPi では、`dietpi` が初期設定のパスワードになっているので \
これでログインし、ダイアログに従ってパスワードの変更を行う。

画面を進めると **DietPi-Software** という画面が出るので、 \
`Search Software` から `docker` と `tailscale` 検索して選択する。 \
(必要なら `git` も選択する。)

![DietPi Software](/Portfolio/images/posts/proxmox_docker/dietpi_software.png)

![DietPi Software でDockerを選択](/Portfolio/images/posts/proxmox_docker/dietpi_software_docker.png)

最後に `Install` を選択すると、\
DietPi と共に Docker と Tailscale がインストールされる。

Tailscale へのログインは以下のコマンドから行う。

```bash
tailscale login
```

## ホストネームの設定

Tailscale のために、ホストネームを `DietPi` から変更する。 \
DietPi の設定は以下のコマンドから設定することができる。

```bash
dietpi-config
```

`dietpi-config` の `Security` → `Hostname` からホストネームを変更する。

## ネットワークの設定

VM に静的 IP アドレスを割り当てる設定を行う。

`dietpi-config` の `Network Options: Adapters ` → `Ethernet` を選択する。\
その後、出てきた設定画面でモードを `STATIC` に変更し、設定を行う。

ここで `Copy` を選択すると現在の設定が入力されるので、\
その後、`Static IP` を任意の IP に変更するのがオススメ。
![ネットワークの設定](/Portfolio/images/posts/proxmox_docker/network.png)

## 時刻の設定

日本時間を設定する。\
`dietpi-config` から `Language/Regional Options` を選択する。

![タイムゾーンの設定](/Portfolio/images/posts/proxmox_docker/timezone.png)

## Vim

Docker Compose のファイルを編集するために Vim を使いたい。\
DietPi では `apt` が使えるため、以下のコマンドでインストールする。

```bash
apt install vim-tiny # 軽量版
# apt install vim
```

## 新規ユーザーの作成

私のサーバー環境では `root` ユーザーを使用せずに別のユーザーを使用する。\
ここでは `user` というユーザーを作成する。

```bash
adduser user
```

次に、`user` が管理者コマンドや `docker` コマンドを実行できるようにする。

```bash
gpasswd -a user sudo
gpasswd -a user docker
```

以上で、Docker 用に DietPi の VM をセットアップすることができた。
