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
    secs=[];cur=None
    for ln in clean(md).split('\n'):
        m=re.match(r'^(#{1,4})\s+(.*?)\s*#*\s*$',ln)
        if m:
            cur=[len(m.group(1)),m.group(2).replace('**','').strip(),[]];secs.append(cur)
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
def parse_page(md,d,ph):
    p=d['path'];g=h2groups(md);r={}
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
                    if lv==4 and bl and bl[-1][0]=='dl' and not x.startswith(('- ','> ')):
                        a,b=bl[-1][1][-1]; bl[-1][1][-1]=(a,(b+'<br>' if b else '')+f([x])); continue
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
    if '進め方' in g and not d.get('_old'):
        fl=[(t,f(ls)) for lv,t,ls in g['進め方'] if lv==3]
        if fl:
            ens=[x[0] for x in d['flow']]
            r['flow']=[[ens[i] if i<len(ens) else 'STEP',t,x] for i,(t,x) in enumerate(fl)]
    r['info']=[(t,f(ls)) for lv,t,ls in g.get('対象・費用・場所',[]) if lv==3]  # removed section => hide
    if 'よくある質問' in g: r['faq']=[(md2h([t],p,ph),f(ls)) for lv,t,ls in g['よくある質問'] if lv==3]
    return r
def top_md(t):
    o=['# トップページ',NOTE,'## 見出し',para(t['copy']),'## リード文',para(h2md(t['sub'])),'## 入口の見出し',t['entry_h'],'## 入口の説明',para(h2md(t['entry_p'])),'## 対象者別の説明']
    for k,lab,lead,hint in t['aud']: o+=['### '+lab,lead,'ボタンの小さい文字：'+hint]
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
    return r
