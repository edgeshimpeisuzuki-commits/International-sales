# 定型の返信と配信停止フォーム(v0.1 案・未承認)

- 定義書:D12-09(配信停止の確認の返信、L4)、D06-04(受付返信)、19.5 R1(2名とも不在のときの受付返信)、19.6の判定の2・7
- これらは受信した文面を含まない定型文なので、承認後は自動で送ってよい(定義書の権限の分離)。件名に `<ADV>` は付けない(広告ではない返信のため)
- 署名と法定表示は営業メールと同じ(sg-wave1-v0.2.md の6)。L4で自動送信するため `This is an automated message.` を1行入れる

## 1. 配信停止の確認(OGN-UNSUB-OK v0.1)

**Subject:** `Re: {{original_subject}}`

```
Hello,

We have removed {{email_address}} from our mailing list. {{scope_sentence}}
You will not receive further sales emails from us. If this was a mistake, just reply to this email.

This is an automated message.
```

`{{scope_sentence}}`:本人だけ → 空。会社単位 → `This applies to all addresses at {{domain}}.`

禁止:停止の確認以外のこと(商品の案内、「本当に停止しますか」)を書かない。

## 2. 受付返信:返事に時間がかかるとき(OGN-ACK-BUSY v0.1)

返信の量が処理できる量を超えたとき、待たせる相手に送る(D06-04)。

```
Hello {{first_name_or_team}},

Thank you for your reply. I have received your message and will respond within {{days}} days.

This is an automated message.
```

`{{days}}` は標準パラメータの対応日数。価格・数量・納期への言及は入れない。

## 3. 受付返信:2名とも不在のとき(OGN-ACK-AWAY v0.1、R1)

```
Hello,

Thank you for your message. I am away until {{return_date}} and will reply after I return.
If you would like to stop receiving our emails, reply "unsubscribe" or use {{unsubscribe_url}}. This is handled automatically while I am away.

This is an automated message.
```

## 4. 配信停止フォームの設計(Googleフォーム)

| 項目 | 内容 |
|---|---|
| 作る人 | 鈴木さん(共通台帳の持ち主のアカウント:個人のGoogleアカウント) |
| タイトル | Unsubscribe |
| 説明文 | `Enter your email address to stop receiving sales emails sent on behalf of OGINO SHOTEN Co., Ltd. Your request is applied within 24 hours.` |
| 質問1 | Email address(必須、回答の検証=メールアドレス) |
| 質問2 | Apply to(必須、ラジオ): `This address only` / `All addresses at my company` |
| 質問3 | Company name(任意) |
| 設定 | ログイン不要(「メールアドレスを収集する」はオフ、回答者のGoogleログインを求めない)。回答の編集はオフ |
| 回答の行き先 | 共通台帳にリンクする(台帳に「フォームの回答 1」タブが増える)。タブ名は「配信停止フォーム」に変える |
| 送信前の照合 | 送る係は「配信停止」タブと「配信停止フォーム」タブの両方と照合する(アドレス完全一致、会社単位はドメイン一致)。AIの判断は使わない |
| 記録 | 毎朝の本処理が、フォームの新しい回答を「配信停止」タブにも写し、反映日時を書く |
| 有効期間 | 30日以上(SGの法律)。フォームは消さず、回答の受付を止めない |
| 試験 | 12/1前に、フォームと返信の両方で実際に停止を試し、照合で止まることを確かめる(判定の2) |

フォームのURLを営業メールの `{{unsubscribe_url}}` に入れる。
