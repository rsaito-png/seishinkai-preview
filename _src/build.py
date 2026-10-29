import re as _re
import os, json, html, shutil
import os as _o
OUT=_o.environ.get('OUT','/workspace/site_v9'); CONTENT=_o.environ.get('CONTENT',''); DUMP=_o.environ.get('DUMP','')
import sys as _s; _s.path.insert(0,_o.path.dirname(_o.path.abspath(__file__))); import content_io as CI; BASE='https://www.psr-seishinkai.org'
ORG='一般社団法人 心理社会的リハビリテーション・星心会'; TEL='059-315-0697'
ADDR='〒512-8048 三重県四日市市山城町59-4'
SNS=[('X','https://x.com/gcbfhq'),('Instagram','https://www.instagram.com/psr_seishinkai/'),('Threads','https://www.threads.com/@psr_seishinkai')]
ICON={'X':'<svg viewBox="0 0 24 24"><path d="M18.9 2H22l-7.6 8.7L23 22h-6.8l-5.3-6.9L4.8 22H1.7l8.1-9.3L1 2h7l4.8 6.3L18.9 2zm-1.2 18h1.9L7.4 3.9H5.4L17.7 20z"/></svg>',
'Instagram':'<svg viewBox="0 0 24 24"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 3.3.1 4.8 1.7 4.9 4.9.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 3.2-1.7 4.8-4.9 4.9-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-3.3-.1-4.8-1.7-4.9-4.9C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8C2.4 3.9 3.9 2.4 7.2 2.3 8.4 2.2 8.8 2.2 12 2.2zM12 0C8.7 0 8.3 0 7.1.1 2.7.3.3 2.7.1 7.1 0 8.3 0 8.7 0 12s0 3.7.1 4.9c.2 4.4 2.6 6.8 7 7 1.2.1 1.6.1 4.9.1s3.7 0 4.9-.1c4.4-.2 6.8-2.6 7-7 .1-1.2.1-1.6.1-4.9s0-3.7-.1-4.9c-.2-4.4-2.6-6.8-7-7C15.7 0 15.3 0 12 0zm0 5.8a6.2 6.2 0 100 12.4 6.2 6.2 0 000-12.4zM12 16a4 4 0 110-8 4 4 0 010 8zm6.4-11.8a1.4 1.4 0 100 2.9 1.4 1.4 0 000-2.9z"/></svg>',
'Threads':'<svg viewBox="0 0 24 24"><path d="M17.7 11.1l-.3-.1c-.2-3.3-2-5.1-5-5.2h-.1c-1.8 0-3.3.8-4.2 2.2l1.6 1.1c.7-1 1.7-1.2 2.6-1.2 1 0 1.8.3 2.3.9.4.4.6 1 .7 1.8-.8-.1-1.7-.2-2.6-.1-2.6.1-4.3 1.7-4.2 3.8.1 1.1.6 2 1.5 2.6.8.5 1.8.8 2.8.7 1.4-.1 2.4-.6 3.2-1.5.6-.7.9-1.6 1.1-2.7.7.4 1.2.9 1.4 1.6.5 1.1.5 2.9-1 4.4-1.3 1.3-2.9 1.9-5.3 1.9-2.6 0-4.6-.9-5.9-2.5C5.2 17.1 4.5 14.8 4.5 12s.7-5.1 1.9-6.6C7.7 3.8 9.7 3 12.3 3c2.7 0 4.7.8 6 2.5.7.8 1.2 1.8 1.5 3l1.9-.5c-.4-1.5-1-2.7-1.9-3.8C18.2 2.1 15.7 1 12.3 1h-.1C8.9 1 6.4 2.1 4.7 4.2 3.2 6.1 2.5 8.7 2.5 12s.7 5.9 2.2 7.8c1.7 2.1 4.2 3.2 7.5 3.2h.1c2.9 0 5-.8 6.7-2.5 2.3-2.3 2.2-5.1 1.4-6.9-.5-1.2-1.6-2.2-2.7-2.5zm-5 4.9c-1.1.1-2.3-.4-2.4-1.5 0-.8.6-1.7 2.4-1.8h.6c.7 0 1.3.1 1.9.2-.2 2.7-1.5 3-2.5 3.1z"/></svg>'}
SVCS=[ # key,name,url,cat,line,thumb
('suishodama','水晶玉','suishodama/','メンタルヘルスコーディネート（環境調整）','眠れない、気分の波がある。原因の環境から手を打ちます。','consult'),
('shichirin','しちりんの会','shichirin/','自費参加｜手続き不要','七輪で火を起こし、焼いて食べます。手続きも診断も要りません。','fish'),
('rydeen','RYDEEN','rydeen/','PCで働く｜2026年11月1日開所','仕事が続かない人が、PCの実務で働く職場です。',None),
('ryozanpaku','梁山泊','ryozanpaku/','メンタルピアレジデンス｜家賃 月8万円','仕事はできる人が、働き続けるための住まいです。親元を出る拠点にもなります。',None),
('chamu','茶夢','chamu/','統合失調症・自閉症の方のための日中の居場所','料理・喫茶・読書・アートで、日中を安全に過ごす場所です。','counter'),
('kintoun','金斗雲','kintoun/','訪問｜アウトリーチ','家族が家から出ないなら、こちらから自宅へ行きます。','homemeal'),
('leo','レオ','leo/','子どもの情緒','おもちゃ、武道、庭いじり。遊びの中で情緒を整えます。','panda'),
('parent','ペアレントトレーニング','leo/parent-training/','保護者向けプログラム','子どもを変える前に、親の関わり方を変えます。','consult'),
('assess','発達検査','leo/assessment/','WISC-V・新版K式','特性を数値で掴み、支援に直結させます。','record'),
('employment','雇用定着サポート','business/employment/','専任担当による職場定着','メンタル不調・発達特性のある社員に専任の担当者をつけます。',None),
('stress','ストレスチェック','business/stress-check/','アドラー心理学×ラインケア','実施して終わらせず、組織を変える材料にします。','karate_sit'),
('agent','エージェントコンサル','business/agent-consulting/','AIエージェント導入','AIエージェントを、事業所の戦力にします。',None),
('sct','実施者養成研修','business/stress-check-training/','ストレスチェック実施者養成研修','歯科医師・看護師・精神保健福祉士・公認心理師の方のための実施者養成研修です。','karate_sit'),
('training','研修','business/training/','児童指導員研修・合気道研修','体を使って支援を学ぶ研修を、土日に行います。','karate_bow')]
def _docmeta(url):
    """name (# line) and first sentence of リード文 from content/<slug>.md, if present"""
    if not CONTENT: return None
    f=_o.path.join(CONTENT,CI.slug(url)+'.md')
    if not _o.path.exists(f): return None
    secs=CI.split(open(f,errors='ignore').read()); h1=next((t for lv,t,_ in secs if lv==1),None)
    lead=next((ls for lv,t,ls in secs if lv==2 and t=='リード文'),[])
    lead=[x for x in lead if x!=CI.NOTE]
    import re as _r
    first=''
    if lead:
        t=_r.sub(r'\*\*|\[([^\]]+)\]\([^)]*\)',lambda m:m.group(1) or '',lead[0]).strip()
        m=_r.match(r'.*?[。！？]',t); first=m.group(0) if m else t
    return h1,first
def _short(n):
    import re as _r
    b=_r.sub(r'[（(].*?[）)]','',n).strip()
    if '・' in b: b=b.split('・')[-1]
    return b.split()[-1] if ' ' in b or '　' in b else b
SHOW_FAQ=False
DUPLOG=[]  # FAQセクションは非表示（FAQPage JSON-LDは出力）
DOCMETA={}
for _i,_s in enumerate(SVCS):
    _m=_docmeta(_s[2])
    if _m and _m[0]:
        DOCMETA[_s[2]]=_m
        SVCS[_i]=(_s[0],_short(_m[0]),_s[2],'',_m[1] or _s[4],_s[5])
SV={s[0]:s for s in SVCS}
AUD=[('self','ご本人','FOR YOU','眠れない、気分の波がある、仕事が続かない、親元を出たい。ご自身のことで困っている大人の方へ。',['suishodama','shichirin','rydeen','ryozanpaku'],'眠れない・仕事が続かない・親元を出たい'),
('family','ご家族','FOR FAMILIES','家族が家から出ない、日中の行き場がない。ご家族の方へ。本人が動けなくても、ご家族からの相談で始められます。',['kintoun','chamu'],'家族が家から出ない・日中の行き場がない'),
('parents','お子さまの保護者','FOR PARENTS','落ち着かない、かんしゃくが多い、集団が苦手なお子さまの保護者の方へ。',['leo','parent','assess'],'落ち着かない・かんしゃく・発達が気になる'),
('partners','企業・支援機関','FOR PARTNERS','企業、JEED（高齢・障害・求職者雇用支援機構）、ハローワーク、労働局の方へ。職場定着を、職場と住まいの両方から支えます。',['employment','stress','sct','agent','training'],'職場定着・ストレスチェック・研修')]
def esc(s): return html.escape(s)
def P(t): return f'<span class="ph">要確認：{t}</span>'
PH=set()
def ph(t): PH.add(t); return P(t)

def head(rel,title,desc,path,ld=None):
    graph=[{"@type":"Organization","@id":BASE+"/#org","name":ORG,"alternateName":"星心会","url":BASE+"/","telephone":TEL,
      "address":{"@type":"PostalAddress","postalCode":"512-8048","addressCountry":"JP","addressRegion":"三重県","addressLocality":"四日市市","streetAddress":"山城町59-4"},
      "areaServed":["四日市市","三重県","名古屋市","愛知県"],"sameAs":[u for _,u in SNS],"logo":BASE+"/img/logo_black.svg"}]
    if ld: graph+=ld
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<!-- TEST PHASE: remove the next line at launch -->
<meta name="robots" content="noindex,nofollow">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{BASE}/{path}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="website"><meta property="og:image" content="{BASE}/img/hero_top.jpg">
<link rel="icon" href="{rel}img/favicon.svg" type="image/svg+xml"><link rel="icon" href="{rel}img/favicon.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="{rel}img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Noto+Sans+JP:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}assets/site.css">
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@graph":graph},ensure_ascii=False)}</script>
</head>
<body>
'''
def sns_html(labels=False):
    return '<div class="sns">'+''.join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{ICON[n]}{(" "+n) if labels else ""}</a>' for n,u in SNS)+'</div>'
def header(rel):
    dr=''.join(f'<h4>{lab}</h4>'+''.join(f'<a href="{rel}{SV[k][2]}">{SV[k][1]}{f'<small>{SV[k][3].split("｜")[0]}</small>' if SV[k][3] else ''}</a>' for k in ks) for _,lab,_,_,ks,_h in AUD)
    return f'''<header class="gh"><a class="logo" href="{rel}"><img src="{rel}img/mark_black.svg" alt=""><span>星心会</span></a>
<nav><a href="{rel}#self">ご本人</a><a href="{rel}#family">ご家族</a><a href="{rel}#parents">保護者</a><a href="{rel}#partners">企業・支援機関</a><a href="{rel}access/">アクセス</a>{sns_html()}</nav>
<a class="cta-btn" href="{rel}contact/">相談する</a><button class="menu-btn" aria-label="メニュー"><i></i><i></i></button></header>
<div class="drawer">{dr}
<h4>INFO</h4><a href="{rel}business/">企業・支援機関の方へ</a><a href="{rel}about/">星心会について</a><a href="{rel}access/">アクセス<small>名古屋から30分</small></a><a href="{rel}faq/">よくある質問</a><a href="{rel}contact/">相談する</a>
{sns_html()}</div>
'''
def footer(rel):
    cols=''.join(f'<div><h5>{lab}</h5><ul>'+''.join(f'<li><a href="{rel}{SV[k][2]}">{SV[k][1]}</a></li>' for k in ks)+'</ul></div>' for _,lab,_,_,ks,_h in AUD)
    return f'''<footer class="gf"><div class="in">
<div><a class="logo" href="{rel}"><img src="{rel}img/mark_black.svg" alt=""><span>星心会</span></a><p style="margin-top:12px">{ORG}<br>{ADDR}<br>TEL <a href="tel:0593150697">{TEL}</a><br>名古屋西ICから車で約30分／三岐線 山城駅から徒歩5分</p></div>
{cols}
<div><h5>INFO</h5><ul><li><a href="{rel}business/">企業・支援機関の方へ</a></li><li><a href="{rel}about/">星心会について</a></li><li><a href="{rel}access/">アクセス</a></li><li><a href="{rel}faq/">よくある質問</a></li><li><a href="{rel}contact/">相談する</a></li><li><a href="{rel}privacy/">プライバシーポリシー</a></li><li><a href="{rel}sitemap/">サイトマップ</a></li></ul>
<h5 style="margin-top:20px">FOLLOW</h5>{sns_html(True).replace('class="sns"','class="sns" style="flex-direction:column;align-items:flex-start;gap:10px"')}</div>
<p class="cp">© 星心会 {ORG}</p></div></footer>
<a class="fab" href="{rel}contact/">相談する</a>
<script src="{rel}assets/site.js"></script>
</body></html>'''
def write(path,body):
    fp=os.path.join(OUT,path,'index.html') if not path.endswith('.html') else os.path.join(OUT,path)
    os.makedirs(os.path.dirname(fp),exist_ok=True); open(fp,'w').write(body)
def relof(path): return '../'*path.count('/') if path else ''

def faq_ld(faq): return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":html.unescape(__import__('re').sub('<[^>]+>','',a))}} for q,a in faq]}

COMMON=[('診断がなくてもいいですか？','かまいません。診断の有無は問いません。今の困りごとから始めます。'),
('病院に行ったことがないのですが。','問題ありません。精神科に通ったことがあるかどうかは前提にしていません。'),
('何をしてくれるのですか？','{what}'),
('手続きが難しそうです。','書類と手続きはこちらで進めます。知識は要りません。'),
('いくらかかりますか？','公的制度を使います。所得に応じた負担上限があり、多くは自己負担なしか低額です。金額は初回連絡でお示しします。'),
('家族に知られずに相談できますか？','できます。連絡方法は本人の指定に従います。')]
CP={'suishodama/','rydeen/','chamu/','leo/','kintoun/','ryozanpaku/'}
def service_page(d):
    path=d['path']; rel=relof(path); d['_old']=path in OLD; ovr=False
    cf=CONTENT and _o.path.join(CONTENT,CI.slug(path)+'.md')
    if cf and _o.path.exists(cf) and not DUMP:
        r=CI.parse_page(open(cf,errors='ignore').read(),d,ph); ovr=True
        if 'old' in r: OLD[path]=r.pop('old')
        d.update(r)
    if path in DOCMETA:
        h1,first=DOCMETA[path]
        d['name']=h1; d['title']=h1+'｜星心会'; d['cat']=d.pop('_pre','')
        if first and not d.get('keep_desc'): d['desc']=first
        d['rel']=[(SV[k][1] if (k:=next((x[0] for x in SVCS if x[2]==u),None)) else n,u) for n,u in d.get('rel',[])]
    if path in CP and not ovr:
        have=' '.join(q for q,a in d['faq'])
        add=[(q,a.format(what=__import__('re').sub('<[^>]+>','',d['sub']))) for q,a in COMMON if (q.startswith('診断') or q[:4] not in have and not (path=='chamu/' and q.startswith('家族に'))) and not (path=='leo/' and q.startswith('家族')) and not (q.startswith('いくら') and ('費用' in have or '料金' in have or path in ('ryozanpaku/','chamu/')))]
        d['faq']=add+[f for f in d['faq'] if not f[0].startswith('診断がなくても')]
    if DUMP: _o.makedirs(DUMP,exist_ok=True); open(_o.path.join(DUMP,CI.slug(path)+'.md'),'w').write(CI.page_md(d,OLD.get(path)))
    ld=[dict({"@type":d.get('type','LocalBusiness'),"name":d['name'],**({"logo":BASE+"/img/"+d['logo'].replace('.webp','.png'),"image":BASE+"/img/"+d['logo'].replace('.webp','.png')} if d.get('logo') else {}),"description":d['desc'],"parentOrganization":{"@id":BASE+"/#org"},"telephone":d.get('tel',TEL),"url":BASE+"/"+path},**({"address":d['addr_ld']} if d.get('addr_ld') else {}),**({"audience":d['audience']} if d.get('audience') else {})),faq_ld(d['faq'])]
    o=head(rel,d['title'],d['desc'],path,ld)+header(rel)
    if d.get('photo'):
        o+=f'<section class="hero{" short" if d.get("short") else ""}"><div class="bg" style="background-image:url({rel}img/{d["photo"]}.jpg);background-position:{d.get("pos","50% 50%")}"></div>'
    else:
        o+=f'<section class="hero type{" short" if d.get("short") else ""}"><div class="big">{d["big"]}</div>'
    mark=f'<img class="mark" src="{rel}img/{d["mark"]}" alt="">' if d.get('mark') else ''
    o+=f'''<div class="hin">{mark}{f'<img class="plogo" src="{rel}img/{d["logo"]}" alt="RYDEEN ロゴ" width="120" height="120">' if d.get('logo') else ''}<p class="en">{d["en"]}</p><h1 class="{'long' if len(d["name"])>5 else ''}{' deco' if d.get('deco') else ''}">{d["name"].replace("ストレスチェック実施者","ストレスチェック<wbr>実施者<wbr>").replace("<wbr>養成研修","養成<wbr>研修") if d.get("deco") else d["name"]}</h1>{f'<p class="svc">{d["cat"]}</p>' if d.get("cat") else ''}
<p class="copy">{''.join(f"<span>{x}</span>" for x in d["copy"])}</p><p class="sub">{d["sub"]}</p>{d.get("badge","")}{f'<a class="go" href="#what">{d["go"]}</a>' if d.get("go") else ''}</div>
<p class="acc">{d["acc"]}</p></section>'''
    if path in OLD:
        if d.get('gal'): o+=(f'<div style="max-width:1040px;margin:0 auto;padding:24px 24px 56px"><img src="{rel}img/{d["gal"][0][0]}.jpg" alt="{esc(d["gal"][0][1])}" loading="lazy" style="display:block;width:100%;max-width:1040px;height:auto;margin:0 auto"></div>' if len(d['gal'])==1 else '<div class="gal">'+''.join(f'<img src="{rel}img/{g}.jpg" alt="{esc(a)}" loading="lazy">' for g,a in d['gal'])+'</div>')
        o+=old_html(OLD[path])
        if d.get('extra'): o+=d['extra'](rel)
    else:
        chips=''.join(f'<button data-a="{esc(a.replace('<br>','\n'))}">{n}{f"<small>{s}</small>" if s else ""}</button>' for n,s,a in d['what'])
        o+=f'''<div class="dark"><section class="blk wide" id="what"><div class="h"><span class="en">WHAT</span><h2>{_re.sub(r"[0-9０-９]+つの",f"{len(d.get('what') or [])}つの",d["what_h"],count=1) if d.get("what") else d["what_h"]}</h2><p>押すと内容が表示されます。</p></div>
    <div>{f'<p class="intro" style="margin:0 0 1.2em;font-size:1.05rem;line-height:1.9">{d["what_intro"]}</p>' if d.get("what_intro") else ""}<div class="chips">{chips}</div><p class="ans" style="white-space:pre-line">押すと内容が表示されます。</p></div></section></div>'''
        if d.get('gal'): o+=(f'<div style="max-width:1040px;margin:0 auto;padding:24px 24px 56px"><img src="{rel}img/{d["gal"][0][0]}.jpg" alt="{esc(d["gal"][0][1])}" loading="lazy" style="display:block;width:100%;max-width:1040px;height:auto;margin:0 auto"></div>' if len(d['gal'])==1 else '<div class="gal">'+''.join(f'<img src="{rel}img/{g}.jpg" alt="{esc(a)}" loading="lazy">' for g,a in d['gal'])+'</div>')
        if d.get('extra'): o+=d['extra'](rel)
        o+=f'''<section class="blk" id="flow"><div class="h"><span class="en">PROCESS</span><h2>進め方</h2><p>ボタンで一段ずつ進みます。</p></div>
    <div class="steps" data-cta="#contact"><script type="application/json">{json.dumps(d["flow"],ensure_ascii=False)}</script><div class="sbar"></div>
    <div class="card"><div class="num"></div><div class="k"></div><h3></h3><p></p><div class="ctl"><button class="ghost prev">もどる</button><button class="btn next">次へ</button></div></div></div></section>'''
    _bt=lambda h:_re.sub(r'\s|　','',_re.sub('<[^>]+>','',h))
    B=_bt(o.split('<p class="acc">')[1].split('</section>',1)[1]) if '<p class="acc">' in o else ''
    def _dup(v):
        t=_bt(v.replace('<br>',''))
        if len(t)>=4 and t in B: return True
        m=_re.search(r'([^\s　、（(]+駅).*?(徒歩\d+分)',t)
        if m and m.group(1).replace('三岐線','') in B and _re.search(_re.escape(m.group(1).replace('三岐線',''))+r'.{0,4}'+m.group(2),B): return True
        return False
    if path in OLD and d['info']:
        _n=[(k,v) for k,v in d['info'] if not _dup(v)]
        if len(_n)<len(d['info']): DUPLOG.append((path,'info',[k for k,v in d['info'] if (k,v) not in _n])); d['info']=_n
    if d['info']: o+='<section class="blk wide" id="info"><div class="h"><span class="en">INFORMATION</span><h2>対象・費用・場所</h2></div><dl class="info">'+''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k,v in d['info'])+'</dl></section>'
    if SHOW_FAQ: o+='<section class="blk wide" id="faq" style="padding-top:0"><div class="h"><span class="en">FAQ</span><h2>よくある質問</h2></div><div>'+''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in d['faq'])+'</div></section>'
    o+='<div class="rel"><span class="en">RELATED</span><div class="two">'+''.join(f'<a class="btn" style="text-align:center;letter-spacing:.1em" href="{rel}{u}">{n} →</a>' for n,u in d['rel'])+'</div></div>'
    tel=d.get('tel',TEL); line=f'{rel}contact/#line'
    B=_bt(o.split('<p class="acc">')[1].split('</section>',1)[1].split('class="rel"')[0]) if '<p class="acc">' in o else ''
    if d.get('acc'):
        _ap=d['acc'].split('／'); _keep=[x for x in _ap if not _dup(x)]
        if len(_keep)<len(_ap):
            DUPLOG.append((path,'acc',[x for x in _ap if x not in _keep]))
            o=o.replace(f'<p class="acc">{d["acc"]}</p>',f'<p class="acc">{"／".join(_keep)}</p>' if _keep else '',1)
    _tdup=path in OLD and _bt(tel) in B
    if _tdup: DUPLOG.append((path,'tel',[tel]))
    cm=f'<img class="mark" src="{rel}img/{d["mark"]}" alt="">' if d.get('mark') else ''
    o+=f'''<section class="cta" id="contact">{cm}<p class="en" style="color:var(--hi)">CONTACT</p><h2>{d.get("cta_h","相談する")}</h2>
<div class="row"><a class="w" href="{line}">LINE</a><a class="o" href="tel:{tel.replace("-","")}">電話</a></div>{'' if _tdup else f'<a class="tnum" href="tel:{tel.replace("-","")}">{tel}</a>'}{d.get("cta_note","")}</section>'''
    o+=footer(rel); write(path,o)

def simple_page(path,title,desc,h1,en,body,photo=None,ld=None,sub=''):
    rel=relof(path); o=head(rel,title,desc,path,ld)+header(rel)
    bg=f'<div class="bg" style="background-image:url({rel}img/{photo}.jpg)"></div>' if photo else f'<div class="big">{en.split()[0][:2]}</div>'
    o+=f'<section class="hero short{"" if photo else " type"}" style="min-height:{"46svh" if photo else "34svh"}">{bg}<div class="hin"><p class="en">{en}</p><h1 class="long">{h1}</h1>{f"<p class=sub>{sub}</p>" if sub else ""}</div></section>'
    o+=body(rel)+footer(rel); write(path,o)

ACC='四日市市山城町／三岐線 山城駅から徒歩5分／名古屋西ICから車で約30分'
ACC2='四日市市あさけが丘／三岐線 山城駅から徒歩12分／名古屋西ICから車で約30分'
YAMA={"@type":"PostalAddress","postalCode":"512-8048","addressCountry":"JP","addressRegion":"三重県","addressLocality":"四日市市","streetAddress":"山城町59-4"}
ASAKE={"@type":"PostalAddress","postalCode":"512-8055","addressCountry":"JP","addressRegion":"三重県","addressLocality":"四日市市","streetAddress":"あさけが丘2-1-42"}
PLACE_Y='三重県四日市市山城町59-4<br>三岐線 山城駅から徒歩5分<br>名古屋西ICから車で約30分／四日市駅から直通バス'
PLACE_A='三重県四日市市あさけが丘2-1-42<br>三岐線 山城駅から徒歩12分<br>名古屋西ICから車で約30分'
NAGOYA=('名古屋在住でも利用できますか？','相談はできます。居住地によって使える制度が異なるため、初回連絡時に確認し、手続きはこちらで進めます。')

PAGES=[]
def partners(rel): return f'''<section class="blk wide" id="partners"><div class="h"><span class="en">FOR PARTNERS</span><h2>企業・支援機関の方へ</h2><p>企業、JEED（高齢・障害・求職者雇用支援機構）、ハローワーク、労働局の方へ。</p></div><div>
<ul class="lst"><li><b>職場定着を支える住まい</b>メンタルピアレジデンス・梁山泊は、ケアの付いた一般の賃貸住居です。現在、入居者のうち3人が障害者枠で一般就労しています。家賃は月8万円で、朝夕食事付きです。ほかに費用はかかりません。</li>
<li><b>紹介・連携の窓口</b>入居の紹介、職場定着の連携、職場との情報共有の方法は、星心会本部が一本で受けます。本人の同意を前提に進めます。</li>
<li><b>定着支援と一体で</b>専任担当による<a href="{rel}business/employment/" style="display:inline;color:var(--hi)">雇用定着サポート</a>と住まいを組み合わせて提供できます。</li></ul>
<div class="cta" style="padding:28px 20px;margin-top:22px;text-align:left"><p class="en" style="color:var(--hi)">CONTACT</p><p style="margin:6px 0 14px">紹介・連携の問い合わせ</p><div class="row" style="margin:0;max-width:none"><a class="o" href="tel:0593150697" style="text-align:center">電話 059-315-0697</a><a class="w" href="{rel}contact/" style="text-align:center">フォーム</a></div></div></div></section>'''
AUD_P=[{"@type":"Audience","audienceType":"企業の人事・雇用担当"},{"@type":"Audience","audienceType":"JEED（高齢・障害・求職者雇用支援機構）"},{"@type":"Audience","audienceType":"ハローワーク"},{"@type":"Audience","audienceType":"労働局"},{"@type":"Audience","audienceType":"働き続けたい社会人・親元を出たい人"}]
TEJUN='書類と手続きはこちらで進めます。'
OLD={}
OLD['ryozanpaku/']=[('h','「実家を出たい。でも、一人暮らしのイメージがつかない…」'),('p','お金のことや日中の過ごし方など、分からないことがあっても大丈夫です。<br>あなたの「出たい」という気持ちから、一緒に現実的な形にしていきます。'),
('h','サポート内容'),('dl',[('ご相談','まずは今のお気持ちや不安をお伺いします'),('住まい探し','一人暮らしの準備と住まいの確保'),('生活サポート','ヘルパーによる日常の支援'),('居場所づくり','日中に安心して過ごせる場所などのご案内')]),
('h','費用・住まいについての安心ポイント'),('dl',[('公的制度の活用','公的制度を利用し、自己負担を大きく抑えます。'),('各種申請の相談','お金に関する各種申請のご相談も承ります。'),('住まいの紹介','面談後に一人暮らしが可能と判断された方には、格安物件をご案内します。')]),
('p','「まだ決める段階じゃない…」という方も大歓迎です。<br>専門の相談員がご対応します。'),
('note','メンタルピアレジデンス・梁山泊は、働き続けるための住まいです。家賃は月8万円です。ほかに費用はかかりません。')]
OLD['kintoun/']=[('h','アウトリーチってなに？'),('p','「困っているのに、自分から相談できない人」のところへ、私たちから積極的に関わっていくことです。'),('p','特に、精神的な不調から外に出にくくなっている人。いわゆる「ひきこもり」の状態にある人や、そのご家族。'),('p','「誰にも会いたくない」「窓口に行く気力がない」そんなときでも、こちらから手を差し伸べます。'),
('h','私たちが大切にしていること'),('p','相談の窓口と訪問の支援を一緒に運営しています。'),('ul',['まずは話を聞くことから始める','無理に外に出そうとしない','「誰かが気にかけてくれている」と感じてもらえる関係をつくる']),('p','「利用するかわからない」という段階でも大丈夫です。'),
('h','費用の心配も少なくできます'),('p','公的制度を利用すると、自己負担を大きく抑えることができます。<br>（所得に応じて負担上限が設定されており、多くの方が無料または低額で利用されています）<br>まずは制度の説明からでも構いません。'),
('h','こんなときにご相談ください'),('ul',['家族が長く家から出られなくなっている','精神的な不調で、相談に行けない','どこに相談していいかわからない','費用が心配でサービスをためらっている']),('p','まずはお話だけでも大丈夫です。'),('h','スタッフ'),('p','精神保健福祉士など有資格者がご対応いたします')]
OLD['chamu/']=[('note','統合失調症・自閉症の方のための日中の居場所です。'),('h','社会参加への第一歩はこちらからどうぞ。'),('p','似た者同士で安心できる喫茶スペースです。人が苦手でも静かで安全な外出をお楽しみいただけます。'),('p','なお一部スタッフは当施設利用者です。ご希望の方には各種相談もお受けできます。'),
('dl',[('営業時間','土・日・祝 定休　11～15時'),('申込み方法','不在のこともありますので必ず予約をお願いします。'),('アクセス','四日市市あさけが丘2-1-42（三岐鉄道三岐線 山城駅 徒歩12分）')])]
OLD['shichirin/']=[('p','七輪を使った簡易バーベキューを行なっております。'),('p','火をつけるところからみなさんに体験いただいております。'),('p','火に癒されると評判のプログラムに参加してみませんか？'),('dl',[('日時','不定期土曜日 11:00～'),('場所','菰野町田光'),('参加費用','食材費込み3,000円')]),('note','自費参加です。手続きは要りません。')]
OLD['leo/']=[('h','こどもの情操教育 レオ'),('h','レオでは・・・'),('ul',['日常生活に必要な動作の指導をしたり、人や物を通して情緒の安定を図ったりします。','集団療育をしています。<br>１部：11:00～14:30<br>２部：放課後～17:00','昼食を提供します。（１回３００円）<br>手作りの和食で情緒を養います。','対象年齢は、満１歳から小学校に上がるまでのお子様です。','主に発達障害のお子様をお預かりします。','地域によっては、送迎のご相談も承ります。']),
('p','たくさんのおもちゃの中から、自分の好きなものを見つけたり、一緒に少し難しいものにもチャレンジしたりします。（「認知・行動」「言語・コミュニケーション」「人間関係・社会性」）'),('p','武道やヨガ、農作業を通じて心身を鍛えます（「健康・生活」「運動・感覚」）。格闘家や農家さんのところへ行き<b>地域連携</b>を行なっています。'),
('h','【行事】'),('p','菰野町のフィールドにお出かけして、遊びながら自然観察をしたり、七輪で火を起こしをしたりします。'),('h','家族支援・進路相談（移行支援）'),('p','※経験豊富な加藤が当事業所の研修講師も担当し、職員の質の向上に取り組んでいます。'),('p','建物の２階です。看板のあるドアからお入りください。')]
OLD['leo/assessment/']=[('h','当施設の特徴：検査から学習支援への直結'),('p','検査で「特性」を可視化するだけでなく、そのデータを日々の学習指導に反映させます。高い専門性を持つ講師陣が子どもの支援現場での長い経験に基づいた具体的な学習アプローチ（視覚・聴覚特性に応じた指導など）を設計します。'),
('dl',[('WISC-V（ウィスク・ファイヴ）','対象：小1 ～ 高2'),('新版K式発達検査','対象：未就学児'),('料金','各 25,000円（税込）<br>※事前面談、検査実施、結果報告書作成、フィードバック面談を含みます。'),('担当','あんどう（公認心理師、滋賀大学教育学部卒業）')]),
('h','⚠️ 公的機関への提出に関するご注意'),('p','当施設は公式マニュアルに則り厳密に検査を実施しますが、市役所の福祉窓口や教育委員会などの公的機関によっては、民間施設が実施した結果を「公的な判定基準（支援学級への入級判定など）」として受理しない（有効と認めない）場合があります。'),('p','自治体により「医療機関での検査に限る」等の規定があるため、特定の申請手続きを目的とされる場合は、必ず事前に提出先窓口へ有効性をご確認の上お申し込みください。')]
OLD['business/stress-check/']=[('h','ストレスチェックを、組織が変わる最強のきっかけに。'),('p','アドラー心理学 × ラインケア支援'),('h','⚠️ 貴社でこんな「形式だけ」のストレスチェックになっていませんか？'),('ul',['✕ 実施しても、データが集まるだけで職場は何も変わらない','✕ 産業医面談は「休職の判定」のみ。予防や復職フォローがない','✕ 管理職が部下のメンタル対応に悩み、一人で抱え込んでいる']),
('h','OUR SOLUTION　診断から現場改善・定着まで、プロフェッショナルが一社完結で支援。'),('dl',[('01 実効性のある「管理職研修」','単なる座学ではありません。<b>自社の診断データを題材</b>に、具体的なケーススタディやグループワークを実施。現場ですぐに使える部下との接し方やラインケアの実践力を養います。'),('02 意識を変えるアドラー流「個別面談」','高ストレス者や悩める管理職への1on1を実施。アドラー心理学に基づき、環境や他人のせいに（他責）するのではなく、<b>「今、自分にできることは何か」</b>へ意識を向けさせ、自律的な解決を促す心理支援を行います。'),('03 組織全体で支える「ラインケア定着支援」','個人の面談記録を残すだけでなく、許可を得た上で現場の管理職へ具体的な対応策をフィードバック。人事に報告して終わらせず、<b>チーム全体で支え合う体制</b>をつくり、特定の管理職への負担集中を防ぎます。')]),
('h','「休職者を出さない」強い組織へ。'),('p','まずは無料相談でお悩みをお聞かせください。<br>貴社の現在の状況、過去の診断結果をもとに、最適な解決プランをご提案します。強引な営業は一切いたしません。')]
OLD['business/employment/']=[('h','精神・発達障害専門　現場に任せない。一人ひとりに、就労支援のプロが担当'),('h','【こんなお悩みはありませんか？】'),('ul',['❌ 突発的な欠勤にどう対応すべきかわからない','❌ 業務の教え方やコミュニケーションに配慮が必要で、管理職が疲弊している','❌ せっかく採用したのに定着せず、すぐに離職してしまう']),
('h','【当社の強み】'),('dl',[('① 労働現場だけでなく「生活空間での実態」まで熟知！','住まい（メンタルピアレジデンス・梁山泊）の運営を通じて24時間体制で当事者と向き合っているため、職場で見せる姿だけでなく<b>「日常の生活空間における行動・メンタルの波・特性（生態）」</b>まで知り尽くしています。職場の面談だけでは見えない体調変化や崩れのサインを早期に察知します。'),('② 精神保健福祉士など有資格者が専任担当！','就労支援の現場で支援計画策定・管理を担ってきたスタッフや精神保健福祉士・公認心理師が本人の専任担当として伴走。本人と企業の「クッション役」となり、トラブルを未然に防ぎます。'),('③ 企業側の負担を軽減するビジネス感覚！','代表者が大手企業出身のため、企業の現場負担や生産性の重要性を熟知しています。福祉の側に寄りすぎる事なく、企業と本人の双方が無理のない体制構築を支援します。')]),
('h','【サポート内容】'),('ul',['✅ 個人への定期面談・生活面も含めた専任伴走サポート（住まい・就労支援での実務に基づく体調・メンタルケア）','✅ 面接への同席および適性・就労意欲の見極め支援','✅ 業務の切り出し・個別の特性に合わせたマニュアルの作成','✅ 「合理的な配慮の合意書」作成支援（過度な負担を防ぎ、業務範囲を明確化）','✅ 受入現場（上司・同僚）向けフォロー＆研修','✅ 活用可能な助成金のご提案']),
('h','【料金プラン】'),('dl',[('A. 導入セットアップパッケージ（3ヶ月間）','新規で採用・受け入れを行う企業様<br>料金：初期15万円 ＋ 月額5万円/人 × 3ヶ月（税別）<br>これから新しく雇用する方向け。業務切り出し、勤務枠組み設計、マニュアル・配慮合意書の作成、現場研修、入社初期3ヶ月間の高頻度な専任フォローまで丸ごと立ち上げます。'),('B. 個人担当・専任定着支援プラン【一番人気】','すでに雇用中・中途で困っている企業様も直接利用OK<br>料金：対象者1名につき 月額 3万円〜（税別）<br>初期導入パッケージ（A）を経由せず、直接このプランからお申し込みいただけます。「すでに雇用している社員の欠勤やトラブルで困っている」「中途採用した社員に個別担当をつけて定着させたい」という企業様に最適です。専任担当者による定期面談（月1〜2回）、生活動向のアセスメント、社内担当者様との定期連携を行い、離職や現場の疲弊を防ぎます。'),('C. スポット現場研修・面談プラン','現状の課題整理・単発相談<br>料金：1回 5万円（税別）<br>※「既存社員の業務整理や合理的な配慮の合意書だけ単発で作ってほしい」「まず1回現場研修をして様子を見たい」という場合にご利用いただけます。')]),
('p','📍 担当地域：三重県・愛知県の全域と滋賀県南東部（その他地域もご相談ください）')]
OLD['business/agent-consulting/']=[('h','お金をかけない！ AI・DXコンサルティング'),('p','個別支援計画も業務日誌も、もう溜め込まない。<br>現場の負担を1/10にする、身の丈に合ったAI導入をご提案します。'),('note','AIチャットの導入から、業務を自律的にこなすAIエージェントの活用へ刷新し、エージェントコンサルになりました。'),
('h','⚠️ こんなお悩み、ありませんか？'),('ul',['サビ管・児発管の書類業務が多すぎて、本来の支援に集中できない','個別支援計画や業務日誌がいつも溜まってしまい、残業が常態化している','「DXやAI」に興味はあるが、高額な専用システムを導入する予算はない','ITツールを導入しても、現場のスタッフが使いこなせるか不安']),
('h','当サービスで実現できること'),('p','あなたの事業所の過去のデータや様式に合わせた、専用のAIの構築・導入をサポートします。'),('ul',['✅ 個別支援計画・サービス等利用計画の爆速化（アセスメントから計画作成まで）','✅ 業務日誌・記録の爆速化（音声入力やメモから自動文章化）','✅ 法定代理受領書の簡単作成（国保連のPDFから自動作成）','✅ Googleツールを使ったDX支援（スプレッドシートやフォーム連携）','✅ １万円の中古ＰＣをサクサク動かす裏ワザ','✅ 更新が止まった自作ＨＰを美しくリニューアルするＡＩテクニック','✅ 処遇改善加算に関わる「資質向上」の研修実績としての活用']),
('h','💰 莫大なシステム投資は一切不要です'),('p','高額な初期費用や、使いもしない多機能システムは必要ありません。現場の状況やご予算に合わせて、2つのプランからお選びいただけます。'),
('dl',[('【プランA】マニュアル単品販売　＼ 迷ったらこれ！ ／','自社でサクッと導入したい事業所様に最適<br>各 18,000円（税込）<br>・個別支援計画一式 高速化マニュアル<br>・計画相談書類一式 高速化マニュアル'),('【プランB】3ヶ月集中 伴走コンサル','システム構築から現場への研修まで丸ごと任せたい場合<br>月額 30,000円（税込）<br>・上記計画系AIはもちろん、適用可能な業務を様々ご提案します。<br>・事業所全体のDX化のご提案 ＋ スタッフ向け研修<br>※サポート期間は3ヶ月固定（総額9万円）。4ヶ月目以降はコンサルを解約し、現場だけで永続運用可能です。')]),
('h','まずは無料相談から！'),('p','「マニュアルの内容を詳しく知りたい」「自社に合うプランを相談したい」など、お気軽にご連絡ください。')]
OLD['business/training/']=[('h','研修情報'),('dl',[('開催','土日開催'),('形式','オーダーメイドにつきご相談ください'),('料金','お志')]),('h','オルタナティブ・スキル（担当：齊藤または外部講師）'),('ul',['野口整体、合気道、各種マッサージなど療育に役立つボディワーク','マクロビオティック調理法','心理占星術による性格分析','シュタイナー哲学講義']),('p','など希望に応じて実施いたします。'),('note','合気道研修を新設しました（内容・日程は準備中です）。')]
def old_html(blocks):
    o='<section class="blk wide" id="what"><div class="prose old">'
    for t,v in blocks:
        if t=='h': o+=f'<h3 style="font-size:19px;margin:34px 0 10px">{v}</h3>'
        elif t=='p': o+=f'<p style="margin:0 0 12px">{v}</p>'
        elif t=='note': o+=f'<p style="margin:0 0 18px;padding:12px 16px;border-left:3px solid var(--hi);font-weight:600">{v}</p>'
        elif t=='ul': o+='<ul class="lst" style="margin:6px 0 14px">'+''.join(f'<li>{x}</li>' for x in v)+'</ul>'
        elif t=='dl': o+='<dl class="info" style="margin:6px 0 16px">'+''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a,b in v)+'</dl>'
    return o+'</div></section>'

PAGES.append(dict(path='suishodama/',name='水晶玉',en='SUISHODAMA',photo='hero_top',pos='50% 88%',mark='suisho_mark_white.svg',
 title='水晶玉｜メンタルヘルスコーディネート（環境調整）｜名古屋から30分（三重県四日市市）',
 desc='眠れない、気分の波がある、親元にいると息が詰まる。水晶玉は、心の状態を左右する環境を評価し、設計し、手配するメンタルヘルスコーディネート（環境調整）です。三重県四日市市山城町、名古屋西ICから車で約30分です。',
 cat='メンタルヘルスコーディネート<em>（環境調整）</em>',copy=['環境調整は、','それ自体がケアです。'],
 sub='心の不調・家庭環境・就労環境・人間関係。<br>心の状態を左右する環境を、<wbr>評価し、設計し、手配し、見直します。',acc=ACC,
 tel='070-3291-9626',addr_ld=YAMA,
 what_h='4つの<br>環境調整',what=[('心の不調','眠れない・気分の波','不眠や気分の波に、生活リズムと日々の環境の側から手を打ちます。'),('家庭環境','親元にいると息が詰まる','親との距離を設計し直します。親元を出て暮らす選択肢も含め、住まい・日中・お金の手続きまで手配します。'),('就労環境','仕事が続かない','就労先とペースを設計し、面接同行から会社との折衝まで行います。通い続けるための生活の組み立ても含みます。'),('人間関係','人間関係に疲れた','似た者同士で集う居場所につなぎます。孤立は放置しません。')],
 flow=[["CONTACT","問い合わせ","電話またはLINEでご連絡ください。氏名と相談内容の要点だけで十分です。"],["ASSESSMENT","アセスメント","心の不調・家庭環境・就労環境・人間関係の現状を評価し、調整の優先順位を決めます。"],["DESIGN & ARRANGE","設計と手配","変える環境と手段を決めて計画書にし、家庭・職場・居場所との連絡と調整まで行います。"],["MONITORING","モニタリング","定期的に再評価し、合わない環境は再調整します。"]],
 info=[('内容','メンタルヘルスコーディネート（環境調整）<br>アセスメント／設計と手配／モニタリング'),('担当','精神保健福祉士などの有資格者'),('場所',PLACE_Y),('受付',ph('受付日・時間')),('料金','多くの場合、自己負担なし '+ph('表記の可否')),('申し込み','電話またはLINE')],
 faq=[('親と離れて暮らしたいです。','対応します。親元を出る計画を立て、住まい（梁山泊・一人暮らし）と日中の行き先まで手配します。'),('料金は？','多くの場合、自己負担はありません。公的制度を使い、'+TEJUN),('家族からの依頼は？','受け付けます。本人の利用意思は面談で確認します。'),NAGOYA,('他の支援機関を利用中でも？','対応します。現在の利用先を前提に設計します。')],
 rel=[('しちりんの会','shichirin/'),('RYDEEN','rydeen/')],cta_h='申し込み'))

PAGES.append(dict(path='rydeen/',name='RYDEEN',en='RYDEEN',big='R',logo='rydeen_logo.webp',
 title='RYDEEN｜PCで働く｜名古屋から30分（三重県四日市市山城町）',
 desc='仕事が続かない、でもPCは得意。そういう人が実務で働く場所がRYDEENです。SNS運用代行などWeb広報の実務を行います。2026年11月1日、三重県四日市市山城町に開所します。名古屋西ICから車で約30分、三岐線山城駅から徒歩5分です。',
 cat='PCで働く',copy=['PCで、','働きます。'],sub='SNS運用代行、Web広報、AIを使った事務。<br>練習ではなく、実務です。',badge='<p class="badge">2026年11月1日 開所</p>',acc=ACC,addr_ld=YAMA,
 what_h='3つの<br>実務',what=[('SNS運用代行','','企業・店舗のSNSを、投稿の企画から作成・予約まで請け負います。'),('Web広報','','ホームページの更新、写真の整理、告知文の作成を、外部の仕事として納品します。'),('AI事務','','AIを道具として使い、文書作成やデータ整理をこなします。使い方は現場で覚えます。')],
 flow=[["VISIT","見学","作業内容と環境を確認します。PCの得意・不得意もここで見ます。"],["TRIAL","体験","実際の作業を体験し、ペースと担当を決めます。"],["CONTRACT","手続き",TEJUN],["WORK","通所","担当業務を持ち、実務として納品します。"]],
 info=[('対象','PC作業が得意、または得意にしたい方'),('場所',PLACE_Y),('開所','2026年11月1日'),('時間',ph('利用時間')),('費用','公的制度の利用可（手続きはこちらで代行） '+ph('利用料')),('申し込み','見学予約は電話またはLINE')],
 faq=[('PCはどの程度使えればいいですか？','見学・体験で作業内容を確認し、担当を決めます。'),('何か準備は要りますか？','要りません。'+TEJUN),('名古屋から通えますか？','通えます。名古屋西ICから車で約30分、三岐線 山城駅から徒歩5分です。四日市駅から直通バスもあります。')],
 rel=[('梁山泊','ryozanpaku/'),('水晶玉','suishodama/')],cta_h='見学を申し込む'))

PAGES.append(dict(path='chamu/',badge='<p class="badge">短時間利用OK</p>',name='茶夢',en='CHAMU',photo='counter',pos='50% 60%',
 title='茶夢（チャム）｜生活介護事業所｜統合失調症・自閉症の方のための日中の居場所｜三重県四日市市あさけが丘',
 desc='茶夢は、統合失調症・自閉症の方のための生活介護事業所です。生産活動を無理強いすることはありません。料理・喫茶・読書・アートで、ゆったりと日中を過ごします。強度行動障害の方もご相談ください。短時間から利用できます。三重県四日市市あさけが丘、名古屋西ICから車で約30分です。',
 cat='統合失調症・自閉症の方のための日中の居場所',copy=['日中を、','安全に過ごす場所です。'],sub='統合失調症・自閉症の方のための日中の居場所です。<br>料理・喫茶・読書・アートで、静かに過ごします。',acc=ACC2,addr_ld=ASAKE,
 what_h='4つの<br>過ごし方',what=[('料理','','台所に立ちます。献立から仕込み、盛り付けまで行います。'),('喫茶','','カウンターで一杯。静かな喫茶スペースで過ごします。'),('読書','','本棚の前で、自分のペースで過ごします。'),('アート','生け花など','花を生け、手を動かします。言葉にしなくていい表現です。')],
 gal=[('kitchen','台所での調理'),('ikebana','生け花'),('library','本棚'),('parfait','喫茶で過ごす参加者')],
 flow=[["VISIT","見学","場所と雰囲気を確認します。予約制です。"],["TRIAL","体験","短時間から体験し、過ごし方を決めます。"],["CONTRACT","手続き",TEJUN],["STAY","利用","短時間から利用できます。ペースは本人が決めます。"]],
 info=[('対象','統合失調症・自閉症の方<br>強度行動障害：応相談'),('場所',PLACE_A),('時間',ph('利用時間')),('申し込み','見学は予約制。電話またはLINE')],
 faq=[('人と話すのが苦手でも大丈夫ですか？','大丈夫です。話さずに過ごすことも前提にしています。'),('短時間だけの利用は？','短時間から利用できます。'),('家族が先に見学できますか？','できます。予約のうえ、ご家族だけの見学にも対応します。'),('スタッフはどんな人ですか？','有資格者が対応します。'),NAGOYA],
 rel=[('金斗雲','kintoun/'),('ご家族の方へ','#family')],cta_h='見学を申し込む'))

PAGES.append(dict(path='shichirin/',name='しちりんの会',en='SHICHIRIN',photo='fish',pos='50% 40%',type='Event',
 title='しちりんの会｜火を起こすところから始める会｜三重県菰野町',
 desc='しちりんの会は、七輪で火を起こし、焼いて食べる自費参加の会です。手続きも診断も要りません。不定期の土曜11:00から、三重県菰野町田光で開催します。参加費は食材費込み3,000円です。',
 cat='自費参加｜手続き不要',copy=['火を起こす','ところから始めます。'],sub='七輪で焼いて、食べます。<br>手続きも、診断も要りません。',acc='三重県菰野町田光／不定期土曜 11:00〜',
 what_h='やること',what=[('火を起こす','','炭に火をつけるところから、全員が自分の手で行います。'),('焼く','','魚や野菜を、七輪の前で焼けるまで待ちます。'),('食べる','','焼いたものをその場で食べます。食材費は参加費に含みます。'),('森','菰野町田光','会場は菰野の森です。街から離れて半日を過ごします。')],
 gal=[('stove','火起こし'),('tent','森のテント'),('tent_in','テントの中'),('walker','菰野の森')],
 flow=[["APPLY","申し込み","LINEまたは電話で参加希望をお伝えください。"],["DATE","日程の連絡","開催日と集合場所をご連絡します。開催は不定期の土曜日です。"],["DAY","当日","11:00から、火を起こし、焼いて、食べます。"]],
 info=[('種別','自費参加'),('日時','不定期土曜日 11:00〜'),('場所','三重県菰野町田光'),('参加費','食材費込み 3,000円'),('手続き','不要。診断も不要'),('申し込み','LINEまたは電話')],
 faq=[('手続きは必要ですか？','不要です。自費参加で、診断も要りません。'),('眠れないだけでも参加していいですか？','参加できます。理由は問いません。'),('費用は？','食材費込み3,000円です。'),('次の開催日は？','不定期の土曜日です。申し込み時にご案内します。'),('名古屋から参加できますか？','参加できます。会場は三重県菰野町田光です。詳しい場所は申し込み後にご案内します。'),('一人で参加してもいいですか？','参加できます。')],
 rel=[('RYDEEN','rydeen/'),('梁山泊','ryozanpaku/')],cta_h='参加を申し込む'))

def leo_extra(rel): return f'''<section class="blk"><div class="h"><span class="en">FOR PARENTS</span><h2>保護者向けプログラム</h2></div>
<div class="cards" style="grid-template-columns:1fr 1fr"><a class="sc" href="{rel}leo/parent-training/"><div class="th" style="background-image:url({rel}img/consult.jpg)"></div><div class="bd"><p class="nm" style="font-size:17px">ペアレント<br>トレーニング</p><p class="ln">関わり方を変えます。</p></div></a>
<a class="sc" href="{rel}leo/assessment/"><div class="th" style="background-image:url({rel}img/record.jpg)"></div><div class="bd"><p class="nm" style="font-size:17px">発達検査</p><p class="ln">WISC-V・新版K式。</p></div></a></div></section>'''
PAGES.append(dict(path='leo/',name='レオ',en='LEO',photo='panda',pos='50% 60%',addr_ld=ASAKE,tel='070-6967-0011',
 title='レオ｜子どもが落ち着かない保護者へ｜おもちゃ・武道・庭いじり｜三重県四日市市あさけが丘',
 desc='子どもが落ち着かない、かんしゃくが多い。レオは、遊びと体で子どもの情緒を整える場所です。おもちゃ、武道・ヨガ、庭いじり、手作りの和食を用意しています。ペアレントトレーニングと発達検査も行います。三重県四日市市あさけが丘、名古屋西ICから車で約30分です。',
 cat='子どもの情緒',copy=['おもちゃ、武道、','庭いじりで整えます。'],sub='体を動かし、手を動かします。<br>情緒は、遊びの中で整えます。',acc=ACC2,
 what_h='4つの<br>柱',what=[('おもちゃ','','大量のおもちゃから好きなものを選び、少し難しいものにも挑みます。認知・言語・社会性を遊びで伸ばします。'),('武道・ヨガ','','格闘家のもとへ出向き、体を鍛えます。運動と感覚を育てます。'),('庭いじり','','花壇を作り、植え、育てます。菰野のフィールドでは自然観察と七輪の火起こしを行います。'),('和食の昼食','1回300円','手作りの和食を提供します。食事も情緒を整える時間です。')],
 gal=[('toyshelf','おもちゃの部屋'),('blocks','積み木'),('zinnia','花壇'),('leo_ext','レオの建物')],extra=leo_extra,
 flow=[["VISIT","見学","建物の2階、看板のあるドアからお入りください。予約制です。"],["PAPER","手続き",TEJUN],["PLAN","計画","お子さまの様子を確認し、過ごし方の計画を作ります。"],["START","利用開始","1部・2部から選んで通います。地域によって送迎の相談も受けます。"]],
 info=[('対象','落ち着かない、こだわりが強い、集団が苦手なお子さま。診断の有無は問いません'+ph('対象年齢の表記')),('時間','1部 11:00〜14:30／2部 放課後〜17:00'),('昼食','1回300円'),('場所',PLACE_A+'<br>建物の2階'),('送迎','地域により相談可'),('費用','公的制度の利用可（自治体の手続きが必要。こちらで案内）')],
 faq=[('送迎はありますか？','地域によって相談を受けます。'),('昼食は？','手作りの和食を1回300円で提供します。'),('保護者向けの支援は？','ペアレントトレーニングと発達検査を行っています。')],
 rel=[('ペアレントトレーニング','leo/parent-training/'),('発達検査','leo/assessment/')],cta_h='見学を申し込む'))

PAGES.append(dict(path='leo/parent-training/',name='ペアレントトレーニング',en='PARENT TRAINING',photo='consult',pos='50% 50%',short=True,type='Service',
 title='ペアレントトレーニング｜子どもへの関わり方を変える保護者プログラム｜三重県四日市市 レオ',
 desc='親の関わり方は、子どもにとって最大の環境です。ペアレントトレーニングでは、行動の見方・ほめ方・指示の出し方を家庭で使える形にします。三重県四日市市、レオで行います。',
 cat='保護者向けプログラム｜レオ',copy=['親の関わり方は、','子どもの最大の環境です。'],sub='子どもを変える前に、関わり方を変えます。',acc='レオ（四日市市あさけが丘）で実施',
 what_h='身につける<br>こと',what=[('行動の見方','','困った行動を、きっかけと結果に分けて見ます。'),('ほめ方','','効くほめ方には型があります。タイミングと言葉を練習します。'),('指示の出し方','','通る指示は短く具体的です。家庭で使える形にします。'),('家庭での練習','','学んだことを家で試し、次回に振り返ります。')],
 flow=[["CONTACT","申し込み","電話またはLINEで、お子さまの年齢と困りごとの要点をお伝えください。"],["SESSION","プログラム","関わり方の型を学びます。"],["HOME","家庭で実践","学んだことを家で試します。"],["REVIEW","振り返り","結果を持ち寄り、関わり方を調整します。"]],
 info=[('対象','お子さまへの関わり方に悩む保護者'),('場所','レオ（三重県四日市市あさけが丘2-1-42）'),('日程',ph('日程・回数')),('費用',ph('参加費')),('担当','有資格者 '+ph('担当者の資格表記'))],
 faq=[('レオを利用していなくても参加できますか？',ph('レオに通っていない方の参加可否')),('診断がなくても参加できますか？','参加できます。診断の有無は問いません。'),('発達検査と組み合わせられますか？','組み合わせられます。検査結果を関わり方の設計に使います。')],
 rel=[('発達検査','leo/assessment/'),('レオ','leo/')],cta_h='参加を申し込む'))

PAGES.append(dict(path='leo/assessment/',name='発達検査',en='ASSESSMENT',photo='record',pos='50% 50%',short=True,type='Service',
 title='発達検査（WISC-V・新版K式）｜25,000円・検査から支援へ直結｜三重県四日市市 レオ',
 desc='WISC-V（小1〜高2）と新版K式発達検査（未就学児）を行います。事前面談・検査・報告書・フィードバック面談込みで各25,000円（税込）です。結果は日々の支援と学習指導に直結させます。三重県四日市市。',
 cat='WISC-V・新版K式｜公認心理師が実施',copy=['特性を数値で掴み、','支援に直結させます。'],sub='検査して終わりにはしません。<br>結果を、日々の学習指導に反映します。',acc='レオ（四日市市あさけが丘）で実施',
 what_h='2つの<br>検査',what=[('WISC-V','小1〜高2','ウィスク・ファイヴ。認知の得意・不得意を指標ごとに数値化します。'),('新版K式','未就学児','新版K式発達検査。未就学のお子さまの発達の状態を確認します。'),('報告書','','結果を報告書にまとめ、視覚・聴覚の特性に応じた指導方法まで書き込みます。'),('フィードバック','','面談で結果を説明し、家庭と支援の現場での使い方を示します。')],
 flow=[["INTERVIEW","事前面談","困りごとと検査の目的を確認します。"],["TEST","検査","公式マニュアルに則り、厳密に実施します。"],["REPORT","報告書","結果と具体的な学習アプローチを文書にします。"],["FEEDBACK","フィードバック面談","結果を説明し、支援に落とし込みます。"]],
 info=[('検査','WISC-V（小1〜高2）／新版K式発達検査（未就学児）'),('料金','各 25,000円（税込）<br>事前面談・検査・報告書・フィードバック面談を含む'),('担当','公認心理師'),('場所','レオ（三重県四日市市あさけが丘2-1-42）'),('申し込み','電話またはLINE')],
 faq=[('市役所や学校に提出できますか？','提出先によっては、民間施設の結果を公的な判定基準（各種申請や入級判定など）として受理しない場合があります。申請目的の場合は、事前に提出先へ有効性を確認してください。'),('料金に含まれるものは？','事前面談、検査実施、結果報告書の作成、フィードバック面談です。'),('検査後の支援は？','結果をもとに学習アプローチを設計します。レオの利用やペアレントトレーニングにも直結します。')],
 rel=[('ペアレントトレーニング','leo/parent-training/'),('レオ','leo/')],cta_h='検査を申し込む'))

PAGES.append(dict(path='kintoun/',name='金斗雲',en='KINTOUN',photo='homemeal',pos='50% 45%',
 addr_ld={"@type":"PostalAddress","addressCountry":"JP","addressRegion":"三重県","addressLocality":"三重郡菰野町","streetAddress":"田光1801-165"},
 title='金斗雲｜訪問・アウトリーチ｜家族が家から出ないご家庭へ（三重県四日市市・菰野町）',
 desc='家族が家から出ない、相談に行けない。金斗雲は、こちらから自宅へ出向く訪問とアウトリーチです。家族からの相談でも始められます。訪問は四日市市・菰野町など三重県内です。',
 cat='訪問｜アウトリーチ',copy=['来られないなら、','こちらから行きます。'],sub='家から出られない、窓口に行けない。<br>その状態を前提に、自宅から始めます。',acc='訪問地域：四日市市・菰野町など三重県内',
 what_h='4つの<br>支援',what=[('アウトリーチ','','相談に来られない人のもとへ出向きます。外に連れ出すことを目的にはしません。'),('家事援助','','食事、掃除、洗濯。生活の土台を自宅で立て直します。'),('外出の同行','','買い物、寺、街。外に出る日は一緒に出ます。'),('家族の相談','','本人が動けなくても、家族からの相談で始められます。')],
 gal=[('kitchen_prep','台所の下ごしらえ'),('clothes','古着屋へ'),('snackwalk','街歩き'),('storefront','街の店先')],
 flow=[["CONTACT","相談","本人でも家族でも、電話またはLINEでご連絡ください。"],["VISIT","訪問","まず話を聞きます。無理に外へ出そうとはしません。"],["PLAN","計画","必要な支援を決めます。"+TEJUN],["SUPPORT","支援開始","定期的に訪問し、生活と外出の範囲を少しずつ広げます。"]],
 info=[('対象','外に出にくい方、そのご家族'),('訪問地域','四日市市・菰野町など三重県内 '+ph('実施地域の詳細')),('事業所','三重県三重郡菰野町田光1801-165'),('担当','精神保健福祉士などの有資格者'),('費用','公的制度の利用可。所得に応じた負担上限あり。手続きはこちらで代行'),('申し込み','電話またはLINE')],
 faq=[('家族からの相談でも始められますか？','始められます。本人が相談できない状態を前提にしています。'),('無理に外へ連れ出されませんか？','連れ出しを目的にはしません。話を聞くところから始めます。'),('費用は？','公的制度を使えます。所得に応じた負担上限があり、'+TEJUN),('名古屋も訪問できますか？','訪問は四日市市・菰野町など三重県内です。名古屋の方は水晶玉にご相談ください。'),('家庭の環境ごと見直したい場合は？','家庭や職場の環境を整える<a href="../suishodama/" style="display:inline;color:var(--hi)">水晶玉</a>で、ご家族からの相談を受け付けます。')],
 rel=[('茶夢','chamu/'),('ご家族の方へ','#family')],cta_h='相談する'))

PAGES.append(dict(path='ryozanpaku/',deco=True,extra=partners,audience=AUD_P,name='梁山泊',en='MENTAL PEER RESIDENCE',big='梁',type='Residence',addr_ld=YAMA,
 title='メンタルピアレジデンス・梁山泊｜働き続ける人の住まい 家賃 月8万円｜名古屋から30分（三重県四日市市山城町）',
 desc='メンタルピアレジデンス・梁山泊は、仕事はできるのに心の波で崩れやすい人が、働き続けるための住まいです。似た者同士で暮らし、仕事帰りに整えます。親元を出たい人の住まいにもなります。家賃は月8万円で、朝夕食事付きです。ほかに費用はかかりません。三重県四日市市山城町、名古屋西ICから車で約30分です。',
 cat='メンタルピアレジデンス｜家賃 月8万円',copy=['仕事はできる人が、','崩れないための住まいです。'],sub='職場定着を支える、住まいとケアの場です。<br>似た者同士で暮らし、仕事帰りに整えます。',acc=ACC,
 what_h='梁山泊の<br>役割',what=[('職場定着','生活基盤','職場定着は生活で決まります。睡眠・食事・帰宅後の過ごし方を整え、欠勤と離職の芽を生活の側で摘みます。'),('ピアで暮らす','似た者同士','同じように心の波を抱えて働く人同士で暮らします。'),('仕事帰りに整える','','職場の緊張を家に持ち込みません。帰って整える場所があります。'),('親元を出る','','親元にいると息が詰まる人の、最初の住まいにもなります。')],
 flow=[["CONTACT","問い合わせ","電話またはLINEで、今の仕事と住まいの状況を要点だけお伝えください。"],["VISIT","見学・面談","建物と暮らし方を確認し、入居の条件を説明します。"],["MOVE","入居","通勤と生活のリズムを組み立てます。"],["KEEP","定着","崩れの兆しは早めに拾い、環境を調整します。職場・紹介元との連携窓口は本部が一本で受けます。"]],
 info=[('正式名称','メンタルピアレジデンス・梁山泊'),('対象','仕事を続けたい、心の波を抱える社会人／親元を出たい人 '+ph('入居条件')),('場所','三重県四日市市山城町59-4<br>三岐線 山城駅から徒歩5分<br>名古屋西ICから車で約30分'),('費用','家賃 月8万円（朝夕食事付き。ほかに費用はかかりません）'),('申し込み','電話 059-315-0697 またはLINE')],
 faq=[('働きながら住めますか？','住めます。働き続けるための住まいとして設計しています。'),('会社に知られずに入居できますか？','対応します。連絡方法は本人の指定に従います。'),('企業や支援機関から紹介できますか？','できます。紹介・連携の窓口は本部（059-315-0697）です。本人の同意のうえで、職場との情報共有の方法を決めます。'),('親と離れて暮らせますか？','暮らせます。親元を出る段取り（住まい・日中・お金の手続き）はこちらで組みます。'),('親に知られずに相談できますか？','対応します。連絡方法は本人の指定に従います。'),('費用は？','家賃は月8万円です。ほかに費用はかかりません。'),('名古屋から移り住めますか？','移り住めます。名古屋西ICから車で約30分です。')],
 rel=[('水晶玉','suishodama/'),('しちりんの会','shichirin/')],cta_h='見学を申し込む'))

BIZ=[('employment','雇用定着サポート','EMPLOYMENT','現場に任せず、専任の担当者をつけます。'),('stress-check','ストレスチェック','STRESS CHECK','実施して終わらせず、組織を変える材料にします。'),('stress-check-training','ストレスチェック実施者養成研修','PRACTITIONER TRAINING','実施者になるための研修を、オンラインで行います。'),('agent-consulting','エージェントコンサル','AGENT CONSULTING','AIエージェントを、現場の戦力にします。'),('training','研修','TRAINING','児童指導員研修と合気道研修を行います。')]
PAGES.append(dict(path='business/stress-check/',name='ストレスチェック',en='STRESS CHECK',photo='karate_sit',short=True,type='Service',
 title='職場ストレスチェック｜アドラー心理学×ラインケア支援｜三重県四日市市 星心会',
 desc='ストレスチェックを、組織が変わるきっかけにします。管理職研修・アドラー流個別面談・ラインケア定着支援まで一社完結で行います。三重県四日市市、名古屋から30分です。',
 cat='企業・法人向け',copy=['実施して終わらせず、','組織を変える材料にします。'],sub='アドラー心理学 × ラインケア支援です。',acc='三重・愛知の企業・法人向け',
 what_h='3つの<br>支援',what=[('管理職研修','','自社の診断データを題材に、ケーススタディとグループワークを行います。現場で使える部下への接し方を身につけます。'),('個別面談','アドラー流','高ストレス者と管理職への1on1です。他責から「今、自分にできること」へ意識を向けます。'),('ラインケア定着','','許可を得たうえで、管理職へ具体的な対応策をフィードバックします。負担を一人に集中させません。')],
 flow=[["CONSULT","無料相談","現状と過去の結果を確認します。"],["PLAN","提案","解決プランを提示します。強引な営業はしません。"],["RUN","実施","チェック・研修・面談を一社完結で行います。"],["FOLLOW","定着","ラインケアの体制を現場に残します。"]],
 info=[('対象','企業・法人'),('料金','無料相談あり／本契約 '+ph('料金')),('担当','公認心理師・精神保健福祉士などの有資格者'),('申し込み','電話または相談フォーム')],
 faq=[('相談は有料ですか？','初回の相談は無料です。'),('産業医との関係は？','産業医の判定に加え、予防と現場での定着を担います。'),('過去の結果も使えますか？','使えます。過去の診断結果をもとに提案します。')],
 rel=[('雇用定着サポート','business/employment/'),('エージェントコンサル','business/agent-consulting/')],cta_h='無料で相談する'))

PAGES.append(dict(path='business/employment/',extra=partners,audience=AUD_P[:4],name='雇用定着サポート',en='EMPLOYMENT',big='E',short=True,type='Service',
 title='雇用定着サポート｜メンタル不調・発達特性のある社員の定着｜三重県四日市市 星心会',
 desc='メンタル不調・発達特性のある社員の雇用定着サポートです。専任担当が本人と企業の間に立ち、面接同席・業務切り出し・合理的配慮の合意書・現場研修まで行います。住まい（メンタルピアレジデンス・梁山泊）も用意できます。月額3万円〜（税別）。',
 cat='企業・支援機関向け｜メンタルヘルス専門',copy=['現場に任せず、','専任をつけます。'],sub='メンタルヘルスの実務家が、社員一人ひとりを担当します。<br>住まい（梁山泊）まで用意できます。',acc='三重・愛知の企業・支援機関向け',
 what_h='定着を支える<br>5つの手段',what=[('専任担当','','定期面談と、生活面まで含めた専任のサポートを行います。体調の崩れを早期に掴みます。'),('採用','','面接に同席し、適性と就労意欲を見極めます。'),('業務設計','','業務の切り出し、特性に合わせたマニュアル、「合理的な配慮の合意書」を作成します。'),('現場研修','','上司・同僚向けのフォローと研修を行い、活用できる助成金を提案します。'),('住まい','梁山泊','職場定着を生活の側から支える住まいとケアの場、メンタルピアレジデンス・梁山泊です。欠勤の原因になりやすい睡眠と生活リズムを、住まいごと整えます。')],
 flow=[["CONSULT","相談","現状と課題を整理します。"],["SETUP","設計","業務と勤務の枠組みを作ります。"],["PLACE","受け入れ","入社初期は高頻度でフォローします。"],["KEEP","定着","月1〜2回の定期面談と、社内担当者との連携を続けます。"]],
 info=[('A 導入セットアップ','初期15万円＋月額5万円/人×3か月（税別）<br>新しく雇用する企業向け'),('B 専任定着支援','対象者1名につき月額3万円〜（税別）<br>雇用中の社員の欠勤・トラブルに直接対応'),('C スポット','1回5万円（税別）<br>現場研修・面談'),('住まい','メンタルピアレジデンス・梁山泊（四日市市山城町）'),('担当','精神保健福祉士・公認心理師などの有資格者')],
 faq=[('すでに雇用している社員だけでも依頼できますか？','依頼できます。プランBから直接申し込めます。'),('企業側に偏った支援ですか？','本人の側にも企業の側にも寄せません。双方に無理のない体制を作ります。'),('社員の住まいまで対応できますか？','対応します。メンタルピアレジデンス・梁山泊を、働き続けるための住まいとして紹介できます。'),('支援機関からの紹介は？','受け付けます。窓口は本部（059-315-0697）です。'),('三重県外の企業も対象ですか？',ph('対応エリア'))],
 rel=[('ストレスチェック','business/stress-check/'),('研修','business/training/')],cta_h='相談する'))

PAGES.append(dict(path='business/agent-consulting/',name='エージェントコンサル',en='AGENT CONSULTING',big='AI',short=True,type='Service',
 title='エージェントコンサル｜対人支援の事業所のAIエージェント導入｜三重県四日市市 星心会',
 desc='対人支援の事業所のためのAIエージェント導入支援です。計画・記録・請求まわりの書類業務とWeb広報をAIエージェントに任せます。自ら運用している事業所が伴走します。',
 cat='事業所・法人向け',copy=['AIエージェントを、','現場の戦力にします。'],sub='書類は溜めず、広報は止めません。<br>自ら使い倒している事業所が教えます。',acc='対人支援の事業所・法人向け',
 what_h='任せられる<br>業務',what=[('計画・記録','','計画書や業務日誌を、アセスメントから文書化まで短縮します。'),('事務・請求','','法定代理受領通知などの定型書類を自動で作ります。'),('Web広報','','ホームページの更新とSNSの運用で、止まった広報を動かします。'),('研修','','スタッフが自分で使えるところまで教えます。処遇改善加算の資質向上研修としても活用できます。')],
 flow=[["CONSULT","無料相談","業務と予算を確認します。"],["DESIGN","設計","任せる業務を決め、環境を作ります。"],["TRAIN","研修","現場が自走できるまで教えます。"],["HANDOVER","引き渡し","以降は事業所だけで運用できます。"]],
 info=[('対象','対人支援の事業所・法人'),('料金',ph('料金プラン')),('実施','オンライン・訪問 '+ph('実施方法')),('申し込み','電話または相談フォーム')],
 faq=[('高額なシステムが必要ですか？','不要です。今ある環境と予算に合わせます。'),('PCに詳しいスタッフがいません。','現場が使えるところまで研修します。'),('旧「AIコンサル」との違いは？','AIチャットの導入から、業務を自律的にこなすAIエージェントの活用へ刷新しました。')],
 rel=[('研修','business/training/'),('ストレスチェック','business/stress-check/')],cta_h='無料で相談する'))

PAGES.append(dict(path='business/stress-check-training/',keep_desc=True,deco=True,gal=[('sct_soudan','相談の様子のイラスト')],name='ストレスチェック実施者養成研修',en='PRACTITIONER TRAINING',big='SC',short=True,type='Course',
 title='ストレスチェック実施者養成研修｜歯科医師・看護師・精神保健福祉士・公認心理師｜オンライン 星心会',
 desc='ストレスチェック実施者養成研修です。歯科医師・看護師・精神保健福祉士・公認心理師の方を対象に、Google Meetのリアルタイム開催で3科目・計5時間を行います。受講料は税込12,800円です。',
 cat='労働安全衛生法に基づく実施者養成研修',copy=['ストレスチェックの','実施者になるための研修です。'],sub='',acc='',
 what_h='3つの<br>科目',what=[],flow=[],info=[],faq=[],
 rel=[('ストレスチェック','business/stress-check/'),('研修','business/training/')],cta_h='申し込む・相談する',cta_note='<p style="margin-top:18px"><a class="btn" href="https://rsaito-png.github.io/portal/sct.html">申込ページへ</a></p>'))

PAGES.append(dict(path='business/training/',name='研修',en='TRAINING',photo='karate_bow',short=True,type='Service',
 title='研修｜児童指導員研修・合気道研修｜三重県四日市市 星心会',
 desc='児童指導員研修と合気道研修を行います。整体・合気道・マッサージなど、子どもと関わる仕事に役立つボディワークを中心に、オーダーメイドで土日に実施します。',
 cat='児童指導員研修・合気道研修',copy=['体を使って、','支援を学びます。'],sub='オーダーメイドで、土日に開催します。',acc='子どもと関わる事業所・法人向け',
 what_h='2つの<br>研修',what=[('児童指導員研修','','野口整体、合気道、各種マッサージなど、子どもと関わる仕事に役立つボディワークです。マクロビオティック調理法なども希望に応じて行います。'),('合気道研修','','内容は準備中です。'),('オーダーメイド','','テーマと人数に合わせて組み立てます。'),('講師','','代表または外部講師が担当します。')],
 gal=[('karate_studio','道場'),('karate_class','稽古'),('karate_sit','座学')],
 flow=[["CONSULT","相談","テーマ・人数・日程を確認します。"],["DESIGN","設計","内容を組み立てます。"],["RUN","実施","土日に実施します。"]],
 info=[('開催','土日'),('形式','オーダーメイド'),('料金','お志 '+ph('料金表記の確認')),('合気道研修',ph('内容・日程・料金'))],
 faq=[('内容は選べますか？','希望に応じて組み立てます。'),('合気道の経験がなくても参加できますか？',ph('合気道研修の参加条件'))],
 rel=[('雇用定着サポート','business/employment/'),('エージェントコンサル','business/agent-consulting/')],cta_h='相談する'))

for d in PAGES: service_page(d)

# ---------- TOP ----------
def card(k,rel=''):
    _,n,u,c,l,t=SV[k]
    th=f'<div class="th" style="background-image:url({rel}img/{t}.jpg)"></div>' if t else f'<div class="th t"><b>{ {"ryozanpaku":"RYOZAN","employment":"EMPLOY","agent":"AI"}.get(k,n)}</b></div>'
    if k=='rydeen': th=f'<div class="th t" style="background:#05070d"><img src="{rel}img/rydeen_logo.webp" alt="RYDEEN ロゴ" style="width:72%;max-width:150px;aspect-ratio:1;border-radius:50%"></div>'
    return f'<a class="sc" href="{rel}{u}">{th}<div class="bd"><p class="nm">{n}</p><p class="ct">{c}</p><p class="ln">{l}</p></div></a>'
TOPC=dict(copy=['環境調整という、','メンタルヘルスケアです。'],sub='名古屋から30分です。',entry_h='どなたの相談ですか。',entry_p='診断も、病院に行ったことも、手続きの知識も要りません。書類と手続きはこちらで進めます。',aud=[(a[0],a[1],a[3],a[5]) for a in AUD])
def top():
    global TOPC
    rel=''
    cf=CONTENT and _o.path.join(CONTENT,'top.md')
    if cf and _o.path.exists(cf) and not DUMP: TOPC=CI.parse_top(open(cf,errors='ignore').read(),TOPC)
    if DUMP: open(_o.path.join(DUMP,'top.md'),'w').write(CI.top_md(TOPC))
    TA={k:(lead,hint) for k,lab,lead,hint in TOPC['aud']}
    o=head(rel,'星心会｜環境調整という、メンタルヘルスケアです。名古屋から30分（三重県四日市市）','星心会は、環境調整によるメンタルヘルスケアを行う三重県四日市市の専門組織です。ご本人、ご家族、お子さまの保護者、企業・支援機関の方へ、それぞれの事業を用意しています。診断も手続きの知識も要りません。名古屋西ICから車で約30分です。','')+header(rel)
    o+=f'''<section class="hero"><div class="bg" style="background-image:url(img/hero_top.jpg);background-position:50% 88%"></div>
<div class="hin"><div class="hlogo"><img src="img/mark_white.svg" alt=""><span>星心会</span></div><p class="en">SEISHINKAI · YOKKAICHI</p>
<p class="copy" style="margin-top:18px">{''.join(f'<span>{x}</span>' for x in TOPC['copy'])}</p><p class="sub" style="font-size:16px">{TOPC['sub']}</p>
</div><p class="acc">名古屋西ICから車で約30分／三岐線 山城駅から徒歩5分／四日市駅から直通バスあり</p></section>
<section class="blk" id="entry" style="max-width:1040px;padding-bottom:10px"><div class="h"><span class="en">ENTRY</span><h2>{TOPC['entry_h']}</h2><p>{TOPC['entry_p']}</p></div>
<div class="aud" style="grid-template-columns:repeat(2,minmax(0,1fr))">{''.join(f'<a href="#{k}">{lab}<small>{TA[k][1]} ↓</small></a>' for k,lab,en,lead,ks,hint in AUD)}</div></section>'''
    for k,lab,en,lead,ks,hint in AUD:
        o+=f'<section class="blk" id="{k}" style="max-width:1040px;padding-top:44px"><div class="h"><span class="en">{en}</span><h2>{lab}</h2><p>{TA[k][0]}</p></div><div class="cards">'+''.join(card(x) for x in ks)+'</div>'
        if k=='partners': o+='<p style="margin-top:18px"><a class="btn" href="business/">企業・支援機関の方へ →</a></p>'
        o+='</section>'
    o+='''<section class="blk wide" id="news"><div class="h"><h2>SNS</h2></div><div class="snsw">
<div class="snsb"><p class="en sl">X</p><div class="tt"><p class="nm">世界のメンタルヘルス・ニュース</p><p class="hd">@gcbfhq</p></div><div class="snss"><a class="xc" href="https://x.com/gcbfhq/status/2113412690064327131" target="_blank" rel="noopener"><time>2026年10月23日</time><p>マレーシアの公的相談電話「Talian HEAL 15555」(毎日8時〜24時)を、保健省が段階的に24時間化する方針。待ち時間を減らす折り返し電話も検討中。相談で一番多い悩みは「仕事のストレス」だという。開設から4年。 #メンタルヘルス #マレーシア</p></a><a class="xc" href="https://x.com/gcbfhq/status/2113060017540591787" target="_blank" rel="noopener"><time>2026年10月22日</time><p>カザフスタンでは、国の名簿に登録しないと「心理士」を名乗れなくなりました。9月施行の新法で、「サイコ〜」と紛らわしい肩書きも禁止。自称ヒーラーの締め出しが狙いです。登録の猶予は1年、10月13日には職業基準も発効。 #カザフスタン #メンタルヘルス</p></a><a class="xc" href="https://x.com/gcbfhq/status/2112710209227436094" target="_blank" rel="noopener"><time>2026年10月21日</time><p>1〜6のうち「4」だけ抜けた番号。中国の全国統一こころの相談電話「12356」は、「没四(4がない)」と「没事(大丈夫)」をかけて「大丈夫ダイヤル」と呼ばれる。広東省では330人が24時間交代で、月4.5万件超の電話を受ける。 #メンタルヘルス #中国</p></a></div><a class="go" href="https://x.com/gcbfhq" target="_blank" rel="noopener">Xで最新の投稿を見る</a></div>
<div class="snsb"><p class="en sl">INSTAGRAM</p><div class="tt"><p class="nm">星心会</p><p class="hd">@psr_seishinkai</p></div><div class="igg"><a href="https://www.instagram.com/psr_seishinkai/" target="_blank" rel="noopener"><img src="img/insta/02_rainbow.jpg" alt="星心会のInstagram投稿" loading="lazy"></a><a href="https://www.instagram.com/psr_seishinkai/" target="_blank" rel="noopener"><img src="img/insta/03_harvest.jpg" alt="星心会のInstagram投稿" loading="lazy"></a><a href="https://www.instagram.com/psr_seishinkai/" target="_blank" rel="noopener"><img src="img/insta/10_marigold.jpg" alt="星心会のInstagram投稿" loading="lazy"></a><a href="https://www.instagram.com/psr_seishinkai/" target="_blank" rel="noopener"><img src="img/insta/16_firewood_stove.jpg" alt="星心会のInstagram投稿" loading="lazy"></a><a href="https://www.instagram.com/psr_seishinkai/" target="_blank" rel="noopener"><img src="img/insta/09_mabo_tofu.jpg" alt="星心会のInstagram投稿" loading="lazy"></a><a href="https://www.instagram.com/psr_seishinkai/" target="_blank" rel="noopener"><img src="img/insta/21_plant_window.jpg" alt="星心会のInstagram投稿" loading="lazy"></a></div><a class="go" href="https://www.instagram.com/psr_seishinkai/" target="_blank" rel="noopener">Instagramで見る</a></div>
<div class="snsb thc"><p class="en sl">THREADS</p><div class="tt"><p class="nm">星心会</p><p class="hd">@psr_seishinkai</p></div><div class="thb"><p class="thm">@</p></div><a class="go" href="https://www.threads.com/@psr_seishinkai" target="_blank" rel="noopener">Threadsで見る</a></div>
</div></section>
<style>#news.blk{display:block}#news .h{margin-bottom:28px}.tt .hd{font-size:13px;opacity:.6;margin:2px 0 0}.xc{display:block;padding:14px 0;border-bottom:1px solid rgba(0,0,0,.15);color:inherit;text-decoration:none}.xc time{display:block;font-size:12px;opacity:.6;margin-bottom:6px}.xc p{font-size:14px;line-height:1.75;margin:0}.snsw{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;align-items:stretch}.snsb{height:500px;display:flex;flex-direction:column;gap:12px;border-top:2px solid currentColor;padding-top:12px;min-width:0}.snsb .sl{margin:0}.snss{flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch;min-height:0}.snss blockquote.twitter-tweet{margin:0 0 14px;padding:12px 0;border-bottom:1px solid rgba(0,0,0,.15);font-size:14px;line-height:1.7}.snss .twitter-tweet-rendered{margin:0 0 12px!important}.igg{display:grid;grid-template-columns:repeat(3,1fr);gap:4px}.igg img{width:100%;aspect-ratio:1;object-fit:cover;display:block}.snsb .nm{font-size:18px;font-weight:700;line-height:1.4;margin:0}.snsb .go{margin-top:auto}.thb{flex:1;display:flex;flex-direction:column;justify-content:center;gap:12px;background:#f3f3f1;padding:24px}.thm{font-size:72px;font-weight:700;line-height:1;margin:0}.tht{font-size:14px;margin:0}@media(max-width:800px){.snsw{grid-template-columns:1fr}.snsb{height:auto}.snss{height:440px;flex:none}.thb{min-height:220px}}</style>
'''
    o+='''<div class="dark"><section class="blk wide"><div class="h"><span class="en">ACCESS</span><h2>名古屋から<br>30分です。</h2></div><div>
<p class="big30">名古屋西IC<br>から車で <em>30</em>分</p>
<img class="stph" src="img/yamashiro_st.jpg" alt="三岐線 山城駅" loading="lazy" width="1600" height="1201" style="width:100%;height:auto;display:block;margin-top:24px"><ul class="lst" style="margin-top:24px;border-top-color:rgba(255,255,255,.4)"><li style="border-color:rgba(255,255,255,.12)">三岐線 山城駅から徒歩5分</li><li style="border-color:rgba(255,255,255,.12)">四日市駅から直通バス</li><li style="border-color:rgba(255,255,255,.12)">本部：三重県四日市市山城町59-4</li></ul>
<a class="go" href="access/" style="margin-top:28px">アクセスを見る</a></div></section></div>
<section class="cta" id="contact"><p class="en" style="color:var(--hi)">CONTACT</p><h2>相談する</h2><p style="font-size:13px;opacity:.7;margin-top:8px">どの事業か決まっていなくてもかまいません。</p>
<div class="row"><a class="w" href="contact/#line">LINE</a><a class="o" href="tel:0593150697">電話</a></div><a class="tnum" href="tel:0593150697">059-315-0697</a></section>'''
    o+=footer(rel); write('',o)
top()

# ---------- business index ----------
def biz(rel):
    ks=AUD[3][4]
    s='<section class="blk" style="max-width:1040px"><div class="h"><span class="en">FOR PARTNERS</span><h2>企業・支援機関の方へ</h2><p>企業、JEED（高齢・障害・求職者雇用支援機構）、ハローワーク、労働局の方へ。精神保健の現場で積んだ実務を、職場と住まいの両方で提供します。</p></div><div class="cards">'+''.join(card(k,rel) for k in ks)+'</div></section>'
    return s+partners(rel)
simple_page('business/','企業・支援機関の方へ｜雇用定着サポート・ストレスチェック・AIエージェント・研修｜星心会','企業、JEED、ハローワーク、労働局の方へ。雇用定着サポート、メンタルピアレジデンス・梁山泊、職場ストレスチェック、エージェントコンサル、研修を提供します。三重県四日市市の星心会です。','企業・支援機関の方へ','FOR PARTNERS',biz,photo='karate_class')

# ---------- about ----------
def about(rel): return f'''<section class="blk wide"><div class="h"><span class="en">PHILOSOPHY</span><h2>理念</h2></div><div>
<p class="big30" style="font-size:34px">まず、情緒の安定です。</p><p style="margin-top:14px;font-size:15px">メンタルヘルス不調に、まず必要なのは情緒の安定です。星心会は「あらぶる心を鎮める」ための環境を、住まい・日中・仕事・人間関係の全方位から整えます。公的制度は、そのための手段として使います。</p></div></section>
<div class="gal"><img src="{rel}img/forest_work.jpg" alt="森の整備" loading="lazy"><img src="{rel}img/harvest.jpg" alt="収穫" loading="lazy"><img src="{rel}img/ikebana.jpg" alt="生け花" loading="lazy"><img src="{rel}img/karate_studio.jpg" alt="道場" loading="lazy"></div>
<section class="blk wide"><div class="h"><span class="en">NAME</span><h2>名称の由来</h2></div><p style="font-weight:600;font-size:21px;line-height:2.1;letter-spacing:.12em">星に心があるならば<br>それを感じ取れるくらい<br>心こまやかな人たちの<br>集まりでありたいと考えています</p></section>
<section class="blk wide" style="padding-top:0"><div class="h"><span class="en">PROFILE</span><h2>法人概要</h2></div><dl class="info">
<dt>法人名</dt><dd>{ORG}</dd><dt>所在地</dt><dd>{ADDR}</dd><dt>電話</dt><dd>{TEL}</dd><dt>設立</dt><dd>令和3年12月13日</dd><dt>従業員数</dt><dd>15名 {ph('最新の人数')}</dd><dt>代表者</dt><dd>齊藤 蓮</dd>
<dt>スタッフ</dt><dd>公認心理師・精神保健福祉士などの有資格者</dd><dt>事業</dt><dd>{'<br>'.join(lab+'：'+'・'.join(SV[k][1] for k in ks) for _,lab,_,_,ks,_h in AUD)}</dd></dl></section>
<section class="blk wide" style="padding-top:0"><div class="h"><span class="en">REPRESENTATIVE</span><h2>代表</h2></div><div class="prose"><p><b>齊藤 蓮</b>（さいとう・れん）<br>公認心理師／精神保健福祉士／第二種衛生管理者／農福連携技術支援者（農林水産省認定）</p>
<p>1984年、三重県津市生まれです。早稲田大学第一文学部東洋哲学専修を卒業後、毎日新聞グループに入社しました。東京での6年間の企業勤務を経て精神保健福祉士に転身し、精神科デイケアに6年間勤務したのち、2022年に独立開業しました。現在、同朋大学大学院でメンタルヘルスのリハビリテーションを研究しています。</p></div></section>'''
simple_page('about/','星心会について｜理念・法人概要・代表｜三重県四日市市','一般社団法人 心理社会的リハビリテーション・星心会の理念「まず、情緒の安定です。」と、法人概要、代表プロフィールを掲載しています。三重県四日市市山城町。','星心会について','ABOUT',about,photo='walker')

# ---------- access ----------
MAP='https://www.google.com/maps/search/?api=1&query='
def access(rel): return f'''<section class="blk wide"><div class="h"><span class="en">FROM NAGOYA</span><h2>名古屋から<br>30分です。</h2></div><div><p class="big30">名古屋西IC<br>から車で <em>30</em>分</p><img class="stph" src="{rel}img/yamashiro_st.jpg" alt="三岐線 山城駅" loading="lazy" width="1600" height="1201" style="width:100%;height:auto;display:block;margin-top:24px">
<ul class="lst" style="margin-top:22px"><li><b>車</b>名古屋西ICから約30分です。</li><li><b>電車</b>三岐鉄道三岐線「山城」駅から徒歩5分です。</li><li><b>バス</b>四日市駅から直通バスがあります。 {ph('路線名・停留所名')}</li></ul></div></section>
<section class="blk wide" style="padding-top:0"><div class="h"><span class="en">LOCATIONS</span><h2>拠点</h2></div><ul class="lst">
<li><b>本部・水晶玉・RYDEEN・梁山泊</b>〒512-8048 三重県四日市市山城町59-4<br><a href="{MAP}三重県四日市市山城町59-4" target="_blank" rel="noopener" style="display:inline;color:var(--hi)">地図を開く</a></li>
<li><b>茶夢・レオ</b>〒512-8055 三重県四日市市あさけが丘2-1-42（山城駅から徒歩12分）<br><a href="{MAP}三重県四日市市あさけが丘2-1-42" target="_blank" rel="noopener" style="display:inline;color:var(--hi)">地図を開く</a></li>
<li><b>金斗雲</b>三重県三重郡菰野町田光1801-165</li><li><b>しちりんの会</b>三重県菰野町田光（詳しい場所は申し込み後にご案内します）</li></ul></section>
<section class="cta"><p class="en" style="color:var(--hi)">CONTACT</p><h2>相談する</h2><div class="row"><a class="w" href="{rel}contact/#line">LINE</a><a class="o" href="tel:0593150697">電話</a></div><a class="tnum" href="tel:0593150697">059-315-0697</a></section>'''
simple_page('access/','アクセス｜名古屋西ICから車で30分・三岐線山城駅から徒歩5分｜星心会（三重県四日市市）','星心会へは、名古屋西ICから車で約30分、三岐線山城駅から徒歩5分です。四日市駅から直通バスもあります。所在地は三重県四日市市山城町59-4です。','アクセス','ACCESS',access,photo='rainbow',sub='名古屋から30分です。')

# ---------- faq ----------
FAQ=[('費用はかかりますか？','事業によります。公的制度を使う事業は所得に応じた負担上限があり、多くの場合、自己負担なしまたは低額です。しちりんの会は自費参加（食材費込み3,000円）、梁山泊は一般の賃貸住居で、家賃は月8万円で、朝夕食事付きです。ほかに費用はかかりません。'),
('診断がなくても相談できますか？','できます。診断の有無は問いません。'),('家族から相談してもいいですか？','受け付けます。本人が動けない状態でも、家族からの相談で始められます。'),
NAGOYA,('どこに相談すればいいかわかりません。','水晶玉が全事業の入口です。どの事業か決まっていなくても、059-315-0697へご連絡ください。'),('名古屋からどのくらいかかりますか？','名古屋西ICから車で約30分です。三岐線 山城駅から徒歩5分、四日市駅から直通バスもあります。'),
('病院に通っていないと使えませんか？','使えます。通院の有無を前提にしていません。生活と環境の側から組み立てます。'),('人間関係に疲れています。どこに相談すればいいですか？','水晶玉で環境を整えるか、しちりんの会に参加してください。住まいごと変えたい方は梁山泊をご覧ください。')]
def faqb(rel): return '<section class="blk"><div>'+''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in FAQ)+'</div><p style="margin-top:30px;font-size:14px">事業ごとの質問は各ページにあります。</p><ul class="lst" style="margin-top:10px">'+''.join(f'<li><a href="{rel}{s[2]}#faq"><span>{s[1]}</span></a></li>' for s in SVCS)+'</ul></section>'
simple_page('faq/','よくある質問｜費用・診断・家族からの相談・名古屋から｜星心会','星心会のよくある質問です。費用、診断の有無、家族からの相談、名古屋在住でも利用できるか、アクセスについてお答えします。',"よくある質問",'FAQ',faqb,ld=[faq_ld(FAQ)])

# ---------- contact ----------
def contact(rel): return f'''<section class="blk"><div class="h"><span class="en">LINE</span><h2 id="line">公式LINE</h2><p>いちばん早い方法です。要点だけでかまいません。</p></div>
<a class="btn" href="#line" style="background:#06c755;width:100%;text-align:center">LINEで相談する</a><p style="margin-top:8px">{ph('公式LINEのURL')}</p></section>
<section class="blk" style="padding-top:0"><div class="h"><span class="en">TEL</span><h2>電話</h2></div><a class="big30" href="tel:0593150697" style="text-decoration:none;letter-spacing:.08em">059-315-0697</a><p style="color:var(--soft);font-size:13px;margin-top:6px">星心会（本部・全事業の窓口）　受付 {ph('受付日・時間')}</p>
<ul class="lst" style="margin-top:20px"><li><b>水晶玉</b><a href="tel:07032919626" style="display:inline">070-3291-9626</a></li><li><b>レオ</b><a href="tel:07069670011" style="display:inline">070-6967-0011</a></li></ul></section>
<section class="blk" style="padding-top:0"><div class="h"><span class="en">FORM</span><h2>フォーム</h2></div><form class="form" onsubmit="return false">
<label>相談したい事業</label><select><option>決まっていない</option>{''.join(f'<option>{s[1]}</option>' for s in SVCS)}</select>
<label>お名前</label><input type="text"><label>メールアドレス</label><input type="email"><label>内容（要点のみ）</label><textarea></textarea>
<button class="btn" type="submit" disabled style="margin-top:18px;width:100%">送信</button><p style="margin-top:8px">{ph('フォーム送信先（未設定のため送信不可）')}</p>
<p style="font-size:12px;color:var(--soft);margin-top:8px"><a href="{rel}privacy/">プライバシーポリシー</a>が適用されます。</p></form></section>'''
simple_page('contact/','相談する｜LINE・電話059-315-0697・フォーム｜星心会（三重県四日市市）','星心会への相談は、公式LINE、電話059-315-0697、相談フォームで受け付けます。どの事業か決まっていなくてもかまいません。','相談する','CONTACT',contact,sub='どの事業か、決まっていなくてもかまいません。')

# ---------- privacy ----------
def priv(rel): return f'''<section class="blk prose"><p>{ORG}（以下「当法人」）は、相談・問い合わせ等で取得した個人情報を、次のとおり取り扱います。</p>
<p><b>1. 利用目的</b><br>相談・問い合わせへの回答、サービスの提供と連絡のために利用します。</p><p><b>2. 第三者提供</b><br>法令に基づく場合を除き、本人の同意なく第三者に提供しません。</p>
<p><b>3. 管理</b><br>漏えい・滅失を防ぐため、適切に管理します。</p><p><b>4. 開示・訂正・削除</b><br>本人からの求めに応じ、法令に従って対応します。</p>
<p><b>5. アクセス解析</b><br>本サイトでは、アクセス解析ツールを使用する場合があります。{ph('使用ツール')}</p><p><b>6. 窓口</b><br>{ORG}　{ADDR}　TEL {TEL}</p><p>{ph('プライバシーポリシー全文の確認')}</p></section>'''
simple_page('privacy/','プライバシーポリシー｜星心会','星心会のプライバシーポリシーです。','プライバシーポリシー','PRIVACY',priv)

# ---------- sitemap page ----------
INFO=[('企業・支援機関の方へ','business/'),('星心会について','about/'),('アクセス','access/'),('よくある質問','faq/'),('相談する','contact/'),('プライバシーポリシー','privacy/')]
ALL=[('トップ','')]+[(s[1],s[2]) for s in SVCS]+INFO
def smap(rel):
    o='<section class="blk"><ul class="lst"><li><a href="'+rel+'"><span>トップ</span></a></li></ul>'
    for _,lab,en,_,ks,_h in AUD: o+=f'<h3 style="margin:30px 0 8px;font-size:15px">{lab}</h3><ul class="lst">'+''.join(f'<li><a href="{rel}{SV[k][2]}"><span>{SV[k][1]}</span></a></li>' for k in ks)+'</ul>'
    return o+'<h3 style="margin:30px 0 8px;font-size:15px">INFO</h3><ul class="lst">'+''.join(f'<li><a href="{rel}{u}"><span>{n}</span></a></li>' for n,u in INFO)+'</ul></section>'
simple_page('sitemap/','サイトマップ｜星心会','星心会のサイトマップです。対象者別に事業を並べています。','サイトマップ','SITEMAP',smap)
open(OUT+'/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{BASE}/{u}</loc></url>\n' for n,u in ALL+[('サイトマップ','sitemap/')])+'</urlset>\n')

# ---------- 404 (absolute-free: uses JS to find base) ----------
o=head('/seishinkai-preview/','ページが見つかりません｜星心会','','404.html')
o=o.replace('<link rel="canonical" href="'+BASE+'/404.html">','')
o=o.replace('<meta charset="utf-8">','<meta charset="utf-8">'+'''<script>/* 404 is served at any depth: rewrite relative links to site root */document.write('<base href="'+(location.pathname.startsWith('/seishinkai-preview/')?'/seishinkai-preview/':'/')+'">')</script>''',1)
o=o.replace('href="/seishinkai-preview/','href="')
write('404.html',o+header('')+'<section class="blk" style="text-align:center;min-height:60svh"><p class="en" style="color:var(--hi)">404</p><h1 style="font-weight:600;font-size:30px;letter-spacing:.14em;margin:10px 0 20px">ページが見つかりません</h1><a class="btn" href="./">トップへ</a> <a class="btn" href="contact/" style="background:var(--hi)">相談する</a></section>'+footer(''))

# ---------- robots / llms ----------
open(OUT+'/robots.txt','w').write('# TEST PHASE: block all crawlers. At launch replace with:\n# User-agent: *\n# Allow: /\n# Sitemap: '+BASE+'/sitemap.xml\nUser-agent: *\nDisallow: /\n')
L=f'''# 星心会（{ORG}）
> 環境調整によるメンタルヘルスケアを行う、三重県四日市市の専門組織です。名古屋西ICから車で約30分、三岐線山城駅から徒歩5分、四日市駅から直通バスがあります。電話は{TEL}、所在地は{ADDR}です。

眠れない、気分の波がある、仕事が続かない、親元にいると息が詰まる、といった悩みに環境調整で対応します。目的は情緒の安定です。精神科にも公的支援にも縁がなかった人を主な対象にしています。書類と手続きは星心会が進めます。全事業の相談窓口は水晶玉です。事業は対象者別に掲載しています（同じ事業が複数の対象に載ることがあります）。

'''
for _,lab,en,lead,ks,_h in AUD:
    L+=f'## {lab}向け\n{lead}\n'+''.join(f'- [{SV[k][1]}]({BASE}/{SV[k][2]}): {'。'.join(x for x in (SV[k][3],SV[k][4]) if x)}\n' for k in ks)+'\n'
L+='''補足：
- 茶夢は統合失調症・自閉症の方のための日中の居場所です。
- メンタルピアレジデンス・梁山泊は、障害者雇用で働く人の職場定着を支える住まいとケアの場です。企業・JEED・ハローワーク・労働局からの紹介・連携は本部（059-315-0697）が窓口です。
- しちりんの会は自費参加です（手続き・診断不要、不定期土曜11:00〜、三重県菰野町田光、食材費込み3,000円）。
- ストレスチェック実施者養成研修は、歯科医師・看護師・精神保健福祉士・公認心理師が対象です。Google Meetのリアルタイム開催で、科目1 2時間・科目2 1.5時間・科目3 1.5時間の計5時間です。受講料は3科目12,800円、科目1免除（衛生管理者）10,800円（いずれも税込）です。申込：https://rsaito-png.github.io/portal/sct.html
- 発達検査はWISC-V（小1〜高2）・新版K式（未就学児）で、各25,000円（税込）です。

## その他
'''+''.join(f'- [{n}]({BASE}/{u})\n' for n,u in INFO[:5])+'\n## SNS\n'+''.join(f'- {n}: {u}\n' for n,u in SNS)
open(OUT+'/llms.txt','w').write(L)

# ---------- redirect stubs ----------
RED=[('aboutus/','about/'),('dormitory/','ryozanpaku/'),('retreat/','kintoun/'),('kissa/','chamu/'),('j/privacy/','privacy/'),
('当事者様/','suishodama/'),('当事者様/無料お役立ちai/','suishodama/'),('保護者様/','leo/'),('保護者様/子どもの情緒安定-児発-放デイ/','leo/'),('保護者様/ペアレントトレーニング/','leo/parent-training/'),
('保護者様/発達検査/','leo/assessment/'),('保護者様/無料-お子様の学習支援ai/','leo/'),('企業様/','business/'),('企業様/職場ストレスチェック/','business/stress-check/'),('企業様/障害者雇用サポート/','business/employment/'),
('福祉-教育-医療関係者様/','business/'),('福祉-教育-医療関係者様/aiコンサル/','business/agent-consulting/'),('福祉-教育-医療関係者様/児童指導員-研修/','business/training/'),('福祉-教育-医療関係者様/消防コンサル/','business/')]
for old,new in RED:
    r='../'*old.count('/')+new
    write(old,f'<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><meta name="robots" content="noindex"><title>移動しました｜星心会</title><link rel="canonical" href="{BASE}/{new}"><meta http-equiv="refresh" content="0; url={r}"><script>location.replace("{r}"+location.hash)</script></head><body><p>このページは移動しました：<a href="{r}">{BASE}/{new}</a></p></body></html>')
open(OUT+'/.nojekyll','w').write('')
print('placeholders:',sorted(PH))

import sys as _sy
for _x in DUPLOG: print('DUP',*_x,file=_sy.stderr)
