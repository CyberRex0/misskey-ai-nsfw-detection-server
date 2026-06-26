# Misskey AI NSFW Detection Server
このソフトウェアは、Misskeyにおいてセンシティブなメディアの検出処理を外部に分離するにあたりサンプル実装を行ったものです。

デフォルトでは、検出モデルに [Falconsai/nsfw_image_detection_26](https://huggingface.co/Falconsai/nsfw_image_detection_26) を利用します。

config.pyの`MODEL_NAME`を編集することで別なモデルに変更可能です。<br>
Gated Modelの場合は`HUGGINGFACE_TOKEN`を設定することでプログラムからアクセス可能です。

------

**2026/06/26 Update**

- [misskey-dev/sensitive-detector](https://github.com/misskey-dev/sensitive-detector) が公開されましたので、API仕様を変更しました。

- GPUを使用する方法を追記しました。

## API仕様
###  /v1/detect-images
#### Parameters

|Param|Type|Description|
|-----|-----|-----|
|image○○|File|評価に使用する画像データ|

※〇〇には数字が入ります。1ファイルごとに+1してください。

#### Responses

```json
{
  "success": true,
  "result": {
    "results": [
      {
        "success": true,
        "predictions": [
          {
            "className": "Neutral",
            "probability": 0.0
          },
          {
            "className": "Sexy",
            "probability": 1.0
          },
          {
            "className": "Hentai",
            "probability": 1.0
          }
        ]
      }
    ]
  }
}
```

(root)

|Key|Type|Description|
|-----|-----|-----|
|success|boolean|処理が成功したかどうか|
|result|object|処理結果|


result

|Key|Type|Description|
|-----|-----|-----|
|results|Array of object|各画像の判定結果|


results

|Key|Type|Description|
|-----|-----|-----|
|success|boolean|画像の判定ができたか|
|predictions|Array of object|判定情報|


predictions

|Key|Type|Description|
|-----|-----|-----|
|className|string|分類名|
|probability|float|分類の度合い|


> [!NOTE]
> APIレスポンスの構造は今後のMisskeyの開発に合わせるため変化します。
> 
> nsfwjsとは異なる判定方法のため、APIの互換性を取るためにprobabilityの値は0.0か1.0固定としています。

## サーバーのセットアップ方法
サーバーはPythonとFastAPIで作成しています。

次世代パッケージマネージャーのuvを使って簡単にセットアップできます。<br>
事前に [uv](https://github.com/astral-sh/uv) のインストールが必要です。

```shell
uv sync # 依存パッケージのインストール
uv run uvicorn main:app --port PORT # サーバー起動
```

※`--port`を指定しなかった場合、デフォルトでは 8000 を使用します。

> [!IMPORTANT]
> GPUを使用する場合は、pyproject.toml の末尾に以下を追記してください。
> ```toml
> [[tool.uv.index]]
> name = "pytorch"
> url = "https://download.pytorch.org/whl/cu126"
> ```
> 
> 追記後、`uv sync -U` を実行してください。

## APIのテスト方法

curl を使ってファイルを送信することが出来ます。

```shell
curl -X POST -F "image0=@sample1.jpg" http://hostname:8000/api/eval-image
```

例のように `-F "imageX=@ファイル名"` と指定すると、multipart/form-data形式でPOSTリクエストが発行されます。

ファイル名先頭の`@`はcurlでローカルファイルを指す記号であるため、必ずつけてください。

## 免責事項
結果の正確性を保証するものではありません。

MIT License<br>
&copy; 2026 CyberRex
