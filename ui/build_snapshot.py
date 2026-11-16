#!/usr/bin/env python3
"""運営画面の「組織図」「部門の詳細」「設定・テスト」タブの写しを、リポジトリから作り直す(D14-18)。

使い方: python3 ui/build_snapshot.py   (リポジトリの最上位で実行)
出力:   ui/ops/data/agents.json, skills.json, settings.json, tests.json
エージェント・スキル・config・tests を変えたPRでは、これを実行して出力も同じPRに入れる
(docs/common-rules.md「画面の更新」)。画面への反映は ui/README.md の手順。
"""
import glob
import json
import os
import re
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "ui", "ops", "data")
CODE = re.compile(r"D\d{2}-\d{2}")

DEPT_NAMES = {
    "D01": "市場インテリジェンス", "D02": "調達・サプライヤー・クライアント管理", "D03": "カテゴリー・商品企画",
    "D04": "規制・商品適合", "D05": "マーケティング", "D06": "販売(B2B)", "D08": "需給計画・在庫",
    "D10": "顧客対応・アカウント", "D11": "決済・貿易金融", "D12": "リスク・コンプライアンス",
    "D13": "コーポレート", "D14": "データ・エージェント基盤", "D16": "サービス提供",
}
SECTIONS = ["D06"]  # 課を持つ部門
CHARTER_KEYS = ["目的", "起動", "受け渡し", "承認ゲート", "KPI", "制約"]


def front(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return (yaml.safe_load(m.group(1)) or {}, text[m.end():]) if m else ({}, text)


def source_label():
    try:
        sha = subprocess.check_output(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"], text=True).strip()
        day = subprocess.check_output(["git", "-C", ROOT, "log", "-1", "--format=%cs"], text=True).strip()
        return f"GitHub edgeshimpeisuzuki-commits/International-sales (main {sha}, {day})"
    except Exception:
        return "GitHub edgeshimpeisuzuki-commits/International-sales"


def agents():
    rows, skill_map = [], {}
    for path in sorted(glob.glob(os.path.join(ROOT, ".claude", "agents", "*.md"))):
        fm, body = front(open(path, encoding="utf-8").read())
        name = fm.get("name") or os.path.basename(path)[:-3]
        desc = str(fm.get("description", ""))
        m = re.match(r"d(\d{2})-", name)
        if m:
            dept, layer = "D" + m.group(1), "部門長"
        elif name == "l0-orchestrator":
            dept, layer = "", "統括"
        elif name in ("sender", "watchdog"):
            dept, layer = "", "共通"
        else:  # 課: 説明の最初のL2で部門を決める
            c = CODE.search(desc)
            dept = c.group(0)[:3] if c else ""
            layer = f"課({dept})" if dept in SECTIONS else "共通"
        row = {"agent": name, "部門": dept, "部門名": DEPT_NAMES.get(dept, ""), "層": layer, "説明": desc}
        for k in CHARTER_KEYS:
            mm = re.search(rf"^- {k}(?:\(仮\))?:(.*)$", body, re.M)
            row[k] = mm.group(1).strip() if mm and layer == "部門長" else ""
        rows.append(row)
        # 担当業務の表: | L2 | フェーズ | 使うスキル | 内容 |
        for line in body.splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 3 and CODE.fullmatch(cells[0] or ""):
                for s in re.findall(r"skills/([\w-]+)", cells[2]):
                    skill_map.setdefault(s, []).append((cells[0], cells[1]))
    return rows, skill_map


def skills(skill_map):
    rows = []
    for path in sorted(glob.glob(os.path.join(ROOT, ".claude", "skills", "*", "SKILL.md"))):
        text = open(path, encoding="utf-8").read()
        fm, body = front(text)
        name = fm.get("name") or os.path.basename(os.path.dirname(path))
        desc = str(fm.get("description", ""))
        pairs = skill_map.get(name, [])
        codes = sorted({c for c, _ in pairs} | set(CODE.findall(desc)))
        if not codes:
            codes = CODE.findall(body)[:1]
        phases = {p for _, p in pairs if p}
        pm = re.search(r"フェーズ:(P\d)", body)
        phase = pm.group(1) if pm else ("P2" if phases == {"P2"} else "P1")
        am = re.search(r"^\|\s*自律度\s*\|(.*)\|\s*$", body, re.M)
        if name.startswith(("l2-", "sec-")):
            desc = re.split(r"の手順と判断基準", desc)[0]
        rows.append({"skill": name, "業務": " ".join(codes), "部門": codes[0][:3] if codes else "",
                     "フェーズ": phase, "自律度": am.group(1).strip() if am else "", "説明": desc})
    return rows


def flatten(d, prefix=""):
    for k, v in d.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            yield from flatten(v, key + ".")
        else:
            yield key, json.dumps(v, ensure_ascii=False) if isinstance(v, list) else str(v)


def settings():
    rows = []
    for rel in ["config/standard-params.yaml"] + sorted(
            os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "config", "clients", "*.yaml"))):
        data = yaml.safe_load(open(os.path.join(ROOT, rel), encoding="utf-8")) or {}
        rows += [{"ファイル": rel, "項目": k, "値": v} for k, v in flatten(data)]
    return rows


def tests():
    rows = []
    readmes = sorted(glob.glob(os.path.join(ROOT, "tests", "p1-full-*", "README.md")))
    if readmes:
        for line in open(readmes[-1], encoding="utf-8"):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) >= 3 and c[1].isdigit() and c[0] != "合計":
                rows.append({"グループ": c[0], "問題数": int(c[1]), "正解": int(c[2])})
    scores = sorted(glob.glob(os.path.join(ROOT, "tests", "reply-classify", "runs", "*-score.md")))
    if scores:
        m = re.search(r"(\d+)/(\d+)", open(scores[-1], encoding="utf-8").read())
        if m:
            rows.append({"グループ": "返信の分類", "問題数": int(m.group(2)), "正解": int(m.group(1))})
    return rows


def main():
    os.makedirs(OUT, exist_ok=True)
    meta = [{"label": "出典", "value": source_label()}]
    a, smap = agents()
    out = {"agents": a, "skills": skills(smap), "settings": settings(), "tests": tests()}
    for name, rows in out.items():
        with open(os.path.join(OUT, f"{name}.json"), "w", encoding="utf-8") as f:
            json.dump({"rows": rows, "meta": meta}, f, ensure_ascii=False, indent=1)
        print(f"{name}: {len(rows)}行")


if __name__ == "__main__":
    sys.exit(main())
