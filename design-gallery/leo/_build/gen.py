#!/usr/bin/env python3
"""Generate the Leo design gallery.

Writes only under design-gallery/leo/. Does not read or modify production
HTML, content markdown, or assets/site.css.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from string import Template

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
sys.path.insert(0, str(HERE))

from d01_10 import DESIGNS as A  # noqa: E402
from d11_20 import DESIGNS as B  # noqa: E402
from d21_30 import DESIGNS as C  # noqa: E402

DESIGNS = A + B + C

EVALS = [
    ("保護者評価（児発）", "https://drive.google.com/file/d/14OypM0APjAh34RtH2quEMIqe6ip6Ho5H/view"),
    ("保護者評価（放デイ）", "https://drive.google.com/file/d/10l7_-n_o4skBCgxZ35YOSQEhlD7Fy_v7/view"),
    ("従業員評価（児発）", "https://drive.google.com/file/d/1YD2ecQgUOtg6cIQg5aTGtEEMQ-LCjVE8/view"),
    ("従業員評価（放デイ）", "https://drive.google.com/file/d/1yrSP-dmLRmtEHtutC6_cvXlzKXXN80FP/view"),
    ("総括表（児発）", "https://drive.google.com/file/d/17myXyFuwv6h46gbrnSeM-U_HvjDwzRTm/view"),
    ("総括表（放デイ）", "https://drive.google.com/file/d/1WEtF9XmGiatfKcp-scK35GLzyXfzONWJ/view"),
]

SUB = {
    "u_panda": "../../../img/panda.jpg",
    "u_toys": "../../../img/toyshelf.jpg",
    "u_blocks": "../../../img/blocks.jpg",
    "u_shichi": "../../../img/child_shichirin.jpg",
    "u_ext": "../../../img/leo_ext.jpg",
    "u_meal": "../../../img/homemeal.jpg",
    "u_karate": "../../../img/karate_class.jpg",
    "u_forest": "../../../img/forest_work.jpg",
    "u_station": "../../../img/yamashiro_st.jpg",
    "u_rainbow": "../../../img/rainbow.jpg",
    "u_pt": "../../../img/pt-classroom.jpg",
    "u_jigsaw": "../../../img/jigsaw.jpg",
    "u_zinnia": "../../../img/zinnia.jpg",
    "u_mari": "../../../img/marigold.jpg",
    "u_mark": "../../../img/mark_black.svg",
    "url_line": "../../../contact/#line",
    "url_pt": "../../../leo/parent-training/",
    "url_as": "../../../leo/assessment/",
    "url_leo": "../../../leo/",
    "tel_href": "tel:07069670011",
    "tel": "070-6967-0011",
    "lead": "情緒を整え落ち着きを取り戻すことを目指します",
    "role": "児童発達支援・放課後等デイサービス",
    "daily": "日常生活に必要な動作の指導をしたり、人や物を通して情緒の安定を図ったりします。",
    "group": "集団療育をしています。１部：11:00～14:30　２部：放課後～17:00",
    "lunch": "昼食を提供します。（１回３００円）手作りの和定食で情緒を養い、偏食指導にも取り組んでいます。",
    "agey": "対象年齢は、満１歳から小学校に上がるまでのお子様です。",
    "dev": "主に発達障害のお子様をお預かりします。",
    "bus": "地域によっては、送迎のご相談も承ります。",
    "toy": "たくさんのおもちゃの中から、自分の好きなものを見つけたり、一緒に少し難しいものにもチャレンジしたりします。（「認知・行動」「言語・コミュニケーション」「人間関係・社会性」）",
    "move": "武道やヨガ、農作業を通じて心身を鍛えます（「健康・生活」「運動・感覚」）。格闘家や農家さんのところへ行き<b>地域連携</b>を行なっています。",
    "event_h": "【行事】",
    "event": "菰野町のフィールドにお出かけして、遊びながら自然観察をしたり、七輪で火を起こしをしたりします。",
    "fam_h": "家族支援・進路相談（移行支援）",
    "kato": "※経験豊富な加藤が当事業所の研修講師も担当し、職員の質の向上に取り組んでいます。",
    "door": "建物の２階です。看板のあるドアからお入りください。",
    "eval_h": "令和7年度　事業所評価の公表",
    "evals": " ".join(
        f'<a href="{url}" target="_blank" rel="noopener">{label}</a>' for label, url in EVALS
    ),
    "target": "落ち着かない、こだわりが強い、集団が苦手なお子さま。診断の有無は問いません。",
    "age": "対象年齢1〜18歳",
    "time": "1部 11:00〜14:30／2部 放課後〜17:00",
    "lunch2": "1回300円（手作りの和定食。偏食指導にも取り組みます）",
    "place": "三重県四日市市あさけが丘2-1-42-2F",
    "walk": "三岐線 山城駅から徒歩12分",
    "car": "名古屋西ICから車で約30分",
    "bus2": "送迎は地域により相談可",
    "fee": "公的制度の利用可（自治体の手続きが必要。こちらで案内）",
    "pt_a": '<a href="../../../leo/parent-training/">ペアレントトレーニング</a>',
    "pt_s": "関わり方を変えます。",
    "as_a": '<a href="../../../leo/assessment/">発達検査</a>',
    "as_s": "WISC-V・新版K式。",
    "visit_h": "見学を申し込む",
}

# bus2 text was slightly adapted with 送迎は for clarity while keeping 地域により相談可.
# The source info line is exactly 「地域により相談可」. Keep it exact.
SUB["bus2"] = "地域により相談可"

KEYS = [
    "lead", "role", "daily", "group", "lunch", "agey", "dev", "bus", "toy", "move",
    "event_h", "event", "fam_h", "kato", "door", "eval_h", "evals",
    "target", "age", "time", "lunch2", "place", "walk", "car", "bus2", "fee",
    "pt_a", "pt_s", "as_a", "as_s", "visit_h", "tel", "tel_href", "url_line",
]

PHRASES = [
    "児童発達支援・放課後等デイサービス",
    "情緒を整え落ち着きを取り戻すことを目指します",
    "日常生活に必要な動作の指導",
    "集団療育をしています。１部：11:00～14:30　２部：放課後～17:00",
    "１回３００円",
    "手作りの和定食で情緒を養い、偏食指導にも取り組んでいます。",
    "満１歳から小学校に上がるまでのお子様です。",
    "主に発達障害のお子様をお預かりします。",
    "地域によっては、送迎のご相談も承ります。",
    "認知・行動",
    "言語・コミュニケーション",
    "人間関係・社会性",
    "健康・生活",
    "運動・感覚",
    "地域連携",
    "【行事】",
    "菰野町のフィールドにお出かけして、遊びながら自然観察をしたり、七輪で火を起こしをしたりします。",
    "家族支援・進路相談（移行支援）",
    "経験豊富な加藤が当事業所の研修講師も担当し、職員の質の向上に取り組んでいます。",
    "建物の２階です。看板のあるドアからお入りください。",
    "令和7年度　事業所評価の公表",
    "保護者評価（児発）",
    "保護者評価（放デイ）",
    "従業員評価（児発）",
    "従業員評価（放デイ）",
    "総括表（児発）",
    "総括表（放デイ）",
    "落ち着かない、こだわりが強い、集団が苦手なお子さま。診断の有無は問いません。",
    "対象年齢1〜18歳",
    "1部 11:00〜14:30／2部 放課後〜17:00",
    "1回300円（手作りの和定食。偏食指導にも取り組みます）",
    "三重県四日市市あさけが丘2-1-42-2F",
    "三岐線 山城駅から徒歩12分",
    "名古屋西ICから車で約30分",
    "地域により相談可",
    "公的制度の利用可（自治体の手続きが必要。こちらで案内）",
    "ペアレントトレーニング",
    "関わり方を変えます。",
    "発達検査",
    "WISC-V・新版K式。",
    "見学を申し込む",
    "070-6967-0011",
    "よくある質問",
]

BASE_CSS = r"""
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;text-size-adjust:100%}
img{max-width:100%;display:block}
a{color:inherit}
:focus{outline:none}
:focus-visible{outline:3px solid var(--focus,#e2a100);outline-offset:3px}
.skip{position:absolute;left:8px;top:-48px;background:#fff;color:#111;padding:.4rem .7rem;z-index:40}
.skip:focus{top:8px}
.pager{display:flex;justify-content:space-between;gap:1rem;padding:1.4rem 6vw 2.4rem;font-size:1rem}
.pager a{text-decoration:underline;text-underline-offset:.2em}
.pager span{opacity:.35}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *,*::before,*::after{animation:none!important;transition:none!important}
}
"""

INDEX_CSS = r"""
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:#f4f1ea;color:#1c1915;font-family:"Zen Kaku Gothic New","Hiragino Sans","Yu Gothic","WenQuanYi Micro Hei",sans-serif;line-height:1.7}
:focus{outline:none}
:focus-visible{outline:3px solid #e2a100;outline-offset:3px}
img{max-width:100%;display:block}
a{color:inherit}
.skip{position:absolute;left:8px;top:-48px;background:#fff;color:#111;padding:.4rem .7rem;z-index:5}
.skip:focus{top:8px}
.mast{padding:8vh 6vw 4vh;max-width:46rem}
.mast .org{margin:0 0 .4rem;font-size:.95rem}
.mast h1{font-weight:900;font-size:clamp(2.2rem,6vw,4.2rem);line-height:1.15;letter-spacing:.04em;margin:0}
.mast .note{font-size:1.05rem;max-width:38rem}
.mast .now{font-size:1rem}
.mast a{text-underline-offset:.2em}
ol{list-style:none;margin:0;padding:0}
ol a{display:flex;min-height:190px;text-decoration:none;align-items:stretch}
ol a:hover .name,.ol a:focus-visible .name{text-decoration:underline;text-underline-offset:.12em}
ol .pic{width:46%;object-fit:cover;min-height:190px}
ol .meta{width:54%;padding:1.1rem 1.3rem 1.2rem;display:flex;flex-direction:column;justify-content:center}
ol .no{font-size:.85rem;letter-spacing:.08em;margin:0}
ol .name{font-size:clamp(1.6rem,3vw,2.3rem);line-height:1.2;margin:.15rem 0 .35rem;font-weight:900}
ol .aim{margin:0;font-size:1rem;max-width:36rem}
ol li:nth-child(even) a{flex-direction:row-reverse}
ol li:nth-child(3n) a{min-height:250px}
ol li:nth-child(3n) .pic{width:58%}
ol li:nth-child(3n) .meta{width:42%}
ol li:nth-child(5n) .name{font-size:clamp(1.9rem,3.4vw,2.7rem)}
.foot{padding:2.5rem 6vw 3rem;font-size:.95rem}
@media (max-width:720px){
  ol a,ol li:nth-child(even) a{flex-direction:column}
  ol .pic,ol li:nth-child(3n) .pic{width:100%;height:180px;min-height:0}
  ol .meta,ol li:nth-child(3n) .meta{width:100%}
}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""


def has_key(body: str, key: str) -> bool:
    return re.search(r"\$%s(?![A-Za-z0-9_])" % re.escape(key), body) is not None


def page_html(d: dict, body: str) -> str:
    n = d["n"]
    slug = f"{n:02d}"
    prev_link = f'<a href="../{n-1:02d}/">前の案</a>' if n > 1 else "<span>前の案</span>"
    next_link = f'<a href="../{n+1:02d}/">次の案</a>' if n < 30 else "<span>次の案</span>"
    title = f"案{slug} {d['name']}｜レオ デザイン案｜星心会"
    desc = d["aim"]
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex,nofollow">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="../../../img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{d['fonts']}" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#main">本文へ</a>
<main id="main">
{body}
</main>
<nav class="pager" aria-label="ほかの案">{prev_link}<a href="../">三十案の一覧</a>{next_link}</nav>
</body>
</html>
"""


def index_html(designs: list[dict]) -> str:
    items = []
    for d in designs:
        slug = f"{d['n']:02d}"
        items.append(
            f"""<li><a href="{slug}/">
<img class="pic" src="../../img/{d['thumb']}" alt="">
<span class="meta" style="background:{d['swatch']};color:{d['ink']}">
<span class="no">案{slug}</span>
<span class="name">{d['name']}</span>
<span class="aim">{d['aim']}</span>
</span></a></li>"""
        )
    lis = "\n".join(items)
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex,nofollow">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>レオのデザイン案 30｜星心会</title>
<meta name="description" content="児童発達支援・放課後等デイサービス「レオ」の見た目の試案30。本番ページは変更していません。">
<link rel="icon" href="../../img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="gallery.css">
</head>
<body>
<a class="skip" href="#list">案の一覧へ</a>
<header class="mast">
<p class="org">星心会 · デザインギャラリー</p>
<h1>レオの、三十の顔</h1>
<p class="note">児童発達支援・放課後等デイサービス「レオ」の見た目の試案です。文言は現行のレオページと同じ内容を、レイアウトと色と文字だけ変えて置いています。本番のページには手を入れていません。</p>
<p class="now"><a href="../../leo/">いまのレオのページ</a></p>
</header>
<ol id="list">
{lis}
</ol>
<p class="foot">案のCSSは <code>design-gallery/leo/NN/style.css</code> に分離しています。サイト共通の <code>assets/site.css</code> は読み込みません。</p>
</body>
</html>
"""


def main() -> None:
    if len(DESIGNS) != 30:
        raise SystemExit(f"expected 30 designs, got {len(DESIGNS)}")
    nums = [d["n"] for d in DESIGNS]
    if nums != list(range(1, 31)):
        raise SystemExit(f"design numbers must be 1..30 in order, got {nums}")
    names = [d["name"] for d in DESIGNS]
    if len(set(names)) != 30:
        raise SystemExit("design names must be unique")

    errors: list[str] = []
    for d in DESIGNS:
        slug = f"{d['n']:02d}"
        for key in KEYS:
            if not has_key(d["body"], key):
                errors.append(f"{slug} missing ${key}")
        try:
            body = Template(d["body"]).substitute(SUB)
        except KeyError as e:
            errors.append(f"{slug} unknown placeholder {e}")
            continue
        text = re.sub(r"<[^>]+>", "", body)
        for phrase in PHRASES:
            if phrase == "よくある質問":
                if phrase in text:
                    errors.append(f"{slug} unexpectedly contains FAQ heading")
            elif phrase not in text and phrase not in body:
                errors.append(f"{slug} missing phrase: {phrase}")
        if "assets/site.css" in body or "assets/site.css" in d["css"]:
            errors.append(f"{slug} references production css")
        folder = OUT / slug
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text(page_html(d, body), encoding="utf-8")
        (folder / "style.css").write_text(BASE_CSS + "\n" + d["css"], encoding="utf-8")

    if errors:
        raise SystemExit("gallery build failed:\n" + "\n".join(errors))

    (OUT / "gallery.css").write_text(INDEX_CSS, encoding="utf-8")
    (OUT / "index.html").write_text(index_html(DESIGNS), encoding="utf-8")
    print(f"wrote 30 designs and index in {OUT}")


if __name__ == "__main__":
    main()
