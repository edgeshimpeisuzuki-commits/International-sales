# 荻野商店 SG 第1波 営業メールのテンプレート(v0.2 仮案・未承認)

- 定義書の該当L2:D05-02(作成)、D06-03(送信)、D04-07(表現チェック)、D12-09(配信停止)
- 状態:**仮案**(11/16 鈴木:仮案として進めてよい)。D04-07の結果(sg-wave1-v0.1.md.check-20261116.md)を反映済み。D04-07の表現チェックと、2名の承認(D06の初回送信の承認)を通るまで使わない
- 本文は50〜100語(署名・法定表示は数えない)。英語。件名の先頭に `<ADV> `(SG)
- ABテストで変えるのは初回の「進め方」だけ。フォロー2通は両方の案で共通(config/experiments/EXP-20261201-approach.yaml)
- 差し込み項目は `{{ }}`。値が空なら送らずに人に回す

## 0. 使う事実(出典:荻野商店の英語サイト https://ochaogino.co.jp/international/ 、11/16確認)

| 事実 | 文面での使い方 |
|---|---|
| 1958年創業、埼玉県寄居町の茶と食品の卸 | 「founded in 1958」 |
| Hojicha Powder(標準品3種)。Organic はSGで使える認証か未確認のため書かない | 商品名 |
| 見積は1kg単位、20kgカートン | 「quoted per kg, packed in 20 kg cartons」 |
| MOQは問合せ時に確認 | MOQは書かない |
| 包装・商品開発は相談可(荻野商店談) | 「can be discussed」までにとどめ、約束しない |

書かないこと:取引実績・取引先名(マレーシア案件など。荻野商店の了承がない)、価格、納期、認証の約束、「AIで作成」。

## 1. 初回 A案:紹介してから条件を聞く(OGN-INTRO-01 v0.2)

**Subject:** `<ADV> Hojicha powder from Japan for {{company_name}}`

```
Hello {{company_name}} team,

I handle overseas sales for OGINO SHOTEN, a Japanese tea wholesaler founded in 1958. I write on their behalf, and we both read replies.

{{segment_line}}

OGINO SHOTEN supplies hojicha powder, quoted per kg and packed in 20 kg cartons. Packaging and blends can be discussed.

Could you share the volume you would need and your target price per kg? If the terms fit, I would suggest a short call.
```

## 2. 初回 B案:質問1つから入る短い文面(OGN-INTRO-02 v0.2)

**Subject:** `<ADV> Quick question on hojicha, {{company_name}}`

```
Hello {{company_name}} team,

Do you currently buy hojicha or other Japanese tea powders?

{{segment_line}}

I handle overseas sales for OGINO SHOTEN, a Japanese tea wholesaler founded in 1958, and write on their behalf. Both of us read replies.

If it is relevant, just reply with a rough volume and the price per kg you are aiming for, and I will check whether we can meet it.
```

## 3. 業態別の差し替え文 `{{segment_line}}`(1文)

| ICP | segment_line |
|---|---|
| ①日本食材の輸入卸・商社 | `As an importer of Japanese food, you may get requests for hojicha from the cafés and dessert shops you supply.` |
| ②食品・飲料メーカー(飲料) | `Hojicha powder brings a roasted flavor to lattes and ready-to-drink teas.` |
| ②食品・飲料メーカー(アイス) | `Hojicha powder is used for a roasted flavor in ice cream and soft serve.` |
| ②食品・飲料メーカー(菓子・製パン) | `Hojicha powder is used for a roasted flavor in baked goods and confectionery.` |

業態が分からない先は送らずに人に回す。

## 4. フォロー1(4日後、両案共通)(OGN-FU1-01 v0.2)

**Subject:** `<ADV> Re: {{original_subject_without_ADV}}`(初回と同じスレッドへの返信として送るときだけ)

```
Hello {{company_name}} team,

Following up on my note about hojicha powder from OGINO SHOTEN, a Japanese tea wholesaler I represent.

Product details are here: https://ochaogino.co.jp/international/

A rough volume and your target price per kg are all I need to check whether we are a fit. If someone else handles ingredient sourcing, I would appreciate a pointer.
```

## 5. フォロー2(10日後・最後、両案共通)(OGN-FU2-01 v0.2)

**Subject:** `<ADV> Re: {{original_subject_without_ADV}}`(初回と同じスレッドへの返信として送るときだけ)

```
Hello {{company_name}} team,

This is my last note on hojicha powder from OGINO SHOTEN, the Japanese tea wholesaler I represent.

If it is not a priority now, no reply is needed and I will close this thread. If it becomes relevant later, a short reply with volume and target price per kg is enough to restart.
```

## 6. 署名と法定表示(全テンプレート共通の末尾)

```
--
Shimpei Suzuki
Overseas Sales Representative for OGINO SHOTEN Co., Ltd.
{{sender_email}}

OGINO SHOTEN Co., Ltd., 1625 Yorii, Yorii-machi, Osato-gun, Saitama 369-1203, Japan
Sent on their behalf by {{agent_name}} ({{agent_contact}}).

To stop receiving these emails, reply "unsubscribe" or use {{unsubscribe_url}}.
Questions or complaints: {{sender_email}}
```

- 定義書5.2:クライアント(送信の名義人)の正式名称・所在地と、代理の自社の名称・連絡先を両方書く(専門家の確認が済むまで)。配信停止は返信と専用フォームの2つ。SGは30日以上有効な連絡先
- L4で自動送信する場合だけ、署名の前に `This is an automated follow-up.` を1行入れる(P1の送信はL3なので入れない)

## 7. 送る前に埋める必要があるもの(未決)

| # | 項目 | 案 | 決める人 |
|---|---|---|---|
| 1 | `{{agent_name}}` 代理の名称 | Knock-Knock(屋号・仮決定) | 2名 |
| 2 | `{{agent_contact}}` 代理の連絡先 | 自社ドメインがないため、当面は鈴木の連絡用アドレス | 2名 |
| 3 | `{{unsubscribe_url}}` 配信停止フォーム | Googleフォーム(30日以上有効、回答は台帳「配信停止」へ) | 鈴木 |
| 4 | 所在地の英語表記 | 荻野商店の英語サイトの表記のまま | 荻野商店に確認(確認15項目に追加) |
| 5 | 「Packaging and blends can be discussed」の可否 | 入れる | 荻野商店に確認 |

## 8. 自己チェック(D04-07の前の下書き段階)

| 観点 | A | B | FU1 | FU2 |
|---|---|---|---|---|
| 本文50〜100語(あいさつ含む) | 82〜91語 | 76〜85語 | 56語 | 56語 |
| 業態に合わせた1文 | ○ | ○ | -(初回で済み) | - |
| 代理であること・両者が読むこと | ○ | ○ | 代理のみ | 代理のみ |
| 希望価格と数量を聞く | ○ | ○ | ○ | ○ |
| 価格・納期・数量・認証の約束なし | ○ | ○ | ○ | ○ |
| 実績・取引先を盛らない | ○ | ○ | ○ | ○ |
| `<ADV>`・配信停止2経路・連絡先 | ○ | ○ | ○ | ○ |

語数は segment_line の4種それぞれを入れて数えた値(11/16)。
