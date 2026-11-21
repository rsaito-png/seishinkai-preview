# レオの基本情報・FAQ・JSON-LD。
# 運営の事実は、令和8年11月1日適用の変更届と添付の運営規程による。
# 送迎の「片道30分圏内」は同日施行の重要事項説明書（R8.11版）。
# 対象年齢は齊藤さん指定（2歳〜18歳）。座標は既存の公開位置情報。
import json, re

BASE = 'https://psr-seishinkai.org'
ORG_ID = BASE + '/#org'
LEO_URL = BASE + '/leo/'
LEO_TEL = '070-6967-0011'
DESC = '情緒を整え、落ち着きを取り戻すことを目指す療育。児童発達支援・放課後等デイサービスのレオは、発達が気になる2歳から18歳までが対象です。三重県四日市市あさけが丘。'
ASAKE = {
    '@type': 'PostalAddress',
    'postalCode': '512-8055',
    'addressCountry': 'JP',
    'addressRegion': '三重県',
    'addressLocality': '四日市市',
    'streetAddress': 'あさけが丘2-1-42',
}
# 事業所番号は変更届・重要事項説明書（2450201047）。座標は既存の公開位置情報。
GEO = {'@type': 'GeoCoordinates', 'latitude': 35.03471102, 'longitude': 136.57804836}
OFFICE_ID = '2450201047'
AREA = ['四日市市', '菰野町', '川越町', '朝日町', '東員町']

G = '<a href="{r}guide/jukyushasho/">受給者証ガイド</a>'

FAQ = [
    (
        'どんな年齢の子が通っていますか？',
        '対象は2歳から18歳までです。小学校入学前は児童発達支援、小学生以降は放課後等デイサービスとして利用します。いま通っている子は、未就学と小学生以降が、ほぼ同じくらいの人数です。診断の有無は問いません。',
    ),
    (
        '週に何日くらい通う子が多いですか？',
        '週1日から2日で通う子が多いです。月曜日から金曜日の中で曜日を選べます。金曜や月曜に通う子がやや多く、毎日通う子は多くありません。',
    ),
    (
        '1日の時間と、過ごし方は？',
        'サービス提供時間は10:30〜17:30、営業時間は10:00〜18:00です。利用の目安は、1部が10:30〜14:30、2部が放課後〜17:00です。未就学のお子さんは午前の部と午後の部の両方、小学生以降は学校が終わってからの利用が中心です。活動の内容は、お子さんやその日のメンバーに合わせて選んでいます。',
    ),
    (
        'どんな活動をしますか？決まったプログラムはありますか？',
        '決まったプログラムを押し付けることはしていません。お子さん一人ひとりや、その日のメンバーの組み合わせを見て活動を選んでいるので、自由度が高いです。宿題やおもちゃ遊び、絵やブロック、おやつなど、日によって内容は変わります。金曜日だけ、体のコントロールと、集団での規律を身につける運動のプログラムを行っています。',
    ),
    (
        '学校まで迎えに来てもらえますか？',
        'できます。学校や園への迎え、自宅への送りを行っています。いま通っている子の多くは、事業所の送迎を使っています。保護者が送迎する日もあります。通常の実施地域は、四日市市、菰野町、川越町、朝日町、東員町で、事業所からおおむね片道30分圏内です。',
    ),
    (
        '祝日や夏休みは通えますか？',
        '土曜日、日曜日、祝日、および年末年始はお休みです。月曜日から金曜日が営業日です。学校の夏休みなど、長い休みのうち平日は、通常どおり通えます。',
    ),
    (
        '昼食は出ますか？',
        '昼食は1回300円です。午前の部で利用する日に食べていく子がいます。学校のあとの午後の部だけの日は、昼食がないことがほとんどです。',
    ),
    (
        '持ち物は何ですか？',
        'リュックなどに、着替え（最低1組）と汚れた服を入れる袋を入れて持ってきてください。レオに着替え用の服はありません。必要な子は、オムツ・おしり拭きと捨てる袋、水筒も持ってきてください。麦茶は事業所でも用意しています。夏場の帽子やタオルなどは、必要に応じてお問い合わせください。',
    ),
    (
        '欠席するときは？',
        '休むときは、電話（070-6967-0011）または公式LINEでご連絡ください。',
    ),
    (
        '見学はできますか？始めるまでどれくらいかかりますか？',
        '見学できます。電話（070-6967-0011）またはLINEでご連絡ください。相談と見学は、受給者証の申請前でも受け付けています。通所の契約は、受給者証が届いてから結びます。手続きはこちらで案内します。契約のあと、多くの子は1か月以内に通い始めています。受給者証の申請にかかる期間は、市町によって異なります。詳しい流れは' + G + 'をご覧ください。',
    ),
    (
        '受給者証をまだ持っていません。初めてでも大丈夫ですか？',
        '大丈夫です。初めて受給者証を申請する方にも、手続きの流れなどをアドバイスできます。相談と見学は、申請の前でも受け付けています。まずはお問い合わせください。',
    ),
    (
        '受給者証はどこで申請しますか？',
        'お住まいの市町です。事業所の所在地ではなく、住んでいる市町に申請します。四日市市はこども発達支援課（059-354-8064）、菰野町は子ども家庭課 発達支援係（059-391-1226）です。詳しくは' + G + 'をご覧ください。',
    ),
    (
        '書類の手続きは大変ですか？',
        '契約書や計画書などの各種書面は、デジタル化を徹底しています。ほかの事業所と比べても、保護者の方の手間をかけないようにしています。',
    ),
    (
        '費用はどのくらいかかりますか？',
        '通所の利用には、お住まいの市町が発行する通所受給者証を使います。利用者負担は原則1割で、世帯の所得に応じた月額上限があります。満3歳になって初めての4月1日から小学校入学前の3年間は、国の制度で児童発達支援の利用者負担が無償です。昼食は1回300円です。手続きの案内は' + G + 'をご覧ください。',
    ),
    (
        '定員は何名ですか？',
        '児童発達支援と放課後等デイサービスをあわせて10名です。',
    ),
    (
        '今、空きはありますか？',
        '2026年12月時点では、月曜日のみ満員で、火〜金曜日は空きがあります。最新の状況はお問い合わせください。',
    ),
    (
        '場所はどこですか？',
        '三重県四日市市あさけが丘2-1-42 2階です。三岐線 山城駅から徒歩12分、名古屋西ICから車で約30分です。電話は070-6967-0011です。',
    ),
]

def faq_resolved(rel):
    return [(q, a.replace('{r}', rel)) for q, a in FAQ]

def facts_html(rel):
    return f'''<section class="leo-facts" id="facts">
  <div class="leo-sec-head">
    <span class="en">INFORMATION</span>
    <h2>基本情報</h2>
  </div>
  <div class="leo-info-card">
    <dl class="leo-dl">
      <dt>種別</dt>
      <dd>児童発達支援・放課後等デイサービス</dd>
      <dt>対象年齢</dt>
      <dd>2歳〜18歳</dd>
      <dt>営業日</dt>
      <dd>月曜日〜金曜日（土日・祝日・年末年始は休み）</dd>
      <dt>時間</dt>
      <dd>営業時間 10:00〜18:00<br>サービス提供時間 10:30〜17:30<br>【1部】10:30〜14:30<br>【2部】放課後〜17:00</dd>
      <dt>場所</dt>
      <dd>三重県四日市市あさけが丘2-1-42 2F<br>三岐線 山城駅 徒歩12分（名古屋西ICから車で約30分）</dd>
      <dt>電話</dt>
      <dd><a href="tel:07069670011">070-6967-0011</a></dd>
      <dt>送迎</dt>
      <dd>四日市市、菰野町、川越町、朝日町、東員町。必要に応じて、おおむね片道30分圏内で送迎します。</dd>
      <dt>費用</dt>
      <dd>通所受給者証を利用（原則1割、世帯所得に応じた月額上限あり）。児童発達支援は、満3歳になって初めての4月から就学前の3年間、国の制度で利用者負担が無償です。昼食は1回300円。</dd>
      <dt>定員</dt>
      <dd>10名（児童発達支援・放課後等デイサービス）</dd>
      <dt>空き状況（2026年12月時点）</dt>
      <dd>月曜日のみ満員。火〜金曜日は空きあり</dd>
      <dt>活動</dt>
      <dd>お子さんやその日のメンバーに合わせて選びます。金曜は運動プログラム。</dd>
    </dl>
  </div>
  <p class="leo-faq-link"><a href="{rel}leo/faq/">レオのよくある質問</a></p>
</section>'''

def faq_body(rel):
    items = ''.join('<details><summary>%s</summary><div>%s</div></details>' % (q, a) for q, a in faq_resolved(rel))
    css = (
        '<style>'
        '.leo-faq{max-width:800px;margin:0 auto;padding:28px 20px 80px;line-height:1.9}'
        '.leo-faq details{border-bottom:1px solid rgba(0,0,0,.12);padding:0}'
        '.leo-faq summary{cursor:pointer;list-style:none;padding:16px 8px;font-weight:700;font-size:16px}'
        '.leo-faq summary::-webkit-details-marker{display:none}'
        '.leo-faq summary:after{content:"+";float:right;font-weight:500;opacity:.5}'
        '.leo-faq details[open] summary:after{content:"\u2212"}'
        '.leo-faq details>div{padding:0 8px 18px;font-size:15px}'
        '.leo-faq .links{margin-top:36px;font-size:14px}'
        '.leo-faq .links a{color:inherit;font-weight:700}'
        '</style>'
    )
    links = (
        '<p class="links"><a href="%sleo/">レオのページへ</a>　／　'
        '<a href="%sguide/jukyushasho/">受給者証ガイド</a>　／　'
        '<a href="%scontact/">相談する</a></p>'
    ) % (rel, rel, rel)
    return css + '<div class="leo-faq">' + items + links + '</div>'

def org_node():
    return {
        '@type': 'Organization',
        '@id': ORG_ID,
        'name': '一般社団法人 心理社会的リハビリテーション・星心会',
        'alternateName': '星心会',
        'url': BASE + '/',
        'telephone': '059-315-0697',
        'address': {
            '@type': 'PostalAddress',
            'postalCode': '512-8048',
            'addressCountry': 'JP',
            'addressRegion': '三重県',
            'addressLocality': '四日市市',
            'streetAddress': '山城町59-4',
        },
        'areaServed': ['四日市市', '三重県', '名古屋市', '愛知県'],
        'logo': BASE + '/img/logo_black.svg',
        'sameAs': [
            'https://x.com/gcbfhq',
            'https://www.instagram.com/psr_seishinkai/',
            'https://www.threads.com/@psr_seishinkai',
            'https://line.me/R/ti/p/@279qxcql',
        ],
        'founder': {'@type': 'Person', '@id': BASE + '/#founder', 'name': '齊藤 連', 'jobTitle': '代表'},
    }

def service_node():
    return {
        '@type': 'Service',
        '@id': LEO_URL + '#service',
        'name': 'レオ',
        'serviceType': '児童発達支援・放課後等デイサービス',
        'url': LEO_URL,
        'provider': {'@id': ORG_ID},
        'areaServed': AREA,
        'telephone': LEO_TEL,
        'address': ASAKE,
        'description': DESC,
    }

def childcare_node():
    return {
        '@type': ['ChildCare', 'LocalBusiness'],
        '@id': LEO_URL + '#place',
        'name': 'レオ',
        'alternateName': '児童発達支援・放課後等デイサービス レオ',
        'url': LEO_URL,
        'telephone': LEO_TEL,
        'address': ASAKE,
        'parentOrganization': {'@id': ORG_ID},
        'openingHours': 'Mo-Fr 10:00-18:00',
        'areaServed': AREA,
        'description': DESC,
        'identifier': {'@type': 'PropertyValue', 'name': '障害福祉サービス等事業所番号', 'value': OFFICE_ID},
        'geo': GEO,
    }

def graph():
    return {'@context': 'https://schema.org', '@graph': [org_node(), service_node(), childcare_node()]}

def jsonld_script():
    return '<script type="application/ld+json">' + json.dumps(graph(), ensure_ascii=False) + '</script>'

def replace_jsonld(html):
    nxt, n = re.subn(
        r'<script type="application/ld\+json">.*?</script>',
        jsonld_script(),
        html,
        count=1,
        flags=re.S,
    )
    if n:
        return nxt
    return html.replace('</head>', jsonld_script() + '\n</head>', 1)
