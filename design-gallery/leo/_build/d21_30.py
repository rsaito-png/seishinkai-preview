# -*- coding: utf-8 -*-
"""Designs 21–30."""

DESIGNS = []

DESIGNS.append({
"n": 21,
"name": "朝の道場",
"aim": "稽古の写真を斜めに断ち、白い床の広さを残す",
"swatch": "#eceae6",
"ink": "#1c1a17",
"thumb": "karate_class.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;700;900&display=swap",
"body": r"""
<article class="dojo">
<a class="back" href="../">一覧</a>
<section class="slash">
<img src="$u_karate" alt="武道の稽古">
<div class="banner">
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</div>
</section>
<section class="floor">
<p>$move</p>
<p>$daily</p>
<p>$group</p>
<p>$time</p>
</section>
<section class="slash low">
<img src="$u_blocks" alt="積み木">
<p class="over">$toy</p>
</section>
<section class="floor">
<p>$agey</p>
<p>$age</p>
<p>$dev</p>
<p>$target</p>
<p>$bus</p>
<p>$lunch</p>
<p>$lunch2</p>
<h2>$event_h</h2>
<p>$event</p>
</section>
<section class="slash low">
<img src="$u_forest" alt="フィールドの木々と作業">
</section>
<section class="floor dark">
<h2>$fam_h</h2>
<p>$kato</p>
<p>$door</p>
<p class="place">$place</p>
<p>$walk</p>
<p>$car</p>
<p>$bus2</p>
<p>$fee</p>
<p class="evalh">$eval_h</p>
<p class="evals">$evals</p>
<p>$pt_a　$pt_s</p>
<p>$as_a　$as_s</p>
<h2>$visit_h</h2>
<p><a href="$url_line">LINE</a></p>
<p><a href="$tel_href">$tel</a></p>
</section>
</article>
""",
"css": r"""
:root{--focus:#c2410c}
body{background:#eceae6;color:#1c1a17;font-family:"Zen Kaku Gothic New",sans-serif;line-height:1.8}
.back{position:absolute;z-index:3;top:.8rem;left:.8rem;background:#fff;color:#1c1a17;text-decoration:none;padding:.25rem .6rem}
.slash{position:relative;background:#1c1a17;clip-path:polygon(0 0,100% 0,100% 86%,0 100%)}
.slash img{width:100%;height:100svh;object-fit:cover;object-position:50% 40%}
.banner{position:absolute;left:0;bottom:12vh;background:#9a3412;color:#fffaf6;padding:1rem 1.4rem 1.2rem;max-width:min(32rem,90vw)}
h1{font-weight:900;font-size:clamp(3.6rem,10vw,7rem);line-height:.9;margin:0}
.lead{font-size:clamp(1.2rem,2.6vw,1.7rem);margin:.4rem 0 0}
.floor{padding:8vh 10vw;max-width:48rem}
.floor.dark{background:#1c1a17;color:#f6f3ee;max-width:none}
.slash.low{clip-path:polygon(0 8%,100% 0,100% 100%,0 92%);margin-top:-4vh}
.slash.low img{height:74vh}
.over{position:absolute;right:6vw;bottom:10vh;background:#fff;color:#1c1a17;padding:.8rem 1rem;max-width:min(24rem,80vw)}
.place{font-size:clamp(1.4rem,3vw,2rem);font-weight:700}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.3rem .7rem .3rem 0}
h2{font-size:1.5rem}
"""
})

DESIGNS.append({
"n": 22,
"name": "季節の便り",
"aim": "花と山道の写真を、手紙の紙に挟んで少し傾ける",
"swatch": "#e7f0f4",
"ink": "#1d3340",
"thumb": "rainbow.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Klee+One:wght@400;600&display=swap",
"body": r"""
<article class="tegami">
<a class="back" href="../">一覧</a>
<header>
<p class="to">保護者のみなさまへ</p>
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</header>
<figure class="tuck a"><img src="$u_rainbow" alt="山へ続く道"></figure>
<p>$daily</p>
<p>$group</p>
<p>$agey</p>
<p>$dev</p>
<p>$bus</p>
<figure class="tuck b"><img src="$u_zinnia" alt="建物のそばのジニア"></figure>
<p>$toy</p>
<p>$move</p>
<p>$lunch</p>
<h2>$event_h</h2>
<p>$event</p>
<figure class="tuck c"><img src="$u_shichi" alt="行事・七輪"></figure>
<figure class="tuck d"><img src="$u_mari" alt="庭のマリーゴールド"></figure>
<h2>$fam_h</h2>
<p>$kato</p>
<p>$door</p>
<p class="place">$place</p>
<p>$walk</p>
<p>$car</p>
<p>$target</p>
<p>$age</p>
<p>$time</p>
<p>$lunch2</p>
<p>$bus2</p>
<p>$fee</p>
<p class="evalh">$eval_h</p>
<p class="evals">$evals</p>
<p>$pt_a　$pt_s</p>
<p>$as_a　$as_s</p>
<section class="sign">
<h2>$visit_h</h2>
<p><a href="$url_line">LINE</a></p>
<p><a href="$tel_href">$tel</a></p>
</section>
</article>
""",
"css": r"""
:root{--focus:#b45309}
body{background:#d5e3ea;color:#1d3340;font-family:"Klee One",sans-serif}
.tegami{width:min(760px,100%);margin:4vh auto;background:#f4f8fa;padding:8vh 8vw 4rem;font-size:1.12rem;line-height:1.9}
.back{color:#1d3340}
.to{margin:0}
h1{font-size:clamp(3rem,8vw,4.8rem);font-weight:600;margin:.2rem 0}
.lead{font-size:clamp(1.25rem,2.6vw,1.7rem)}
.tuck{margin:1.2rem 0}
.tuck img{width:min(100%,460px);height:auto}
.tuck.a{transform:rotate(-2deg)}
.tuck.b{transform:rotate(2.2deg);margin-left:12%}
.tuck.c{transform:rotate(-1deg)}
.tuck.d{width:min(70%,320px);transform:rotate(3deg);margin-left:20%}
.place{font-size:1.4rem}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.25rem .6rem .25rem 0}
.sign h2{font-size:1.8rem}
@media(max-width:700px){.tuck.b,.tuck.d{margin-left:0}}
"""
})

DESIGNS.append({
"n": 23,
"name": "字が建物",
"aim": "「レオ」の字の中に写真を透かし、文字そのものを部屋にする",
"swatch": "#161616",
"ink": "#f2f2ef",
"thumb": "panda.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Kaisei+Tokumin:wght@400;700;800&display=swap",
"body": r"""
<article class="glyph">
<a class="back" href="../">一覧</a>
<header>
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</header>
<section class="copy">
<p>$daily</p>
<p>$group</p>
<p>$toy</p>
<img src="$u_blocks" alt="積み木">
<p>$move</p>
<p>$lunch</p>
<p>$agey</p>
<p>$dev</p>
<p>$bus</p>
<h2>$event_h</h2>
<p>$event</p>
<img src="$u_shichi" alt="行事・七輪">
<h2>$fam_h</h2>
<p>$kato</p>
<p>$door</p>
<img src="$u_ext" alt="レオの建物">
<p class="place">$place</p>
<p>$walk</p>
<p>$car</p>
<p>$target</p>
<p>$age</p>
<p>$time</p>
<p>$lunch2</p>
<p>$bus2</p>
<p>$fee</p>
<p class="evalh">$eval_h</p>
<p class="evals">$evals</p>
<p>$pt_a　$pt_s</p>
<p>$as_a　$as_s</p>
<h2>$visit_h</h2>
<p><a href="$url_line">LINE</a></p>
<p><a href="$tel_href">$tel</a></p>
</section>
</article>
""",
"css": r"""
:root{--focus:#f5b942}
body{background:#f2f2ef;color:#161616;font-family:"Kaisei Tokumin",serif;line-height:1.85}
.back{position:absolute;z-index:2;top:.7rem;right:.8rem;color:#161616}
header{padding:4vh 4vw 0}
h1{margin:0;font-weight:800;font-size:clamp(7rem,34vw,20rem);line-height:.78;letter-spacing:-.06em;color:#161616}
@supports ((-webkit-background-clip:text) or (background-clip:text)){
h1{background:url(../../../img/panda.jpg) center 60%/cover no-repeat;-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent}
}
.role{margin:0 0 -.5rem;font-size:1.05rem;color:#161616}
.lead{color:#161616;font-size:clamp(1.3rem,3vw,2rem);margin:0 0 1rem;max-width:16em}
.copy{width:min(40rem,88vw);margin:0 auto 2rem;font-size:1.12rem;padding-bottom:2rem}
.copy img{width:100%;height:auto;margin:1rem 0}
.place{font-size:1.6rem}
a{text-decoration:underline;text-underline-offset:.18em;color:#161616}
.evals a{display:inline-block;margin:.3rem .7rem .3rem 0}
h2{font-size:1.5rem}
"""
})

DESIGNS.append({
"n": 24,
"name": "掌の物語",
"aim": "一章が画面ひとつ。次の言葉は、親指の届く下のほうに置く",
"swatch": "#12324a",
"ink": "#f3f7fb",
"thumb": "toyshelf.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Zen+Kurenaido&display=swap",
"body": r"""
<article class="palm">
<a class="back" href="../">一覧</a>
<section class="ch c1">
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
<img src="$u_panda" alt="おもちゃの棚と、床に座るパンダのぬいぐるみ">
</section>
<section class="ch c2">
<p>$daily</p>
<p>$group</p>
<p>$time</p>
<img src="$u_toys" alt="おもちゃの部屋">
<p>$toy</p>
</section>
<section class="ch c3">
<p>$move</p>
<img src="$u_karate" alt="武道の稽古">
<p>$agey</p>
<p>$age</p>
<p>$dev</p>
<p>$target</p>
</section>
<section class="ch c4">
<p>$lunch</p>
<p>$lunch2</p>
<img src="$u_meal" alt="手作りの和定食">
<p>$bus</p>
<p>$bus2</p>
</section>
<section class="ch c5">
<h2>$event_h</h2>
<p>$event</p>
<img src="$u_shichi" alt="行事・七輪">
</section>
<section class="ch c6">
<h2>$fam_h</h2>
<p>$kato</p>
<p>$door</p>
<img src="$u_ext" alt="レオの建物">
<p class="place">$place</p>
<p>$walk</p>
<p>$car</p>
<p>$fee</p>
<p class="evalh">$eval_h</p>
<p class="evals">$evals</p>
<p>$pt_a　$pt_s</p>
<p>$as_a　$as_s</p>
<h2>$visit_h</h2>
<p><a href="$url_line">LINE</a></p>
<p><a class="tel" href="$tel_href">$tel</a></p>
</section>
</article>
""",
"css": r"""
:root{--focus:#ffe08a}
body{margin:0;font-family:"Zen Kurenaido",sans-serif;color:#102033;line-height:1.7}
.back{position:fixed;z-index:4;top:.5rem;right:.5rem;background:#fff;color:#102033;text-decoration:none;padding:.25rem .55rem}
.ch{min-height:100svh;padding:12vh 7vw 18vh;display:flex;flex-direction:column;justify-content:flex-end;font-size:clamp(1.25rem,3.4vw,1.7rem)}
.ch img{width:100%;height:34vh;object-fit:cover;margin:.8rem 0;order:-1}
.c1{background:#12324a;color:#f3f7fb}
.c2{background:#e7f2ea;color:#143028}
.c3{background:#f3e6d4;color:#2a1c10}
.c4{background:#f7f1e4;color:#3a1416}
.c5{background:#1d3a2a;color:#e7f2ea}
.c6{background:#102033;color:#f3f7fb}
h1{font-size:clamp(4rem,16vw,7rem);margin:0;line-height:.9}
.lead{font-size:clamp(1.4rem,4vw,2rem)}
.place{font-size:clamp(1.3rem,3.5vw,1.8rem)}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.25rem .6rem .25rem 0;font-size:1rem}
.tel{font-size:clamp(1.6rem,5vw,2.2rem)}
h2{font-size:1.6rem;margin:0}
"""
})

DESIGNS.append({
"n": 25,
"name": "道順だけ",
"aim": "地図は描かず、歩く時間と地名だけを道路標示のように大きく置く",
"swatch": "#2b2b2b",
"ink": "#f6f3ea",
"thumb": "rainbow.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Kosugi&display=swap",
"body": r"""
<article class="way">
<a class="back" href="../">一覧</a>
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
<p class="huge">$walk</p>
<img src="$u_station" alt="三岐線の駅">
<p class="huge">$place</p>
<p class="sub">$car</p>
<img src="$u_rainbow" alt="山へ続く道">
<p>$door</p>
<img src="$u_ext" alt="レオの建物">
<section class="rest">
<p>$daily</p>
<p>$group</p>
<p>$time</p>
<p>$toy</p>
<p>$move</p>
<p>$lunch</p>
<p>$lunch2</p>
<p>$agey</p>
<p>$age</p>
<p>$dev</p>
<p>$target</p>
<p>$bus</p>
<p>$bus2</p>
<p>$fee</p>
<h2>$event_h</h2>
<p>$event</p>
<h2>$fam_h</h2>
<p>$kato</p>
<p class="evalh">$eval_h</p>
<p class="evals">$evals</p>
<p>$pt_a　$pt_s</p>
<p>$as_a　$as_s</p>
<h2>$visit_h</h2>
<p><a href="$url_line">LINE</a></p>
<p><a href="$tel_href">$tel</a></p>
</section>
</article>
""",
"css": r"""
:root{--focus:#fff4c2}
body{background:#2b2b2b;color:#f6f3ea;font-family:Kosugi,sans-serif;line-height:1.7}
.way{padding:8vh 8vw 2rem 3rem;border-left:16px solid #f0c419}
.back{color:#f6f3ea}
h1{font-size:clamp(3rem,10vw,6rem);margin:.2rem 0}
.huge{font-size:clamp(2rem,6vw,3.6rem);line-height:1.25;margin:1rem 0;color:#f0c419}
.lead{font-size:clamp(1.2rem,3vw,1.7rem);max-width:16em}
.way img{width:100%;max-height:70vh;object-fit:cover;margin:1rem 0}
.rest{max-width:40rem;color:#f6f3ea;font-size:1.08rem}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.3rem .7rem .3rem 0}
h2{font-size:1.4rem;color:#f0c419}
"""
})

DESIGNS.append({
"n": 26,
"name": "一輪の間",
"aim": "白い部屋の中央に花を一輪。説明は端に細い縦の文",
"swatch": "#f7f7f5",
"ink": "#222",
"thumb": "marigold.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Hina+Mincho&display=swap",
"body": r"""
<article class="ma">
<a class="back" href="../">一覧</a>
<aside class="edge">
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</aside>
<figure class="flower">
<img src="$u_zinnia" alt="建物のそばのジニア">
</figure>
</article>
<section class="rest">
<p>$daily</p>
<p>$group</p>
<p>$toy</p>
<p>$move</p>
<p>$lunch</p>
<p>$agey</p>
<p>$dev</p>
<p>$bus</p>
<h2>$event_h</h2>
<p>$event</p>
<h2>$fam_h</h2>
<p>$kato</p>
<p>$door</p>
<p class="place">$place</p>
<p>$walk</p>
<p>$car</p>
<p>$target</p>
<p>$age</p>
<p>$time</p>
<p>$lunch2</p>
<p>$bus2</p>
<p>$fee</p>
<p class="evalh">$eval_h</p>
<p class="evals">$evals</p>
<p>$pt_a　$pt_s</p>
<p>$as_a　$as_s</p>
<h2>$visit_h</h2>
<p><a href="$url_line">LINE</a></p>
<p><a href="$tel_href">$tel</a></p>
</section>
""",
"css": r"""
:root{--focus:#b45309}
body{background:#f7f7f5;color:#222;font-family:"Hina Mincho",serif}
.back{position:absolute;top:.6rem;left:.6rem;z-index:2}
.ma{display:flex;min-height:100svh}
.edge{width:min(22vw,12rem);padding:12vh 1rem;font-size:1.15rem;line-height:2;writing-mode:vertical-rl;height:100svh}
h1{font-size:2.6rem;margin:.4rem 0;font-weight:400}
.flower{flex:1;display:flex;align-items:center;justify-content:center}
.flower img{width:min(52vh,480px);height:auto}
.rest{width:min(40rem,88vw);margin:0 auto;padding:1rem 0 3rem;font-size:1.08rem;line-height:1.9}
.place{font-size:1.45rem}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.3rem .7rem .3rem 0}
@media(max-width:760px){
  .ma{flex-direction:column}
  .edge{writing-mode:horizontal-tb;width:100%;height:auto;overflow:visible;padding:5rem 6vw 2rem}
  .flower{padding:1rem 0 3rem}
  .flower img{width:min(80vw,420px)}
}
"""
})

DESIGNS.append({
"n": 27,
"name": "章扉",
"aim": "布張りの本。章が変わるたび、扉絵が画面いっぱいに開く",
"swatch": "#243e36",
"ink": "#f4f1e6",
"thumb": "forest_work.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Sawarabi+Mincho&display=swap",
"body": r"""
<article class="book">
<a class="back" href="../">一覧</a>
<section class="doorcloth">
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</section>
<section class="opener">
<img src="$u_toys" alt="おもちゃの部屋">
<h2>おもちゃ</h2>
</section>
<section class="page">
<p>$daily</p>
<p>$toy</p>
<p>$agey</p>
<p>$dev</p>
</section>
<section class="opener">
<img src="$u_karate" alt="武道の稽古">
<h2>からだ</h2>
</section>
<section class="page">
<p>$move</p>
<p>$group</p>
<p>$time</p>
<p>$bus</p>
<p>$bus2</p>
</section>
<section class="opener">
<img src="$u_meal" alt="手作りの和定食">
<h2>昼</h2>
</section>
<section class="page">
<p>$lunch</p>
<p>$lunch2</p>
</section>
<section class="opener">
<img src="$u_shichi" alt="行事・七輪">
<h2>$event_h</h2>
</section>
<section class="page">
<p>$event</p>
<p>$target</p>
<p>$age</p>
</section>
<section class="opener">
<img src="$u_ext" alt="レオの建物">
<h2>$fam_h</h2>
</section>
<section class="page last">
<p>$kato</p>
<p>$door</p>
<p class="place">$place</p>
<p>$walk</p>
<p>$car</p>
<p>$fee</p>
<p class="evalh">$eval_h</p>
<p class="evals">$evals</p>
<p>$pt_a　$pt_s</p>
<p>$as_a　$as_s</p>
<h2>$visit_h</h2>
<p><a href="$url_line">LINE</a></p>
<p><a href="$tel_href">$tel</a></p>
</section>
</article>
""",
"css": r"""
:root{--focus:#e2b657}
body{background:#eef2f6;color:#1c2830;font-family:"Sawarabi Mincho",serif;line-height:1.9}
.back{position:absolute;z-index:2;top:.8rem;left:.8rem;color:#f4f1e6}
.doorcloth{min-height:100svh;background:#243e36;color:#f4f1e6;display:flex;flex-direction:column;justify-content:center;padding:10vh 8vw}
h1{font-size:clamp(4rem,12vw,8rem);margin:.2rem 0;font-weight:400;letter-spacing:.18em}
.lead{font-size:clamp(1.3rem,3vw,1.9rem);max-width:14em}
.opener{position:relative;min-height:100svh;background:#111}
.opener img{width:100%;height:100svh;object-fit:cover}
.opener h2{position:absolute;left:6vw;bottom:8vh;margin:0;color:#fff;font-size:clamp(2rem,6vw,4rem);font-weight:400;text-shadow:0 2px 16px rgba(0,0,0,.45)}
.page{padding:10vh 10vw;font-size:1.15rem;max-width:46rem}
.page.last{background:#243e36;color:#f4f1e6;max-width:none}
.place{font-size:1.5rem}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.3rem .7rem .3rem 0}
.page h2{font-size:2rem}
"""
})

DESIGNS.append({
"n": 28,
"name": "長い影",
"aim": "夕方の光。文字は写真の下に伸びる影の中へ沈める",
"swatch": "#1f2430",
"ink": "#f6efe6",
"thumb": "child_shichirin.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap",
"body": r"""
<article class="dusk">
<a class="back" href="../">一覧</a>
<section class="low">
<img src="$u_shichi" alt="行事・七輪">
<div class="shadow">
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
<p>$event_h $event</p>
</div>
</section>
<section class="low">
<img src="$u_rainbow" alt="山へ続く道">
<div class="shadow">
<p>$move</p>
<p>$daily</p>
</div>
</section>
<section class="low">
<img src="$u_ext" alt="レオの建物">
<div class="shadow">
<h2>$fam_h</h2>
<p>$kato</p>
<p>$door</p>
<p class="place">$place</p>
<p>$walk</p>
<p>$car</p>
</div>
</section>
<section class="after">
<p>$group</p>
<p>$time</p>
<p>$toy</p>
<p>$lunch</p>
<p>$lunch2</p>
<p>$agey</p>
<p>$age</p>
<p>$dev</p>
<p>$target</p>
<p>$bus</p>
<p>$bus2</p>
<p>$fee</p>
<p class="evalh">$eval_h</p>
<p class="evals">$evals</p>
<p>$pt_a　$pt_s</p>
<p>$as_a　$as_s</p>
<h2>$visit_h</h2>
<p><a href="$url_line">LINE</a></p>
<p><a href="$tel_href">$tel</a></p>
</section>
</article>
""",
"css": r"""
:root{--focus:#ffbf47}
body{background:#1f2430;color:#f6efe6;font-family:"Noto Sans JP",sans-serif;line-height:1.8}
.back{position:absolute;z-index:3;top:.7rem;left:.7rem;color:#f6efe6}
.low{position:relative;min-height:100svh;background:#1f2430}
.low img{width:100%;height:100svh;object-fit:cover}
.shadow{position:absolute;left:0;right:0;bottom:0;padding:18vh 7vw 8vh;background:linear-gradient(transparent,rgba(20,16,12,.2) 18%,rgba(20,16,12,.88))}
h1{font-size:clamp(3.6rem,10vw,7rem);margin:0;font-weight:700;letter-spacing:.08em}
.lead{font-size:clamp(1.2rem,2.8vw,1.7rem);max-width:18em}
.place{font-size:clamp(1.3rem,3vw,1.8rem)}
.after{padding:8vh 8vw;max-width:42rem}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.3rem .7rem .3rem 0}
h2{font-size:1.5rem}
"""
})

DESIGNS.append({
"n": 29,
"name": "ことばの川",
"aim": "文章が丸い写真を石のように避けて、川の水みたいに回りこむ",
"swatch": "#d5e6ea",
"ink": "#0c3a4a",
"thumb": "blocks.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Yusei+Magic&display=swap",
"body": r"""
<article class="river">
<a class="back" href="../">一覧</a>
<header>
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</header>
<img class="stone" src="$u_blocks" alt="積み木">
<p>$daily</p>
<p>$toy</p>
<p>$group</p>
<img class="stone left" src="$u_panda" alt="おもちゃの棚と、床に座るパンダのぬいぐるみ">
<p>$move</p>
<p>$agey</p>
<p>$dev</p>
<p>$bus</p>
<img class="stone" src="$u_meal" alt="手作りの和定食">
<p>$lunch</p>
<p>$lunch2</p>
<p>$time</p>
<img class="stone left" src="$u_forest" alt="フィールドの木々と作業">
<h2>$event_h</h2>
<p>$event</p>
<p>$target</p>
<p>$age</p>
<h2>$fam_h</h2>
<p>$kato</p>
<p>$door</p>
<p class="place">$place</p>
<p>$walk</p>
<p>$car</p>
<p>$bus2</p>
<p>$fee</p>
<p class="evalh">$eval_h</p>
<p class="evals">$evals</p>
<p>$pt_a　$pt_s</p>
<p>$as_a　$as_s</p>
<h2>$visit_h</h2>
<p><a href="$url_line">LINE</a></p>
<p><a href="$tel_href">$tel</a></p>
</article>
""",
"css": r"""
:root{--focus:#b45309}
body{background:#d5e6ea;color:#0c3a4a;font-family:"Yusei Magic",sans-serif}
.river{padding:6vh 6vw 3rem;font-size:1.18rem;line-height:2.05}
.back{color:#0c3a4a}
h1{font-size:clamp(3.4rem,9vw,6rem);margin:.1rem 0;font-weight:400}
.lead{font-size:clamp(1.25rem,2.8vw,1.8rem);max-width:16em}
.stone{float:right;width:min(42vw,380px);height:min(42vw,380px);object-fit:cover;border-radius:50%;shape-outside:circle(50%);margin:0 0 1rem 1.4rem}
.stone.left{float:left;margin:0 1.4rem 1rem 0}
.place{font-size:1.5rem;clear:both}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.3rem .7rem .3rem 0}
h2{font-size:1.5rem;clear:both}
.river::after{content:"";display:block;clear:both}
@media(max-width:700px){
  .stone,.stone.left{float:none;display:block;width:min(70vw,320px);height:min(70vw,320px);margin:1rem auto}
}
"""
})

DESIGNS.append({
"n": 30,
"name": "星から二階へ",
"aim": "夜の星から始まり、明るいおもちゃ部屋と二階のドアで朝になる",
"swatch": "#0c1220",
"ink": "#f4f7fb",
"thumb": "leo_ext.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Yuji+Mai&display=swap",
"body": r"""
<article class="night">
<a class="back" href="../">一覧</a>
<section class="sky">
<p class="org">星心会</p>
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</section>
<section class="day">
<img src="$u_panda" alt="おもちゃの棚と、床に座るパンダのぬいぐるみ">
<div>
<p>$daily</p>
<p>$toy</p>
<p>$group</p>
<p>$agey</p>
<p>$dev</p>
<p>$bus</p>
</div>
</section>
<section class="day reverse">
<div>
<p>$move</p>
<p>$lunch</p>
<h2>$event_h</h2>
<p>$event</p>
</div>
<img src="$u_shichi" alt="行事・七輪">
</section>
<section class="day">
<img src="$u_blocks" alt="積み木">
<div>
<p>$time</p>
<p>$lunch2</p>
<p>$target</p>
<p>$age</p>
</div>
</section>
<section class="arrival">
<img src="$u_ext" alt="レオの建物">
<div class="card">
<h2>$fam_h</h2>
<p>$kato</p>
<p>$door</p>
<p class="place">$place</p>
<p>$walk</p>
<p>$car</p>
<p>$bus2</p>
<p>$fee</p>
<p class="evalh">$eval_h</p>
<p class="evals">$evals</p>
<p>$pt_a　$pt_s</p>
<p>$as_a　$as_s</p>
<h2>$visit_h</h2>
<p><a href="$url_line">LINE</a></p>
<p><a href="$tel_href">$tel</a></p>
</div>
</section>
</article>
""",
"css": r"""
:root{--focus:#e2b657}
body{background:#0c1220;color:#f4f7fb;font-family:"Yuji Mai",serif;line-height:1.9}
.back{position:absolute;z-index:3;top:.8rem;right:.8rem;color:#f4f7fb}
.sky{min-height:100svh;display:flex;flex-direction:column;justify-content:center;padding:10vh 8vw;
background:
radial-gradient(1.6px 1.6px at 12% 22%, #f0e2c0 50%, transparent 52%),
radial-gradient(1.4px 1.4px at 28% 68%, #f0e2c0 50%, transparent 52%),
radial-gradient(1.8px 1.8px at 47% 18%, #fff 45%, transparent 50%),
radial-gradient(1.3px 1.3px at 63% 42%, #f0e2c0 50%, transparent 52%),
radial-gradient(1.5px 1.5px at 78% 26%, #f0e2c0 50%, transparent 52%),
radial-gradient(1.2px 1.2px at 86% 74%, #fff 45%, transparent 50%),
radial-gradient(1.7px 1.7px at 18% 84%, #f0e2c0 50%, transparent 52%),
radial-gradient(1.1px 1.1px at 54% 78%, #f0e2c0 50%, transparent 52%),
#0c1220}
.org{letter-spacing:.28em;margin:0}
h1{font-size:clamp(4rem,12vw,8rem);margin:.2rem 0;font-weight:400;letter-spacing:.2em}
.lead{font-size:clamp(1.25rem,3vw,1.8rem);max-width:16em}
.day{display:flex;background:#f4f7fb;color:#102033;min-height:80vh}
.day img{width:54%;object-fit:cover}
.day div{width:46%;padding:6vh 4vw;display:flex;flex-direction:column;justify-content:center}
.day.reverse{flex-direction:row-reverse}
.arrival{position:relative}
.arrival img{width:100%;height:100svh;object-fit:cover}
.card{position:absolute;right:5vw;bottom:6vh;background:rgba(244,247,251,.94);color:#102033;padding:1.2rem 1.3rem;max-width:min(34rem,88vw)}
.place{font-size:1.3rem}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.25rem .6rem .25rem 0}
h2{font-size:1.35rem;margin:.2rem 0}
@media(max-width:760px){
  .day,.day.reverse{flex-direction:column}
  .day img,.day div{width:100%}
  .day img{height:56vw}
  .card{position:relative;right:auto;bottom:auto;max-width:none}
}
"""
})
