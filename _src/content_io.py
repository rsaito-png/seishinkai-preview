# Markdown <-> page data for Google Docs editing
import re,os,posixpath
BASE='https://www.psr-seishinkai.org'
NOTE='ここを書き換えると、サイトに反映されます'
def slug(path): return path.strip('/').replace('/','-') or 'top'
PHR=re.compile(r'<span class="ph">要確認：(.*?)</span>')
def h2md(s,path=''):
    s=PHR.sub(lambda m:'【要確認：'+m.group(1)+'】',s)
    s=s.replace('<wbr>','')
    s=re.sub(r'<b>(.*?)</b>',r'**\1**',s)
    def lk(m):
        u=m.group(1)
        if not u.startswith('http'): u=BASE+'/'+posixpath.normpath(posixpath.join(path,u)).lstrip('./')+'/'
        return f'[{m.group(2)}]({u})'
    s=re.sub(r'<a href="([^"]+)"[^>]*>(.*?)</a>',lk,s)
    return [x.strip() for x in re.split(r'<br\s*/?>',s)]
def md2h(lines,path='',ph=None):
    rel='../'*path.count('/')
    out=[]
    for s in lines:
        s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
        def lk(m):
            u=m.group(2)
            if u.startswith(BASE+'/'): u=rel+u[len(BASE)+1:]
            return f'<a href="{u}" style="display:inline;color:var(--hi)">{m.group(1)}</a>'
        s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lk,s)
        s=re.sub(r'【要確認：(.*?)】',lambda m:ph(m.group(1)) if ph else m.group(0),s)
        out.append(s)
    return '<br>'.join(out)
def para(lines): return '\n\n'.join(lines)
def page_md(d,old_blocks=None):
    p=d['path']; o=[f'# {d["name"]}',NOTE,'## 見出し',para(d['copy']),'## リード文',para(h2md(d['sub'],p)),'## 本文']
    if old_blocks:
        for t,v in old_blocks:
            if t=='h': o.append('### '+' '.join(h2md(v,p)))
            elif t=='p': o.append(para(h2md(v,p)))
            elif t=='note': o.append('\n\n'.join('> '+x for x in h2md(v,p)))
            elif t=='ul': o.append('\n'.join('- '+' '.join(h2md(x,p)) for x in v))
            elif t=='img':
                src,alt=v; o.append(f'![{alt}](../img/{src}.jpg)' if not str(src).endswith(('.jpg','.png','.webp')) else f'![{alt}]({src})')
            elif t=='dl':
                for a,b in v: o+=['#### '+' '.join(h2md(a,p)),para(h2md(b,p))]
    else:
        for n,s,a in d['what']: o+=['### '+n+(f'｜{s}' if s else ''),para(h2md(a,p))]
        o.append('## 進め方')
        for en,t,x in d['flow']: o+=['### '+t,para(h2md(x,p))]
    o.append('## 対象・費用・場所')
    for k,v in d['info']: o+=['### '+k,para(h2md(v,p))]
    o.append('## よくある質問')
    for q,a in d['faq']: o+=['### '+q,para(h2md(a,p))]
    return '\n\n'.join(o)+'\n'
def clean(md):
    md=md.replace('\r','')
    md=re.sub(r'\\([\\`*_{}\[\]()#+\-.!>~|<])',r'\1',md)
    md=re.sub(r'^\s*[*+]\s+','- ',md,flags=re.M)
    md=md.replace('\u00a0',' ')
    return md
def split(md):
    """returns list of (level,title,[lines]) sections"""
    secs=[];cur=None;h2='';prev=''
    for ln in clean(md).split('\n'):
        m=re.match(r'^(#{1,4})\s+(.*?)\s*#*\s*$',ln)
        # Docs export: a heading whose style was lost becomes "title<2 spaces>" + soft return + body.
        # In info/FAQ sections treat such a paragraph-opening line as an h3 (text unchanged).
        if not m and (h2.startswith('対象・費用') or h2=='よくある質問') and not prev.strip() and re.search(r'\S {2,}$',ln):
            m=re.match(r'^()(.*?)\s*$',ln); m=('###',ln.strip())
            cur=[3,m[1],[]];secs.append(cur);prev=ln;continue
        prev=ln
        if m:
            cur=[len(m.group(1)),m.group(2).replace('**','').strip(),[]];secs.append(cur)
            if cur[0]==2: h2=cur[1]
        elif cur is not None and ln.strip(): cur[2].append(ln.strip())
    return secs
def h2groups(md):
    g={};order=[];cur=None
    for lv,t,ls in split(md):
        if lv==2: cur=t;g[cur]=[];order.append(cur)
        elif cur and lv>=3: g[cur].append((lv,t,ls))
        if lv==2 and ls: g[cur].append((0,'',ls))
    return g
def lines(ls): return [x for x in ls if x!=NOTE]
# Top-page business cards. Match #### headings to SVCS keys by the current Japanese names.
CARD_NAMES=[
('ストレスチェック実施者養成研修','sct'),('実施者養成研修','sct'),
('ペアレントトレーニング','parent'),('雇用定着サポート','employment'),('エージェントコンサル','agent'),
('しちりんの会','shichirin'),('ストレスチェック','stress'),('発達検査','assess'),
('水晶玉','suishodama'),('梁山泊','ryozanpaku'),('金斗雲','kintoun'),('茶夢','chamu'),
('レオ','leo'),('研修','training'),('RYDEEN','rydeen'),('ライディーン','rydeen')]
CARD_KEYS={n:k for n,k in CARD_NAMES}
CARD_IDS={'suishodama','shichirin','rydeen','ryozanpaku','kintoun','chamu','leo','parent','assess','employment','stress','sct','agent','training'}
CARD_LABEL={'suishodama':'水晶玉','shichirin':'しちりんの会','rydeen':'RYDEEN','ryozanpaku':'梁山泊','kintoun':'金斗雲','chamu':'茶夢','leo':'レオ','parent':'ペアレントトレーニング','assess':'発達検査','employment':'雇用定着サポート','stress':'ストレスチェック','sct':'ストレスチェック実施者養成研修','agent':'エージェントコンサル','training':'研修'}
CARD_GROUPS=[('ご本人',['suishodama','shichirin','rydeen','ryozanpaku']),('ご家族',['kintoun','chamu']),('お子さまの保護者',['leo','parent','assess']),('企業・支援機関',['employment','stress','sct','agent','training'])]
def card_key(name):
    """Map a #### heading or svc key to an SVCS key. Longer Japanese names win."""
    raw=re.sub(r'\*','',(name or '')).strip()
    if not raw: return None
    if raw in CARD_IDS: return raw
    if raw in CARD_KEYS: return CARD_KEYS[raw]
    base=re.sub(r'[（(].*?[）)]','',raw).strip()
    flat=re.sub(r'\s+','',base)
    for cand in (base,flat):
        if cand in CARD_IDS: return cand
        if cand in CARD_KEYS: return CARD_KEYS[cand]
    best=None
    for n,k in sorted(CARD_NAMES,key=lambda x:len(x[0]),reverse=True):
        nn=re.sub(r'\s+','',n)
        if nn and (nn in flat or n in raw or nn.lower() in flat.lower()):
            best=(nn,k); break
    return best[1] if best else None
def _card_group(title):
    t=re.sub(r'[\s*]+','',title or '')
    t=re.sub(r'[（(].*?[）)]','',t)
    for a,g in (('お子さまの保護者','お子さまの保護者'),('お子様の保護者','お子さまの保護者'),('企業・支援機関','企業・支援機関'),('ご本人','ご本人'),('ご家族','ご家族'),('保護者','お子さまの保護者')):
        if t==a or t.startswith(a): return g
    return None
def _card_fields(ls):
    cat=line=None; cur=None
    for raw in ls:
        x=raw.replace('**','').strip()
        if not x or x==NOTE: continue
        m=re.match(r'^(カテゴリ|一行案内|一行)\s*[:：]\s*(.*)$',x)
        if m:
            cur='cat' if m.group(1)=='カテゴリ' else 'line'
            val=m.group(2).strip()
            if cur=='cat': cat=val if cat is None else (cat+val).strip()
            else: line=val if line is None else (line+val).strip()
        elif cur=='cat': cat=((cat or '')+x).strip()
        elif cur=='line': line=((line or '')+x).strip()
    return cat,line
def _card_rec(title,cat,line,key):
    disp=re.sub(r'\*','',title or '').strip()
    r={'name':CARD_LABEL.get(key,disp) if (not disp or disp in CARD_IDS) else disp}
    if cat is not None: r['cat']=cat
    if line is not None: r['line']=line
    return r
def _bare_key(line):
    """A line that is exactly a known card name (not a カテゴリ/一行案内 label)."""
    t=re.sub(r'[\s　*]+','',line or '')
    if not t or re.match(r'^(カテゴリ|一行案内|一行)',t): return None
    if t in CARD_IDS: return t
    return CARD_KEYS.get(t)
def _field_line(x):
    return bool(re.match(r'^(カテゴリ|一行案内|一行)\s*[:：]',x or ''))
def _chunks(title,ls):
    """Split one heading's body when a card name is a plain line (no ####), as with ペアレントトレーニング."""
    rows=[raw.replace('**','').strip() for raw in ls if raw.replace('**','').strip() and raw.strip()!=NOTE]
    out=[]; ct=title; buf=[]
    for i,x in enumerate(rows):
        nxt=rows[i+1] if i+1<len(rows) else ''
        k=_bare_key(x)
        if not _field_line(x) and (k or _field_line(nxt)) and (buf or (k and k!=card_key(ct))):
            if k!=card_key(ct):
                out.append((ct,buf)); ct=x; buf=[]; continue
        buf.append(x)
    out.append((ct,buf))
    return out
def _parse_cards(sec):
    """#### name under ### audience. A bare card-name line also starts a card. Name match first."""
    cards={}; used=set(); group=None; pos=0; pending=[]
    groups={lab:ks for lab,ks in CARD_GROUPS}
    def flush():
        nonlocal pending
        ks=groups.get(group) or []
        for p,title,cat,line in pending:
            key=ks[p] if p<len(ks) and ks[p] not in used else next((k for k in ks if k not in used),None)
            if not key: continue
            used.add(key); cards[key]=_card_rec(title,cat,line,key)
        pending=[]
    def take(title,ls):
        nonlocal pos
        cat,line=_card_fields(ls); key=card_key(title)
        if key and key not in used:
            used.add(key); cards[key]=_card_rec(title,cat,line,key)
        else: pending.append((pos,title,cat,line))
        pos+=1
    for lv,title,ls in sec:
        if lv==3 and _card_group(title):
            flush(); group=_card_group(title); pos=0; continue
        if lv>=4 or (lv==3 and card_key(title) and not _card_group(title)):
            for ct,cls in _chunks(title,ls): take(ct,cls)
    flush(); return cards
def _norm_h(s):
    s=re.sub(r'[\s　*]+','',s or '')
    return re.sub(r'[（(].*?[）)]','',s)
def _misc_block(g,name):
    """### heading under a named ## section. None when the section is absent."""
    sec=None
    for k,v in g.items():
        if name in _norm_h(k): sec=v; break
    if sec is None: return None
    out={}
    cur=None
    for lv,title,ls in sec:
        body=[x for x in ls if x and x!=NOTE]
        if lv==3:
            cur=_norm_keep(title); out[cur]={'lines':body,'h4':[]}
        elif lv>=4 and cur:
            out[cur]['h4'].append((_norm_keep(title),body))
        elif (lv==0 or lv is None) and not cur:
            for x in body:
                m=re.match(r'^([^：:]{1,30})[:：]\s*(.*)$',x.replace('**','').strip())
                if m: out[_norm_keep(m.group(1))]={'lines':[m.group(2).strip()] if m.group(2).strip() else [],'h4':[]}
    return out
def _norm_keep(title):
    return re.sub(r'\*','',title or '').strip()
def pick_slot(title,table):
    """Exact heading match, else the longest prefix. table is [(aliases, slot)]."""
    t=_norm_h(title)
    if not t: return None
    pref=None
    for keys,slot in table:
        for k in keys:
            kk=_norm_h(k)
            if t==kk: return slot
            if kk and t.startswith(kk) and (pref is None or len(kk)>len(pref[0])): pref=(kk,slot)
    return pref[1] if pref else None
def misc_slots(block,table):
    """Map recognized ### headings to {slot: block}. Unknown headings are ignored."""
    if not block: return {}
    out={}
    for title,body in block.items():
        slot=pick_slot(title,table)
        if slot and slot not in out: out[slot]=dict(body,title=title)
    return out
PAGE_SLOTS=[
 (['事業名の下の一行','事業名の下'],'under'),
 (['バッジ'],'badge'),
 (['写真下のアクセス','写真下の一行','写真下'],'acc'),
 (['本文ボタン欄の見出し','本文の見出し'],'what'),
 (['関連ページボタン','関連ページ','下の関連'],'rel'),
 (['申し込み欄の見出し','申し込み欄'],'cta'),
 (['企業・支援機関の方へ'],'partners'),
 (['保護者向けプログラム'],'parents'),
 (['代表齊藤のGrokBotの使い方','GrokBotの使い方','代表齊藤の使い方','追加の欄：代表齊藤の使い方'],'howto'),
 (['追加の欄：Grok Botの活躍','Grok Botの活躍','GrokBotの活躍','実際の作業画面'],'demo'),
 (['申込ページへ'],'apply'),
 (['見出し下2行','見出しの下','見出し下'],'sub')]
TOP_SLOTS=[
 (['見出しの下のアクセス','見出し下のアクセス','見出し下アクセス'],'hero_acc'),
 (['企業・支援機関の欄の下のボタン'],'partner_btn'),
 (['SNS欄','SNS'],'sns'),
 (['アクセス欄'],'access'),
 (['相談欄'],'contact')]
NAV_SLOTS=[
 (['上のメニュー','上メニュー'],'top'),
 (['開くメニュー','ドロワー'],'drawer'),
 (['フッター'],'foot'),
 (['各ページ共通の部品','共通の部品'],'parts'),
 (['もどる／次へ','もどる/次へ'],'steps'),
 (['もどる'],'prev'),
 (['次へ'],'next')]
def _cards_by_key(cards):
    by={}
    if isinstance(cards,dict): items=list(cards.items())
    elif isinstance(cards,(list,tuple)):
        items=[]
        for v in cards:
            if isinstance(v,dict): items.append((v.get('key') or v.get('name'),v))
    else: return by
    for k,v in items:
        if isinstance(v,(list,tuple)): v={'name':v[0] if v else '','cat':v[1] if len(v)>1 else None,'line':v[2] if len(v)>2 else None}
        if not isinstance(v,dict): continue
        key=k if k in CARD_IDS else card_key(str(k) if k else '')
        if not key: key=card_key(v.get('name') or '')
        if key: by[key]=v
    return by
def parse_page(md,d,ph):
    p=d['path'];g=h2groups(md);r={}
    pre=[];seen=False
    for x in md.splitlines():
        x=x.strip()
        if x.startswith('# '): seen=True; continue
        if x.startswith('## '): break
        if seen and x and x!=NOTE: pre.append(x)
    r['_pre']=' '.join(pre)
    f=lambda ls:md2h(lines(ls),p,ph)
    if g.get('見出し'): r['copy']=[x for _,_,ls in g['見出し'] for x in lines(ls)]
    if g.get('リード文'): r['sub']=f([x for _,_,ls in g['リード文'] for x in ls])
    if '本文' in g:
        if d.get('_old'):
            bl=[]
            for lv,t,ls in g['本文']:
                if lv==3: bl.append(('h',md2h([t],p,ph)))
                if lv==4: bl.append(('dl',[(md2h([t],p,ph),'')]))
                buf=[]
                def flush():
                    if buf: bl.append(('p',f(buf))); buf.clear()
                for x in ls:
                    if lv==4 and bl and bl[-1][0]=='dl' and not x.startswith(('- ','> ','![')):
                        a,b=bl[-1][1][-1]; bl[-1][1][-1]=(a,(b+'<br>' if b else '')+f([x])); continue
                    mimg=re.match(r'^!\[([^\]]*)\]\(([^)]+)\)\s*$',x)
                    if mimg:
                        flush(); src=mimg.group(2).strip(); alt=mimg.group(1).strip() or ''
                        # normalize ../img/foo.jpg -> foo
                        m2=re.search(r'/img/([^/]+?)\.(?:jpg|jpeg|png|webp)$',src,re.I)
                        if m2: src=m2.group(1)
                        elif src.endswith(('.jpg','.jpeg','.png','.webp')): src=re.sub(r'\.(?:jpg|jpeg|png|webp)$','',src,flags=re.I)
                        bl.append(('img',(src,alt))); continue
                    if x.startswith('- '):
                        flush(); it=f([x[2:]])
                        if bl and bl[-1][0]=='ul' and bl[-1][2]: bl[-1][1].append(it)
                        else: bl.append(('ul',[it],True))
                        continue
                    if x.startswith('>'):
                        flush(); bl.append(('note',f([x.lstrip('> ').strip()]))); continue
                    if bl and bl[-1][0]=='ul': bl[-1]=('ul',bl[-1][1],False)
                    buf.append(x)
                flush()
                if bl and bl[-1][0]=='ul': bl[-1]=('ul',bl[-1][1],False)
            # merge consecutive dl
            out=[]
            for b in bl:
                if b[0]=='ul': b=('ul',b[1])
                if b[0]=='dl' and out and out[-1][0]=='dl': out[-1][1].extend(b[1])
                else: out.append((b[0],list(b[1]) if b[0] in('dl','ul') else b[1]))
            # merge consecutive notes/p lines into original style: each paragraph is own block
            r['old']=out
        else:
            w=[]
            for lv,t,ls in g['本文']:
                if lv==3: n,_,s=t.partition('｜'); w.append((n,s,f(ls)))
            if w: r['what']=w
            r['what_intro']=f([x for lv,t,ls in g['本文'] if lv==0 for x in ls])
    if '進め方' in g and not d.get('_old'):
        fl=[(t,f(ls)) for lv,t,ls in g['進め方'] if lv==3]
        if fl:
            ens=[x[0] for x in d['flow']]
            r['flow']=[[ens[i] if i<len(ens) else 'STEP',t,x] for i,(t,x) in enumerate(fl)]
    if g.get('保護者の声'): r['voice']=[f([x]) for _,_,ls in g['保護者の声'] for x in lines(ls)]
    r['info_h']=next((k for k in g if k.startswith('対象・費用')),None)
    r['info']=[(t,f(ls)) for lv,t,ls in next((v for k,v in g.items() if k.startswith('対象・費用')),[]) if lv==3]  # removed section => hide
    if 'よくある質問' in g: r['faq']=[(md2h([t],p,ph),f(ls)) for lv,t,ls in g['よくある質問'] if lv==3]
    misc=_misc_block(g,'ページのその他の表示')
    if misc is not None: r['misc']=misc
    return r
def top_md(t):
    o=['# トップページ',NOTE,'## 見出し',para(t['copy']),'## リード文',para(h2md(t['sub'])),'## 入口の見出し',t['entry_h'],'## 入口の説明',para(h2md(t['entry_p'])),'## 対象者別の説明']
    for k,lab,lead,hint in t['aud']: o+=['### '+lab,lead,'ボタンの小さい文字：'+hint]
    by=_cards_by_key(t.get('cards'))
    if by:
        o.append('## 事業カード（トップに並ぶ案内）')
        for lab,ks in CARD_GROUPS:
            rows=[(k,by[k]) for k in ks if k in by]
            if not rows: continue
            o.append('### '+lab)
            for k,v in rows:
                nm=(v.get('name') or '').strip() or CARD_LABEL[k]
                o.append('#### '+nm)
                if 'cat' in v and v['cat'] is not None: o.append('カテゴリ：'+v['cat'])
                if 'line' in v and v['line'] is not None: o.append('一行案内：'+v['line'])
    return '\n\n'.join(o)+'\n'
def parse_top(md,t):
    g=h2groups(md);r=dict(t)
    j=lambda k:[x for _,_,ls in g.get(k,[]) for x in lines(ls)]
    if j('見出し'): r['copy']=j('見出し')
    if j('リード文'): r['sub']=md2h(j('リード文'))
    if j('入口の見出し'): r['entry_h']=''.join(j('入口の見出し'))
    if j('入口の説明'): r['entry_p']=md2h(j('入口の説明'))
    if '対象者別の説明' in g:
        m={lab:(k,lab,lead,hint) for k,lab,lead,hint in t['aud']}
        for lv,lab,ls in g['対象者別の説明']:
            if lv==3 and lab in m:
                k,_,lead,hint=m[lab]
                L=[x for x in ls if not x.startswith('ボタンの小さい文字')]; H=[x.split('：',1)[1] for x in ls if x.startswith('ボタンの小さい文字')]
                m[lab]=(k,lab,md2h(L) if L else lead,H[0] if H else hint)
        r['aud']=list(m.values())
    for k,sec in g.items():
        if '事業カード' in re.sub(r'\s+','',k):
            r['cards']=_parse_cards(sec); break
    misc=_misc_block(g,'ページのその他の表示')
    nav=_misc_block(g,'共通ナビ・フッター')
    if misc is not None: r['misc']=misc
    if nav is not None: r['nav']=nav
    return r
