# Playwrightの準備と確認

Webアプリを実際のブラウザーで操作するための手順です。CodexやClaude Codeなど、ローカルのコマンドを実行できるAI向けです。メンバーには、使うフォルダーと確認結果を日本語で説明します。

## 使えるものを先に調べる

接続済みのPlaywrightツール、CLI、実行中のセッションを確認します。既存のPlaywright MCPやクライアントのブラウザー機能で操作できる場合は、同じセッションで動作確認へ進みます。Playwright自体を使ったか、別のブラウザー機能を使ったかは区別して報告します。

新たにCLIを準備する場合は、Node.js・npm・npxの有無を確認します。Node.jsが不足していれば、[Node.js公式](https://nodejs.org/en/download)と[Playwrightの必要環境](https://playwright.dev/docs/intro#system-requirements)から、OSに対応するサポート中のLTS版を選びます。管理者の操作が必要なら、その操作だけ案内します。既存のNode.jsやブラウザーを無断で入れ替えません。

CLIは利用者専用のツールフォルダーで実行します。例はmacOS・Linuxの`~/.cache/team-ai-connectors/playwright`、Windowsの`%LOCALAPPDATA%/team-ai-connectors/playwright`です。以下のコマンドはターミナル用で、macOSとWindowsのPowerShellで共通です。

```text
node --version
npm --version
npx --version
npx --yes --package @playwright/cli@0.1.22 playwright-cli --help
npx --yes --package @playwright/cli@0.1.22 playwright-cli list
```

初回はnpmのキャッシュへCLIがダウンロードされます。実行に使う版をそろえるため、以下も同じ`0.1.22`を使います。既存の別の版で動作している場合は、その版を記録して使い回せます。

## ブラウザーを準備する

使えるブラウザーがなければ、同じCLIからChromiumを準備します。

```text
npx --yes --package @playwright/cli@0.1.22 playwright-cli install-browser chromium
```

インストールや実行の失敗は記録し、ネットワーク制限、OSの不足パッケージ、権限などを切り分けます。OSの変更や管理者権限が必要なら、必要な操作を具体的に伝えます。別の検証を続けられる場合は進めます。

この準備に`npm init playwright`、アプリへの`npm install`、グローバルインストールは不要です。`package.json`・ロックファイル・既存のブラウザー設定を変更しません。`install --skills`による追加のスキル生成も不要です。このチームのスキルに操作手順が含まれています。

## 実際に操作して確かめる

1. このスキルの[確認用ページ](../assets/playwright-smoke.html)を、[付属のサーバー](../scripts/serve-smoke.cjs)で配信します。`node "スキルの絶対パス/scripts/serve-smoke.cjs"`を起動したままにし、出力された`url`を使います。Node.jsの標準機能だけで動き、空いているポートを選びます。`127.0.0.1`から確認用ページだけを配信し、外部公開はしません。`file://`はCLIでブロックされるため使いません。
2. 使えるセッションがあれば確認用のタブだけを`tab-new`で追加します。なければ、一覧と重ならない専用セッションを作ります。以下の`team-setup-check`は例です。既存の同名セッションに`open`すると再起動されるため、そのまま実行しません。

```text
npx --yes --package @playwright/cli@0.1.22 playwright-cli -s=team-setup-check open "確認用ページのURL" --browser=chromium
npx --yes --package @playwright/cli@0.1.22 playwright-cli -s=team-setup-check snapshot
```

3. 最新のスナップショットから「動作を確認する」ボタンの参照を読み取ります。`e番号`は実際の参照に置き換えます。

```text
npx --yes --package @playwright/cli@0.1.22 playwright-cli -s=team-setup-check click e番号
npx --yes --package @playwright/cli@0.1.22 playwright-cli -s=team-setup-check snapshot
npx --yes --package @playwright/cli@0.1.22 playwright-cli -s=team-setup-check screenshot
```

4. 「まだ確認していません」が「確認できました」に変わったことと、生成された画像の内容を確かめます。コマンド、使った版、操作結果、画像の保存先を記録します。証拠は対象プロジェクトの`output/playwright/`など、既存の保存規則に合わせて保管し、自動でコミットしません。
5. 今回作った専用セッションだけを`-s=team-setup-check close`で閉じます。既存セッションを使った場合は追加したタブだけを閉じます。今回起動した確認用サーバーも終了します。`close-all`・`kill-all`は使いません。

ヘルプ表示、ダウンロード、キャッシュの存在だけでは動作確認は完了しません。この確認はブラウザー操作の準備を確かめるもので、対象アプリの動作や認証を検証したことにはしません。

## QAと利用体験の確認で使う

QA・利用体験の確認でも、利用可能な接続とセッションを先に確認します。不足していれば、この手順で検証用のCLIとブラウザーを準備してから再開します。この準備は検証に含め、同じ作業の許可を重ねて求めません。アプリの依存関係を変更する必要がある場合は、検証用ツールの準備と分けて扱います。

対象アプリでは実際のURL、ログイン状態、画面幅などを記録します。操作前のスナップショットにある参照を使い、画面が変わったら取り直します。スクリーンショット、必要に応じて動画・トレースを残します。保存や送信などの操作は、その確認で許可された範囲に従います。

シェルを使えないクライアントでは、利用可能なブラウザー機能で確認し、メンバーのPCへPlaywrightを導入したとは報告しません。iOSなどのネイティブアプリは既存のXcode・シミュレーター等で操作します。モバイルブラウザーの再現だけで、ネイティブアプリを確認済みにはしません。

手順は[MicrosoftのCLI案内](https://github.com/microsoft/playwright-cli)、[ブラウザーの導入](https://playwright.dev/docs/browsers)、[npm execの案内](https://docs.npmjs.com/cli/v11/commands/npm-exec/)に基づきます。MCP接続が必要なクライアントでは、既存設定を保ったうえで[公式Playwright MCP](https://github.com/microsoft/playwright-mcp)の対応手順を選び、実際のツール呼び出しまで確認します。
