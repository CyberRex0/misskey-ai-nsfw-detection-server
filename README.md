# Misskey AI NSFW Detection Server
このソフトウェアは、Misskeyにおいてセンシティブなメディアの検出処理を外部に分離するにあたり
サンプル実装を行ったものです。

デフォルトでは、検出モデルに [Falconsai/nsfw_image_detection](https://huggingface.co/Falconsai/nsfw_image_detection) を利用します。

config.pyの`MODEL_NAME`を編集することで別なモデルに変更可能です。

## API仕様
###  /api/eval-image
#### Parameters

|Param|Type|Description|
|-----|-----|-----|
|file|File|評価に使用する画像データ|

#### Responses

```json
{
    "is_nsfw": true
}
```

|Key|Type|Description|
|-----|-----|-----|
|is_nsfw|Boolean|画像がNSFWであるか|

注: APIレスポンスの構造は今後のMisskeyの開発に合わせるため変化します。

## サーバーのセットアップ方法
サーバーはPythonとFastAPIで作成しています。

次世代パッケージマネージャーのuvを使って簡単にセットアップできます。<br>
事前に [uv](https://github.com/astral-sh/uv) のインストールが必要です。

```shell
uv sync # 依存パッケージのインストール
uv run uvicorn main:app --port PORT # サーバー起動
```

※`--port`を指定しなかった場合、デフォルトでは 8000 を使用します。

※PyTorchをGPUで動作させる方法については準備中

## APIのテスト方法

curl を使ってファイルを送信することが出来ます。

```shell
curl -X POST -F "file=@sample1.jpg" http://hostname:8000/api/eval-image
```

例のように `-F "file=@ファイル名"` と指定すると、multipart/form-data形式でPOSTリクエストが発行されます。ファイル名先頭の`@`はcurlでローカルファイルを指す記号であるため、必ずつけてください。

## 免責事項
結果の正確性を保証するものではありません。

MIT License<br>
&copy; 2025 CyberRex