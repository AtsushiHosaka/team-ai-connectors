# 追加設定ガイド

[導入ガイド](quickstart.md)を終えてから、必要な項目だけ進めてください。設定ファイルの編集や認証に慣れていない場合は、メンターと一緒に作業してください。

ターミナルでの作業は、取得済みの`team-ai-connectors`フォルダーを開いて進めます。AIの入力欄に入れる箇所は、各手順に明記しています。同じリポジトリをもう一度取得する必要はありません。

## 1. NotionやJiraをつなぐ

NotionやAtlassianを使っている人向けの設定です。各自のアカウントでログインします。Atlassianの接続には、利用中のAtlassian Cloudのサイトが必要です。

このリポジトリの`notion`と`atlassian`プラグインは、各サービスの公式MCPサーバーに接続します。MCPは、AIと外部サービスをつなぐ仕組みです。プラグイン自体は、このリポジトリの管理者が用意したものです。

Codexでは`/plugins`を開き、`team-ai-connectors`から必要なプラグインを選びます。Claude Codeでは、AIの入力欄に使うサービスのコマンドを入力します。

```text
/plugin install notion@team-ai-connectors
/plugin install atlassian@team-ai-connectors
```

インストール後は、クライアントの接続画面やログイン案内から認証します。接続するワークスペースやサイトを確認してください。Claude Codeでは`/mcp`で接続状態を確認できます。

設定手順の詳細は、[Notion公式ガイド](https://developers.notion.com/guides/mcp/get-started-with-mcp)と[Atlassian公式ガイド](https://atlassian.github.io/atlassian-mcp-server/)にあります。

## 2. 設定ファイルから接続を追加する

プラグインを使わず、Codex・Claude Code・VS Code用の設定を作る方法です。同じサービスについて、プラグインと設定ファイルの両方を登録する必要はありません。

スクリプトにはPython 3.11以上が必要です。追加のPythonパッケージは不要です。Windowsで`python3`が使えず、`py -3`でPythonが起動する場合は、以降の`python3`を`py -3`に置き換えてください。

利用できる接続先を一覧で確認します。

```sh
python3 scripts/configure.py list
```

一覧にあるSlackは、AIクライアントの標準の接続機能から設定します。次の`export`ではSlackの設定を生成できません。Slackを読むための接続は、[導入ガイド](quickstart.md)を参照してください。

### 使うクライアントの設定を生成する

次のうち、自分が使うクライアントのコマンドを1つ選んでください。`--connectors`の後ろには、必要なサービス名だけを書きます。

CodexでNotionとGitHubを使う場合は、次のコマンドです。

```sh
python3 scripts/configure.py export --client codex --connectors notion github
```

Claude CodeでNotionとGitHubを使う場合は、次のコマンドです。

```sh
python3 scripts/configure.py export --client claude-code --connectors notion github
```

VS CodeでNotion・GitHub・Atlassianを使う場合は、次のコマンドです。

```sh
python3 scripts/configure.py export --client vscode --connectors notion github atlassian
```

設定はターミナルに表示されます。ファイルに保存したい場合は、`--output`で新しいファイル名を指定します。

```sh
python3 scripts/configure.py export --client codex --connectors notion github --output codex-connectors.toml
```

同じ名前のファイルがあると、スクリプトは上書きせず終了します。別の名前で保存してください。AIクライアントの設定ファイルを、このコマンドで直接更新することはありません。

### 既存の設定に必要な部分を追加する

生成した設定は、サービスへの接続部分だけを含んでいます。メンターと一緒に既存の設定ファイルを開き、次の部分を追加してください。

| クライアント | 設定ファイルの場所 | 追加する部分 |
| --- | --- | --- |
| Codex | `~/.codex/config.toml` | `mcp_servers`の各テーブル |
| Claude Code | 開発プロジェクト内の`.mcp.json` | `mcpServers`内の項目 |
| VS Code | 開発プロジェクト内の`.vscode/mcp.json` | `servers`内の項目 |

`~`は自分のホームフォルダーを表します。既存の設定を残して、同名の接続が重複しないように追加します。生成した一部分で設定ファイル全体を置き換えないでください。

VS CodeではMCPに対応したAI機能も必要です。エディターのインストールだけで接続が使えるわけではありません。[VS Code公式ガイド](https://code.visualstudio.com/docs/agent-customization/mcp-servers)も確認してください。

### NotionとAtlassianにログインする

生成した設定を追加したCodexでは、必要なサービスのコマンドをターミナルで実行します。

```sh
codex mcp login team-notion
codex mcp login team-atlassian
```

`team-notion`と`team-atlassian`は、スクリプトが生成する接続名です。プラグインで追加した場合は、このコマンドではなくプラグインのログイン案内に従ってください。Claude Codeでは`/mcp`、VS CodeではMCPの接続画面から認証します。

ブラウザーが開いたら自分のアカウントでログインし、接続先と許可する操作を確認します。ログイン後は、普段から閲覧できるページを1件読めるか試してください。

### GitHubの認証を設定する

このリポジトリが生成するGitHub設定は、各自のトークンを`GITHUB_MCP_TOKEN`という環境変数から読みます。環境変数は、起動するプログラムに値を渡すための設定です。

メンターと一緒に、対象のリポジトリと必要な読み取り権限に絞ったトークンを作成してください。その値を環境変数に設定し、AIクライアントを起動する前に有効にします。トークンそのものを設定ファイルに書く必要はありません。

`gh auth login`でのログインと、この環境変数は別の設定です。`.env`ファイルも自動では読み込まれません。別に起動したGUIアプリには、ターミナルで設定した環境変数が渡らない場合があります。

生成される設定には`X-MCP-Readonly: true`が入り、この接続では読み取り専用の操作を要求します。トークン自体の権限が変わるわけではありません。トークンはチャットやGitに保存しないでください。

VS Codeでは、GitHubの公式MCP接続でブラウザーから認証する方法もあります。詳しくは[GitHub公式のVS Code向け案内](https://github.com/github/github-mcp-server#install-in-vs-code)と[読み取り専用設定](https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md)を参照してください。

接続後に、AIへ次のように頼みます。

```text
GitHubの接続を使って、AtsushiHosaka/team-ai-connectorsのREADMEを読んでください。
内容を短く説明し、参照したページのリンクを返してください。変更はしないでください。
```

実際のページを読めたら、接続の確認は完了です。設定ファイルが生成できただけでは、ログインや閲覧が成功したとは判断できません。

## 3. Slackへの通知を追加する

Slackに接続済みのAIから投稿する場合は、投稿先と内容を指定します。送信機能が使えることを確認してから、AIの入力欄に依頼してください。

```text
work-sessionを使って、#開発チャンネルに作業開始を投稿してください。
今日の目標は検索機能の追加です。最初に画面の動きを整理します。
```

`#開発チャンネル`は実際の投稿先に置き換えます。スキルを読み込んだりエディターを開いたりするだけで、自動投稿はされません。

### 決まったチャンネルへWebhookで送る

Incoming Webhookは、決まったSlackチャンネルへ通知を送る仕組みです。Slackを検索したり、過去の投稿を読んだりする機能はありません。

Slackの管理者にWebhookを用意してもらい、ローカルの環境変数`SLACK_WEBHOOK_URL`に設定します。URLの渡し方と設定はメンターに確認してください。URLは秘密情報なので、チャット・コード・Gitには貼りません。詳しくは[Slack公式ガイド](https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/)を参照してください。

最初は、送信せずに内容を確認します。次のコマンドはターミナルに通知内容をJSONで表示します。

```sh
python3 scripts/slack_notify.py --event started --summary "検索機能の開発を始めます"
```

実際に送るときだけ`--send`を付けます。次の例では、Webhookに設定されたチャンネルへ完了通知を送ります。

```sh
python3 scripts/slack_notify.py --event completed --summary "検索機能の動作を確認しました" --link "https://github.com/AtsushiHosaka/team-ai-connectors" --send
```

`--link`には実際の作業やPRのURLを指定してください。スクリプトから送信先のチャンネルは変更できません。成功時は`Slack confirmed delivery to the webhook's configured channel.`と表示されます。Slack上でも投稿を確認してください。

`--event`には次の4種類が使えます。

| 値 | 通知する場面 |
| --- | --- |
| `started` | 作業を始めたとき |
| `blocked` | 困っていて助けが必要なとき |
| `review` | レビューを依頼するとき |
| `completed` | 作業が完了したとき |

## 4. スキルのZIPを作る

カスタムスキルのZIPアップロードに対応した画面では、個別のスキルをアップロードする方法もあります。利用できる機能はアカウントやクライアントによって異なります。

```sh
python3 scripts/package_skills.py --output dist
```

`dist`フォルダーにできたZIPを、対応する画面からアップロードします。同名のZIPがある場合は上書きされないため、`--output`に別のフォルダー名を指定してください。ZIPにはスキルの指示が入っています。サービスへのログインは別に必要です。

## 5. 更新とローカル確認

更新時も、最初に取得したフォルダーを使います。自分でファイルを変更している場合は、変更の扱いをメンターと確認してから進めてください。

```sh
git pull --ff-only
```

ローカルのフォルダーを`.`で登録したプラグインは、クライアントの再読み込みや新しいセッションの案内に従います。GitHubのリポジトリを直接登録したマーケットプレイスには、別の更新操作があります。Codexでは次のコマンドです。

```sh
codex plugin marketplace upgrade team-ai-connectors
```

Claude Codeでは`/plugin`の画面から更新します。[Codexのプラグインガイド](https://learn.chatgpt.com/docs/plugins)と[Claude Codeのマーケットプレイスガイド](https://code.claude.com/docs/en/plugin-marketplaces)で、利用中のクライアントの操作を確認してください。

設定の生成、ZIP作成、Webhookのプレビューなどを確かめるローカルテストもあります。

```sh
python3 -m unittest discover -s tests -v
```

テストの成功と、各自のアカウントでの接続成功は別です。外部サービスは、実際にページを読む、Slackの投稿を確認するなどの方法で確かめてください。

接続に失敗したら、使っているアカウント、権限、環境変数、クライアントの接続状態を確認します。メンターへの相談には、失敗した手順とエラーを添えてください。詳しい仕組みと参照先は[接続と認証の資料](connectors.md)にもあります。
