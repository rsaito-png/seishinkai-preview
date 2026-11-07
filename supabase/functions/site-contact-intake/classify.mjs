// Deterministic sales screen. No network and no model.
// A message is quarantined only when a strong pitch matches and nothing in it
// looks like a real consultation, referral, or welfare/medical contact.
// Ambiguous wording stays in the normal inbox with review = needs-review.

const SALES = [
  { id: "sales-call", label: "営業の連絡・提案", re: /営業(の|ご)?(連絡|電話|メール|提案|させて)|営業させて/ },
  { id: "pitch", label: "売り込み・テレアポ", re: /売り込み|勧誘|テレアポ|飛び込み営業/ },
  { id: "seo", label: "SEO・広告の売り込み", re: /SEO対策|検索順位|リスティング広告|MEO対策/ },
  { id: "web-pitch", label: "制作サービスの提案", re: /(ホームページ|ウェブサイト|Webサイト|ＨＰ|HP)(の)?(制作|リニューアル).{0,24}(提案|案内|お見積|いかが)/ },
  { id: "ad-space", label: "掲載・タイアップの勧誘", re: /広告枠|掲載しませんか|タイアップのご案内/ },
  { id: "vendor-pitch", label: "自社商材の案内", re: /(弊社|当社)の(商品|商材|サービス|ソリューション).{0,40}(ご案内|ご提案|いかがでしょ|導入しませんか)/ },
  { id: "catalog", label: "資料・カタログの送付", re: /カタログを?送|資料を送付させて|サービスのご案内状/ },
  { id: "lead-gen", label: "リード提供・成果報酬", re: /成果報酬|リード(の)?(獲得|提供|販売)/ },
  { id: "discount-push", label: "期間限定の売り込み", re: /(今だけ|期間限定).{0,24}(キャンペーン|特別価格|格安)/ },
];

const LEGIT = [
  { id: "service-use", label: "利用・見学の相談", re: /利用した|利用したい|見学|体験|空き|料金を教えて|対象になりますか|受給者証/ },
  { id: "welfare", label: "医療・福祉・教育の文脈", re: /障害|福祉|医療|病院|学校|保護者|児童|放デイ|児発|就労|相談支援|ケアマネ|相談員/ },
  { id: "referral", label: "紹介・連携", re: /紹介した|ご紹介|連携のお願い|連携したい|ハローワーク|行政|役場/ },
  { id: "family", label: "家族・本人の相談", re: /家族|親が|子ども|本人が|家から出/ },
  { id: "named-service", label: "星心会の事業名", re: /水晶玉|しちりん|梁山泊|茶夢|金斗雲|レオ|RYDEEN|星心会の/ },
];

const WEAK = [
  { id: "weak-vendor", label: "会社名・提案の語", re: /株式会社|ご提案|お見積|弊社|当社/ },
];

function hits(rules, text) {
  return rules.filter((rule) => rule.re.test(text));
}

export function classifyInquiry(parts) {
  const text = [parts && parts.service, parts && parts.name, parts && parts.body].filter(Boolean).join("\n");
  const sales = hits(SALES, text);
  const legit = hits(LEGIT, text);
  const weak = hits(WEAK, text);
  if (sales.length && legit.length === 0) {
    return {
      lane: "sales",
      review: "clear",
      sales_reason: "業者の営業と判断しました：" + sales.map((rule) => rule.label).join("、"),
    };
  }
  if (sales.length && legit.length) {
    return {
      lane: "normal",
      review: "needs-review",
      sales_reason: "営業に似た語がありますが、相談・紹介・福祉の文脈があるため通常の受信に残しました（" + sales.map((rule) => rule.label).join("、") + "）",
    };
  }
  if (weak.length && legit.length === 0) {
    return {
      lane: "normal",
      review: "needs-review",
      sales_reason: "会社名や提案の語がありますが、売り込みとは断定できないため通常の受信に残しました",
    };
  }
  return { lane: "normal", review: "clear", sales_reason: null };
}

export function unreadCount(rows) {
  return (rows || []).filter((row) => row && row.test !== true && row.lane === "normal" && !row.read_at).length;
}

export function assertOwner(actor) {
  if (!actor || actor.owner !== true) {
    const error = new Error("forbidden");
    error.code = "forbidden";
    throw error;
  }
}

export function markRead(rows, actor, id) {
  assertOwner(actor);
  const row = rows.find((item) => item.id === id);
  if (!row || row.test === true) return null;
  if (!row.read_at) row.read_at = new Date().toISOString();
  return row;
}

export function restoreInquiry(rows, actor, id) {
  assertOwner(actor);
  const row = rows.find((item) => item.id === id);
  if (!row || row.test === true) return null;
  if (row.lane === "sales") {
    row.lane = "normal";
    row.review = "restored";
    row.restored_at = new Date().toISOString();
  }
  return row;
}
