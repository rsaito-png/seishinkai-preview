document.querySelector('.menu-btn')?.addEventListener('click',()=>document.body.classList.toggle('open'));
document.querySelectorAll('.drawer a').forEach(a=>a.addEventListener('click',()=>document.body.classList.remove('open')));
document.querySelectorAll('.chips').forEach(c=>{const ans=c.parentElement.querySelector('.ans');
 c.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;c.querySelectorAll('button').forEach(x=>x.classList.toggle('on',x===b));ans.textContent=b.dataset.a;});});
document.querySelectorAll('.steps').forEach(s=>{const F=JSON.parse(s.querySelector('script').textContent);let i=0;const q=k=>s.querySelector(k),n=F.length;
 const bar=q('.sbar');bar.innerHTML=F.map(()=>'<i></i>').join('');
 function r(a){q('.num').innerHTML=`0${i+1}<small>/ 0${n}</small>`;q('.k').textContent=F[i][0];q('h3').textContent=F[i][1];q('p').textContent=F[i][2];
  bar.querySelectorAll('i').forEach((x,k)=>x.classList.toggle('on',k<=i));q('.prev').disabled=i===0;q('.next').textContent=i===n-1?'相談する':'次へ';
  if(a){const c=q('.card');c.classList.remove('anim');void c.offsetWidth;c.classList.add('anim');}}
 q('.next').onclick=()=>{if(i===n-1){location.href=s.dataset.cta;return}i++;r(1)};q('.prev').onclick=()=>{if(i>0){i--;r(1)}};r(0);});
const aud=document.querySelector('.aud');if(aud){const cards=document.querySelector('.cards'),self=document.querySelector('.self');
 aud.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;const on=!b.classList.contains('on');
  aud.querySelectorAll('button').forEach(x=>x.classList.toggle('on',on&&x===b));cards.classList.toggle('filtered',on);
  const order=on?b.dataset.order.split(','):[];
  cards.querySelectorAll('.sc').forEach(c=>{const k=order.indexOf(c.dataset.k);c.classList.toggle('pick',k>=0);c.style.order=on?(k>=0?k:10):'';});
  if(self)self.classList.toggle('pick',on&&order.includes('shichirin'));
  document.getElementById('services').scrollIntoView({behavior:'smooth'});});}
const fab=document.querySelector('.fab'),ctas=document.querySelectorAll('.cta,.gf');
if(fab&&'IntersectionObserver'in window){const vis=new Set();const io=new IntersectionObserver(es=>{es.forEach(e=>e.isIntersecting?vis.add(e.target):vis.delete(e.target));fab.classList.toggle('hide',vis.size>0)});ctas.forEach(c=>io.observe(c));}
if(fab){const f=()=>fab.classList.toggle('top',scrollY<innerHeight*0.6);addEventListener('scroll',f,{passive:true});f();}

/* Consultation clicks. Params are page_path and link_location only — never the phone number or the LINE ID. */
function inquiryAcceptedParams(pathname) {
  var path = String(pathname || '/').split('?')[0].split('#')[0];
  if (!path || path.charAt(0) !== '/') path = '/' + (path || '');
  return { page_path: path, method: 'server_receipt', form_id: 'contact-intake', business: contentGroup(path) };
}
function contentGroup(pathname) {
  var path = String(pathname || '/').split('?')[0].split('#')[0];
  if (!path || path.charAt(0) !== '/') path = '/' + (path || '');
  var parts = path.split('/').filter(Boolean);
  var first = parts[0] || '';
  if (!first) return 'top';
  if (first === 'leo' || first === 'chamu' || first === 'kintoun' || first === 'ryozanpaku' || first === 'rydeen' || first === 'suishodama' || first === 'contact') return first;
  return 'corporate';
}
function consultClickEvent(href, pagePath, linkLocation) {
  var raw = String(href || '');
  var name = '';
  if (/^tel:/i.test(raw)) name = 'phone_click';
  else if (/^https?:\/\/(www\.)?line\.me\//i.test(raw)) name = 'line_click';
  if (!name) return null;
  var path = String(pagePath || '/').split('?')[0].split('#')[0];
  if (!path || path.charAt(0) !== '/') path = '/' + (path || '');
  var loc = String(linkLocation || 'body');
  if (!/^[a-z0-9_-]{1,40}$/.test(loc)) loc = 'body';
  return { name: name, params: { page_path: path, link_location: loc, business: contentGroup(path) } };
}
function consultLinkLocation(anchor) {
  var marked = anchor.closest('[data-track]');
  if (marked) return marked.getAttribute('data-track') || 'body';
  if (anchor.closest('header, .gh, .drawer')) return 'header';
  if (anchor.closest('footer, .gf')) return 'footer';
  if (anchor.closest('#line')) return 'contact';
  if (anchor.closest('.cta, #contact')) {
    var parts = location.pathname.split('/').filter(Boolean);
    return parts.length ? parts[parts.length - 1] : 'home';
  }
  return 'body';
}
document.addEventListener('click', function (e) {
  var anchor = e.target && e.target.closest ? e.target.closest('a[href]') : null;
  if (!anchor || typeof gtag !== 'function') return;
  var event = consultClickEvent(anchor.getAttribute('href'), location.pathname, consultLinkLocation(anchor));
  if (!event) return;
  gtag('event', event.name, event.params);
}, true);

/* First landing only. sessionStorage, or localStorage for 30 days when sessionStorage is unavailable. */
var ATTR_KEY = 'seishinkai-attr';
var ATTR_TTL = 30 * 24 * 60 * 60 * 1000;
function attrClean(value, max) {
  var v = String(value || '').trim();
  if (!v || v.length > max || /[\u0000-\u001F\u007F]/.test(v)) return '';
  return v;
}
function readAttrStore() {
  try {
    var raw = sessionStorage.getItem(ATTR_KEY);
    if (raw) return JSON.parse(raw);
  } catch (e) {}
  try {
    var saved = localStorage.getItem(ATTR_KEY);
    if (!saved) return null;
    var rec = JSON.parse(saved);
    if (!rec || !rec.saved_at || Date.now() - Number(rec.saved_at) > ATTR_TTL) {
      localStorage.removeItem(ATTR_KEY);
      return null;
    }
    return rec;
  } catch (e2) {
    return null;
  }
}
function writeAttrStore(rec) {
  var text = JSON.stringify(rec);
  try {
    sessionStorage.setItem(ATTR_KEY, text);
    return;
  } catch (e) {}
  try { localStorage.setItem(ATTR_KEY, text); } catch (e2) {}
}
function captureAttribution() {
  var existing = readAttrStore();
  if (existing) return existing;
  var params;
  try { params = new URLSearchParams(location.search); } catch (e) { params = { get: function () { return ''; } }; }
  var host = '';
  try { if (document.referrer) host = new URL(document.referrer).hostname; } catch (e2) {}
  var path = '/';
  try { path = String(location.pathname || '/').split('?')[0].split('#')[0] || '/'; } catch (e3) {}
  var rec = {
    utm_source: attrClean(params.get('utm_source'), 100),
    utm_medium: attrClean(params.get('utm_medium'), 100),
    utm_campaign: attrClean(params.get('utm_campaign'), 100),
    referrer_host: attrClean(host, 253).toLowerCase(),
    landing_path: path.charAt(0) === '/' && path.length <= 200 ? path : '/',
    saved_at: Date.now()
  };
  writeAttrStore(rec);
  return rec;
}
function attributionPayload(submitPath) {
  var rec = captureAttribution() || {};
  var path = String(submitPath || '/').split('?')[0].split('#')[0] || '/';
  return {
    utm_source: rec.utm_source || '',
    utm_medium: rec.utm_medium || '',
    utm_campaign: rec.utm_campaign || '',
    referrer_host: rec.referrer_host || '',
    landing_path: rec.landing_path || '/',
    submit_path: path.charAt(0) === '/' ? path : '/'
  };
}

var SCROLL_BUSINESS = { leo: 1, chamu: 1, kintoun: 1, ryozanpaku: 1, rydeen: 1, suishodama: 1 };
function scroll50Event(group) {
  if (!SCROLL_BUSINESS[group]) return null;
  return { name: 'scroll_50', params: { business: group, content_group: group } };
}
function installScroll50() {
  var group = contentGroup(location.pathname);
  var event = scroll50Event(group);
  if (!event || typeof gtag !== 'function' || typeof addEventListener !== 'function') return;
  var sent = false;
  function send() {
    if (sent) return;
    var doc = document.documentElement;
    var height = Math.max(doc.scrollHeight || 0, doc.offsetHeight || 0, 1);
    var seen = (window.scrollY || window.pageYOffset || 0) + (window.innerHeight || 0);
    if (seen / height < 0.5) return;
    sent = true;
    gtag('event', event.name, event.params);
  }
  addEventListener('scroll', send, { passive: true });
  send();
}
try { captureAttribution(); } catch (e) {}
try { installScroll50(); } catch (e2) {}
