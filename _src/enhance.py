# 手置きHTML（レオ・茶夢・RYDEEN・トップ）も含め、ビルドの最後に追記ブロックを差し込む。
# <!--enh:ID--> ... <!--/enh:ID--> で囲み、毎回置き換えるので何度ビルドしても重複しない。
import os, re, json, html
BASE='https://psr-seishinkai.org'
CSS='''<style>.enh{max-width:880px;margin:0 auto;padding:56px 24px;line-height:1.95}.enh h2{font-size:24px;letter-spacing:.08em;margin:0 0 18px}.enh h3{font-size:17px;margin:26px 0 6px}.enh p{margin:0 0 10px}.enh .en{display:block;font-size:12px;letter-spacing:.2em;opacity:.6;margin-bottom:6px}.enh ol,.enh ul{padding-left:1.3em;margin:0 0 10px}.enh li{margin:4px 0}.enh dl{display:grid;grid-template-columns:8em 1fr;gap:8px 16px;margin:0}.enh dt{font-weight:700}.enh dd{margin:0}.enh a{color:inherit;text-decoration:underline}.enh .note{font-size:13px;opacity:.75}.enh .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}.enh .grid a{display:block;border:1px solid currentColor;border-radius:10px;padding:14px 16px;text-decoration:none}.enh .grid b{display:block;margin-bottom:4px}</style>'''
def sec(en,h,body,id_=''):
    return f'<section class="enh"{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}><span class="en">{en}</span><h2>{h}</h2>{body}</section>'
def faq_html(qa): return sec('FAQ','よくある質問',''.join(f'<h3>{q}</h3><p>{a}</p>' for q,a in qa),'faq')
def faq_ld(qa): return '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a)}} for q,a in qa]},ensure_ascii=False)+'</script>'
G='<a href="{r}guide/jukyushasho/">受給者証ガイド</a>'

FAQ={
'leo/':[('対象は何歳ですか？','満1歳から18歳までです。小学校入学前は児童発達支援、小学生以降は放課後等デイサービスとして利用します。'),
 ('診断がないと利用できませんか？','診断の有無は問いません。今の困りごとから始めます。'),
 ('費用はいくらですか？','公的制度（通所受給者証）を使います。所得に応じた負担上限があり、満3歳になって初めての4月1日から小学校入学前の3年間は、国の制度で利用者負担が無償です。昼食は1回300円です。手続きは'+G+'をご覧ください。'),
 ('利用時間は？','1部が11:00〜14:30、2部が放課後〜17:00です。'),
 ('送迎はありますか？','地域によって相談を受けます。お問い合わせの際にお住まいの地域をお知らせください。')],
'chamu/':[('診断がなくても利用できますか？','診断の有無は問いません。今の困りごとから始めます。'),
 ('人と話すのが苦手でも大丈夫ですか？','大丈夫です。少人数で活動しており、話さずに過ごすことも前提にしています。'),
 ('営業時間は？','平日11時〜15時です。短時間からの利用もできます。'),
 ('強度行動障害があっても相談できますか？','ご相談ください。状態をうかがったうえで、利用できるか一緒に考えます。'),
 ('家族だけで先に見学できますか？','できます。見学は予約制で、電話またはLINEで受け付けます。')],
'kintoun/':[('家族からの相談でも始められますか？','始められます。本人が相談できない状態を前提にしています。'),
 ('無理に外へ連れ出されませんか？','連れ出しを目的にはしません。話を聞くところから始めます。'),
 ('どこまで訪問してくれますか？','四日市市・菰野町を中心とした三重県内です。名古屋からの相談は、電話または相談フォームで受け付けます。'),
 ('費用は？','公的制度を使えます。所得に応じた負担上限があり、多くの方が無料または低額で利用しています。'),
 ('どんなスタッフが来ますか？','介護福祉士、看護師などの有資格者が対応します。')],
'ryozanpaku/':[('費用は？','家賃は月8万円で、朝夕食事付きです。ほかに費用はかかりません。'),
 ('働きながら住めますか？','住めます。働き続けるための住まいとして設計しています。'),
 ('親と離れて暮らせますか？','暮らせます。親元を出る段取り（住まい・日中・お金の手続き）はこちらで組みます。'),
 ('会社に知られずに入居できますか？','対応します。連絡方法は本人の指定に従います。'),
 ('企業や支援機関から紹介できますか？','できます。窓口は本部（059-315-0697）です。本人の同意のうえで、職場との情報共有の方法を決めます。')],
}
NEW_LD={'leo/','chamu/'}  # 他はビルドの FAQPage が既にある

def leo_blocks(r):
    day=sec('A DAY','1日の流れ','''<h3>1部（11:00〜14:30）</h3><ul><li>11:00 来所・あいさつ</li><li>活動：おもちゃ遊び、武道・ヨガ・農作業など（日によって変わります）</li><li>昼食：手作りの和定食（1回300円。偏食指導にも取り組みます）</li><li>14:30 終了</li></ul>
<h3>2部（放課後〜17:00）</h3><ul><li>学校が終わってから来所</li><li>遊びや体を動かす活動</li><li>17:00 終了</li></ul>
<p>季節の行事として、菰野町のフィールドで自然観察や七輪の火起こしなどをします。</p><p class="note">内容と順番は日によって変わります。見学のときに当日の様子をご覧いただけます。</p>''')
    start=sec('HOW TO START','利用開始までの流れ',f'''<ol><li><b>問い合わせ</b>　電話（070-6967-0011）またはLINEでご連絡ください。</li><li><b>見学</b>　お子さまと一緒に教室の様子をご覧ください。</li><li><b>受給者証の申請</b>　お住まいの市町で通所受給者証を申請します。四日市市はこども発達支援課（059-354-8064）、菰野町は子ども家庭課 発達支援係（059-391-1226）です。詳しくは<a href="{r}guide/jukyushasho/">受給者証ガイド</a>へ。</li><li><b>契約</b>　受給者証が届いたら、レオと利用契約を結びます。</li><li><b>利用開始</b>　個別支援計画にそって通所を始めます。</li></ol><p class="note">手続きでわからないことは、こちらで案内します。</p>''')
    ev=sec('EVALUATION','令和7年度 事業所評価（児童発達支援）の要点','''<p>保護者評価（対象11名・回答10名、2026年2月実施）と従業者評価（対象4名・回答3名）をもとにまとめた総括表の要点です。</p>
<h3>強み</h3><ul><li>体験型プログラムの多様性（茶道、畑、料理など）。季節に応じたイベントや、家庭では経験しにくい活動を取り入れています。</li><li>LINEによる高頻度・詳細な活動報告。毎回、活動の様子を写真と文章で共有しています。</li><li>専門性の高い個別支援と共感的な姿勢。職員一人ひとりがこどもの特性を理解し、寄り添った支援を行っています。</li></ul>
<h3>課題と改善の取り組み</h3><ul><li>業務継続計画（BCP）の浸透：具体的な場面を想定したロールプレイング研修を行い、役割分担を掲示します。</li><li>非常災害訓練・安全計画の周知：訓練の様子をLINEで配信・掲示し、安全計画をあらためて配布します。</li><li>地域交流の機会：近隣の公園や図書館などの利用を再開し、地域行事への参加を計画します。</li></ul>
<p class="note">放課後等デイサービスの評価と各評価表の全文は、このページの「令和7年度 事業所評価の公表」のPDFでご覧いただけます。</p>''')
    return day+start+ev

def chamu_more(r):
    return sec('ABOUT CHAMU','茶夢で過ごす1日',f'''<p>茶夢は、統合失調症・自閉症の方のための生活介護事業所です。生産活動を無理強いせず、ゆったり過ごしていただくことに専念しています。</p>
<h3>できること</h3><ul><li><b>料理</b>：一緒に台所に立ち、作って食べます。</li><li><b>喫茶</b>：お茶を淹れて、静かに過ごします。</li><li><b>読書</b>：好きな本を、好きなペースで読めます。</li><li><b>アート</b>：手を動かして表現します。</li></ul>
<h3>こんな方に</h3><ul><li>人が苦手で、大人数の場所がつらい方</li><li>日中に安心して過ごせる場所を探している方</li><li>強度行動障害があり、受け入れ先に困っている方（ご相談ください）</li></ul>
<h3>利用の流れ</h3><ol><li>電話またはLINEで見学を予約（ご家族だけの見学も可）</li><li>見学・面談</li><li>お住まいの市町で障害福祉サービスの申請（手続きはこちらで案内します）</li><li>契約・利用開始（短時間からでもかまいません）</li></ol>
<dl><dt>営業時間</dt><dd>平日 11時〜15時</dd><dt>場所</dt><dd>四日市市あさけが丘2-1-42（三岐線 山城駅 徒歩12分）</dd></dl>''')

def kintoun_more(r):
    return sec('AREA','訪問地域と、ご依頼の例','''<h3>訪問地域</h3><p>三重県四日市市・菰野町を中心に、三重県内へ訪問します。地域によっては対応できない場合があるため、まずはご住所をお知らせください。名古屋からの相談は、電話または<a href="../contact/">相談フォーム</a>で受け付けます。</p>
<h3>ご依頼の例</h3><p class="note">個人が特定されないよう、よくある相談の形にまとめています。</p><ul><li>「子どもが何年も部屋から出てこない。本人は相談に行かないので、まず家族の話を聞いてほしい」（ご家族から）</li><li>「精神的な不調で、役所や病院の窓口まで行けない。自宅で話を聞いてほしい」（ご本人から）</li><li>「どこに相談すればよいかわからない。費用も心配」（ご家族から）</li></ul>
<p>いずれも、まず話を聞くところから始めます。無理に外へ連れ出すことはしません。</p>''')

def eval_detail(kind,r):
    if kind=='assess': b='''<dl><dt>検査</dt><dd>WISC-V（小1〜高2）／新版K式発達検査（未就学児）</dd><dt>料金</dt><dd>各25,000円（税込）</dd><dt>含まれるもの</dt><dd>事前面談、検査実施、結果報告書の作成、フィードバック面談</dd><dt>担当</dt><dd>あんどう（公認心理師）</dd><dt>場所</dt><dd>レオ（四日市市あさけが丘2-1-42）</dd><dt>申し込み</dt><dd>電話またはLINE</dd></dl><h3>流れ</h3><ol><li>電話またはLINEで申し込み</li><li>事前面談</li><li>検査実施</li><li>結果報告書の作成</li><li>フィードバック面談</li></ol><p class="note">所要時間は検査の種類やお子さまの様子で変わるため、申し込み時にお問い合わせください。公的機関への提出を目的とする場合は、事前に提出先へ有効性をご確認ください。</p>'''
    else: b='''<dl><dt>内容</dt><dd>アドラー心理学に基づくペアレントトレーニング（個別相談）</dd><dt>日程</dt><dd>水曜午前（予約制）</dd><dt>費用</dt><dd>レオの利用者とそのご家族は無料。それ以外の方は1回4,000円</dd><dt>担当</dt><dd>加藤幸弘（公認心理師、学校心理士、日本アドラー心理学会認定カウンセラー）</dd><dt>場所</dt><dd>レオ（四日市市あさけが丘2-1-42）</dd></dl><h3>流れ</h3><ol><li>電話またはLINEで予約</li><li>カウンセラーが話を丁寧に聴きます</li><li>整理したことを、ご家庭で試します</li></ol><p class="note">1回あたりの時間は予約時にご確認ください。</p>'''
    return sec('DETAILS','料金・流れのまとめ',b)

def top_blocks(r):
    items=[('親元を出たい・働きながら暮らしたい','梁山泊','ryozanpaku/'),('日中に安心して過ごせる場所がほしい','茶夢','chamu/'),('家族が家から出られない','金斗雲','kintoun/'),('子どもが落ち着かない・発達が気になる','レオ','leo/'),('子どもへの関わり方に悩んでいる','ペアレントトレーニング','leo/parent-training/'),('子どもの特性を知りたい','発達検査','leo/assessment/'),('診断も手続きもなく、気軽に集まりたい','しちりんの会','shichirin/'),('どこに相談すればいいかわからない','相談フォーム','contact/')]
    g='<div class="grid">'+''.join(f'<a href="{r}{u}"><b>{q}</b>→ {n}</a>' for q,n,u in items)+'</div>'
    return sec('FIND','困りごとから探す',g+f'<p class="note" style="margin-top:14px">児童発達支援・放課後等デイサービスの手続きは<a href="{r}guide/jukyushasho/">受給者証ガイド</a>をご覧ください。</p>')+sec('NEWS','お知らせ',f'<p><a href="{r}news/">お知らせ一覧</a></p>')

PLAN=[ # path, id, html_fn, anchor ('cta' or regex)
 ('leo/','leoextra',leo_blocks,'cta'),
 ('chamu/','more',chamu_more,'cta'),
 ('kintoun/','area',kintoun_more,'cta'),
 ('leo/parent-training/','detail',lambda r:eval_detail('pt',r),'cta'),
 ('','find',top_blocks,r'<section class="blk" id="self">'),
]
def put(o,id_,block,anchor):
    o=re.sub(r'<!--enh:'+id_+r'-->.*?<!--/enh:'+id_+r'-->','',o,flags=re.S)
    blk=f'<!--enh:{id_}-->{block}<!--/enh:{id_}-->'
    if anchor=='head': return o.replace('</head>',blk+'</head>',1)
    pat=r'<section class="[^"]*cta[^"]*"' if anchor=='cta' else re.escape(anchor)
    m=re.search(pat,o) or re.search(r'<footer class="gf">',o)
    return o[:m.start()]+blk+o[m.start():] if m else o+blk
def run(OUT):
    todo={}
    for p,i,f,a in PLAN: todo.setdefault(p,[]).append((i,f,a))
    for p in FAQ: todo.setdefault(p,[]).append(('faq',lambda r,p=p:faq_html(FAQ[p]),'cta'))
    for p,lst in todo.items():
        fn=os.path.join(OUT,p,'index.html')
        if not os.path.isfile(fn): continue
        r='../'*p.count('/')
        o=open(fn,encoding='utf-8').read()
        o=put(o,'css',CSS,'head')
        for i,f,a in lst: o=put(o,i,f(r),a)
        if p in NEW_LD: o=put(o,'faqld',faq_ld(FAQ[p]),'head')
        open(fn,'w',encoding='utf-8').write(o)
