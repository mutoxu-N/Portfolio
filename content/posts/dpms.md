---
# description: ""
showTableOfContents: true
tags: ["OS","DPMS", "Windows", "C++"]
title: "モニター電源をコントロールするDPMSをC++から使ってみた"
type: "post"
date: 2025-01-16
---

## 要約
コンピュータが操作されていないときなどに、モニターを省電力モードに移動したりするための技術として **DPMS**(Display Power Management Signaling) というものがある。

Linuxなら `xset` コマンドで設定を変更することができるが、今回はWindows APIを使ってDPMSによる画面オフを行ってみた。

{{< linkcard "https://wiki.archlinux.jp/index.php/Display_Power_Management_Signaling">}}


## プログラム
実際のプログラムは以下のとおり. 

```c++
#include <windows.h>

int main() {
    HWND w = GetConsoleWindow();
    if (w == NULL) {
        return 1;
    }

    // DPMS off
    SendMessage(w, WM_SYSCOMMAND, SC_MONITORPOWER, (LPARAM)2);

    return 0;
}
```

これを実行すると、PCからの映像出力が停止された。キーボードやマウスのライティングもオフになったが、マウスやキーボードを触ることで復帰できた。

DPMSによってモニターやライティングをオフにしても、音声出力は途切れなかったため、音楽だけを聞きたいときは、これを使って省電力化することができそう。