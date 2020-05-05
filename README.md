# yoiotemae
よいお点前
「・・・　IoT ・・・」の略称（略称は検討中）

複数のセンサーを接続したRasberryPiを対象としたIoT-PFのテンプレート

## 想定環境
複数のRasberryPiがあり、それぞれのRasberryPiには複数のセンサ（温度、湿度、照度　等）がついている。
ただし、個々のRasberryPiに接続されているセンサーは異なることがある。
（温度センサのみが接続されているRasberryPiもあれば、温度、湿度、照度の3つのセンサがついているRasberryPiもある）

## 実施したいこと
RasberryPiのセンサから取得できる情報をサーバに送信したい

## このyoiotemaeで実施したいこと
- 設定ファイルを編集することで、どのセンサが接続されているか管理できる
- 設定ファイルを編集することで、センサから情報を取得する際のパラメータを管理できる
- 設定ファイルにサーバ送信に関するパラメータを管理できる
- センサの種類は今後も増えていくので、独立したモジュールとして構築したい

## 現段階の実現方式
- 設定ファイルをconfig/para.configに設置
- lib配下に各センサに対応するpyファイルを作成し、共通メソッドとして、インスタンス生成時に
パラメータ（複数の可能性あり）を受け取り、getメソッドによりセンサからの情報（服須の可能性あり）を取得できる仕様とする
- メインとなるmain.pyは、設定ファイルに基づき、必要なモジュールを動的に読み込み、センサからの情報を取得し、
設定ファイルに基づいいてサーバに送信するjsonを生成する

## 改善希望点
センサー種類が増えていっても（lib配下にモジュールが増えても）main.pyを編集しなくてもよいようにしたい。
現状では、センサーの種類が増えるたびに、次のようなif分を追加する必要がある。

```python
    if cfg.has_section('sensor1'):
        try:
            module = importlib.import_module('lib.sensor1')
            sensor1 = module.Sensor1(cfg.getint("sensor1", "bus_number"))
            ret = sensor1.get()

            data[cfg['sensor1']['name1']] = ret[0]
            data[cfg['sensor1']['name2']] = ret[1]
            data[cfg['sensor1']['name3']] = ret[2]
        except Exception as e:
            print(e)
```
