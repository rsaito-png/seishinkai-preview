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
