---
# description: ""
showTableOfContents: true
tags: ["C++","Windows"]
title: "ディスプレイ設定変更.exe"
type: "post"
date: 2024-11-14
---
## 概要
デュアルディスプレイの設定変更を一発で行うことのできる実行可能ファイル。
`Windows+P`で設定を変えることができるが、
アニメーションに時間がかかったり、どの設定を使用するかを選択する手間があるため、
**一発で**特定の設定に移動できるようにしたかった。
![ショートカットキーで設定する例](/images/posts/display_config/win_p.gif)


また、exeファイルにしておくと、
[Elgato Stream Deck](https://www.elgato.com/jp/ja/p/stream-deck-mk2-black)に登録することができ、
物理ボタン押下でディスプレイの設定を自由に変更することができるようになる。

![Stream Deckの設定例](/images/posts/display_config/deck.png)

{{< linkcard "https://github.com/mutoxu-N/DisplayConfigChanger" >}}
ソースコード: [GitHub](https://github.com/mutoxu-N/DisplayConfigChanger)

## 動機
2枚のモニターには、それぞれ2つの映像入力を行っている。
片方の映像入力はメインPCのものである。

この前提で、以下のような使い分けをこまめに切り替えたいので、
今回のソフトウェアを開発した。

### PC画面のみ１
動画を見たり、簡単な調べ物をしたり、ゲームをしたり、
シングルディスプレイで事足りるときは、
メインモニターのみを使用。
- メイン: メインPC
- サブ: OFF

### PC画面のみ２
サブPCをいじりながらメインPCで作業するときには、
左右でPCを分けて使用する。
(最近はSSHで済ませてしまうのであまり使わない)
- メイン: メインPC
- サブ: サブPC


### 拡張
プログラミングや動画編集など2画面が必要なときにデュアルディスプレイで使用。
- メイン: メインPC
- サブ: メインPC

### セカンドスクリーンのみ
サブPCで作業をするときや、Switchなどのゲーム機で遊ぶときなどは、
サブモニターでメインPCの画面を映す。
- メイン: ゲーム機やサブPC
- サブ: メインPC


## プログラム
プログラム自体は単純で、
Windowsの[SetDisplayConfig関数](https://learn.microsoft.com/ja-jp/windows/win32/api/winuser/nf-winuser-setdisplayconfig)を呼び出すだけだった。


```c++
#include <windows.h>
#include <winuser.h>

int main() {
    SetDisplayConfig(0,NULL,0,NULL,SDC_TOPOLOGY_INTERNAL|SDC_APPLY);
    return 0;
}
```
