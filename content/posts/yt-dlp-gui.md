---
# description: ""
showTableOfContents: true
tags: ["Python", "yt-dlp"]
title: "yt-dlpにGUIをつけてYouTube動画を一括ダウンロードしたい"
type: "post"
date: 2024-11-14
---

## 概要
YouTubeなどの動画プラットフォームから動画をダウンロードしたりするためのコマンドラインツールとして、
[yt-dlp](https://github.com/yt-dlp/yt-dlp)というものが存在する。

このソフトウェアは[Pythonライブラリ](https://pypi.org/project/yt-dlp/)として利用することもでき、
これとTkinterを使用して利用しやすいGUIを実装した。

ソースコード/インストール: [GitHub](https://github.com/mutoxu-N/yt-dlp-GUI)


## CLIの問題点{#problem}
### 詳しくないと使えない

CLIツールの主な問題として、使うために知識が必要であることがある。
特にターミナルを起動してコマンドを実行するのは、
不慣れな人にとって**恐怖**そのもの。

### オプションなどのコマンドを覚える必要がある
`yt-dlp`は高度なソフトウェアであり、
数多くのオプションを扱えるが、
その多くが**意味不明**でよく分からない。

### ある操作を繰り返しす際にコマンドを書くのが面倒
ある動画をダウンロードするコマンドがあっても、
複数の動画をDLしたいときには、1動画に対して1つずつコマンドを実行する必要がある。
スクリプトを書ける人なら繰り返しを使って一括処理できそうだが、
**全員がShellScriptを扱えるわけじゃない**。

## 実装した内容
[CLIの問題点](#problem)の内容を踏まえて以下のような機能を実装した。

### GUI
とにかくCLIは難しい(~~難しそうにみえる~~)ので、
TkinterでGUIを作成した。
![yt-dlpのGUI画像](/posts/imgs/yt-dlp/gui.png)

### MP3形式でDL
音楽などは、動画より音声でDLしたいという需要がある。
その中でもMP3形式は幅広く利用されているためこれに対応した。

### 一括DL
出力フォルダに`download_list.txt`を配置することで、
複数の動画から一括でダウンロードを実行することができる。
デフォルトではMP3形式でダウンロードされるので、
ダウンロードしたい音楽のURLを1行ずつ記載しておけば、
すべてが自動でDLされる。
![一括DLの設定ファイル例](/posts/imgs/yt-dlp/list.png)


### 限定動画のDL
YouTubeの動画の中には、視聴条件として

- YouTube Premiumに加入
- メンバーシップに参加

が設定されているものがある。

このような限定動画に対応するために、
ブラウザのCookie情報を読み込んでダウンロードを行う機能を実装している。

[Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
のような拡張機能を利用して `youtube.com` のCookie情報をテキストファイルに出力すれば、
ブラウザのログイン情報を使って動画をDLすることができる。
