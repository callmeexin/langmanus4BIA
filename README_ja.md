# 🦜🤖 BiaGhosterCoder

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![WeChat](https://img.shields.io/badge/WeChat-BIA-Ghostcoder-brightgreen?logo=wechat&logoColor=white)](./assets/wechat_community.jpg)
[![Discord Follow](https://dcbadge.vercel.app/api/server/m3MszDcn?style=flat)](https://discord.gg/m3MszDcn)

[English](./README.md) | [简体中文](./README_zh.md) | [日本語](./README_ja.md)

> オープンソースから来て、オープンソースに戻る

BIA-Ghostcoderは、オープンソースコミュニティの素晴らしい仕事に基づいて構築された、コミュニティ主導のAI自動化フレームワークです。私たちの目標は、言語モデルをウェブ検索、クロール、Pythonコードの実行などの専門ツールと組み合わせることです。

## デモビデオ

> **タスク**: HuggingFace上のDeepSeek R1の影響指数を計算します。この指数は、フォロワー、ダウンロード、いいねなどの要素の加重和を考慮して設計できます。

![Demo](./assets/demo.gif)

- [YouTubeで視聴](https://youtu.be/sZCHqrQBUGk)

## 目次

- [クイックスタート](#クイックスタート)
- [プロジェクト声明](#プロジェクト声明)
- [アーキテクチャ](#アーキテクチャ)
- [機能](#機能)
- [なぜBIA-Ghostcoderなのか？](#なぜBIA-Ghostcoderなのか)
- [セットアップ](#セットアップ)
    - [前提条件](#前提条件)
    - [インストール](#インストール)
    - [設定](#設定)
- [使用方法](#使用方法)
- [Docker](#docker)
- [Web UI](#web-ui)
- [開発](#開発)
- [FAQ](#faq)
- [貢献](#貢献)
- [ライセンス](#ライセンス)
- [謝辞](#謝辞)

## クイックスタート

```bash
# リポジトリをクローン
git clone https://github.com/BIA-Ghostcoder/BIA-Ghostcoder.git
cd BIA-Ghostcoder

# 依存関係をインストール
uv sync

# Playwrightをインストールして、デフォルトでChromiumを使用
uv run playwright install

# 環境を設定
cp .env.example .env
# .envファイルを編集して、APIキーを入力

# プロジェクトを実行
uv run main.py
```

## プロジェクト声明

これは、元同僚のグループが余暇に開発した学術的に駆動されたオープンソースプロジェクトです。Multi-AgentとDeepResearchの分野でのアイデアを探求し、交換することを目的としています。

- **目的**: このプロジェクトの主な目的は、学術研究、GAIAリーダーボードへの参加、および関連論文の将来の発表です。
- **独立性声明**: このプロジェクトは完全に独立しており、私たちの主な仕事の責任とは無関係です。雇用主や組織の見解や立場を代表するものではありません。
- **無関係声明**: このプロジェクトは、Manus（会社、組織、その他のエンティティを指すかどうかにかかわらず）とは無関係です。
- **明確化声明**: このプロジェクトをソーシャルメディアプラットフォームで宣伝したことはありません。このプロジェクトに関連する不正確な報告は、その学術的精神と一致しません。
- **貢献管理**: 問題とPRは、私たちの自由時間に対処され、遅延が発生する可能性があります。ご理解いただきありがとうございます。
- **免責事項**: このプロジェクトはMITライセンスの下でオープンソース化されています。ユーザーはその使用に伴うすべてのリスクを負います。このプロジェクトの使用から生じる直接的または間接的な結果について、いかなる責任も負いません。

## アーキテクチャ

BIA-Ghostcoderは、スーパーバイザーが専門のエージェントを調整して複雑なタスクを達成する階層型マルチエージェントシステムを実装しています。

![BiaGhosterCoder Architecture](./assets/architecture.png)

システムは、次のエージェントが協力して動作します。

1. **コーディネーター** - 初期のインタラクションを処理し、タスクをルーティングするエントリーポイント
2. **プランナー** - タスクを分析し、実行戦略を作成
3. **スーパーバイザー** - 他のエージェントの実行を監督および管理
4. **リサーチャー** - 情報を収集および分析
5. **コーダー** - コードの生成および修正を担当
6. **ブラウザー** - ウェブブラウジングおよび情報検索を実行
7. **レポーター** - ワークフロー結果のレポートおよび要約を生成

## 機能

### コア機能

- 🤖 **LLM統合**
    - [litellm](https://docs.litellm.ai/docs/providers)を通じて、ほとんどのモデルに接続することができます。 
    - Qwenなどのオープンソースモデルのサポート
    - OpenAI互換のAPIインターフェース
    - 異なるタスクの複雑さに対応するマルチティアLLMシステム

### ツールと統合

- 🔍 **検索と取得**
    - Tavily APIを介したウェブ検索
    - Jinaによるニューラル検索
    - 高度なコンテンツ抽出

### 開発機能

- 🐍 **Python統合**
    - 組み込みのPython REPL
    - コード実行環境
    - uvによるパッケージ管理

### ワークフロー管理

- 📊 **可視化と制御**
    - ワークフローグラフの可視化
    - マルチエージェントのオーケストレーション
    - タスクの委任と監視

## なぜBIA-Ghostcoderなのか？

私たちはオープンソースの協力の力を信じています。このプロジェクトは、次のような素晴らしいプロジェクトの仕事なしには実現できませんでした。

- [Qwen](https://github.com/QwenLM/Qwen) - オープンソースのLLMを提供
- [Tavily](https://tavily.com/) - 検索機能を提供
- [Jina](https://jina.ai/) - クロール検索技術を提供
- [Browser-use](https://pypi.org/project/browser-use/) - ブラウザ制御を提供
- その他多くのオープンソースの貢献者

私たちはコミュニティに還元することを約束し、コード、ドキュメント、バグレポート、機能提案など、あらゆる種類の貢献を歓迎します。

## セットアップ

### 前提条件

- [uv](https://github.com/astral-sh/uv) パッケージマネージャー

### インストール

BIA-Ghostcoderは、依存関係の管理を簡素化するために[uv](https://github.com/astral-sh/uv)を利用しています。
以下の手順に従って、仮想環境を設定し、必要な依存関係をインストールします。

```bash
# ステップ1: uvを使用して仮想環境を作成およびアクティブ化
uv python install 3.12
uv venv --python 3.12

source .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate

# ステップ2: プロジェクトの依存関係をインストール
uv sync
```

これらの手順を完了することで、環境が適切に構成され、開発の準備が整います。

### 設定

BIA-Ghostcoderは3層のLLMシステムを使用しており、それぞれ推論、基本タスク、および視覚言語タスクに用いられます。プロジェクトのルートディレクトリにある`conf.yaml`を使って設定を行います。`conf.yaml.example`を`conf.yaml`にコピーして設定を始めることができます：
```bash
cp conf.yaml.example conf.yaml
```

```yaml
# trueに設定するとconf.yamlの設定を読み取り、falseに設定すると元の.envの設定を使用します。デフォルトはfalseです（既存の設定と互換性があります）
USE_CONF: true

# LLM 設定
## litellmの設定パラメータに従ってください: https://docs.litellm.ai/docs/providers 。具体的なプロバイダのドキュメントをクリックして、completionパラメータの例を参照できます
REASONING_MODEL:
  model: "volcengine/ep-xxxx"
  api_key: $REASONING_API_KEY # .envファイル内の環境変数ENV_KEYを$ENV_KEYを使って参照することができます
  api_base: $REASONING_BASE_URL

BASIC_MODEL:
  model: "azure/gpt-4o-2024-08-06"
  api_base: $AZURE_API_BASE
  api_version: $AZURE_API_VERSION
  api_key: $AZURE_API_KEY

VISION_MODEL:
  model: "azure/gpt-4o-2024-08-06"
  api_base: $AZURE_API_BASE
  api_version: $AZURE_API_VERSION
  api_key: $AZURE_API_KEY
```

プロジェクトのルートディレクトリに.envファイルを作成し、以下の環境変数を設定することができます。.env.exampleファイルをテンプレートとしてコピーして始めることができます：
```bash
cp .env.example .env
```
```ini
# ツールのAPIキー
TAVILY_API_KEY=your_tavily_api_key
JINA_API_KEY=your_jina_api_key  # オプション

# ブラウザ設定
CHROME_INSTANCE_PATH=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome  # オプション、Chromeの実行可能ファイルのパス
CHROME_HEADLESS=False  # オプション、デフォルトは False
CHROME_PROXY_SERVER=http://127.0.0.1:10809  # オプション、デフォルトは None
CHROME_PROXY_USERNAME=  # オプション、デフォルトは None
CHROME_PROXY_PASSWORD=  # オプション、デフォルトは None
```


> **注意：**
>
> - システムは異なるタイプのタスクに対して異なるモデルを使用します：
>     - 推論用のLLMは複雑な意思決定と分析に用いられます
>     - 基本的なLLMは簡単なテキストタスクに用いられます
>     - 視覚言語LLMは画像理解に関連するタスクに用いられます
> - すべてのLLMの設定は独立してカスタマイズすることができます
> - Jina APIキーはオプションです。独自のキーを提供することで、より高いレート制限を得ることができます（[jina.ai](https://jina.ai/) でこのキーを取得できます）
> - Tavily検索のデフォルト設定は最大5つの結果を返すことです（[app.tavily.com](https://app.tavily.com/) でこのキーを取得できます） 


### プリコミットフックの設定

BIA-Ghostcoderには、各コミット前にリントとフォーマットチェックを実行するプリコミットフックが含まれています。設定するには：

1. プリコミットスクリプトを実行可能にする：

```bash
chmod +x pre-commit
```

2. プリコミットフックをインストールする：

```bash
ln -s ../../pre-commit .git/hooks/pre-commit
```

プリコミットフックは自動的に次のことを行います：

- リントチェックを実行（`make lint`）
- コードフォーマットを実行（`make format`）
- 再フォーマットされたファイルをステージングに追加
- リントまたはフォーマットエラーがある場合、コミットを防止

## 使用方法

### 基本的な実行

デフォルト設定でBIA-Ghostcoderを実行するには：

```bash
uv run main.py
```

### APIサーバー

BIA-Ghostcoderは、ストリーミングサポートを備えたFastAPIベースのAPIサーバーを提供します。

```bash
# APIサーバーを起動
make serve

# または直接実行
uv run server.py
```

APIサーバーは次のエンドポイントを公開します：

- `POST /api/chat/stream`: LangGraph呼び出し用のチャットエンドポイント（ストリーミングサポート付き）
    - リクエストボディ：
  ```json
  {
    "messages": [{ "role": "user", "content": "Your query here" }],
    "debug": false
  }
  ```
    - エージェントの応答を含むサーバー送信イベント（SSE）ストリームを返します

### 高度な設定

BIA-Ghostcoderは、`src/config`ディレクトリ内のさまざまな設定ファイルを通じてカスタマイズできます。

- `env.py`: LLMモデル、APIキー、およびベースURLを設定
- `tools.py`: ツール固有の設定を調整（例：Tavily検索結果の制限）
- `agents.py`: チーム構成とエージェントシステムプロンプトを変更

### エージェントプロンプトシステム

BIA-Ghostcoderは、`src/prompts`ディレクトリ内の高度なプロンプトシステムを使用して、エージェントの動作と責任を定義します。

#### コアエージェントの役割

- **スーパーバイザー（[`src/prompts/supervisor.md`](src/prompts/supervisor.md)）**：リクエストを分析し、どの専門家が処理するかを決定することによってチームを調整し、タスクを委任します。タスクの完了とワークフローの移行について決定します。

- **リサーチャー（[`src/prompts/researcher.md`](src/prompts/researcher.md)）**：ウェブ検索とデータ収集を通じて情報収集を専門とします。Tavily検索とウェブクロール機能を使用し、数学的計算やファイル操作を避けます。

- **コーダー（[`src/prompts/coder.md`](src/prompts/coder.md)）**：Pythonおよびbashスクリプトに焦点を当てたプロフェッショナルなソフトウェアエンジニアの役割。次のことを処理します：

    - Pythonコードの実行と分析
    - シェルコマンドの実行
    - 技術的な問題解決と実装

- **ファイルマネージャー（[`src/prompts/file_manager.md`](src/prompts/file_manager.md)）**：すべてのファイルシステム操作を処理し、適切にフォーマットされたコンテンツをmarkdown形式で保存することに重点を置きます。

- **ブラウザー（[`src/prompts/browser.md`](src/prompts/browser.md)）**：ウェブインタラクションの専門家であり、次のことを処理します：
    - ウェブサイトのナビゲーション
    - ページのインタラクション（クリック、入力、スクロール）
    - ウェブページからのコンテンツ抽出

#### プロンプトシステムのアーキテクチャ

プロンプトシステムは、テンプレートエンジン（[`src/prompts/template.py`](src/prompts/template.py)）を使用して：

- 役割固有のmarkdownテンプレートをロード
- 変数の置換を処理（例：現在の時間、チームメンバー情報）
- 各エージェントのシステムプロンプトをフォーマット

各エージェントのプロンプトは、個別のmarkdownファイルで定義されており、基礎となるコードを変更せずに動作と責任を簡単に変更できます。

## Docker

BIA-GhostcoderはDockerコンテナで実行できます。デフォルトではポート8000でAPIを提供します。

Dockerを実行する前に、`.env`ファイルに環境変数を準備する必要があります。

```bash
docker build -t BIA-Ghostcoder .
docker run --name BIA-Ghostcoder -d --env-file .env -e CHROME_HEADLESS=True -p 8000:8000 BIA-Ghostcoder
```

CLIをDockerで実行することもできます。

```bash
docker build -t BIA-Ghostcoder .
docker run --rm -it --env-file .env -e CHROME_HEADLESS=True BIA-Ghostcoder uv run python main.py
```

## Web UI

BIA-GhostcoderはデフォルトのWeb UIを提供します。

詳細については、[BIA-Ghostcoder/BIA-Ghostcoder-web-ui](https://github.com/BIA-Ghostcoder/BIA-Ghostcoder-web)プロジェクトを参照してください。

## Docker Compose (バックエンドとフロントエンドを含む)

BIA-Ghostcoderは、バックエンドとフロントエンドの両方を簡単に実行するためのdocker-compose設定を提供しています：

```bash
# バックエンドとフロントエンドを起動
docker-compose up -d

# バックエンドは http://localhost:8000 で利用可能
# フロントエンドは http://localhost:3000 で利用可能, ブラウザでアクセス可能
```

これにより：
1. BIA-Ghostcoderバックエンドコンテナをビルドして起動
2. BiaGhosterCoder Web UIコンテナをビルドして起動
3. 共有ネットワークを使用してそれらを接続

サービスを開始する前に、必要なAPIキーを含む`.env`ファイルが準備されていることを確認してください。

## 開発

### テスト

テストスイートを実行：

```bash
# すべてのテストを実行
make test

# 特定のテストファイルを実行
pytest tests/integration/test_workflow.py

# カバレッジを使用して実行
make coverage
```

### コード品質

```bash
# リントを実行
make lint

# コードをフォーマット
make format
```

## FAQ

詳細については、[FAQ.md](docs/FAQ.md)を参照してください。

## 貢献

あらゆる種類の貢献を歓迎します！タイプミスの修正、ドキュメントの改善、新機能の追加など、あなたの助けを感謝します。始める方法については、[貢献ガイド](CONTRIBUTING.md)を参照してください。

## ライセンス

このプロジェクトはオープンソースであり、[MITライセンス](LICENSE)の下で利用可能です。

## 謝辞

BIA-Ghostcoderを可能にするすべてのオープンソースプロジェクトと貢献者に特別な感謝を捧げます。私たちは巨人の肩の上に立っています。

特に以下のプロジェクトに深い感謝を表します：
- [LangChain](https://github.com/langchain-ai/langchain)：私たちのLLM相互作用とチェーンを支える優れたフレームワーク
- [LangGraph](https://github.com/langchain-ai/langgraph)：洗練されたマルチエージェントオーケストレーションを実現
- [Browser-use](https://pypi.org/project/browser-use/)：ブラウザ制御を提供

これらの素晴らしいプロジェクトはBIA-Ghostcoderの基盤を形成し、オープンソースコラボレーションの力を示しています。

## スター履歴

[![Star History Chart](https://api.star-history.com/svg?repos=BIA-Ghostcoder/BIA-Ghostcoder&type=Date)](https://www.star-history.com/#BIA-Ghostcoder/BIA-Ghostcoder&Date)
