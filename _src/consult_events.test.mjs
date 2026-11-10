import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const code = readFileSync(path.join(root, "assets/site.js"), "utf8");
const api = new Function("document", `${code}\nreturn { consultClickEvent, inquiryAcceptedParams };`)({
  querySelector() { return null; },
  querySelectorAll() { return []; },
  addEventListener() {},
});

test("phone and LINE clicks carry only the page and the location", () => {
  const phone = api.consultClickEvent("tel:0593150697", "/leo/assessment/", "assessment");
  assert.equal(phone.name, "phone_click");
  assert.deepEqual(phone.params, { page_path: "/leo/assessment/", link_location: "assessment" });
  assert.equal(JSON.stringify(phone).includes("059"), false);

  const line = api.consultClickEvent("https://line.me/R/ti/p/@279qxcql", "/contact/#line", "contact");
  assert.equal(line.name, "line_click");
  assert.deepEqual(line.params, { page_path: "/contact/", link_location: "contact" });
  assert.equal(JSON.stringify(line).includes("@279"), false);
  assert.equal(JSON.stringify(line).includes("line.me"), false);
});

test("a saved inquiry event has no personal fields", () => {
  const accepted = api.inquiryAcceptedParams("/contact/?q=1#line");
  assert.deepEqual(accepted, { page_path: "/contact/", method: "server_receipt", form_id: "contact-intake" });
  assert.equal(JSON.stringify(accepted).includes("059"), false);
  assert.equal(Object.hasOwn(accepted, "name"), false);
  assert.equal(Object.hasOwn(accepted, "email"), false);
  assert.equal(Object.hasOwn(accepted, "body"), false);
});

test("internal LINE buttons and ordinary links are not consult events", () => {
  assert.equal(api.consultClickEvent("../contact/#line", "/leo/", "leo"), null);
  assert.equal(api.consultClickEvent("https://psr-seishinkai.org/contact/", "/", "body"), null);
  const cleaned = api.consultClickEvent("tel:0593150697", "/contact/?from=ad", "not a place");
  assert.deepEqual(cleaned.params, { page_path: "/contact/", link_location: "body" });
});
