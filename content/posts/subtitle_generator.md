---
# description: ""
showTableOfContents: true
tags: ["Python","Faster-Whisper","Whisper"]
title: "PythonとWhisperで音声や動画からSRTファイルを生成する"
type: "post"
date: 2024-07-22
---

## 要約
音声文字起こし用の深層学習モデル[Whisper](https://github.com/openai/whisper)の高速版である
[Faster-Whisper](https://github.com/SYSTRAN/faster-whisper)を使った、
**字幕ファイル生成プログラム**(SRT)。

実行時に出てくるダイアログで音声ファイルを選択すると、
それに応じた字幕ファイルが生成される。
SRTファイルは動画編集ソフトなどに直接読み込むことができるため、
動画字幕を自動生成したいときに利用できる。

## 注意点
Faster-Whisperのモデルを使用しているため、
文字起こし精度はモデルに依存します。
僕の環境だと、`large-v3` のモデルを使用しても誤字が多く、
字幕表示/非表示のタイミングも大きくズレているため、手動での調整が必須となっています。


## プログラム
{{< linkcard "https://github.com/mutoxu-N/SubtitleGenerator" >}}
ソースコード: [GitHub](https://github.com/mutoxu-N/SubtitleGenerator)