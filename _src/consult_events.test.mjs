import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const code = readFileSync(path.join(root, "assets/site.js"), "utf8");
const api = new Function("document", `${code}\nreturn { consultClickEvent, reviewClickEvent, inquiryAcceptedParams, contentGroup, scroll50Event };`)({
  querySelector() { return null; },
  querySelectorAll() { return []; },
  addEventListener() {},
});

test("phone and LINE clicks carry the page, the location, and the business", () => {
  const phone = api.consultClickEvent("tel:0593150697", "/leo/assessment/", "assessment");
  assert.equal(phone.name, "phone_click");
  assert.deepEqual(phone.params, { page_path: "/leo/assessment/", link_location: "assessment", business: "leo" });
  assert.equal(JSON.stringify(phone).includes("059"), false);

  const line = api.consultClickEvent("https://line.me/R/ti/p/@279qxcql", "/contact/#line", "contact");
  assert.equal(line.name, "line_click");
  assert.deepEqual(line.params, { page_path: "/contact/", link_location: "contact", business: "contact" });
  assert.equal(JSON.stringify(line).includes("@279"), false);
  assert.equal(JSON.stringify(line).includes("line.me"), false);
});

test("content groups follow the first path segment", () => {
  assert.equal(api.contentGroup("/"), "top");
  assert.equal(api.contentGroup("/leo/parent-training/"), "leo");
  assert.equal(api.contentGroup("/chamu/"), "chamu");
  assert.equal(api.contentGroup("/kintoun/"), "kintoun");
  assert.equal(api.contentGroup("/ryozanpaku/"), "ryozanpaku");
  assert.equal(api.contentGroup("/rydeen/"), "rydeen");
  assert.equal(api.contentGroup("/suishodama/"), "suishodama");
  assert.equal(api.contentGroup("/contact/"), "contact");
  assert.equal(api.contentGroup("/about/"), "corporate");
  assert.equal(api.contentGroup("/privacy/"), "corporate");
  assert.equal(api.contentGroup("/kokyu/"), "corporate");
});

test("scroll_50 is only for a business page and only once per call", () => {
  assert.deepEqual(api.scroll50Event("leo"), { name: "scroll_50", params: { business: "leo", content_group: "leo" } });
  assert.equal(api.scroll50Event("corporate"), null);
  assert.equal(api.scroll50Event("top"), null);
  assert.equal(api.scroll50Event("contact"), null);
});

test("a saved inquiry event has no personal fields", () => {
  const accepted = api.inquiryAcceptedParams("/contact/?q=1#line");
  assert.deepEqual(accepted, { page_path: "/contact/", method: "server_receipt", form_id: "contact-intake", business: "contact" });
  assert.equal(JSON.stringify(accepted).includes("059"), false);
  assert.equal(Object.hasOwn(accepted, "name"), false);
  assert.equal(Object.hasOwn(accepted, "email"), false);
  assert.equal(Object.hasOwn(accepted, "body"), false);
});

test("internal LINE buttons and ordinary links are not consult events", () => {
  assert.equal(api.consultClickEvent("../contact/#line", "/leo/", "leo"), null);
  assert.equal(api.consultClickEvent("https://psr-seishinkai.org/contact/", "/", "body"), null);
  const cleaned = api.consultClickEvent("tel:0593150697", "/contact/?from=ad", "not a place");
  assert.deepEqual(cleaned.params, { page_path: "/contact/", link_location: "body", business: "contact" });
});

test("Google Maps review links fire review_click with the page and business, and do not include the cid", () => {
  const href = "https://www.google.com/maps?cid=6914631722605448341";
  const leo = api.reviewClickEvent(href, "/leo/", "reviews");
  assert.equal(leo.name, "review_click");
  assert.deepEqual(leo.params, { page_path: "/leo/", link_location: "reviews", business: "leo" });
  assert.equal(JSON.stringify(leo).includes("691463"), false);
  assert.equal(JSON.stringify(leo).includes("cid"), false);

  const faq = api.reviewClickEvent(href, "/leo/faq/?from=home", "reviews");
  assert.deepEqual(faq.params, { page_path: "/leo/faq/", link_location: "reviews", business: "leo" });

  assert.equal(api.reviewClickEvent("https://www.google.com/maps/search/?api=1&query=三重県四日市市あさけが丘2-1-42", "/access/", "body"), null);
  assert.equal(api.consultClickEvent(href, "/leo/", "reviews"), null);
});
