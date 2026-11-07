import { shouldCountLead, validateIntake } from "../../supabase/functions/site-contact-intake/shared.mjs";

const COPY = {
  name_required: "お名前を入力してください。",
  name_invalid: "お名前は80字以内で、改行は使えません。",
  email_required: "メールアドレスを入力してください。",
  email_invalid: "メールアドレスの形を確認してください。",
  body_required: "内容を入力してください。",
  body_invalid: "内容は2000字以内にしてください。",
  service_invalid: "相談したい事業を選び直してください。",
  rejected: "送信できませんでした。入力内容は残しています。時間をおいて再度お試しください。",
  rate_limited: "送信が集中しています。時間をおいて、もう一度お試しください。入力内容は残しています。",
  persist: "送信できませんでした。入力内容は残しています。時間をおいて再度お試しください。",
  network: "送信できませんでした。入力内容は残しています。通信を確認して、もう一度お試しください。",
  stopped: "送信は停止しています。受付の準備が終わるまで、このフォームからは送れません。",
};

function fieldMessage(fields) {
  if (!fields) return COPY.rejected;
  const order = ["name", "email", "service", "body"];
  for (const key of order) {
    if (fields[key]) return COPY[key + "_" + fields[key]] || COPY.rejected;
  }
  return COPY.rejected;
}

function messageFor(body) {
  if (body.code === "rate_limited") return COPY.rate_limited;
  if (body.code === "persist" || body.code === "not_configured") return body.code === "not_configured" ? COPY.stopped : COPY.persist;
  if (body.code === "invalid") return fieldMessage(body.fields);
  return COPY.rejected;
}

function successText(body) {
  const ref = body.reference ? "受付番号 " + body.reference + "。" : "";
  if (body.duplicate) return "同じ内容はすでに受け付けています。" + ref + "重複としては数えません。";
  return "受け付けました。" + ref + "内容は保存されました。";
}

function readConfig() {
  const cfg = window.SEISHINKAI_CONTACT_INTAKE || {};
  const endpoint = typeof cfg.endpoint === "string" ? cfg.endpoint : "";
  return { enabled: cfg.enabled === true && endpoint.startsWith("https://"), endpoint };
}

function storageKey(name) {
  try {
    return window.sessionStorage.getItem(name);
  } catch {
    return null;
  }
}

function storageSet(name, value) {
  try {
    window.sessionStorage.setItem(name, value);
  } catch {
    /* private mode still submits with an in-memory key */
  }
}

export function installContactIntake(doc = document) {
  const form = doc.getElementById("contact-intake");
  if (!form) return;
  const status = doc.getElementById("contact-status");
  const error = doc.getElementById("contact-error");
  const button = form.querySelector("button[type=submit]");
  let sending = false;
  let idem = storageKey("seishinkai-contact-idem") || crypto.randomUUID();
  storageSet("seishinkai-contact-idem", idem);
  const openedPrev = Number(storageKey("seishinkai-contact-opened"));
  if (!openedPrev || Date.now() - openedPrev < 0 || Date.now() - openedPrev > 24 * 60 * 60 * 1000) {
    storageSet("seishinkai-contact-opened", String(Date.now()));
  }

  function setError(text) {
    if (error) error.textContent = text || "";
    if (text && error) error.focus?.();
  }

  async function onSubmit() {
    if (sending) return;
    const cfg = readConfig();
    if (!cfg.enabled) {
      if (status) status.textContent = COPY.stopped + "お電話 059-315-0697 をご利用ください。";
      if (button) button.disabled = true;
      return;
    }
    const data = new FormData(form);
    const input = {
      service: String(data.get("service") || ""),
      name: String(data.get("name") || ""),
      email: String(data.get("email") || ""),
      body: String(data.get("body") || ""),
      company_url: String(data.get("company_url") || ""),
      idempotency_key: idem,
      opened_at: Number(storageKey("seishinkai-contact-opened") || Date.now()),
    };
    const validated = validateIntake(input);
    if (!validated.ok) {
      setError(validated.spam ? COPY.rejected : fieldMessage(validated.errors));
      return;
    }
    if (dwellErrorSafe(input.opened_at)) {
      setError(COPY.rejected);
      return;
    }
    sending = true;
    form.setAttribute("aria-busy", "true");
    if (button) {
      button.disabled = true;
      button.textContent = "送信しています";
    }
    setError("");
    try {
      const response = await fetch(cfg.endpoint, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(input),
      });
      const body = await response.json().catch(() => ({}));
      if (!response.ok || body.ok !== true) {
        setError(messageFor(body));
        if (status) status.textContent = "";
        return;
      }
      if (status) status.textContent = successText(body);
      setError("");
      if (shouldCountLead(body) && typeof window.gtag === "function") {
        window.gtag("event", "contact_inquiry_accepted", { method: "server_receipt", form_id: "contact-intake" });
      }
      if (body.stored === true) {
        idem = crypto.randomUUID();
        storageSet("seishinkai-contact-idem", idem);
      }
    } catch {
      setError(COPY.network);
    } finally {
      sending = false;
      form.setAttribute("aria-busy", "false");
      if (button) {
        button.disabled = !readConfig().enabled;
        button.textContent = "送信";
      }
    }
  }

  form.addEventListener("contact-intake-submit", onSubmit);
  if (readConfig().enabled) {
    if (button) button.disabled = false;
    if (status && status.textContent.includes("停止")) status.textContent = "送信すると内容が保存されます。メールは送りません。";
  } else if (button) button.disabled = true;
}

function dwellErrorSafe(opened) {
  return Date.now() - Number(opened) < 2000;
}

if (typeof document !== "undefined") installContactIntake(document);
