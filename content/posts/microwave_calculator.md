---
# description: ""
showTableOfContents: true
tags: ["Android", "Android Studio","Kotlin"]
title: "電子レンジ温め時間計算アプリ"
type: "post"
date: 2023-04-06
---

![アプリアイコン](/Portfolio/images/posts/microwave_calculator/icon.webp)

## 要約
Androidアプリに興味があり、一番はじめに作ったアプリ。 \
Google Playストアへのリリースを行った。

{{< linkcard "https://play.google.com/store/apps/details?id=com.github.mutoxu_n.MicrowaveCalculator" >}}


## 機能
- 異なるワット数の温め時間を計算する
- 自分の使っているレンジに合わせてワット数を登録できる

![アプリ画面例](/Portfolio/images/posts/microwave_calculator/screen.webp)

## 動機
自宅の電子レンジのワット数が730Wのものであり、
長時間の温めが必要な冷凍食品の温め時間が分からないことがあった。
( 短時間だったら適当に調整できるが500W15分とかだと, 
730Wで10分くらい...？」と不安になる )
![自宅のレンジ](/Portfolio/images/posts/microwave_calculator/730w.webp)

そこで、自分の使っているワット数をいくつか登録できるような**温め時間計算アプリ**が欲しかった。

下の入力ボックスにワット数を入力し、ワット数ボタンを長押しすると、ボタンに入力されているワット数が登録される。
900Wや1500Wの電子レンジを持っている人も、自分のレンジに合わせてワット数を登録することができる。

## 発表
株式会社サポーターズ主催 ライトニングトーク大会で発表しました。(2023/4/27)
{{< linkcard "https://talent.supporterz.jp/events/65ad84d5-9f88-4149-b752-f37f1682c08d/" >}}

## ソースコード
{{< linkcard "https://github.com/mutoxu-N/MicrowaveCalculator" >}}
ソースコード: [GitHub](https://github.com/mutoxu-N/MicrowaveCalculator)