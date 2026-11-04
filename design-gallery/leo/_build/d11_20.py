# -*- coding: utf-8 -*-
"""Designs 11–20."""

DESIGNS = []

DESIGNS.append({
"n": 11,
"name": "立面図",
"aim": "建物の写真を立面に見立て、寸法の線は一本だけ添える",
"swatch": "#d5e4ee",
"ink": "#10283a",
"thumb": "leo_ext.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=BIZ+UDPGothic:wght@400;700&display=swap",
"body": r"""
<article class="elev">
<a class="back" href="../">一覧</a>
<header class="sheet">
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</header>
<figure class="front">
<img src="$u_ext" alt="レオの建物">
<svg class="dim" viewBox="0 0 800 36" aria-hidden="true"><line x1="8" y1="18" x2="792" y2="18"/><line x1="8" y1="8" x2="8" y2="28"/><line x1="792" y1="8" x2="792" y2="28"/></svg>
<figcaption>$place</figcaption>
</figure>
<section class="notes">
<p>$door</p>
<p>$walk</p>
<p>$car</p>
<p>$daily</p>
<p>$group</p>
<p>$time</p>
<p>$agey</p>
<p>$age</p>
<p>$dev</p>
<p>$target</p>
<p>$bus</p>
<p>$bus2</p>
</section>
<figure class="inset"><img src="$u_panda" alt="おもちゃの棚と、床に座るパンダのぬいぐるみ"><figcaption>$toy</figcaption></figure>
<section class="notes">
<p>$move</p>
<h2>$event_h</h2>
<p>$event</p>
<p>$lunch</p>
<p>$lunch2</p>
<p>$fee</p>
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
:root{--focus:#c2410c}
body{background:#d5e4ee;color:#10283a;font-family:"BIZ UDPGothic",sans-serif;font-size:1.05rem;line-height:1.75}
.elev{padding:4vh 5vw 2rem}
.back{color:#10283a}
h1{font-weight:700;font-size:clamp(3rem,8vw,5.5rem);letter-spacing:.14em;margin:.2rem 0}
.lead{font-size:clamp(1.2rem,2.4vw,1.6rem);max-width:24em}
.front img{width:100%;max-height:78vh;object-fit:cover;object-position:50% 40%}
.dim{width:100%;height:28px;stroke:#10283a;fill:none;stroke-width:1.5}
.front figcaption{font-size:clamp(1.3rem,3vw,1.9rem);margin-top:.3rem}
.notes{max-width:42rem;margin:1.5rem 0}
.inset{width:min(100%,640px);margin:1rem 0 1rem auto}
.inset img{width:100%;height:auto}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.3rem .7rem .3rem 0}
h2{font-size:1.35rem;margin:1rem 0 .3rem}
"""
})

DESIGNS.append({
"n": 12,
"name": "丸い窓",
"aim": "円い窓の向こうに部屋を見せ、余白は松の緑と白い壁",
"swatch": "#f3f6f2",
"ink": "#1e3a2f",
"thumb": "panda.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=M+PLUS+2:wght@400;600;800&display=swap",
"body": r"""
<article class="window">
<a class="back" href="../">一覧</a>
<section class="top">
<div class="round"><img src="$u_panda" alt="おもちゃの棚と、床に座るパンダのぬいぐるみ"></div>
<div class="side">
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
<p>$daily</p>
</div>
</section>
<section class="quiet">
<p>$group</p>
<p>$agey</p>
<p>$dev</p>
<p>$bus</p>
<p>$toy</p>
</section>
<section class="pair">
<img src="$u_blocks" alt="積み木">
<p>$move</p>
</section>
<section class="quiet">
<p>$lunch</p>
<h2>$event_h</h2>
<p>$event</p>
</section>
<section class="pair rev">
<img src="$u_zinnia" alt="建物のそばのジニア">
<div>
<h2>$fam_h</h2>
<p>$kato</p>
<p>$door</p>
<p class="place">$place</p>
<p>$walk</p>
<p>$car</p>
</div>
</section>
<section class="quiet">
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
:root{--focus:#b45309}
body{background:#f3f6f2;color:#1e3a2f;font-family:"M PLUS 2",sans-serif;font-size:1.08rem;line-height:1.85}
.back{position:absolute;top:1rem;left:1rem;color:#1e3a2f}
.top{display:flex;align-items:center;gap:6vw;min-height:100svh;padding:8vh 6vw}
.round{width:min(46vw,520px);aspect-ratio:1;border-radius:50%;overflow:hidden;flex:none;background:#1e3a2f}
.round img{width:100%;height:100%;object-fit:cover;object-position:50% 70%}
h1{font-weight:800;font-size:clamp(3.4rem,7vw,6rem);margin:.1rem 0;letter-spacing:.08em}
.lead{font-size:clamp(1.25rem,2.4vw,1.7rem)}
.quiet{width:min(38rem,86vw);margin:0 auto;padding:6vh 0}
.pair{display:flex;align-items:center;gap:4vw;padding:4vh 8vw}
.pair img{width:42%;height:360px;object-fit:cover;border-radius:50% 50% 0 0}
.pair.rev{flex-direction:row-reverse}
.place{font-size:1.45rem;font-weight:600}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.3rem .7rem .3rem 0}
h2{font-size:1.5rem}
@media(max-width:760px){
  .top,.pair,.pair.rev{flex-direction:column}
  .round{width:min(78vw,420px)}
  .pair img{width:100%;height:240px}
}
"""
})

DESIGNS.append({
"n": 13,
"name": "昼の膳",
"aim": "和定食の俯瞰を主役にし、朱の卓の色でページを染める",
"swatch": "#6e1d22",
"ink": "#fff6ee",
"thumb": "homemeal.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Shippori+Mincho+B1:wght@400;700;800&display=swap",
"body": r"""
<article class="zen">
<a class="back" href="../">一覧</a>
<section class="table">
<img src="$u_meal" alt="手作りの和定食">
<div class="cap">
<p class="role">$role</p>
<h1>レオ</h1>
<p>$lunch</p>
</div>
</section>
<section class="lacquer">
<p class="lead">$lead</p>
<p>$daily</p>
<p>$group</p>
<p>$agey</p>
<p>$dev</p>
<p>$bus</p>
<p>$lunch2</p>
</section>
<section class="beside">
<img src="$u_toys" alt="おもちゃの部屋">
<p>$toy</p>
</section>
<section class="lacquer deep">
<p>$move</p>
<h2>$event_h</h2>
<p>$event</p>
<img src="$u_shichi" alt="行事・七輪">
</section>
<section class="beside">
<div>
<h2>$fam_h</h2>
<p>$kato</p>
<p>$door</p>
</div>
<img src="$u_ext" alt="レオの建物">
</section>
<section class="lacquer">
<p class="place">$place</p>
<p>$walk</p>
<p>$car</p>
<p>$target</p>
<p>$age</p>
<p>$time</p>
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
:root{--focus:#ffe08a}
body{background:#f6efe8;color:#3a1416;font-family:"Shippori Mincho B1",serif;line-height:1.9}
.back{position:absolute;z-index:3;top:.8rem;left:.8rem;background:#fff6ee;color:#6e1d22;text-decoration:none;padding:.3rem .6rem}
.table{position:relative;min-height:100svh;background:#3a1416}
.table img{width:100%;height:100svh;object-fit:cover}
.cap{position:absolute;right:0;top:0;bottom:0;width:min(42vw,460px);background:rgba(110,29,34,.9);color:#fff6ee;display:flex;flex-direction:column;justify-content:flex-end;padding:8vh 1.6rem}
h1{font-size:clamp(3.4rem,7vw,5.5rem);margin:.2rem 0;font-weight:800;letter-spacing:.12em}
.lacquer{background:#6e1d22;color:#fff6ee;padding:8vh 10vw}
.deep{background:#4a1418}
.lead{font-size:clamp(1.4rem,3vw,2rem)}
.beside{display:flex;align-items:center;background:#f6efe8;color:#3a1416}
.beside img{width:56%;height:70vh;object-fit:cover}
.beside > p,.beside > div{width:44%;padding:2rem}
.place{font-size:clamp(1.5rem,3vw,2.1rem)}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.35rem .8rem .35rem 0}
h2{font-size:1.6rem}
.lacquer img{width:min(100%,720px);margin-top:1rem;height:auto}
@media(max-width:760px){
  .cap{position:relative;width:100%;background:#6e1d22}
  .table img{height:70vh}
  .beside{flex-direction:column}
  .beside > img,.beside > p,.beside > div{width:100%}
  .beside img{height:52vw}
}
"""
})

DESIGNS.append({
"n": 14,
"name": "森の徒歩",
"aim": "森の写真と文章を左右に振り、緑の中を歩いて読む",
"swatch": "#10241c",
"ink": "#e4efd8",
"thumb": "forest_work.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Kiwi+Maru:wght@400;500&display=swap",
"body": r"""
<article class="walk">
<a class="back" href="../">一覧</a>
<section class="step right">
<img src="$u_forest" alt="フィールドの木々と作業">
<div>
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</div>
</section>
<section class="step left">
<div>
<p>$daily</p>
<p>$group</p>
<p>$agey</p>
<p>$dev</p>
<p>$bus</p>
</div>
<img src="$u_rainbow" alt="山へ続く道">
</section>
<section class="step right">
<img src="$u_shichi" alt="行事・七輪">
<div>
<h2>$event_h</h2>
<p>$event</p>
<p>$move</p>
</div>
</section>
<section class="step left">
<div>
<p>$toy</p>
<p>$lunch</p>
</div>
<img src="$u_mari" alt="庭のマリーゴールド">
</section>
<section class="step right">
<img src="$u_ext" alt="レオの建物">
<div>
<h2>$fam_h</h2>
<p>$kato</p>
<p>$door</p>
<p class="place">$place</p>
<p>$walk</p>
<p>$car</p>
</div>
</section>
<section class="ground">
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
:root{--focus:#f2c14e}
body{background:#10241c;color:#e4efd8;font-family:"Kiwi Maru",serif;line-height:1.9}
.back{position:absolute;z-index:2;top:.7rem;left:.7rem;color:#e4efd8}
.step{display:flex;align-items:stretch;min-height:88vh}
.step img{flex:0 0 56%;width:56%;min-width:0;object-fit:cover;min-height:70vh}
.step div{flex:1;min-width:0;padding:8vh 4vw;display:flex;flex-direction:column;justify-content:center}
h1{font-size:clamp(3.2rem,7vw,5.5rem);margin:.2rem 0;font-weight:500}
.lead{font-size:clamp(1.25rem,2.6vw,1.7rem)}
.place{font-size:1.45rem}
.ground{padding:8vh 10vw;background:#1a3a2c}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.3rem .7rem .3rem 0}
h2{font-size:1.5rem}
@media(max-width:760px){
  .step{flex-direction:column;min-height:0}
  .step.left{flex-direction:column-reverse}
  .step img,.step div{flex-basis:auto;width:100%;margin:0}
  .step img{min-height:0;height:64vw}
}
"""
})

DESIGNS.append({
"n": 15,
"name": "山城、十二分",
"aim": "方向幕のような黄と黒で、駅から歩く時間を大きく示す",
"swatch": "#f0c419",
"ink": "#1a1408",
"thumb": "yamashiro_st.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Kosugi+Maru&display=swap",
"body": r"""
<article class="rail">
<a class="back" href="../">一覧</a>
<section class="blind">
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
<p class="mins">$walk</p>
</section>
<section class="platform">
<img src="$u_station" alt="三岐線の駅">
</section>
<section class="board">
<p class="place">$place</p>
<p>$car</p>
<p>$door</p>
<p>$daily</p>
<p>$group</p>
<p>$time</p>
<p>$agey</p>
<p>$age</p>
<p>$dev</p>
<p>$target</p>
<p>$bus</p>
<p>$bus2</p>
</section>
<section class="platform">
<img src="$u_ext" alt="レオの建物">
</section>
<section class="board ink">
<p>$toy</p>
<p>$move</p>
<p>$lunch</p>
<h2>$event_h</h2>
<p>$event</p>
<p>$lunch2</p>
<p>$fee</p>
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
body{background:#1a1408;color:#1a1408;font-family:"Kosugi Maru",sans-serif;line-height:1.75}
.back{position:absolute;z-index:2;top:.7rem;right:.7rem;color:#1a1408}
.blind{background:#f0c419;min-height:100svh;padding:16vh 7vw;display:flex;flex-direction:column;justify-content:center}
h1{font-size:clamp(4rem,14vw,9rem);margin:0;line-height:.9}
.mins{font-size:clamp(2rem,6vw,3.6rem);margin:.6rem 0 0}
.lead{font-size:clamp(1.3rem,3vw,1.9rem);max-width:16em}
.platform img{width:100%;height:70vh;object-fit:cover}
.board{background:#f0c419;padding:6vh 8vw;font-size:1.15rem}
.board.ink{background:#1a1408;color:#f6e7b0}
.place{font-size:clamp(1.6rem,4vw,2.4rem)}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.35rem .8rem .35rem 0}
h2{font-size:1.5rem}
.board.ink :focus-visible{outline-color:#fff4c2}
"""
})

DESIGNS.append({
"n": 16,
"name": "木のつみき",
"aim": "角度のばらついた木片の上に、短い文を載せる",
"swatch": "#c4a574",
"ink": "#2a1c10",
"thumb": "blocks.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Kaisei+HarunoUmi:wght@400;700&display=swap",
"body": r"""
<article class="pile">
<a class="back" href="../">一覧</a>
<header class="wood w0">
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</header>
<img class="hero" src="$u_blocks" alt="積み木">
<p class="wood w1">$daily</p>
<p class="wood w2">$group</p>
<p class="wood w3">$toy</p>
<img class="hero lean" src="$u_toys" alt="おもちゃの部屋">
<p class="wood w4">$move</p>
<p class="wood w5">$lunch</p>
<p class="wood w1">$agey</p>
<p class="wood w2">$dev $bus</p>
<h2 class="wood w3">$event_h</h2>
<p class="wood w4">$event</p>
<img class="hero" src="$u_shichi" alt="行事・七輪">
<h2 class="wood w5">$fam_h</h2>
<p class="wood w1">$kato</p>
<p class="wood w2">$door</p>
<p class="wood w0 place">$place</p>
<p class="wood w3">$walk</p>
<p class="wood w4">$car</p>
<p class="wood w5">$target</p>
<p class="wood w1">$age</p>
<p class="wood w2">$time</p>
<p class="wood w3">$lunch2</p>
<p class="wood w4">$bus2</p>
<p class="wood w5">$fee</p>
<p class="wood w1">$eval_h</p>
<p class="wood w2 evals">$evals</p>
<p class="wood w3">$pt_a　$pt_s</p>
<p class="wood w4">$as_a　$as_s</p>
<section class="wood w0 visit">
<h2>$visit_h</h2>
<p><a href="$url_line">LINE</a></p>
<p><a href="$tel_href">$tel</a></p>
</section>
</article>
""",
"css": r"""
:root{--focus:#7a1f1f}
body{background:#efe4d2;color:#2a1c10;font-family:"Kaisei HarunoUmi",serif;line-height:1.75}
.pile{padding:6vh 4vw 3rem}
.back{color:#2a1c10}
.hero{width:min(100%,820px);margin:1.2rem auto;height:auto}
.lean{transform:rotate(1.5deg)}
.wood{display:inline-block;max-width:min(34rem,92vw);padding:1rem 1.15rem;margin:.55rem .4rem;background:#e7d3b0;color:#2a1c10}
.w0{background:#f3e6d0;display:block;max-width:none}
.w1{background:#ddc29a;transform:rotate(-1.6deg)}
.w2{background:#c4a574;transform:rotate(1.3deg)}
.w3{background:#8d6744;color:#f8f1e6;transform:rotate(-0.6deg)}
.w4{background:#5c3d27;color:#f8f1e6;transform:rotate(1.8deg)}
.w5{background:#f3e6d0;transform:rotate(-1.1deg)}
h1{font-size:clamp(3.4rem,9vw,6rem);margin:.1rem 0}
.lead{font-size:clamp(1.2rem,2.6vw,1.7rem)}
.place{font-size:clamp(1.4rem,3vw,2rem)}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.25rem .55rem .25rem 0}
h2{font-size:1.35rem;margin:0 0 .3rem}
.w3 :focus-visible,.w4 :focus-visible{outline-color:#ffe08a}
@media(max-width:700px){.wood{transform:none!important}}
"""
})

DESIGNS.append({
"n": 17,
"name": "藍の暖簾",
"aim": "のれんを二つに割り、その奥に二階の入口がある",
"swatch": "#1a2744",
"ink": "#f4efe4",
"thumb": "child_shichirin.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Yuji+Syuku&display=swap",
"body": r"""
<article class="noren">
<a class="back" href="../">一覧</a>
<section class="curtain">
<div class="panel left"><p class="role">$role</p><h1>レ</h1></div>
<div class="panel right"><h1>オ</h1><p class="lead">$lead</p></div>
</section>
<section class="beyond">
<img src="$u_ext" alt="レオの建物">
<div class="say">
<p>$door</p>
<p class="place">$place</p>
<p>$walk</p>
<p>$car</p>
</div>
</section>
<section class="cloth">
<p>$daily</p>
<p>$group</p>
<p>$agey</p>
<p>$dev</p>
<p>$bus</p>
<p>$toy</p>
<img src="$u_panda" alt="おもちゃの棚と、床に座るパンダのぬいぐるみ">
<p>$move</p>
<p>$lunch</p>
<h2>$event_h</h2>
<p>$event</p>
<img src="$u_shichi" alt="行事・七輪">
<h2>$fam_h</h2>
<p>$kato</p>
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
:root{--focus:#e2b657}
body{background:#f4efe4;color:#1a2744;font-family:"Yuji Syuku",serif;line-height:1.9}
.back{position:absolute;z-index:3;top:.7rem;left:.8rem;background:#f4efe4;color:#1a2744;text-decoration:none;padding:.2rem .6rem}
.curtain{display:flex;min-height:100svh;overflow:hidden}
.panel{width:50%;background:#1a2744;color:#f4efe4;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:14vh 6vw 16vh;position:relative}
.panel.right{background:#243456}
h1{font-size:clamp(5.5rem,14vw,10rem);margin:0;font-weight:400;line-height:1;writing-mode:horizontal-tb}
.role,.lead{position:absolute;left:8%;right:8%;bottom:8vh;margin:0;font-size:1.05rem;line-height:1.7;text-align:center}
.beyond{position:relative}
.beyond img{width:100%;height:80vh;object-fit:cover}
.say{position:absolute;left:6vw;bottom:6vh;background:rgba(244,239,228,.92);color:#1a2744;padding:1rem 1.2rem;max-width:min(28rem,80vw)}
.place{font-size:1.35rem}
.cloth{padding:8vh 10vw;background:#f4efe4}
.cloth img{width:min(100%,760px);margin:1rem auto;height:auto}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.3rem .7rem .3rem 0}
h2{font-size:1.5rem}
@media(max-width:700px){
  .panel{padding:18vh 4vw 8rem}
  h1{font-size:4.4rem}
  .role,.lead{font-size:.95rem}
}
"""
})

DESIGNS.append({
"n": 18,
"name": "図鑑の頁",
"aim": "一枚の野外写真のまわりに、標本ラベルのような短い注を置く",
"swatch": "#e4ebe3",
"ink": "#1c2416",
"thumb": "child_shichirin.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&display=swap",
"body": r"""
<article class="plate">
<a class="back" href="../">一覧</a>
<header>
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</header>
<figure class="specimen">
<img src="$u_shichi" alt="行事・七輪">
</figure>
<div class="labels">
<p>$event_h $event</p>
<p>$daily</p>
<p>$move</p>
<p>$toy</p>
</div>
<figure class="specimen small">
<img src="$u_forest" alt="フィールドの木々と作業">
</figure>
<div class="labels">
<p>$group</p>
<p>$time</p>
<p>$lunch</p>
<p>$lunch2</p>
<p>$agey</p>
<p>$age</p>
<p>$dev</p>
<p>$target</p>
<p>$bus</p>
<p>$bus2</p>
</div>
<figure class="specimen">
<img src="$u_mari" alt="庭のマリーゴールド">
</figure>
<section class="labels">
<h2>$fam_h</h2>
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
:root{--focus:#9a3412}
body{background:#e4ebe3;color:#1c2416;font-family:"Noto Serif JP",serif;line-height:1.8}
.plate{padding:6vh 6vw 2rem}
.back{color:#1c2416}
h1{font-size:clamp(3.2rem,8vw,5.5rem);margin:.1rem 0;font-weight:700;letter-spacing:.14em}
.lead{font-size:clamp(1.2rem,2.6vw,1.7rem);max-width:20em}
.specimen{margin:2rem 8vw}
.specimen img{width:100%;max-height:78vh;object-fit:cover}
.specimen.small{margin-left:18vw;margin-right:0;width:min(70%,640px)}
.labels{max-width:38rem;margin:1rem 0 2rem 10vw}
.labels p{margin:.7rem 0;font-size:1.08rem}
.place{font-size:1.45rem}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.3rem .7rem .3rem 0}
h2{font-size:1.4rem}
@media(max-width:700px){
  .specimen,.specimen.small,.labels{margin-left:0;margin-right:0;width:100%}
}
"""
})

DESIGNS.append({
"n": 19,
"name": "午後の電波",
"aim": "一日を番組の章に見立て、暗い木のスタジオで聴く",
"swatch": "#3a2418",
"ink": "#f6efe4",
"thumb": "karate_class.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Stick&family=Zen+Kaku+Gothic+New:wght@400;700&display=swap",
"body": r"""
<article class="fm">
<a class="back" href="../">一覧</a>
<header class="onair">
<p class="lamp">放送中</p>
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</header>
<section class="track">
<img src="$u_panda" alt="おもちゃの棚と、床に座るパンダのぬいぐるみ">
<p>$daily</p>
<p>$toy</p>
</section>
<section class="track alt">
<p>$group</p>
<p>$time</p>
<p>$agey</p>
<p>$age</p>
<p>$dev</p>
<p>$target</p>
</section>
<section class="track">
<img src="$u_karate" alt="武道の稽古">
<p>$move</p>
</section>
<section class="track alt">
<img src="$u_meal" alt="手作りの和定食">
<p>$lunch</p>
<p>$lunch2</p>
</section>
<section class="track">
<h2>$event_h</h2>
<p>$event</p>
<p>$bus</p>
<p>$bus2</p>
</section>
<section class="track alt">
<img src="$u_ext" alt="レオの建物">
<h2>$fam_h</h2>
<p>$kato</p>
<p>$door</p>
<p class="place">$place</p>
<p>$walk</p>
<p>$car</p>
<p>$fee</p>
</section>
<section class="track signoff">
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
:root{--focus:#f0c419}
body{background:#24170f;color:#f6efe4;font-family:"Zen Kaku Gothic New",sans-serif;line-height:1.8}
.back{color:#f6efe4;position:absolute;top:.7rem;right:.8rem}
.onair{min-height:100svh;padding:16vh 8vw;background:radial-gradient(circle at 80% 20%,#6b2430 0,transparent 28%),#24170f}
.lamp{display:inline-block;background:#e23b2f;color:#fff;padding:.2rem .7rem;border-radius:999px;font-family:Stick,sans-serif}
h1{font-family:Stick,sans-serif;font-size:clamp(4rem,12vw,8rem);margin:.2rem 0;font-weight:400}
.lead{font-size:clamp(1.3rem,3vw,1.9rem);max-width:16em}
.track{padding:7vh 8vw}
.track img{width:min(100%,760px);height:auto;margin-bottom:1rem;border-radius:1.2rem}
.track.alt{background:#3a2418}
.place{font-size:1.5rem}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.3rem .7rem .3rem 0}
h2{font-family:Stick,sans-serif;font-size:1.8rem;font-weight:400}
.signoff h2{font-size:2.4rem}
"""
})

DESIGNS.append({
"n": 20,
"name": "壁に掛ける",
"aim": "色のついた壁に、大きさの違う写真を高さ違いで掛ける",
"swatch": "#c9bfd0",
"ink": "#241826",
"thumb": "panda.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Shippori+Antique&family=Zen+Old+Mincho:wght@400;700&display=swap",
"body": r"""
<article class="wall">
<a class="back" href="../">一覧</a>
<header class="label">
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</header>
<figure class="hang h1"><img src="$u_panda" alt="おもちゃの棚と、床に座るパンダのぬいぐるみ"><figcaption>$daily</figcaption></figure>
<figure class="hang h2"><img src="$u_blocks" alt="積み木"><figcaption>$toy</figcaption></figure>
<figure class="hang h3"><img src="$u_shichi" alt="行事・七輪"><figcaption>$event_h $event</figcaption></figure>
<figure class="hang h4"><img src="$u_zinnia" alt="建物のそばのジニア"></figure>
<section class="caption">
<p>$group</p>
<p>$move</p>
<p>$lunch</p>
<p>$agey</p>
<p>$dev</p>
<p>$bus</p>
<p>$target</p>
<p>$age</p>
<p>$time</p>
<p>$lunch2</p>
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
<figure class="hang h5"><img src="$u_ext" alt="レオの建物"></figure>
</article>
""",
"css": r"""
:root{--focus:#7c3aed}
body{background:#c9bfd0;color:#241826;font-family:"Zen Old Mincho",serif;line-height:1.85}
.wall{padding:5vh 5vw 3rem;position:relative;min-height:100vh}
.back{color:#241826}
.label{max-width:28rem;padding-top:6vh}
h1{font-family:"Shippori Antique",serif;font-size:clamp(3.4rem,8vw,6rem);margin:.1rem 0;font-weight:400}
.lead{font-size:clamp(1.2rem,2.5vw,1.7rem)}
.hang{background:#f7f4f2;padding:.7rem .7rem 1rem;display:inline-block;box-shadow:0 14px 30px rgba(36,24,38,.16)}
.hang img{width:100%;height:auto;object-fit:cover}
.h1{width:min(68%,760px);margin:2rem 0 1rem 6vw}
.h2{width:min(38%,360px);margin:1rem 0 2rem 48vw}
.h3{width:min(52%,520px);margin:1rem 8vw}
.h4{width:min(28%,260px);margin:-2rem 0 1rem 62vw}
.h5{width:min(74%,800px);margin:2rem 0 0 10vw}
figcaption{font-size:.95rem;padding-top:.45rem}
.caption{max-width:36rem;margin:2rem 8vw;font-size:1.08rem}
.place{font-size:1.4rem}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.3rem .7rem .3rem 0}
h2{font-size:1.4rem}
@media(max-width:760px){
  .hang,.h1,.h2,.h3,.h4,.h5{width:100%;margin:1rem 0}
}
"""
})
