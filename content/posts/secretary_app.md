---
# description: ""
showTableOfContents: true
tags: ["Android","Android Studio","Jetpack Compose"]
title: "予定テンプレート作成アプリ「Secretary」"
type: "post"
date: 2024-05-23
---

## 概要
Jetpack Composeを使った画面構築を試してみようと作成した
**予定テンプレート作成アプリ**。
一連の予定をテンプレートとして保存し、
カレンダーに追加することができる。

## 主な機能
- 予定のテンプレートを作成する
- テンプレートをカレンダーに追加する

## 具体的な設定方法
以下のような設定を行う。
1. [00:00] 外出の準備
1. [00:10] 塾へ送る
1. [02:00] 部屋を掃除する
1. [04:00] 迎えに行く

![アプリ画面](/Portfolio/images/posts/secretary/screen.webp)


この予定を、ある時間を起点として予定を作成し、
スマホのカレンダーに登録することができる。

### 設定例1: `12:00` に設定した場合
1. [12:00] 外出の準備
2. [12:10] 塾へ送る
3. [14:00] 部屋を掃除する
4. [16:00] 迎えに行く

![設定例1](/Portfolio/images/posts/secretary/register_example1.webp)


### 設定例2: `18:00` に設定した場合
1. [18:00] 外出の準備
1. [18:10] 塾へ送る
1. [20:00] 部屋を掃除する
1. [22:00] 迎えに行く

![設定例2](/Portfolio/images/posts/secretary/register_example2.webp)

## プログラム
{{< linkcard "https://github.com/mutoxu-N/Secretary" >}}
ソースコード: [GitHub](https://github.com/mutoxu-N/Secretary)
