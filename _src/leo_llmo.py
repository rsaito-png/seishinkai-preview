# レオの基本情報・FAQ・JSON-LD。事実は公式サイトと WAM NET オープンデータのみ。
import json, re

BASE = 'https://psr-seishinkai.org'
ORG_ID = BASE + '/#org'
LEO_URL = BASE + '/leo/'
LEO_TEL = '070-6967-0011'
DESC = '情緒を整え、落ち着きを取り戻すことを目指す療育。児童発達支援・放課後等デイサービスのレオは、発達が気になる満1歳から18歳までが対象です。三重県四日市市あさけが丘。'
ASAKE = {
    '@type': 'PostalAddress',
    'postalCode': '512-8055',
    'addressCountry': 'JP',
    'addressRegion': '三重県',
    'addressLocality': '四日市市',
    'streetAddress': 'あさけが丘2-1-42',
}
# WAM NET 障害福祉サービス等情報公表システム オープンデータ（2026年9月末時点）児童発達支援・事業所番号2450201047
WAM_GEO = {'@type': 'GeoCoordinates', 'latitude': 35.03471102, 'longitude': 136.57804836}
WAM_ID = '2450201047'

G = '<a href="{r}guide/jukyushasho/">受給者証ガイド</a>'

FAQ = [
    (
        '受給者証がなくても相談できますか？',
        '相談と見学は、受給者証の申請前でも受け付けています。発達のお悩み相談（月曜・金曜 13:00〜14:00）は無料で、診断の有無は問いません。電話は070-6967-0011です。通所の利用契約は、受給者証が届いてから結びます。手続きはこちらで案内します。',
    ),
    (
        '診断がなくても利用できますか？',
        '診断の有無は問いません。今の困りごとから始めます。',
    ),
    (
        '対象は何歳ですか？',
        '満1歳から18歳までです。',
    ),
    (
        '放課後等デイサービスと児童発達支援の違いは何ですか？',
        '小学校入学前は児童発達支援、小学生以降は放課後等デイサービスとして利用します。いずれもレオ（四日市市あさけが丘）で行います。',
    ),
    (
        '費用はどのくらいかかりますか？',
        '通所の利用には、お住まいの市町が発行する通所受給者証を使います。利用者負担は原則1割で、世帯の所得に応じた月額上限があります。満3歳になって初めての4月1日から小学校入学前の3年間は、国の制度で児童発達支援の利用者負担が無償です。昼食は1回300円です。手続きの案内は' + G + 'をご覧ください。',
    ),
    (
        '送迎はありますか？',
        '地域によって相談を受けます。対応できる範囲はお住まいの地域によって異なるため、お問い合わせの際にお知らせください。',
    ),
    (
        '見学はできますか？',
        'できます。電話（070-6967-0011）またはLINEでご連絡のうえ、お子さまと一緒に教室の様子をご覧ください。体験の可否など、当日の案内はお問い合わせください。',
    ),
    (
        '利用開始までの流れは？',
        '問い合わせ（電話070-6967-0011またはLINE）→見学→お住まいの市町で通所受給者証を申請→受給者証が届いたらレオと契約→個別支援計画にそって利用開始、の順です。四日市市の申請窓口はこども発達支援課（059-354-8064）、菰野町は子ども家庭課 発達支援係（059-391-1226）です。詳しくは' + G + 'へ。手続きでわからないことは、こちらで案内します。',
    ),
    (
        '利用時間は？',
        '1部が11:00〜14:30、2部が放課後〜17:00です。',
    ),
    (
        '場所はどこですか？',
        '三重県四日市市あさけが丘2-1-42 2階です。三岐線 山城駅から徒歩12分、名古屋西ICから車で約30分です。電話は070-6967-0011です。',
    ),
    (
        '受給者証はどこで申請しますか？',
        'お住まいの市町です。事業所の所在地ではなく、住んでいる市町に申請します。四日市市はこども発達支援課（059-354-8064）、菰野町は子ども家庭課 発達支援係（059-391-1226）です。詳しくは' + G + 'をご覧ください。',
    ),
    (
        '定員は何名ですか？',
        '児童発達支援の定員は10名です（WAM NET 障害福祉サービス等情報公表システムのオープンデータ、2026年9月末時点、事業所番号2450201047）。放課後等デイサービスの定員は、同時点の公開データでは確認できませんでした。最新の空きや定員は、お問い合わせください。',
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
      <dd>満1歳〜18歳</dd>
      <dt>利用時間</dt>
      <dd>【1部】11:00〜14:30<br>【2部】放課後〜17:00</dd>
      <dt>場所</dt>
      <dd>三重県四日市市あさけが丘2-1-42 2F<br>三岐線 山城駅 徒歩12分（名古屋西ICから車で約30分）</dd>
      <dt>電話</dt>
      <dd><a href="tel:07069670011">070-6967-0011</a></dd>
      <dt>送迎</dt>
      <dd>地域によって相談を受けます</dd>
      <dt>費用</dt>
      <dd>通所受給者証を利用（原則1割、世帯所得に応じた月額上限あり）。児童発達支援は、満3歳になって初めての4月から就学前の3年間、国の制度で利用者負担が無償です。昼食は1回300円。</dd>
      <dt>定員</dt>
      <dd>児童発達支援 10名（WAM NET、2026年9月末時点）</dd>
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
        'areaServed': ['四日市市', '三重県'],
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
        'areaServed': ['四日市市', '三重県'],
        'description': DESC,
        'identifier': {'@type': 'PropertyValue', 'name': '障害福祉サービス等事業所番号', 'value': WAM_ID},
        'geo': WAM_GEO,
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
