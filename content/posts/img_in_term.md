---
# description: ""
showTableOfContents: true
tags: ["Rust"]
title: "ターミナルで画像を表示するアプリ"
type: "post"
date: 2025-01-28
---

## 要約
SSHでサーバーを触っているときに、サクっと画像を確認したいときがある。

ターミナルで画像を表示するためのプロトコルは、
普段使いしているコマンドプロンプトでは使用できないため、[▀](https://0g0.org/unicode/2580/) を使って画像を表示した。

![画面例](/Portfolio/images/posts/img_in_term/img_in_term.png)

\
このソフトウェアは以下の機能を持っている。
- ANSIエスケープシーケンスで画像を表示する
- 画像の拡大・縮小
- 視点移動
- 透過画像の表示
- 画面サイズに応じて画像を表示

半透明の画像も表示できる。
![画面例(透過)](/Portfolio/images/posts/img_in_term/img_in_term_grad.png)


## ターミナルで画像を表示するプロトコル
「**ターミナルで画像を表示したい**」という要望はあるようで、画像を表示プロトコルが存在していることが分かっている。

{{<linkcard "https://io.cyberdefense.jp/entry/%E3%82%BF%E3%83%BC%E3%83%9F%E3%83%8A%E3%83%AB%E5%86%85%E3%81%A7%E7%94%BB%E5%83%8F%E8%A1%A8%E7%A4%BA%E3%81%99%E3%82%8B%E6%89%8B%E6%B3%95%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6%E3%81%8B%E3%82%93%E3%81%8C%E3%81%88%E3%82%8B/">}}

しかし、Windowsのコマンドプロンプトでは [Sixel](https://en.wikipedia.org/wiki/Sixel)も[Inline Images Protocol](https://iterm2.com/documentation-images.html)も使えないので、別の方法を考える必要がある。

## なぜコマンドプロンプト
[WezTerm](https://wezfurlong.org/wezterm/index.html)のようなターミナルを使用すれば、Sixelなどのプロトコルを利用できるのに、頑なにコマンドプロンプトを使い続けるのには理由がある。

単純に、**設定しなくても使いやすいから**である。

### `cmd` コマンド
Windowsエクスプローラーでは、ファイルパスが表示されている部分でコマンドを実行することができる。 
![エクスプローラーでコマンドを実行](/Portfolio/images/posts/img_in_term/cmd_in_exp.png)

この部分で `cmd` を実行すると、コマンドプロンプトで現在のフォルダを開くことができるのだ。\
**いちいち `cd` で移動する必要が無く**、即座に作業に移行できる。\
特にWindowsでは、`cd/d` を使うべき場面があるため、これを回避できるのも大きい。

Weztermで同じことをやろうと思うと、\
パスを通したり、エイリアスを設定したりする必要があるので**面倒**だ。


### フォントが良い
初期設定でこの丸っこいフォントが使われているのが良い。 \
(`Cascadia Mono`というフォントのようだ。)

![コマンドプロンプトの画面例](/Portfolio/images/posts/img_in_term/prompt.png)


また, デフォルトの配色も彩度が高くて見やすい。\
以下のShellスクリプトを実行した結果を比べてみる。
```bash
echo;
for ((i=40; i<=47; i++)) do printf '%d ' $i; done; echo;
for ((i=40; i<=47; i++)) do printf '\e[%dm  \e[m ' $i; done; echo;
echo;
```

まず、コマンドプロンプトの配色。色が濃くて見やすい。
![コマンドプロンプトの配色](/Portfolio/images/posts/img_in_term/color_scheme_prompt.png)

次に、Weztermの配色。比べると少し淡い色だ。
![Weztermの配色](/Portfolio/images/posts/img_in_term/color_scheme_wezterm.png)
特に、Weztermの白(`47`)はグレーに寄っていて、文字が読みにくい印象がある。

Weztermはホームディレクトリの `.wezterm.lua` を使って設定を行えるため、\
以下のような設定を行った。

```lua
local wezterm = require 'wezterm'
local config = {}

if wezterm.config_builder then
  config = wezterm.config_builder()
end

-- フォントの設定
config.font = wezterm.font("Cascadia Mono", {weight="Medium", stretch="Normal", style="Normal"})
config.font_size = 12

-- テーマ
config.color_scheme = 'Abernathy'

return config
```

\
この設定で配色をチェックしてみると、だいぶ見やすくなった。
![Weztermの配色(改良版)](/Portfolio/images/posts/img_in_term/color_scheme_wezterm_improved.png)


\
Weztermでは、設定ファイルをホームディレクトリに置くと設定を反映させることができるが、\
**設定しなくても見やすい**コマンドプロンプトには勝てない。

---
以上の理由でコマンドプロンプトを使いたいため、\

コマンドプロンプトでも画像が見れるようなソフトを作成した。


## 車輪の再発明
ANSIエスケープで画像を表示するために、文字で色を表す方法が存在する。\
今回は `▀` '(U+2580) を使用して画像を描画する。

文字色と背景色を設定して `▀` を描画すると、縦2ピクセルを描画することができる。\
これを用いて画像を表示していく。

・・・

ここで大きな誤算があった。

調べる限り、この方法で画像を表示している人は居らず、\
独自性があると考えていたのだが、[chafa](https://hpjansson.org/chafa/) というプログラムが存在していた。

しかも、chafa ではGIFアニメーションを再生することができる。\
(~~プログラムを書く前に知りたかった...~~)


**ただ、** 透過画像の表示や画像の拡大などの要素は chafa に実装されてなさそうなので、\
差別化はできていた。 (よかった)

## インストーラーの作成
昔から、 `make install` でインストールできるソフトウェアに憧れていたので、\
今回は `make` を用いたインストーラーを作成した。

というか、[Gemini](https://gemini.google.com/)に書いてもらった。

Geminiの出力をそのままコピペすると、\
Ubuntu上でコマンドをインストールできるようになった。(生成AIに感謝)

## プログラム
初めてRustに挑戦したので、所有権関連の実装に手間取ったが、少しずつ慣れていきたい。

{{< linkcard "https://github.com/mutoxu-N/ImgInTerm" >}}
ソースコード: [GitHub](https://github.com/mutoxu-N/ImgInTerm)


