# クライアント別の導入と確認

## Codex

チームのマーケットプレイスが未登録の場合だけ、取得済みのチームリポジトリをターミナルで登録します。`.`はそのリポジトリのフォルダーを表します。

```sh
codex plugin marketplace add .
codex plugin add team-workflows@team-ai-connectors
```

`natural-japanese`の導入を依頼された場合は、次を使います。

```sh
codex plugin add natural-japanese@team-ai-connectors
```

古いCodexで`plugin add`が使えなければ、対応する公式手順で更新するか、`/plugins`から同じプラグインを選びます。既に別経路で導入済みの場合は、新たな重複登録をしません。新しいセッションでスキルの表示と呼び出しを確認します。

参照先は[Codexのプラグイン](https://learn.chatgpt.com/docs/plugins)と[Codex CLIの導入](https://learn.chatgpt.com/docs/cli)です。

## Claude Code

初回だけ、取得済みのリポジトリをマーケットプレイスに登録します。次のコマンドは、Claude Codeを起動した後の入力欄に入れます。

```text
/plugin marketplace add .
/plugin install team-workflows@team-ai-connectors
```

`natural-japanese`の導入を依頼された場合は、次を使います。

```text
/plugin install natural-japanese@team-ai-connectors
```

エージェントがターミナルから実行する場合は、対応する`claude plugin install natural-japanese@team-ai-connectors`を使えます。先に`claude plugin list`などで現在の導入状況を確認します。新しいセッションでスキルを読み込めることを確かめます。

参照先は[Claude Codeのマーケットプレイス](https://code.claude.com/docs/en/plugin-marketplaces)です。

## ChatGPTなどのブラウザー画面

このGitHubマーケットプレイスのCLIコマンドを、ブラウザーのチャット入力欄にそのまま送らせません。アカウントで利用できるプラグイン・スキルの導入画面を確認します。

カスタムスキルのアップロードに対応する画面では、チームのリリースから必要なZIPを取得します。`natural-japanese`は[配布元のリリース](https://github.com/coji/natural-japanese/releases)と、その時点のアップロード手順を確認します。リポジトリにアクセスできることと、ブラウザーでそのスキルを使えることは別に確かめます。

## 日本語文章の検査

`natural-japanese`の配布元は[coji/natural-japanese](https://github.com/coji/natural-japanese)です。チームのカタログは確認したコミットを固定して参照しています。

導入後、その版の`SKILL.md`と必要な依存ツールを確認します。`uv`が必要なら、既存の導入を優先し、不足時は[公式のuv導入案内](https://docs.astral.sh/uv/getting-started/installation/)に従います。別の同名ツールで代用したり、検査を実行せず合格扱いにしたりしません。

依存ツールの追加が依頼に含まれ、実行できる環境なら導入して検査します。管理者の操作やブラウザー認証が必要な場合は、その具体的な操作だけ案内します。
