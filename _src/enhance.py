# 手置きHTML（レオ・茶夢・RYDEEN・トップ）も含め、ビルドの最後に追記ブロックを差し込む。
# <!--enh:ID--> ... <!--/enh:ID--> で囲み、毎回置き換えるので何度ビルドしても重複しない。
import os, re, json, html
import leo_llmo
BASE='https://psr-seishinkai.org'
CSS='''<style>.enh{max-width:880px;margin:0 auto;padding:56px 24px;line-height:1.95}.enh h2{font-size:24px;letter-spacing:.08em;margin:0 0 18px}.enh h3{font-size:17px;margin:26px 0 6px}.enh p{margin:0 0 10px}.enh .en{display:block;font-size:12px;letter-spacing:.2em;opacity:.6;margin-bottom:6px}.enh ol,.enh ul{padding-left:1.3em;margin:0 0 10px}.enh li{margin:4px 0}.enh dl{display:grid;grid-template-columns:8em 1fr;gap:8px 16px;margin:0}.enh dt{font-weight:700}.enh dd{margin:0}.enh a{color:inherit;text-decoration:underline}.enh .note{font-size:13px;opacity:.75}.enh .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}.enh .grid a{display:block;border:1px solid currentColor;border-radius:10px;padding:14px 16px;text-decoration:none}.enh .grid b{display:block;margin-bottom:4px}.enh#faq details{border-bottom:1px solid rgba(0,0,0,.12);padding:0}.enh#faq summary{cursor:pointer;list-style:none;box-sizing:border-box;display:flex;align-items:center;justify-content:space-between;gap:16px;width:100%;padding:16px 4px;min-height:52px;font-weight:700;font-size:16px;line-height:1.45;text-align:left}.enh#faq summary::-webkit-details-marker{display:none}.enh#faq summary:after{content:'+';flex:0 0 auto;font-weight:500;font-size:22px;line-height:1;opacity:.45}.enh#faq details[open] summary:after{content:'\\2212'}.enh#faq details>div{padding:0 4px 18px;font-size:15px;line-height:1.9}.enh#faq summary:focus-visible{outline:2px solid currentColor;outline-offset:2px}.enh .cm-who-list,.enh .cm-act-grid,.enh .cm-steps{padding-left:0;margin:0}.enh .cm-who-list{display:grid;gap:10px;list-style:none}.enh .cm-who-list li{background:rgba(0,0,0,.03);border-radius:12px;padding:14px 16px;margin:0}.enh .cm-act-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;list-style:none}.enh .cm-act-grid li{background:rgba(0,0,0,.03);border-radius:12px;padding:16px 16px 14px;margin:0}.enh .cm-act-grid b{display:block;margin:0 0 4px;font-size:15px}.enh .cm-steps{display:grid;gap:10px;list-style:none;counter-reset:step}.enh .cm-steps li{counter-increment:step;display:grid;grid-template-columns:2.2em 1fr;gap:12px;align-items:start;background:rgba(0,0,0,.03);border-radius:12px;padding:14px 16px;margin:0}.enh .cm-steps li:before{content:counter(step);font-weight:700;opacity:.5}@media(max-width:640px){.enh .cm-act-grid{grid-template-columns:1fr}}</style>'''
def sec(en,h,body,id_=''):
    return f'<section class="enh"{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}><span class="en">{en}</span><h2>{h}</h2>{body}</section>'
def faq_html(qa): return sec('FAQ','よくある質問',''.join(f'<details><summary>{q}</summary><div>{a}</div></details>' for q,a in qa),'faq')
def faq_ld(qa): return '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a)}} for q,a in qa]},ensure_ascii=False)+'</script>'
G='<a href="{r}guide/jukyushasho/">受給者証ガイド</a>'

FAQ={
# レオのFAQは /leo/faq/ に移し、このページへは注入しない。
'chamu/':[('診断がなくても利用できますか？','診断の有無は問いません。今の困りごとから始めます。'),
 ('人と話すのが苦手でも大丈夫ですか？','大丈夫です。少人数で活動しており、話さずに過ごすことも前提にしています。'),
 ('営業時間は？','平日11時〜15時です。短時間からの利用もできます。'),
 ('強度行動障害があっても相談できますか？','ご相談ください。状態をうかがったうえで、利用できるか一緒に考えます。'),
 ('家族だけで先に見学できますか？','できます。見学は予約制で、電話または問合せフォームで受け付けます。'),
 ('病院に通っていなくても利用できますか？','利用できます。通院の有無は前提にしていません。'),
 ('費用はどのくらいかかりますか？','公的制度を使います。所得に応じた負担上限があり、多くの場合、自己負担なしまたは低額です。'),
 ('土日や祝日は利用できますか？','土曜日、日曜日、祝日はお休みです。'),
 ('今、空きはありますか？','2026年12月時点で、空きはあります。'),
 ('四日市市以外からも通えますか？','送迎は応相談です。'),
 ('相談支援専門員ですが、茶夢さんは共生型と聞きました。','はい。短時間の利用も歓迎いたします。繊細な方にとってなるべくハードルを下げた事業所であることを目指しています。')],
'kintoun/':[('家族からの相談でも始められますか？','始められます。本人が相談できない状態を前提にしています。'),
 ('無理に外へ連れ出されませんか？','連れ出しを目的にはしません。話を聞くところから始めます。'),
 ('どこまで訪問してくれますか？','四日市市・菰野町を中心とした三重県内です。名古屋からの相談は、電話または問合せフォームで受け付けます。'),
 ('費用は？','公的制度を使えます。所得に応じた負担上限があり、多くの方が無料または低額で利用しています。'),
 ('どんなスタッフが来ますか？','介護福祉士、看護師などの有資格者が対応します。')],
'ryozanpaku/':[('親に知られずに相談できますか？','常識の範囲内でご希望に応じます。'),
 ('空室はありますか？部屋は何室ですか？','部屋は5室です。2026年12月時点で、空きは2室あります。入居できるのは男性の方です。'),
 ('入居時にかかる費用は？','入居支度金として合計16万円をいただきます。'),
 ('生活の支援はありますか？','宿直の職員がいます。食事の提供、ヘルパーによる家事援助（掃除・洗濯・洗い物など）、相談援助があります。'),
 ('県外や遠方からでも入れますか？','はい。県外からでも、日本全国から入居できます。見学は、電話または問合せフォームで受け付けます。'),
 ('四日市でグループホームを探しています。梁山泊は候補になりますか？','四日市市にありますが、グループホーム（共同生活援助）ではありません。一般の賃貸住居で、居宅介護を利用できます。受給者証は不要です。'),
 ('県外から入るとき、役所の手続きは必要ですか？','グループホーム（共同生活援助）ではないため、入居先の市町村で受給者証を申請する必要はありません。')],
}
NEW_LD={'chamu/'}  # レオの FAQPage は /leo/faq/ に置く

def leo_blocks(r):
    ev=sec('EVALUATION','令和7年度 事業所評価（児童発達支援）の要点','''<p>保護者評価（対象11名・回答10名、2026年2月実施）と従業者評価（対象4名・回答3名）をもとにまとめた総括表の要点です。</p>
<h3>強み</h3><ul><li>体験型プログラムの多様性（茶道、畑、料理など）。季節に応じたイベントや、家庭では経験しにくい活動を取り入れています。</li><li>LINEによる高頻度・詳細な活動報告。毎回、活動の様子を写真と文章で共有しています。</li><li>専門性の高い個別支援と共感的な姿勢。職員一人ひとりがこどもの特性を理解し、寄り添った支援を行っています。</li></ul>
<h3>課題と改善の取り組み</h3><ul><li>業務継続計画（BCP）の浸透：具体的な場面を想定したロールプレイング研修を行い、役割分担を掲示します。</li><li>非常災害訓練・安全計画の周知：訓練の様子をLINEで配信・掲示し、安全計画をあらためて配布します。</li><li>地域交流の機会：近隣の公園や図書館などの利用を再開し、地域行事への参加を計画します。</li></ul>
<p class="note">放課後等デイサービスの評価と各評価表の全文は、このページの「令和7年度 事業所評価の公表」のPDFでご覧いただけます。</p>''')
    return ev+leo_llmo.facts_html(r)

def chamu_more(r):
    return sec('ABOUT CHAMU','茶夢で過ごす1日','''<h3>できること</h3>
<ul class="cm-act-grid"><li><b>料理</b>一緒に台所に立ち、作って食べます。</li><li><b>喫茶</b>お茶を淹れて、静かに過ごします。</li><li><b>読書</b>好きな本を、好きなペースで読めます。</li><li><b>アート</b>手を動かして表現します。</li></ul>
<h3>こんな方に</h3>
<ul class="cm-who-list"><li>人が苦手で、大人数の場所がつらい方</li><li>日中に安心して過ごせる場所を探している方</li><li>強度行動障害があり、受け入れ先に困っている方（ご相談ください）</li></ul>
<h3>利用の流れ</h3>
<ol class="cm-steps"><li>電話または問合せフォームで見学を予約（ご家族だけの見学も可）</li><li>見学・面談</li><li>お住まいの市町で障害福祉サービスの申請（手続きはこちらで案内します）</li><li>契約・利用開始（短時間からでもかまいません）</li></ol>''')

def kintoun_more(r):
    return sec('AREA','訪問地域と、ご依頼の例','''<h3>訪問地域</h3><p>三重県四日市市・菰野町を中心に、三重県内へ訪問します。地域によっては対応できない場合があるため、まずはご住所をお知らせください。名古屋からの相談は、電話または<a href="../contact/">問合せフォーム</a>で受け付けます。</p>
<h3>ご依頼の例</h3><p class="note">個人が特定されないよう、よくある相談の形にまとめています。</p><ul><li>「子どもが何年も部屋から出てこない。本人は相談に行かないので、まず家族の話を聞いてほしい」（ご家族から）</li><li>「精神的な不調で、役所や病院の窓口まで行けない。自宅で話を聞いてほしい」（ご本人から）</li><li>「どこに相談すればよいかわからない。費用も心配」（ご家族から）</li></ul>
<p>いずれも、まず話を聞くところから始めます。無理に外へ連れ出すことはしません。</p>''')

def eval_detail(kind,r):
    if kind=='assess': b='''<dl><dt>検査</dt><dd>WISC-V（小1〜高2）／新版K式発達検査（未就学児）</dd><dt>料金</dt><dd>各25,000円（税込）</dd><dt>含まれるもの</dt><dd>事前面談、検査実施、結果報告書の作成、フィードバック面談</dd><dt>担当</dt><dd>あんどう（公認心理師）</dd><dt>場所</dt><dd>レオ（四日市市あさけが丘2-1-42）</dd><dt>申し込み</dt><dd>電話または問合せフォーム</dd></dl><h3>流れ</h3><ol><li>電話または問合せフォームで申し込み</li><li>事前面談</li><li>検査実施</li><li>結果報告書の作成</li><li>フィードバック面談</li></ol><p class="note">所要時間は検査の種類やお子さまの様子で変わるため、申し込み時にお問い合わせください。公的機関への提出を目的とする場合は、事前に提出先へ有効性をご確認ください。</p>'''
    else: b='''<dl><dt>内容</dt><dd>アドラー心理学に基づくペアレントトレーニング（個別相談）</dd><dt>日程</dt><dd>水曜午前（予約制）</dd><dt>費用</dt><dd>レオの利用者とそのご家族は無料。それ以外の方は1回4,000円</dd><dt>担当</dt><dd>加藤幸弘（公認心理師、学校心理士、日本アドラー心理学会認定カウンセラー）</dd><dt>場所</dt><dd>レオ（四日市市あさけが丘2-1-42）</dd></dl><h3>流れ</h3><ol><li>電話または問合せフォームで予約</li><li>カウンセラーが話を丁寧に聴きます</li><li>整理したことを、ご家庭で試します</li></ol><p class="note">1回あたりの時間は予約時にご確認ください。</p>'''
    return sec('DETAILS','料金・流れのまとめ',b)

def top_blocks(r):
    items=[('親元を出たい・働きながら暮らしたい','梁山泊','ryozanpaku/'),('日中に安心して過ごせる場所がほしい','茶夢','chamu/'),('家族が家から出られない','金斗雲','kintoun/'),('子どもが落ち着かない・発達が気になる','レオ','leo/'),('子どもへの関わり方に悩んでいる','ペアレントトレーニング','leo/parent-training/'),('子どもの特性を知りたい','発達検査','leo/assessment/'),('診断も手続きもなく、気軽に集まりたい','しちりんの会','shichirin/'),('どこに相談すればいいかわからない','問合せフォーム','contact/')]
    g='<div class="grid">'+''.join(f'<a href="{r}{u}"><b>{q}</b>→ {n}</a>' for q,n,u in items)+'</div>'
    return sec('FIND','困りごとから探す',g+f'<p class="note" style="margin-top:14px">児童発達支援・放課後等デイサービスの手続きは<a href="{r}guide/jukyushasho/">受給者証ガイド</a>をご覧ください。</p>')+sec('NEWS','お知らせ',f'<p><a href="{r}news/">お知らせ一覧</a></p>')

PLAN=[ # path, id, html_fn, anchor ('cta' or regex)
 ('leo/','leoextra',leo_blocks,'cta'),
 ('chamu/','more',chamu_more,'cta'),
 ('kintoun/','area',kintoun_more,'cta'),
 ('leo/parent-training/','detail',lambda r:eval_detail('pt',r),'cta'),
 # 新トップ（2026-11-10）は手置きHTML。find/news を差し込むとデザインが崩れるので対象外。
 # ('','find',top_blocks,r'<section class="blk" id="self">'),
]
def put(o,id_,block,anchor):
    o=re.sub(r'<!--enh:'+id_+r'-->.*?<!--/enh:'+id_+r'-->','',o,flags=re.S)
    blk=f'<!--enh:{id_}-->{block}<!--/enh:{id_}-->'
    if anchor=='head': return o.replace('</head>',blk+'</head>',1)
    pat=r'<section class="[^"]*cta[^"]*"' if anchor=='cta' else re.escape(anchor)
    m=re.search(pat,o) or re.search(r'<footer class="gf">',o)
    return o[:m.start()]+blk+o[m.start():] if m else o+blk
def style_ryozanpaku(o):
    """梁山泊の本文をカードと写真の見せ方にする。文言は変えない。build 後も残す。"""
    if 'Noto+Serif+JP' not in o:
        o=o.replace(
            'family=Inter:wght@400;500;600&family=Noto+Sans+JP:wght@400;500;600&display=swap',
            'family=Inter:wght@400;500;600&family=Noto+Sans+JP:wght@400;500;600&family=Noto+Serif+JP:wght@500;700&display=swap',
            1)
    if 'assets/ryozanpaku.css' not in o:
        o=re.sub(
            r'(<link rel="stylesheet" href="[^"]*assets/site\.css[^"]*">)',
            r'\1\n<link rel="stylesheet" href="../assets/ryozanpaku.css?v=20261122i">',
            o, count=1)
    o=re.sub(r'(assets/ryozanpaku\.css\?v=)[^"]+', r'\g<1>20261122i', o)
    old='<section class="blk" id="what"><div class="prose old"><h3 class="oh">家賃・部屋数</h3><dl class="info" style="margin:6px 0 16px"><dt>家賃</dt><dd>家賃 月8万円（朝夕食事付き）</dd></dl><h3 class="oh">場所</h3><p style="margin:0 0 12px">三重県四日市市山城町59-4<br>三岐線 山城駅から徒歩5分<br>名古屋西ICから車で約30分<br>三岐バス「団地下」 徒歩30秒<br>マックスバリュ（7〜23時営業） 徒歩1分<br>クスリのアオキ 徒歩3分<br>ローソン 徒歩7分</p><h3 class="oh">部屋・建物の様子</h3><img class="pin" src="../img/ryozanpaku-room.jpg" alt="梁山泊の居室。6畳で、エアコンと窓があります。" loading="lazy" width="720" height="540"><p style="margin:0 0 12px">居室（6畳・クローゼット付き）</p><img class="pin" src="../img/ryozanpaku-dining.jpg" alt="梁山泊の食堂。壁際にテーブルと椅子が並んでいます。" loading="lazy" width="720" height="540"><p style="margin:0 0 12px">食堂</p><img class="pin" src="../img/ryozanpaku-exterior.jpg" alt="梁山泊の建物の外観。四日市市山城町にあります。" loading="lazy" width="720" height="540"><p style="margin:0 0 12px">建物の外観</p></div></section>'
    new='''<section class="blk" id="what"><div class="ryo-body">
<p class="ryo-chips"><span>受給者証不要</span><span>全国から入居可</span><span>働きながら暮らせる</span><span>障害者雇用で働く方に</span><span>就職活動の拠点にも</span></p>
<section class="ryo-story" aria-labelledby="ryo-story-h">
<h2 id="ryo-story-h">雇用されても、続かない人が多い。</h2>
<p class="ryo-stat-num">49.3<span>%</span></p>
<p class="ryo-stat-label">精神障害のある人の、就職後1年の職場定着率</p>
<p class="ryo-stat-src"><a href="https://www.nivr.jeed.go.jp/research/report/houkoku/houkoku137.html" target="_blank" rel="noopener">障害者職業総合センター「障害者の就業状況等に関する調査研究」（2017年）</a>。ハローワーク紹介・一般企業（就労継続支援A型を除く）。</p>
<div class="ryo-flow">
<div class="ryo-flow-row">
<div class="ryo-flow-cell"><b>栄養豊かな<br>食事</b></div>
<div class="ryo-flow-cell"><b>家事の<br>サポート</b><small>居宅介護</small></div>
<div class="ryo-flow-cell"><b>社会経験豊富な<br>職員からの<br>アドバイス</b></div>
</div>
<div class="ryo-flow-arrow" aria-hidden="true">↓</div>
<div class="ryo-flow-result">メンタルが安定する</div>
<div class="ryo-flow-arrow" aria-hidden="true">↓</div>
<div class="ryo-flow-result">仕事が続く</div>
</div>
</section>
<div class="ryo-facts">
<div class="ryo-rent">
<img class="ryo-photo" src="../img/homemeal.jpg" alt="食事の様子" width="800" height="500">
<div class="ryo-rent-inner">
<p class="ryo-sec-title">家賃</p>
<p class="ryo-num">月8万円<small>朝夕食事付き</small></p>
</div>
</div>
<div class="ryo-place">
<img class="ryo-photo" src="../img/yamashiro_st.jpg" alt="山城駅" width="800" height="500" loading="lazy">
<div class="ryo-place-inner">
<p class="ryo-sec-title">場所</p>
<p>三重県四日市市山城町59-4<br>三岐線 山城駅から徒歩5分<br>名古屋西ICから車で約30分<br>三岐バス「団地下」 徒歩30秒<br>マックスバリュ（7〜23時営業） 徒歩1分<br>クスリのアオキ 徒歩3分<br>ローソン 徒歩7分</p>
</div>
</div>
</div>
<div class="ryo-rooms">
<p class="ryo-sec-title">部屋・建物の様子</p>
<figure>
<img class="ryo-photo" src="../img/ryozanpaku-room.jpg" alt="梁山泊の居室。6畳で、エアコンと窓があります。" width="1600" height="1200" loading="lazy">
<figcaption>居室（6畳・クローゼット付き）</figcaption>
</figure>
<figure>
<img class="ryo-photo" src="../img/ryozanpaku-dining.jpg" alt="梁山泊の食堂。壁際にテーブルと椅子が並んでいます。" width="1280" height="1280" loading="lazy">
<figcaption>食堂</figcaption>
</figure>
<figure>
<img class="ryo-photo" src="../img/ryozanpaku-exterior.jpg" alt="梁山泊の建物の外観。四日市市山城町にあります。" width="1280" height="1280" loading="lazy">
<figcaption>建物の外観</figcaption>
</figure>
</div>
</div></section>'''
    if old in o:
        o=o.replace(old,new,1)
    # Already-styled pages: keep the card layout, apply later copy/layout fixes.
    o=re.sub(r'<p class="svc">メンタルピアレジデンス｜家賃 月8万円</p>\s*','',o,count=1)
    catch='<p class="copy ryo-catch"><span class="ryo-catch-main">障害者雇用（精神）で働く人のためのシェアハウス。</span><span class="ryo-catch-sub">朝夕食事付き。</span></p>'
    o=re.sub(r'(<section class="hero ryo-hero">[\s\S]*?)<p class="copy(?: ryo-catch)?">[\s\S]*?</p>', r'\1'+catch, o, count=1)
    _catch_css=(""".hero.ryo-hero .copy.ryo-catch{display:inline-block;width:fit-content;max-width:100%;margin:12px 0 0;padding:10px 16px 12px;box-sizing:border-box;background:rgba(15,23,42,.82);color:#fff;font-family:"Noto Serif JP",serif;font-weight:700;line-height:1.5;letter-spacing:.04em;text-shadow:none;border-bottom:4px solid #2e7d32}
.hero.ryo-hero .copy.ryo-catch span{display:block}
.hero.ryo-hero .ryo-catch-main{font-size:clamp(17px,2.5vw,24px)}
.hero.ryo-hero .ryo-catch-sub{margin-top:6px;font-size:clamp(16px,2.2vw,22px);letter-spacing:.1em;color:#dcfce7;font-weight:700}""")
    if '.copy.ryo-catch{' not in o:
        o=o.replace('.hero.ryo-hero .sub{font-size:14px;font-weight:400;color:#e2e8f0;text-shadow:0 1px 3px rgba(0,0,0,.65)}',
                    '.hero.ryo-hero .sub{font-size:14px;font-weight:400;color:#e2e8f0;text-shadow:0 1px 3px rgba(0,0,0,.65)}\n'+_catch_css, 1)
    short='<p>三重県四日市市山城町59-4<br>三岐線 山城駅から徒歩5分<br>名古屋西ICから車で約30分</p>'
    long='<p>三重県四日市市山城町59-4<br>三岐線 山城駅から徒歩5分<br>名古屋西ICから車で約30分<br>三岐バス「団地下」 徒歩30秒<br>マックスバリュ（7〜23時営業） 徒歩1分<br>クスリのアオキ 徒歩3分<br>ローソン 徒歩7分</p>'
    o=o.replace(short,long,1)
    o=re.sub(r'\n?<div class="ryo-visit">[\s\S]*?</div>\s*','\n',o,count=1)
    chips='<p class="ryo-chips"><span>受給者証不要</span><span>全国から入居可</span><span>働きながら暮らせる</span><span>障害者雇用で働く方に</span><span>就職活動の拠点にも</span></p>'
    if '<p class="ryo-chips">' in o:
        o=re.sub(r'<p class="ryo-chips">[\s\S]*?</p>',chips,o,count=1)
    elif '<div class="ryo-body">' in o:
        o=o.replace('<div class="ryo-body">','<div class="ryo-body">\n'+chips,1)
    story=("""<section class="ryo-story" aria-labelledby="ryo-story-h">
<h2 id="ryo-story-h">雇用されても、続かない人が多い。</h2>
<p class="ryo-stat-num">49.3<span>%</span></p>
<p class="ryo-stat-label">精神障害のある人の、就職後1年の職場定着率</p>
<p class="ryo-stat-src"><a href="https://www.nivr.jeed.go.jp/research/report/houkoku/houkoku137.html" target="_blank" rel="noopener">障害者職業総合センター「障害者の就業状況等に関する調査研究」（2017年）</a>。ハローワーク紹介・一般企業（就労継続支援A型を除く）。</p>
<div class="ryo-flow">
<div class="ryo-flow-row">
<div class="ryo-flow-cell"><b>栄養豊かな<br>食事</b></div>
<div class="ryo-flow-cell"><b>家事の<br>サポート</b><small>居宅介護</small></div>
<div class="ryo-flow-cell"><b>社会経験豊富な<br>職員からの<br>アドバイス</b></div>
</div>
<div class="ryo-flow-arrow" aria-hidden="true">↓</div>
<div class="ryo-flow-result">メンタルが安定する</div>
<div class="ryo-flow-arrow" aria-hidden="true">↓</div>
<div class="ryo-flow-result">仕事が続く</div>
</div>
</section>""")
    if '<section class="ryo-story"' in o:
        o=re.sub(r'<section class="ryo-story"[\s\S]*?</section>',story,o,count=1)
    elif '<p class="ryo-chips">' in o:
        o=re.sub(r'(<p class="ryo-chips">[\s\S]*?</p>)',r'\1\n'+story,o,count=1)

    o=re.sub(r'\n?<div class="ryo-lead-card">[\s\S]*?</div>\s*','\n',o,count=1)
    o=re.sub(r'\n?<p class="ryo-sec-title">入居までの流れ</p>\s*<ol class="ryo-steps">[\s\S]*?</ol>\s*','\n',o,count=1)
    if 'class="ryo-rooms"' not in o and 'class="ryo-facts"' in o:
        rooms='''<div class="ryo-rooms">
<p class="ryo-sec-title">部屋・建物の様子</p>
<figure>
<img class="ryo-photo" src="../img/ryozanpaku-room.jpg" alt="梁山泊の居室。6畳で、エアコンと窓があります。" width="1600" height="1200" loading="lazy">
<figcaption>居室（6畳・クローゼット付き）</figcaption>
</figure>
<figure>
<img class="ryo-photo" src="../img/ryozanpaku-dining.jpg" alt="梁山泊の食堂。壁際にテーブルと椅子が並んでいます。" width="1280" height="1280" loading="lazy">
<figcaption>食堂</figcaption>
</figure>
<figure>
<img class="ryo-photo" src="../img/ryozanpaku-exterior.jpg" alt="梁山泊の建物の外観。四日市市山城町にあります。" width="1280" height="1280" loading="lazy">
<figcaption>建物の外観</figcaption>
</figure>
</div>
'''
        o=re.sub(r'(<div class="ryo-facts">[\s\S]*?</div>\s*</div>\s*</div>)\s*(</div></section>)', r'\1\n'+rooms+r'\2', o, count=1)
    return o

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
        if p=='leo/':
            o=re.sub(r'<!--enh:faq-->.*?<!--/enh:faq-->','',o,flags=re.S)
            o=re.sub(r'<!--enh:faqld-->.*?<!--/enh:faqld-->','',o,flags=re.S)
        if p=='ryozanpaku/':
            o=style_ryozanpaku(o)
        open(fn,'w',encoding='utf-8').write(o)
