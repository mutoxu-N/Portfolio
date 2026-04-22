---
# description: ""
showTableOfContents: true
tags: ["IoT", "C++", "ESP32", "esp-matter", "Matter"]
title: "ESP32を使ったMatterデバイス開発の環境構築"
type: "post"
date: 2026-04-18
---

## はじめに

Espressif社のマイコン **ESP32** とESP用のMatterライブラリ **esp-matter** を使ってMatterデバイスを開発する際の環境構築の備忘録。

今回の開発で使うものは以下のとおりである。

### ESP32

今回は [`ESP32-C6-DevKitC-1`](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32c6/esp32-c6-devkitc-1/index.html) という開発ボードを用意する。
ESP32-C6 は Wi-Fi、Bluetooth LE、Zigbee、Thread に対応したチップであり、これらの規格を扱えるMatterデバイスの開発に適している。

### VSCode

言わずと知れたテキストエディタ (もはやIDE)
{{< linkcard "https://code.visualstudio.com/" >}}

C++で開発する際の定番プラグイン **C/C++** も導入しよう。
{{< linkcard "https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools" >}}

また、今回は ESP-IDF による開発なので、**ESP-IDF**という拡張機能も利用できる。
(今回の説明では触れないが、調べると便利な機能が利用できる)
{{< linkcard "https://marketplace.visualstudio.com/items?itemName=espressif.esp-idf-extension" >}}

### WSL

Windows上でLinuxを実行するためのもの。\
今回は `Ubuntu 24.04.3 LTS` を使い、VSCodeでWSL内のファイルを編集して開発を行う。

{{< alert "warning" >}}
ESP-IDF自体はWindowsでの開発も可能だが、esp-matterはLinuxでの開発が基本となっているので、WindowsユーザーはWSLを利用しよう。
{{< /alert>}}

### ESP-IDF

ESP32の開発を行うためのライブラリ
{{< linkcard "https://github.com/espressif/esp-idf" >}}

### esp-matter

ESP-IDF と併せて、ESP32上でMatterデバイスを開発するためのライブラリ
{{< linkcard "https://github.com/espressif/esp-matter" >}}

## 環境構築

長くなるので、WSL、VSCode、ESP-IDF(拡張機能)の導入方法は省略する。 \
以降は、ESP-IDF(拡張機能)がインストールされたVSCodeで、 \
WSL内のホームディレクトリを開いている前提で進めていく。

### ESP-IDF(ライブラリ)のインストール

#### バージョンの確認

[esp-matter](https://github.com/espressif/esp-matter)を見ると、
`ESP-IDF v5.5.1` の利用が推奨されている。 \
今回は、v5.5.1 をインストールするが、この部分は更新される可能性があるので、\
随時確認してほしい。

![ESP-IDFのバージョン](/Portfolio/images/posts/esp-idf_tutorial/esp-idf_version.png)

ここからは、公式ドキュメントが用意されているので、それを参考にする。
{{< alert "info">}}
ESP-IDF と esp-matter のドキュメントがあるので、基本は esp-matter の方を踏襲する。
{{< /alert >}}

{{< linkcard "https://docs.espressif.com/projects/esp-idf/en/v5.5.1/esp32c6/get-started/linux-macos-setup.html#" >}}
{{< linkcard "https://docs.espressif.com/projects/esp-matter/en/latest/esp32c6/developing.html#esp-idf-setup" >}}

#### 必要なパッケージのインストール

まずは、ESP-IDFで使用するパッケージをインストールする。

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git wget flex bison gperf python3 python3-pip python3-venv cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0
```

#### ESP-IDF のインストール

`~/esp/v5.5.1/esp-idf` 内にESP-IDFをダウンロードする。

```bash
mkdir -p ~/esp/v5.5.1
cd ~/esp/v5.5.1
git clone -b v5.5.1 --recursive https://github.com/espressif/esp-idf.git

```

以下を実行してインストール。

```bash
cd ~/esp/esp-idf
git submodule update --init --recursive;
./install.sh
```

#### ESP-Matter のインストール

`~/esp-matter` に esp-matter をインストールする。

まずは、 `esp-idf` を有効化する。

```bash
cd ~/esp/v5.5.1/esp-idf
source ./export.sh
```

次にesp-matterをダウンロード、インストールする。
{{< alert "info">}}
`./scripts/checkout_submodules.py --platform esp32 linux --shallow` と `./isntall.sh` の実行には時間がかかるので気長に待とう。
{{< /alert >}}

```bash
cd ~
git clone --depth 1 https://github.com/espressif/esp-matter.git
cd esp-matter
git submodule update --init --depth 1
cd ./connectedhomeip/connectedhomeip
./scripts/checkout_submodules.py --platform esp32 linux --shallow

cd ~/esp-matter
./install.sh
. ./export.sh
```

以上で、開発環境の構築は完了した。

## サンプルプロジェクトの実行

### 開発ボードをWSLに接続

購入した開発ボードをPCに接続しても、WSLからは認識されない。 \
WSL内でUSBが認識できるように設定を行う。

ここでは、 `usbipd` というツールを用いる。
{{< linkcard "https://github.com/dorssel/usbipd-win/releases" >}}

winget が使えるなら、以下のコマンドでインストールできる。

```powershell
winget install --interactive --exact dorssel.usbipd-win
```

次に、管理者権限で起動したコマンドプロンプト/PowerShell で

```powershell
usbipd list
```

を実行する。 \
USBデバイス一覧が出てくるので、開発ボードっぽいデバイスを選択する。 (今回は `1-1` )
![USBデバイス一覧](/Portfolio/images/posts/esp-idf_tutorial/usbipd_not-shared_example.png)

`STATE` が `Not Shared` になっているはずなので、これを `Shared` に変更する。 \
(ここに管理者権限が必要です。)

```powershell
usbipd bind --busid 1-1
```

次に、WSLにアタッチする。 \
開発をしているときは、常に以下のコマンドを実行し続ける必要がある。

```powershell
usbipd attach -awb 1-1
```

ここまで行うと、WSL内で

```bash
lsusb
```

を実行すると、ESP32-C6が認識されたことがわかる。

```
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 002: ID 303a:1001 Espressif USB JTAG/serial debug unit
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
```

### 開発の前の設定

次に、開発時に必要な設定を行う。

まずは、ESP-IDFとesp-matterの有効化だ。\
これらのコマンドを実行することで、環境変数が設定され、各種ツールやライブラリが使えるようになる。

```bash
cd ~/esp/v5.5.1/esp-idf; source ./export.sh
cd =/esp-matter; source ./export.sh
```

これらはターミナルを起動するたびに設定する必要がある。

### サンプルプロジェクト

esp-matter のサンプルプロジェクトは、`~/esp-matter/examples/` に用意されている。\
まずは、単純な照明のサンプルを実行する。

```bash
cd ~/esp-matter/examples/light
```

#### 実行

実行する機器の種類を設定する。

```bash
idf.py set-target esp32c6
```

ここで設定される環境変数はターミナル再起動でリセットされてしまう場合があるため、 \
実行時にエラーが出たら以下を実行して環境変数を再設定する。

```bash
export ESP_MATTER_DEVICE_PATH=$ESP_MATTER_PATH/device_hal/device/esp32c6_devkit_c
```

次に、デバイスの接続ポートを設定する。\
VSCodeの下部バーにコンセントのようなマークが存在するのでクリックすると、デバイスのポートを選択できる。
![ポート選択画面](/Portfolio/images/posts/esp-idf_tutorial/esp-idf_port-list.png)

今回は1台しか接続していないので、ひとつだけ表示されているが、 \
複数台で開発する場合は適切に設定しよう。

ここまで設定すれば、あとは実行するだけである。 \
以下のコマンドで、ビルド&書き込みをした後、シリアル通信のモニターを自動表示することができる。

```bash
idf.py build flash monitor
```

「権限がない」と言われたら、デバイス権限を変更する。

```bash
sudo chmod 666 /dev/ttyACM0
```

モニターを閉じるときは `Ctrl+[` を押す。

#### 動作確認

デバイスが動作し始めると、スマホにデバイス追加画面が表示されるので、その指示に従ってデバイスを追加する。

{{< alert "error" >}}
著者の環境では、Wi-FiがWPA3だとWi-Fi接続に失敗するので、事前にスマホ側でWPA2のアクセスポイントに接続してから、デバイス追加を実行した。
{{< /alert >}}

接続のためのQRコードが必要な場合、以下のQRコードを利用する。 \
(PINを利用する場合: `34970112332`)

{{< linkcard "https://project-chip.github.io/connectedhomeip/qrcode.html?data=MT:Y.K9042C00KA0648G00" >}}

実際に HomeAssistant に追加すると以下のような操作パネルからデバイスを操作できる。
![HomeAssistantの操作パネル](/Portfolio/images/posts/esp-idf_tutorial/ha_sample.png)

## Matterデバイス開発の手引き

動作確認をしたら、自作のMatterデバイスを作成したくなると思う。 \
ここでは、サンプルプロジェクトを例に開発に必要な知識を簡単に紹介する。

### 使用するサンプル

ここでは、 esp-matter の[lightサンプル](https://github.com/espressif/esp-matter/tree/main/examples/light)を使用する。
{{< linkcard "https://github.com/espressif/esp-matter/tree/main/examples/light" >}}

### ファイル構成

esp-matter では、`main/` 内の3つのファイルを使用する。

- [`app_main.cpp`](https://github.com/espressif/esp-matter/blob/main/examples/light/main/app_main.cpp)
- [`app_driver.cpp`](https://github.com/espressif/esp-matter/blob/main/examples/light/main/app_driver.cpp)
- [`app_priv.h`](https://github.com/espressif/esp-matter/blob/main/examples/light/main/app_priv.h)

### `app_main.cpp`

Matterノードの作成やネットワークへの接続などを行うためのメインプログラム。 \
ここで、デバイスの仕様やMatterデバイスとして必要な機能のセットアップを行う。

`app_main()` は初めに実行される関数で、ノードの構築などを行う。\
重要な部分は以下の通り。

```c++
extern "C" void app_main() {
    // Matter ノードの作成とコールバック関数の設定
    node::config_t node_config;
    node_t *node = node::create(&node_config, app_attribute_update_cb, app_identification_cb);

	  // ライトの設定管理インスタンス
    extended_color_light::config_t light_config;
    // (ライトの初期設定)

    // ライトの設定を渡し、カラー照明(extended_color_light)を作成 & nodeに登録
    endpoint_t *endpoint = extended_color_light::create(node, &light_config, ENDPOINT_FLAG_NONE, light_handle);
}
```

`app_attribute_update_cb(...)` では、Matter側で属性の変更が発生した場合に、
`app_driver.cpp` の関数を呼び出し、ハードウェア制御を行うようになっている。

```cpp
static esp_err_t app_attribute_update_cb(attribute::callback_type_t type, uint16_t endpoint_id, uint32_t cluster_id, uint32_t attribute_id, esp_matter_attr_val_t *val, void *priv_data)
{
    esp_err_t err = ESP_OK;

    if (type == PRE_UPDATE) {
        app_driver_handle_t driver_handle = (app_driver_handle_t)priv_data;

        // ここで app_driver.cpp へ渡す
        err = app_driver_attribute_update(driver_handle, endpoint_id, cluster_id, attribute_id, val);
    }
    return err;
}
```

### `app_driver.cpp`

#### 属性の分類

Matterとハードウェアの橋渡しをするプログラム。

属性の変更が行われたときに `app_main.cpp` から
`app_driver_attribute_update(...)` が実行される。 \
ここでは属性の情報を読み取り、それに合わせたハードウェア制御
(今回はLEDの制御)を行う関数を実行する。
エンドポイント、クラスタ、属性のIDをもとに処理を分岐して実装している。

```cpp
esp_err_t app_driver_attribute_update(app_driver_handle_t driver_handle, uint16_t endpoint_id, uint32_t cluster_id,
                                      uint32_t attribute_id, esp_matter_attr_val_t *val)
{
    esp_err_t err = ESP_OK;
    if (endpoint_id == light_endpoint_id) { // 1. On/Off クラスタ
        led_driver_handle_t handle = (led_driver_handle_t)driver_handle;

        if (cluster_id == OnOff::Id) {
            if (attribute_id == OnOff::Attributes::OnOff::Id) {
                err = app_driver_light_set_power(handle, val);
            }

        } else if (cluster_id == LevelControl::Id) { // 2. 明るさクラスタ
            if (attribute_id == LevelControl::Attributes::CurrentLevel::Id) {
                err = app_driver_light_set_brightness(handle, val);
            }

        } else if (cluster_id == ColorControl::Id) { // 3. 色クラスタ
            // 色の指定方法によって分岐
            if (attribute_id == ColorControl::Attributes::CurrentHue::Id) {
                // 色相
                err = app_driver_light_set_hue(handle, val);

            } else if (attribute_id == ColorControl::Attributes::CurrentSaturation::Id) {
                // 彩度
                err = app_driver_light_set_saturation(handle, val);

            } else if (attribute_id == ColorControl::Attributes::ColorTemperatureMireds::Id) {
                // 色温度
                err = app_driver_light_set_temperature(handle, val);

            } else if (attribute_id == ColorControl::Attributes::CurrentX::Id) {
                // X座標？
                current_x = val->val.u16;
                err = app_driver_light_set_xy(handle, current_x, current_y);

            } else if (attribute_id == ColorControl::Attributes::CurrentY::Id) {
                // Y座標？
                current_y = val->val.u16;
                err = app_driver_light_set_xy(handle, current_x, current_y);
            }
        }
    }
    return err;
}
```

`app_driver_light_set_〇〇(...)` では、
受け取った属性値をLEDなどの物理側(int, boolなど) に変換する。
例えば、明るさの設定を行うときは、

```cpp
err = app_driver_light_set_brightness(handle, val);
```

が実行されるが、

```cpp
static esp_err_t app_driver_light_set_brightness(led_driver_handle_t handle, esp_matter_attr_val_t *val)
{
		// 0~254 を 0~100 に再マップ
    int value = REMAP_TO_RANGE(val->val.u8, MATTER_BRIGHTNESS, STANDARD_BRIGHTNESS);
    return led_driver_set_brightness(handle, value); // ESP-Matter で提供されている関数
}
```

というように、LED用に値を変換している。

#### LEDの制御

またこのファイルでは、物理ボタン押下時のコールバック関数
`app_driver_button_toggle_cb(...)` も定義されている。

```cpp
static void app_driver_button_toggle_cb(void *arg, void *data)
{
    ESP_LOGI(TAG, "Toggle button pressed");
    uint16_t endpoint_id = light_endpoint_id;
    uint32_t cluster_id = OnOff::Id;
    uint32_t attribute_id = OnOff::Attributes::OnOff::Id;

    // 属性の取得
    attribute_t *attribute = attribute::get(endpoint_id, cluster_id, attribute_id);

    esp_matter_attr_val_t val = esp_matter_invalid(NULL);
    attribute::get_val(attribute, &val); // 現在の属性値を取得
    val.val.b = !val.val.b; // 属性値を反転(トグル)させる、 `.b` を付けることでboolで取得
    attribute::update(endpoint_id, cluster_id, attribute_id, &val); // 属性値を反映
}
```

物理ボタンを押すとライトのON/OFFを切り替えることができる機能が実装されている。 \
ここではLEDの状態を変えるのではなく、**属性の変更** を行うことが特徴である。

1. 物理ボタン押下
2. エンドポイント `light_endpoint_id` のクラスタ `OnOff::Id` の属性 `OnOff::Attributes::OnOff::Id` の属性を取得
3. 属性値を反転させる
4. 属性情報を更新する
5. LEDに反映される

上記のように、
前に作成した **「属性が変わったらLEDの状態を変更する」** \
という仕組みを介してLEDを操作する。

これにより、

- 物理ボタン押下でOn/Offの操作が行われた
- スマホなどからMatterデバイスのOn/Offを切り替えた

  のどちらの場合でも、

1. 属性が変更
2. 属性に合わせたLED状態を反映

という実装になり、状態を正しく扱うことができる。

{{< alert "info" >}}
ユーザーが操作した結果をハードウェアに直接伝えずに、 \
一度**属性**を挟むようにしよう！
{{< /alert >}}

#### デバイスを使う準備

`app_driver.cpp` はハードウェア制御を担うファイルであるため、
デバイスを扱うための準備を行う。

例えば、 `app_driver_light_init` では、LED制御を行うためのハンドルを作成し、
`app_main.cpp` に返す。

```cpp
app_driver_handle_t app_driver_light_init() {
    /* initialize led */
    led_driver_config_t config = led_driver_get_config(); // 情報取得
    led_driver_handle_t handle = led_driver_init(&config); // 初期化
    return (app_driver_handle_t)handle; // LED を操作するためのハンドルを app_main.cpp に返す
}
```

他にも、物理ボタンを扱う準備も行う。\
`app_driver_button_init()` では、ボタンのGPIOピンの登録や押下時のコールバック関数の登録を行う。

```cpp
app_driver_handle_t app_driver_button_init() {
    /* Initialize button */
    button_handle_t handle = NULL;
    const button_config_t btn_cfg = {0};
    const button_gpio_config_t btn_gpio_cfg = button_driver_get_config();

    if (iot_button_new_gpio_device(&btn_cfg, &btn_gpio_cfg, &handle) !=
        ESP_OK) {
        ESP_LOGE(TAG, "Failed to create button device");
        return NULL;
    }

		// ボタン押下で app_driver_button_toggle_cb を実行
    iot_button_register_cb(handle, BUTTON_PRESS_DOWN, NULL,
                           app_driver_button_toggle_cb, NULL);
    return (app_driver_handle_t)handle;
}
```

`app_main.cpp` では以下のように呼び出され、\
Matter側でハードウェアを制御するためのハンドルとして用いられている。

```cpp
extern "C" void app_main()
{
		//...
    app_driver_handle_t light_handle = app_driver_light_init();
    app_driver_handle_t button_handle = app_driver_button_init();
    app_reset_button_register(button_handle); // 長押しでリセットを登録
		//...
}
```

### `app_priv.h`

属性の初期値など、 `app_main.cpp` と `app_driver.cpp` で共通して使用する変数などを設定するヘッダファイル。

```cpp
/** Standard max values (used for remapping attributes) */
#define STANDARD_BRIGHTNESS 100
#define STANDARD_HUE 360
#define STANDARD_SATURATION 100
#define STANDARD_TEMPERATURE_FACTOR 1000000

/** Matter max values (used for remapping attributes) */
#define MATTER_BRIGHTNESS 254
#define MATTER_HUE 254
#define MATTER_SATURATION 254
#define MATTER_TEMPERATURE_FACTOR 1000000
```

例えば、`app_driver_light_set_brightness(...)`では\
Matterで使う値の範囲とLED制御で使う値の範囲が異なるので、\
`REMAP_TO_RANGE(val->val.u8, MATTER_BRIGHTNESS, STANDARD_BRIGHTNESS)` で値を変更していた。

また `app_priv.h` では、
`app_driver.cpp` で実装する関数のプロトタイプ宣言も定義されている。

```cpp

app_driver_handle_t app_driver_light_init();
app_driver_handle_t app_driver_button_init();
esp_err_t app_driver_attribute_update(app_driver_handle_t driver_handle, uint16_t endpoint_id, uint32_t cluster_id, uint32_t attribute_id, esp_matter_attr_val_t *val);
esp_err_t app_driver_light_set_defaults(uint16_t endpoint_id);
```

さらに、Threadを使う場合の設定なども行える。

```cpp
#if CHIP_DEVICE_CONFIG_ENABLE_THREAD
#define ESP_OPENTHREAD_DEFAULT_RADIO_CONFIG()                                           \
    {                                                                                   \
        .radio_mode = RADIO_MODE_NATIVE,                                                \
    }

#define ESP_OPENTHREAD_DEFAULT_HOST_CONFIG()                                            \
    {                                                                                   \
        .host_connection_mode = HOST_CONNECTION_MODE_NONE,                              \
    }

#define ESP_OPENTHREAD_DEFAULT_PORT_CONFIG()                                            \
    {                                                                                   \
        .storage_partition_name = "nvs", .netif_queue_size = 10, .task_queue_size = 10, \
    }
#endif
```

## 豆知識

### menuconfig

`idf.py menuconfig` を実行するとプロジェクト設定を行うことができる。 \
(画面が表示されるまで時間がかかることがある。)

![menuconfigのトップ画面](/Portfolio/images/posts/esp-idf_tutorial/menuconfig.png)

この画面は Vim のような操作感で扱える。\
`/` で検索を行うことができるため、何か設定するときには検索するのが良い。

例えばログレベルを設定したい場合には`/LOG_LEVEL` で検索すれば良い。
![ログレベルの設定](/Portfolio/images/posts/esp-idf_tutorial/log_level.png)

### ターミナルの開始時の設定

VSCode を再起動するなど、開発時にターミナルを再起動したときには、 \
以下のコマンドで環境変数を再設定すると良い。

```bash
cd ~/esp/v5.5.1/esp-idf; source ./export.sh; cd ../../..
cd ~/esp-matter; source ./export.sh; cd ..
export ESP_MATTER_DEVICE_PATH=$ESP_MATTER_PATH/device_hal/device/esp32c6_devkit_c
```
