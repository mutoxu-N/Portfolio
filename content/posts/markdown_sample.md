---
title: "マークダウン備忘録"
date: 2024-10-27T16:24:27+09:00
description: "マークダウンとその見た目を確認できます。"
tags: ["Markdown"]
type: post
weight: 25
showTableOfContents: true
draft: true
---


# ようこそ！
\<\!\-\-more\-\-\> より上はサマリーとして表示されます。
デフォルトだと半角スペース区切りで70単語文が表示されますが、
日本語には半角スペースが無いので全文がサマリーとして表示されてしまいます。
\<\!\-\-more\-\-\> を使いましょう！

<!--more-->

**太字** __ふとい__

*斜体* _ななめ_

~~打ち消し~~

> 引用
>> 引用で引用
>>> で引用

- 箇条書き1
- 箇条書き2
- 箇条書き3

1. 箇条書き1
2. 箇条書き2
3. 箇条書き3

|Left|Center|Right|
|:---|:----:|----:|
|L   |C     |R    |

`hugo new site Sample`

```kotlin
fun main() {
    val a = 2
    val b = 4
    var c: Double = a + b
    c *= 2
    println(c.pow(5))
}
```

```
e^{i\pi} = -1
```



URL: 
[Hugo](https://gohugo.io/)

# H1
## H2
### H3
#### H4
##### H5
###### H6

- [ ] ボックス1
- [x] ボックス2

* * *
***
*****
- - - 
---

注釈[^1]もつけられます。
IT系の話では横文字[^yokomoji]や略称が多いのでこれは便利ですね。
ページの一番下に表示されます。

[^1]: 本文の語句や文章をとりあげてその意味を解説すること。また、その解説したもの。
[^yokomoji]: 横書きにする習慣の文字。特に、西洋の文字。

### ID付きの目次 {#sample}
```java
class MyClass() {
    public static void main(String args[]) {
        System.out.println("Hello World");
    }
}
```

[目次へリンク](#sample)

定義リスト
: 定義の内容

自動車
: 原動機の動力によって車輪を回転させ、軌条や架線を用いずに路上を走る車

---
絵文字も使えるよ😊😊😊 

でも絵文字のショートコードは使えないみたい :unamused:

---

URLは自動でリンクになります (http://www.example.com)