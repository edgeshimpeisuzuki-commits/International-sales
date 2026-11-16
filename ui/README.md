# 画面(UI)のソース

画面はClaudeのアーティファクトとして公開している。ここはその正本のソース。画面を直すときは、ここを直してから画面に反映する(同じPRで)。

| 画面 | ソース | アーティファクト |
|---|---|---|
| 運営画面(運営・組織図・部門の詳細・設定・テスト) | ui/ops/index.html、ui/ops/store/*-datasets.json、ui/ops/data/*.json | https://claude.ai/artifact/V5T7F6ocfLQsmyxb3kSqrS |
| 承認画面(承認・却下) | ui/approve.html | https://claude.ai/artifact/GXTwknjGpMN4otWetBHaks (台帳に書き込むため、運営画面と別の手作りページ) |
| 荻野商店さま 月次レポート(クライアント向け) | ui/client/index.html、ui/client/data/*.json | https://claude.ai/artifact/TSDdqVd6HPJn3cWpNT6sP3 |

- ui/ops/store/ の url(/_blob/…)は運営画面に上げたファイルの場所。上げ直したらここも書き換える。
- 共通台帳のIDは `{{LEDGER_SHEET_ID}}` と書いてある。画面に反映するときに実際のIDに置き換える(config の ledger_env と同じ扱い)。
- 見せる相手は画面の共有設定で決める(鈴木が操作)。リポジトリに入れても画面の共有は変わらない。
- クライアント向けの画面には買い手の社名・担当者の連絡先を載せない(CLAUDE.md)。

## 組織図・部門の詳細・設定・テストの写しを作り直す

エージェント(.claude/agents)、スキル(.claude/skills)、config、tests を変えたPRでは:

1. `python3 ui/build_snapshot.py` を実行し、ui/ops/data/*.json の変化も同じPRに入れる。
2. mainに取り込んだら、4つのJSONを運営画面に上げ直し(upload_asset)、datasets/agents・skills・settings・tests の url と updated を差し替える。
3. 運営画面のタブで、件数と出典(コミット)が変わったことを確かめる。

画面のHTMLを直したときは、files/index.html(運営画面・月次レポート)または承認画面を公開し直す。
