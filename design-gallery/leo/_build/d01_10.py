# -*- coding: utf-8 -*-
"""Designs 01–10. Layout shells only; copy is substituted by gen.py."""

DESIGNS = []

DESIGNS.append({
"n": 1,
"name": "朝のひかり",
"aim": "朝日の入るおもちゃ部屋を画面いっぱいに使い、言葉は左下の暗い面に短く置く",
"swatch": "#16324a",
"ink": "#f4f7fb",
"thumb": "panda.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Outfit:wght@500&family=Zen+Old+Mincho:wght@400;700;900&display=swap",
"body": r"""
<article class="d1">
<a class="back" href="../">一覧</a>
<section class="hero">
<img src="$u_panda" alt="おもちゃの棚と、床に座るパンダのぬいぐるみ">
<div class="cap">
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</div>
</section>
<section class="flow">
<p class="drop">$daily</p>
<p>$group</p>
<p>$lunch</p>
<p>$agey</p>
<p>$dev</p>
<p>$bus</p>
</section>
<section class="break">
<img src="$u_toys" alt="おもちゃの部屋">
<p>$toy</p>
</section>
<section class="break alt">
<p>$move</p>
<img src="$u_blocks" alt="積み木">
</section>
<section class="break">
<img src="$u_shichi" alt="行事・七輪">
<h2>$event_h</h2>
<p>$event</p>
</section>
<section class="door">
<img src="$u_ext" alt="レオの建物">
<div>
<h2>$fam_h</h2>
<p>$kato</p>
<p>$door</p>
</div>
</section>
<section class="facts">
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
<p class="kin">$pt_a　$pt_s</p>
<p class="kin">$as_a　$as_s</p>
</section>
<section class="visit">
<h2>$visit_h</h2>
<p><a href="$url_line">LINE</a></p>
<p><a class="tel" href="$tel_href">電話 $tel</a></p>
</section>
</article>
""",
"css": r"""
:root{--focus:#ffbf47;--ink:#102033;--paper:#e7eef3}
body{background:var(--paper);color:var(--ink);font-family:"Zen Old Mincho",serif;font-size:1.15rem;line-height:1.9}
.back{position:absolute;z-index:3;top:1rem;left:1rem;background:#e7eef3;color:#102033;text-decoration:none;padding:.35rem .7rem}
.hero{position:relative;min-height:100svh;background:#102033;color:#f4f7fb}
.hero img{width:100%;height:100svh;object-fit:cover;object-position:50% 62%}
.cap{position:absolute;left:5vw;bottom:6vh;background:rgba(16,32,51,.9);color:#f4f7fb;padding:1.3rem 1.5rem 1.4rem;max-width:min(34rem,90vw)}
.role{font-family:Outfit,sans-serif;margin:0 0 .3rem;font-size:1rem}
h1{font-weight:900;font-size:clamp(3.4rem,9vw,6.4rem);line-height:.95;margin:0;letter-spacing:.06em}
.lead{font-size:clamp(1.25rem,2.5vw,1.8rem);margin:.7rem 0 0}
.flow{width:min(40rem,88vw);margin:0 auto;padding:4.5rem 0 1rem}
.flow p{font-size:1.22rem}
.break{width:min(68rem,92vw);margin:2.5rem auto;display:flex;gap:2rem;align-items:flex-end}
.break img{width:54%;height:min(72vh,640px);object-fit:cover}
.break p,.break h2{width:46%;margin:0}
.break h2{font-size:1.8rem;font-weight:700;margin-bottom:.6rem}
.break.alt{flex-direction:row-reverse}
.door{display:flex;min-height:80vh}
.door img{width:58%;object-fit:cover}
.door div{width:42%;padding:8vh 4vw;background:#102033;color:#f4f7fb;display:flex;flex-direction:column;justify-content:flex-end}
.door h2{font-size:clamp(1.6rem,3vw,2.2rem);margin:0 0 .8rem}
.facts{width:min(40rem,88vw);margin:0 auto;padding:3rem 0}
.place{font-size:clamp(1.6rem,4vw,2.4rem);line-height:1.4}
.evals a,.kin a,.visit a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.35rem .8rem .35rem 0}
.visit{background:#102033;color:#f4f7fb;padding:4.5rem 8vw}
.visit h2{font-size:clamp(2rem,5vw,3.2rem);margin:0 0 1rem}
.tel{font-size:clamp(1.6rem,4vw,2.4rem);text-decoration:underline}
@media(max-width:760px){
  .break,.break.alt,.door{flex-direction:column}
  .break img,.break p,.break h2,.door img,.door div{width:100%}
  .break img{height:58vw}
  .door div{padding:2rem 6vw 2.5rem}
}
"""
})

DESIGNS.append({
"n": 2,
"name": "見開き絵本",
"aim": "絵と文を左右に分け、見開きごとに写真と文章が入れ替わる",
"swatch": "#e5f2e4",
"ink": "#163226",
"thumb": "toyshelf.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;700;900&display=swap",
"body": r"""
<article class="book">
<a class="back" href="../">一覧</a>
<section class="spread cover">
<div class="pic"><img src="$u_toys" alt="おもちゃの部屋"></div>
<div class="txt">
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</div>
</section>
<section class="spread flip">
<div class="txt">
<p>$daily</p>
<p>$group</p>
<p>$agey</p>
<p>$dev</p>
<p>$bus</p>
</div>
<div class="pic"><img src="$u_panda" alt="おもちゃの棚と、床に座るパンダのぬいぐるみ"></div>
</section>
<section class="spread">
<div class="pic"><img src="$u_blocks" alt="積み木"></div>
<div class="txt">
<p>$toy</p>
<p>$move</p>
</div>
</section>
<section class="spread flip">
<div class="txt">
<h2>$event_h</h2>
<p>$event</p>
<p>$lunch</p>
</div>
<div class="pic"><img src="$u_shichi" alt="行事・七輪"></div>
</section>
<section class="spread">
<div class="pic"><img src="$u_ext" alt="レオの建物"></div>
<div class="txt">
<h2>$fam_h</h2>
<p>$kato</p>
<p>$door</p>
</div>
</section>
<section class="spread flip soft">
<div class="txt">
<p>$target</p>
<p>$age</p>
<p>$time</p>
<p>$lunch2</p>
<p>$place</p>
<p>$walk</p>
<p>$car</p>
<p>$bus2</p>
<p>$fee</p>
</div>
<div class="pic"><img src="$u_meal" alt="手作りの和定食"></div>
</section>
<section class="end">
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
:root{--focus:#c4492c}
body{margin:0;background:#f3f7f1;color:#163226;font-family:"Zen Maru Gothic",sans-serif;font-size:1.12rem;line-height:1.85}
.back{position:absolute;z-index:2;top:.8rem;left:.8rem;background:#163226;color:#f3f7f1;text-decoration:none;padding:.3rem .65rem;border-radius:999px}
.spread{display:flex;min-height:100svh;background:#f3f7f1}
.spread .pic,.spread .txt{width:50%}
.spread img{width:100%;height:100svh;object-fit:cover}
.txt{padding:10vh 6vw;display:flex;flex-direction:column;justify-content:center}
.cover{background:#e5f2e4}
h1{font-size:clamp(4rem,8vw,7rem);line-height:1;margin:.2rem 0;font-weight:900}
.role{margin:0;font-size:1.05rem}
.lead{font-size:clamp(1.4rem,2.6vw,2rem);margin:.4rem 0 0}
.flip{flex-direction:row-reverse;background:#fffdf8}
.flip.soft{background:#e7f0ea}
h2{font-size:1.7rem;margin:0 0 .4rem}
.end{padding:8vh 8vw 4rem;background:#163226;color:#f3f7f1}
.end a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.4rem .9rem .4rem 0}
.end h2{font-size:clamp(2rem,5vw,3rem)}
@media(max-width:760px){
  .spread,.flip{flex-direction:column}
  .spread .pic,.spread .txt{width:100%}
  .spread img{height:62vw;min-height:220px}
  .txt{padding:1.6rem 6vw 2rem}
}
"""
})

DESIGNS.append({
"n": 3,
"name": "座敷の縦書き",
"aim": "藍の壁に縦書きを落とし、写真は横一文字の開口部にする",
"swatch": "#1b2744",
"ink": "#f3ead7",
"thumb": "leo_ext.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;600;700&display=swap",
"body": r"""
<article class="zashiki">
<a class="back" href="../">一覧</a>
<section class="tate">
<div class="col name">
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</div>
<div class="col">
<p>$daily</p>
<p>$group</p>
<p>$agey</p>
<p>$dev</p>
<p>$bus</p>
</div>
</section>
<figure class="slit"><img src="$u_ext" alt="レオの建物"><figcaption>$door</figcaption></figure>
<section class="tate short">
<div class="col">
<p>$toy</p>
<p>$move</p>
<p>$lunch</p>
</div>
</section>
<figure class="slit"><img src="$u_panda" alt="おもちゃの棚と、床に座るパンダのぬいぐるみ"></figure>
<section class="tate short">
<div class="col">
<h2>$event_h</h2>
<p>$event</p>
</div>
<div class="col">
<h2>$fam_h</h2>
<p>$kato</p>
</div>
</section>
<figure class="slit"><img src="$u_shichi" alt="行事・七輪"></figure>
<section class="tate facts">
<div class="col">
<p>$place</p>
<p>$walk</p>
<p>$car</p>
<p>$target</p>
<p>$age</p>
</div>
<div class="col">
<p>$time</p>
<p>$lunch2</p>
<p>$bus2</p>
<p>$fee</p>
<p class="evalh">$eval_h</p>
<p class="evals">$evals</p>
</div>
</section>
<section class="close">
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
body{background:#1b2744;color:#f3ead7;font-family:"Shippori Mincho",serif;font-size:1.12rem;line-height:2}
.back{position:absolute;z-index:3;top:.8rem;right:.8rem;color:#1b2744;background:#f3ead7;text-decoration:none;padding:.3rem .7rem}
.tate{display:flex;justify-content:flex-end;gap:2.2rem;padding:8vh 6vw;min-height:100svh}
.tate.short{min-height:70vh}
.col{writing-mode:vertical-rl;max-height:86vh}
h1{font-size:4.2rem;font-weight:700;margin:0;letter-spacing:.18em}
.role,.lead{margin:.4rem 0}
.lead{font-size:1.25rem}
h2{font-size:1.35rem;font-weight:600;margin:0}
.slit{margin:0}
.slit img{width:100%;height:42vh;object-fit:cover}
.slit figcaption{padding:.6rem 6vw 0;color:#f3ead7}
.evals a,.close a{text-decoration:underline;text-underline-offset:.2em}
.evals a{display:inline}
.close{padding:6vh 8vw 3rem;background:#f3ead7;color:#1b2744}
.close h2{font-size:clamp(2rem,5vw,3rem);margin:1rem 0}
@media(max-width:760px){
  .tate,.tate.short{flex-direction:column;min-height:0;align-items:flex-start}
  .col{writing-mode:horizontal-tb;max-height:none}
  h1{writing-mode:horizontal-tb;height:auto;font-size:3.4rem;letter-spacing:.12em}
}
"""
})

DESIGNS.append({
"n": 4,
"name": "社会面",
"aim": "巨大な見出しと段組み。仕切り線は引かない、紙面だけの新聞",
"swatch": "#d7d4cc",
"ink": "#161616",
"thumb": "blocks.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Zen+Antique&family=Noto+Serif+JP:wght@400;700&display=swap",
"body": r"""
<article class="paper">
<a class="back" href="../">一覧</a>
<header class="mast">
<p class="kicker">四日市・あさけが丘</p>
<h1>レオ</h1>
<p class="role">$role</p>
<p class="lead">$lead</p>
</header>
<div class="cols">
<p>$daily</p>
<p>$group</p>
<p>$lunch</p>
<p>$agey</p>
<p>$dev</p>
<p>$bus</p>
<p>$toy</p>
</div>
<figure class="cut">
<img src="$u_blocks" alt="積み木">
<figcaption>積み木</figcaption>
</figure>
<div class="cols">
<p>$move</p>
<h2>$event_h</h2>
<p>$event</p>
</div>
<figure class="cut wide">
<img src="$u_shichi" alt="行事・七輪">
</figure>
<div class="cols">
<h2>$fam_h</h2>
<p>$kato</p>
<p>$door</p>
<p>$target</p>
<p>$age</p>
<p>$time</p>
<p>$lunch2</p>
<p>$place</p>
<p>$walk</p>
<p>$car</p>
<p>$bus2</p>
<p>$fee</p>
</div>
<figure class="cut">
<img src="$u_ext" alt="レオの建物">
</figure>
<section class="tail">
<p class="evalh">$eval_h</p>
<p class="evals">$evals</p>
<p>$pt_a　$pt_s</p>
<p>$as_a　$as_s</p>
<h2>$visit_h</h2>
<p><a href="$url_line">LINE</a>　<a href="$tel_href">$tel</a></p>
</section>
</article>
""",
"css": r"""
:root{--focus:#9a3412}
body{background:#cfcbc2;color:#161616;font-family:"Noto Serif JP",serif;font-size:1.05rem;line-height:1.85}
.paper{width:min(980px,100%);margin:0 auto;background:#e4e1d9;padding:2.2rem 6vw 1rem}
.back{color:#161616}
.mast{text-align:center;padding-bottom:1rem}
.kicker{letter-spacing:.22em;margin:0}
h1{font-family:"Zen Antique",serif;font-weight:400;font-size:clamp(4.5rem,14vw,8.5rem);line-height:.85;margin:.1rem 0}
.role{margin:.2rem 0}
.lead{font-size:clamp(1.3rem,3vw,1.8rem);margin:.3rem auto 0;max-width:22em}
.cols{columns:3;column-gap:1.6rem;margin:1.2rem 0}
.cols h2{font-size:1.25rem;margin:0 0 .3rem;break-after:avoid}
.cols p{margin:.55rem 0}
.cut{margin:1rem 0 1.4rem}
.cut img{width:100%;max-height:70vh;object-fit:cover}
.cut figcaption{font-size:.95rem;margin-top:.3rem}
.tail a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.3rem .7rem .3rem 0}
.tail h2{font-family:"Zen Antique",serif;font-size:2.2rem;font-weight:400}
@media(max-width:900px){.cols{columns:2}}
@media(max-width:640px){.cols{columns:1}.paper{padding-top:1.2rem}}
"""
})

DESIGNS.append({
"n": 5,
"name": "一枚のポスター",
"aim": "行事の写真に名前を重ね、電話番号は下端で手にとって切れる",
"swatch": "#7d1c1c",
"ink": "#fff6ee",
"thumb": "child_shichirin.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Noto+Sans+JP:wght@400;700&display=swap",
"body": r"""
<article class="poster">
<a class="back" href="../">一覧</a>
<section class="face">
<img src="$u_shichi" alt="行事・七輪">
<div class="type">
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</div>
</section>
<section class="backside">
<p>$daily</p>
<p>$group</p>
<p>$lunch</p>
<p>$agey</p>
<p>$dev</p>
<p>$bus</p>
<p>$toy</p>
<img src="$u_panda" alt="おもちゃの棚と、床に座るパンダのぬいぐるみ">
<p>$move</p>
<h2>$event_h</h2>
<p>$event</p>
<img src="$u_blocks" alt="積み木">
<h2>$fam_h</h2>
<p>$kato</p>
<p>$door</p>
<img src="$u_ext" alt="レオの建物">
<p>$target</p>
<p>$age</p>
<p>$time</p>
<p>$lunch2</p>
<p class="place">$place</p>
<p>$walk</p>
<p>$car</p>
<p>$bus2</p>
<p>$fee</p>
<p class="evalh">$eval_h</p>
<p class="evals">$evals</p>
<p>$pt_a　$pt_s</p>
<p>$as_a　$as_s</p>
</section>
<section class="stub">
<h2>$visit_h</h2>
<p><a href="$url_line">LINE</a></p>
<p><a href="$tel_href">$tel</a></p>
</section>
</article>
""",
"css": r"""
:root{--focus:#ffe08a}
body{background:#2a0d0d;color:#2a0d0d;font-family:"Noto Sans JP",sans-serif;line-height:1.8}
.back{position:absolute;z-index:3;top:.7rem;left:.7rem;background:#fff6ee;color:#7d1c1c;text-decoration:none;padding:.3rem .6rem}
.face{position:relative;min-height:100svh;background:#1a0909;color:#fff6ee}
.face img{width:100%;height:100svh;object-fit:cover;object-position:50% 30%}
.type{position:absolute;inset:auto 0 0 0;padding:8vh 6vw 10vh;background:linear-gradient(transparent,rgba(60,8,8,.55) 20%,rgba(60,8,8,.88))}
.role{margin:0;font-size:1rem}
h1{font-family:"Dela Gothic One",sans-serif;font-size:clamp(4.5rem,18vw,11rem);line-height:.9;margin:0;font-weight:400;letter-spacing:.04em}
.lead{font-size:clamp(1.3rem,3vw,2rem);max-width:16em;margin:.4rem 0 0}
.backside{background:#f6efe6;padding:8vh 8vw;font-size:1.12rem}
.backside img{width:min(100%,680px);margin:1.2rem 0;transform:rotate(-1.2deg)}
.place{font-family:"Dela Gothic One",sans-serif;font-size:clamp(1.6rem,4vw,2.4rem);line-height:1.35}
.evals a,.backside a,.stub a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.35rem .8rem .35rem 0}
.stub{background:#7d1c1c;color:#fff6ee;padding:2rem 8vw 2.4rem;clip-path:polygon(0 14px,3% 0,7% 12px,12% 0,18% 14px,24% 0,31% 13px,38% 0,46% 14px,54% 0,63% 12px,71% 0,79% 14px,88% 0,94% 12px,100% 0,100% 100%,0 100%)}
.stub h2{font-family:"Dela Gothic One",sans-serif;font-weight:400;font-size:clamp(1.8rem,4vw,2.6rem);margin:1rem 0 .4rem}
.stub a{font-size:clamp(1.5rem,4vw,2.3rem)}
"""
})

DESIGNS.append({
"n": 6,
"name": "余白の手紙",
"aim": "画面に一文だけ。写真は遠くに、小さく、遅れて現れる",
"swatch": "#f6f5f2",
"ink": "#1d2a33",
"thumb": "zinnia.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Kaisei+Opti:wght@400;700&display=swap",
"body": r"""
<article class="letter">
<a class="back" href="../">一覧</a>
<section class="beat"><p class="role">$role</p><h1>レオ</h1></section>
<section class="beat"><p class="lead">$lead</p></section>
<section class="beat"><p>$daily</p></section>
<section class="beat quiet"><img src="$u_zinnia" alt="建物のそばのジニア"></section>
<section class="beat"><p>$group</p></section>
<section class="beat"><p>$toy</p></section>
<section class="beat quiet"><img src="$u_blocks" alt="積み木"></section>
<section class="beat"><p>$move</p></section>
<section class="beat"><h2>$event_h</h2><p>$event</p></section>
<section class="beat quiet"><img src="$u_shichi" alt="行事・七輪"></section>
<section class="beat"><p>$lunch</p></section>
<section class="beat"><p>$agey</p><p>$dev</p><p>$bus</p></section>
<section class="beat"><h2>$fam_h</h2><p>$kato</p><p>$door</p></section>
<section class="beat quiet"><img src="$u_ext" alt="レオの建物"></section>
<section class="beat"><p>$place</p><p>$walk</p><p>$car</p></section>
<section class="beat"><p>$target</p><p>$age</p><p>$time</p></section>
<section class="beat"><p>$lunch2</p><p>$bus2</p><p>$fee</p></section>
<section class="beat"><p class="evalh">$eval_h</p><p class="evals">$evals</p></section>
<section class="beat"><p>$pt_a　$pt_s</p><p>$as_a　$as_s</p></section>
<section class="beat last"><h2>$visit_h</h2><p><a href="$url_line">LINE</a></p><p><a href="$tel_href">$tel</a></p></section>
</article>
""",
"css": r"""
:root{--focus:#b45309}
body{background:#f6f5f2;color:#1d2a33;font-family:"Kaisei Opti",serif}
.back{position:fixed;top:.8rem;right:.8rem;z-index:3;color:#1d2a33}
.beat{min-height:100svh;display:flex;flex-direction:column;justify-content:center;padding:12vh 10vw;font-size:clamp(1.35rem,2.8vw,2rem);line-height:1.7}
.beat p{margin:.4rem 0;max-width:18em}
h1{font-size:clamp(4rem,12vw,8rem);font-weight:700;margin:0;line-height:1}
h2{font-weight:700;font-size:1.4em;margin:0 0 .4rem}
.quiet{align-items:flex-end}
.quiet img{width:min(42vw,420px);height:auto;margin-right:6vw}
.evals a,.beat a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.3rem .7rem .3rem 0;font-size:1rem}
.last a{font-size:clamp(1.4rem,3vw,2rem)}
@media(max-width:700px){.quiet img{width:70vw;margin:0}}
"""
})

DESIGNS.append({
"n": 7,
"name": "スケッチ帖",
"aim": "線のない紙に、テープで留めた写真と、鉛筆で書いたような字",
"swatch": "#e7eef3",
"ink": "#243038",
"thumb": "blocks.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Klee+One:wght@400;600&family=Yomogi&display=swap",
"body": r"""
<article class="sketch">
<a class="back" href="../">一覧</a>
<header class="cover">
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</header>
<p class="note n1">$daily</p>
<p class="note n2">$group</p>
<figure class="tape t1"><img src="$u_toys" alt="おもちゃの部屋"><figcaption>$toy</figcaption></figure>
<p class="note n3">$move</p>
<figure class="tape t2"><img src="$u_blocks" alt="積み木"></figure>
<p class="note n4">$lunch</p>
<p class="note n5">$agey $dev $bus</p>
<h2 class="note">$event_h</h2>
<p class="note">$event</p>
<figure class="tape t3"><img src="$u_shichi" alt="行事・七輪"></figure>
<h2 class="note">$fam_h</h2>
<p class="note">$kato</p>
<p class="note">$door</p>
<figure class="tape t4"><img src="$u_ext" alt="レオの建物"></figure>
<p class="note big">$place</p>
<p class="note">$walk</p>
<p class="note">$car</p>
<p class="note">$target</p>
<p class="note">$age</p>
<p class="note">$time</p>
<p class="note">$lunch2</p>
<p class="note">$bus2</p>
<p class="note">$fee</p>
<p class="note">$eval_h</p>
<p class="note evals">$evals</p>
<p class="note">$pt_a　$pt_s</p>
<p class="note">$as_a　$as_s</p>
<section class="sign">
<h2>$visit_h</h2>
<p><a href="$url_line">LINE</a></p>
<p><a href="$tel_href">$tel</a></p>
</section>
</article>
""",
"css": r"""
:root{--focus:#d94a4a}
body{background:#e7eef3;color:#243038;font-family:"Klee One",sans-serif;font-size:1.15rem;line-height:1.85}
.sketch{padding:6vh 6vw 2rem}
.back{color:#243038}
.cover h1,.note,.sign h2{font-family:Yomogi,cursive}
h1{font-size:clamp(3.5rem,10vw,6.5rem);margin:.2rem 0;font-weight:400;transform:rotate(-2deg)}
.lead{font-size:clamp(1.3rem,3vw,1.8rem);max-width:16em}
.note{max-width:36rem;background:rgba(255,255,255,.45);padding:.2rem .4rem}
.n1{transform:rotate(-0.6deg)}
.n2{transform:rotate(0.8deg);margin-left:8vw}
.n3{margin-left:4vw}
.tape{display:inline-block;background:#f7f7f4;padding:.7rem .7rem 1.4rem;box-shadow:0 10px 24px rgba(36,48,56,.12);margin:1.2rem 0}
.tape img{width:min(78vw,560px);height:auto}
.t1{transform:rotate(-2.5deg)}
.t2{transform:rotate(2deg);margin-left:10vw}
.t3{transform:rotate(-1deg)}
.t4{transform:rotate(1.4deg);margin-left:6vw}
.tape::before{content:"";display:block;width:4.2rem;height:.9rem;margin:-1.15rem auto .4rem;background:rgba(214,168,92,.72);transform:rotate(-2deg)}
.big{font-size:1.6rem}
.evals a,.sign a,.note a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.25rem .6rem .25rem 0}
.sign{margin-top:2rem}
.sign h2{font-size:2rem;font-weight:400}
@media(max-width:700px){.t2,.t4,.n2{margin-left:0}}
"""
})

DESIGNS.append({
"n": 8,
"name": "切り紙",
"aim": "不規則な色面を重ね、写真ははさみで抜いた形の中に置く",
"swatch": "#0e3b3a",
"ink": "#f6f1df",
"thumb": "homemeal.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;700;800&display=swap",
"body": r"""
<article class="cut">
<a class="back" href="../">一覧</a>
<section class="hero">
<div class="blob b1"></div>
<div class="blob b2"></div>
<div class="photo p1"><img src="$u_panda" alt="おもちゃの棚と、床に座るパンダのぬいぐるみ"></div>
<div class="words">
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</div>
</section>
<section class="band y">
<p>$daily</p>
<p>$group</p>
<p>$agey</p>
<p>$dev</p>
<p>$bus</p>
</section>
<section class="band photo-row">
<div class="photo p2"><img src="$u_meal" alt="手作りの和定食"></div>
<div>
<p>$lunch</p>
<p>$toy</p>
<p>$move</p>
</div>
</section>
<section class="band g">
<h2>$event_h</h2>
<p>$event</p>
<div class="photo p3"><img src="$u_forest" alt="フィールドの木々と作業"></div>
</section>
<section class="band coral">
<h2>$fam_h</h2>
<p>$kato</p>
<p>$door</p>
<div class="photo p4"><img src="$u_ext" alt="レオの建物"></div>
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
:root{--focus:#ffe08a}
body{background:#f6f1df;color:#14221f;font-family:"M PLUS Rounded 1c",sans-serif;font-size:1.12rem;line-height:1.8}
.back{position:absolute;z-index:4;top:.8rem;left:.8rem;background:#f6f1df;color:#0e3b3a;text-decoration:none;padding:.3rem .7rem;border-radius:999px}
.hero{position:relative;min-height:100svh;overflow:hidden;background:#0e3b3a;color:#f6f1df}
.blob{position:absolute;border-radius:50%}
.b1{width:46vw;height:46vw;background:#f2c14e;right:-8vw;top:-10vw}
.b2{width:26vw;height:26vw;background:#e36a4a;left:-12vw;bottom:-14vh}
.photo img{width:100%;height:100%;object-fit:cover}
.p1{position:absolute;width:min(34vw,440px);height:min(38vw,480px);right:7vw;top:24vh;border-radius:58% 42% 60% 40%;overflow:hidden}
.words{position:relative;z-index:2;padding:18vh 7vw 0;max-width:28rem}
h1{font-size:clamp(4rem,12vw,8rem);line-height:.9;margin:0;font-weight:800}
.lead{font-size:clamp(1.3rem,3vw,1.9rem);max-width:11em}
.band{padding:8vh 8vw;position:relative}
.band.y{background:#f2c14e;color:#1b1a12}
.band.g{background:#0e3b3a;color:#f6f1df}
.band.coral{background:#e36a4a;color:#1b120f}
.photo-row{display:flex;gap:2rem;align-items:center;background:#f6f1df}
.photo-row .p2{width:46%;height:360px;border-radius:40% 60% 46% 54%;overflow:hidden;flex:none}
.photo-row div{flex:1}
.p3{width:min(100%,680px);height:380px;border-radius:50% 50% 46% 54% / 38% 38% 62% 62%;overflow:hidden;margin-top:1rem}
.p4{width:min(100%,520px);height:300px;border-radius:30% 70% 60% 40%;overflow:hidden;margin:1rem 0}
.place{font-size:clamp(1.5rem,3vw,2.1rem);font-weight:700}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.3rem .7rem .3rem 0}
h2{font-size:1.7rem;margin:0 0 .4rem}
@media(max-width:760px){
  .p1{width:64vw;height:64vw;left:auto;right:4vw;bottom:4vh;top:auto}
  .b1{width:42vw;height:42vw;right:-14vw;top:-6vw}
  .words{padding-top:14vh}
  .photo-row{flex-direction:column}
  .photo-row .p2{width:100%;height:240px}
}
"""
})

DESIGNS.append({
"n": 9,
"name": "暗室",
"aim": "黒い部屋に、白い余白を大きく取った写真だけを置く",
"swatch": "#141311",
"ink": "#f3f1ea",
"thumb": "karate_class.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=BIZ+UDPMincho:wght@400;700&display=swap",
"body": r"""
<article class="darkroom">
<a class="back" href="../">一覧</a>
<header class="open">
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</header>
<figure class="print">
<img src="$u_panda" alt="おもちゃの棚と、床に座るパンダのぬいぐるみ">
<figcaption>$daily</figcaption>
</figure>
<figure class="print">
<img src="$u_toys" alt="おもちゃの部屋">
<figcaption>$toy</figcaption>
</figure>
<figure class="print small">
<img src="$u_blocks" alt="積み木">
<figcaption>$move</figcaption>
</figure>
<p class="aside">$group</p>
<p class="aside">$lunch</p>
<p class="aside">$agey $dev $bus</p>
<figure class="print">
<img src="$u_shichi" alt="行事・七輪">
<figcaption><span class="eh">$event_h</span> $event</figcaption>
</figure>
<figure class="print">
<img src="$u_karate" alt="武道の稽古">
</figure>
<figure class="print">
<img src="$u_meal" alt="手作りの和定食">
<figcaption>$lunch2</figcaption>
</figure>
<figure class="print">
<img src="$u_ext" alt="レオの建物">
<figcaption><span class="eh">$fam_h</span> $kato $door</figcaption>
</figure>
<section class="margin">
<p>$target</p>
<p>$age</p>
<p>$time</p>
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
:root{--focus:#e7c98a}
body{background:#141311;color:#f3f1ea;font-family:"BIZ UDPMincho",serif;line-height:1.85}
.back{position:absolute;top:.8rem;right:.8rem;color:#f3f1ea}
.open{padding:18vh 8vw 4vh;max-width:40rem}
h1{font-size:clamp(3.5rem,8vw,6rem);margin:.2rem 0;font-weight:700;letter-spacing:.12em}
.lead{font-size:clamp(1.25rem,2.6vw,1.7rem)}
.print{width:min(920px,92vw);margin:6vh auto;background:#f3f1ea;color:#1a1916;padding:4vw 4vw 1.4rem}
.print img{width:100%;max-height:78vh;object-fit:cover}
.print.small{width:min(560px,84vw)}
figcaption{padding-top:.8rem;font-size:1.05rem}
.aside{width:min(36rem,84vw);margin:2rem auto;font-size:1.15rem;color:#d9d3c6}
.margin{width:min(36rem,88vw);margin:4rem auto 2rem}
.place{font-size:1.5rem}
a{text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.35rem .75rem .35rem 0}
h2{font-size:2rem}
"""
})

DESIGNS.append({
"n": 10,
"name": "絵巻",
"aim": "一日を横方向の絵巻にし、狭い画面では縦にほどく",
"swatch": "#d7e3d2",
"ink": "#1a2a22",
"thumb": "forest_work.jpg",
"fonts": "https://fonts.googleapis.com/css2?family=Kaisei+Decol:wght@400;700&display=swap",
"body": r"""
<article class="emaki">
<a class="back" href="../">一覧</a>
<div class="scroll">
<section class="panel title">
<p class="role">$role</p>
<h1>レオ</h1>
<p class="lead">$lead</p>
</section>
<section class="panel pic"><img src="$u_panda" alt="おもちゃの棚と、床に座るパンダのぬいぐるみ"><p>$daily</p></section>
<section class="panel"><p>$group</p><p>$agey</p><p>$dev</p><p>$bus</p></section>
<section class="panel pic"><img src="$u_toys" alt="おもちゃの部屋"><p>$toy</p></section>
<section class="panel pic"><img src="$u_karate" alt="武道の稽古"><p>$move</p></section>
<section class="panel pic"><img src="$u_forest" alt="フィールドの木々と作業"><h2>$event_h</h2><p>$event</p></section>
<section class="panel pic"><img src="$u_meal" alt="手作りの和定食"><p>$lunch</p><p>$lunch2</p></section>
<section class="panel pic"><img src="$u_ext" alt="レオの建物"><h2>$fam_h</h2><p>$kato</p><p>$door</p></section>
<section class="panel">
<p>$target</p><p>$age</p><p>$time</p>
<p class="place">$place</p><p>$walk</p><p>$car</p><p>$bus2</p><p>$fee</p>
</section>
<section class="panel last">
<p class="evalh">$eval_h</p>
<p class="evals">$evals</p>
<p>$pt_a　$pt_s</p>
<p>$as_a　$as_s</p>
<h2>$visit_h</h2>
<p><a href="$url_line">LINE</a></p>
<p><a href="$tel_href">$tel</a></p>
</section>
</div>
</article>
""",
"css": r"""
:root{--focus:#c4492c}
body{background:#1a2a22;color:#1a2a22;font-family:"Kaisei Decol",serif}
.back{position:fixed;z-index:5;top:.6rem;left:.6rem;background:#f4f7ef;color:#1a2a22;text-decoration:none;padding:.3rem .6rem}
.scroll{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;height:100svh}
.panel{flex:0 0 78vw;scroll-snap-align:start;height:100svh;padding:12vh 6vw 8vh;background:#e7f0df;overflow:auto}
.title{flex-basis:64vw}
.panel.pic{padding:0;position:relative;background:#102018;color:#f4f7ef}
.panel img{width:100%;height:100svh;object-fit:cover}
.panel.pic p,.panel.pic h2{position:absolute;right:6vw;left:auto;bottom:8vh;margin:0;max-width:min(24rem,70%);font-size:1.2rem;text-align:right;text-shadow:0 1px 10px rgba(0,0,0,.55)}
.title{background:#d7e3d2}
h1{font-size:clamp(4rem,10vw,8rem);margin:0;line-height:1}
.lead{font-size:clamp(1.3rem,3vw,2rem)}
.place{font-size:1.7rem}
h2{font-size:1.5rem}
a{color:inherit;text-decoration:underline;text-underline-offset:.18em}
.evals a{display:inline-block;margin:.3rem .7rem .3rem 0}
.last h2{font-size:2.2rem}
@media(max-width:760px){
  .scroll{flex-direction:column;overflow-x:hidden;height:auto;scroll-snap-type:y mandatory}
  .panel{flex-basis:auto;width:100%;height:auto;min-height:100svh}
  .title{min-height:78svh}
  .panel img{height:70vh}
  .panel.pic p,.panel.pic h2{position:relative;left:auto;right:auto;bottom:auto;text-align:left;max-width:none;padding:1rem 6vw 1.4rem;text-shadow:none}
}
"""
})
