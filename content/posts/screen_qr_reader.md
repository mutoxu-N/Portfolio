---
# description: ""
showTableOfContents: true
tags: ["Rust", "Dioxus", "QRコード"]
title: "画面上のQRコードを読み取るアプリ「ScreenQRReader」"
type: "post"
date: 2026-06-04
---

## 概要

画面上のQRコードを読むためデスクトップアプリ。

![アプリアイコン](/Portfolio/images/posts/screen_qr_reader/icon.png)

## 主な機能

- **ホットキー起動:** `Ctrl+Shift+Q` を押すだけで、いつでもキャプチャを開始できます。
- **直感的な範囲選択:** マウスをドラッグして、QRコードが含まれる領域を選択できます。
- **QR読み取り:**
  - 読み取った内容がURLの場合、自動的にデフォルトのブラウザで開きます。
  - テキストデータの場合、クリップボードにコピーします。
- **タスクトレイ常駐:** アプリはバックグラウンドで動作します。タスクトレイからアプリを閉じることができます。

## 動機

- Dioxusを触ってみたかった
- 就活中のオンラインイベントで画面上のQRを読み取る機会が多く、PCで簡単に読み取りたかった

## 技術

RustのDioxusというUIフレームワークを使用しています。
{{< linkcard "https://dioxuslabs.com/" >}}

RustではTauriというフレームワークが人気ですが、
どうしてもWeb技術を触る必要があります。
一方で、DioxusはRustだけで完結しています。\
ずっと興味を持っていたので、採用してみました。

QR処理は[rqrr](https://docs.rs/rqrr/latest/rqrr/)というクレートを使っています。

## プログラム

{{< linkcard "https://github.com/mutoxu-N/ScreenQRReader" >}}
ソースコード: [GitHub](https://github.com/mutoxu-N/ScreenQRReader)
