// Server-only notification text. The approved recipient is fixed.
// This does not send mail and does not add Cc/Bcc.

export const RECIPIENT = "rsaito@psr-seishinkai.org";
export const SUBJECT = "【星心会】ウェブサイトからの相談";

function assertHeaderSafe(label, value) {
  if (typeof value !== "string" || /[\r\n\u0000]/.test(value)) {
    const error = new Error("header_rejected");
    error.code = "header_rejected";
    error.label = label;
    throw error;
  }
}

export function buildNotice(row) {
  assertHeaderSafe("name", row.name);
  assertHeaderSafe("email", row.email);
  assertHeaderSafe("service", row.service);
  if (typeof row.body !== "string" || row.body.includes("\u0000")) {
    const error = new Error("header_rejected");
    error.code = "header_rejected";
    throw error;
  }
  const created = row.created_at instanceof Date ? row.created_at.toISOString() : String(row.created_at);
  const text = [
    "星心会ウェブサイトの相談フォームから新しい問い合わせです。",
    "このメールは受付通知です。送信者への自動返信ではありません。",
    "",
    "受付番号: " + row.id,
    "受付時刻: " + created,
    "相談したい事業: " + row.service,
    "お名前: " + row.name,
    "メールアドレス: " + row.email,
    "",
    "内容:",
    row.body,
    "",
    "返信は、上のメールアドレスへ直接お願いします。",
  ].join("\n");
  return { to: RECIPIENT, subject: SUBJECT, text };
}

export function safeMailCode(error) {
  const code = String(error && (error.code || error.message) || "");
  if (/^mail_http_\d{3}$/.test(code)) return code;
  if (code === "recipient_rejected" || code === "mail_network" || code === "header_rejected") return code;
  return "mail_failed";
}

export function createMailer(env, fetchImpl) {
  if (!env || env.CONTACT_INTAKE_ENABLED !== "1") return null;
  if (env.CONTACT_MAIL_TRANSPORT !== "https-json") return null;
  const url = String(env.CONTACT_MAIL_URL || "");
  const token = String(env.CONTACT_MAIL_TOKEN || "");
  const from = String(env.CONTACT_MAIL_FROM || "");
  if (!url.startsWith("https://") || !token || !from || /[\r\n\u0000]/.test(from) || !from.includes("@")) return null;
  return async function send(message) {
    if (!message || message.to !== RECIPIENT || message.subject !== SUBJECT) {
      const error = new Error("recipient_rejected");
      error.code = "recipient_rejected";
      throw error;
    }
    let response;
    try {
      response = await fetchImpl(url, {
        method: "POST",
        headers: {
          "content-type": "application/json",
          "authorization": "Bearer " + token,
        },
        body: JSON.stringify({
          to: RECIPIENT,
          from,
          subject: message.subject,
          text: message.text,
        }),
      });
    } catch {
      const error = new Error("mail_network");
      error.code = "mail_network";
      throw error;
    }
    if (!response.ok) {
      const error = new Error("mail_http_" + response.status);
      error.code = "mail_http_" + response.status;
      throw error;
    }
  };
}
