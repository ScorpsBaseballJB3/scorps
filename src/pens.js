/* Shared bullpen stats + render helpers (kid pages and coach page). 9-hole net = inner 3x3 of a 5x5 grid. */
const PT={FB:"Fastball","2S":"2-seam",CB:"Curve",SL:"Slider",CH:"Change"};
const PC={FB:"#9b6ce0","2S":"#e0a4f0",CB:"#60a5fa",SL:"#4fc3b0",CH:"#facc15"};
const PORDER=["FB","2S","CB","SL","CH"];
const isK=p=>p.x>=1&&p.x<=3&&p.y>=1&&p.y<=3;
const holeN=(x,y)=>(y-1)*3+x;
const pctS=(a,b)=>b?Math.round(100*a/b)+"%":"–";
const avg=a=>a.length?Math.round(10*a.reduce((s,x)=>s+x,0)/a.length)/10:null;
function penStats(P){
  const n=P.length,k=P.filter(isK).length,ms=n-k,gm=P.filter(p=>!isK(p)&&p.g).length;
  const by={};P.forEach(p=>{const b=by[p.t]=by[p.t]||{n:0,k:0,gm:0,v:[]};b.n++;if(isK(p))b.k++;else if(p.g)b.gm++;if(typeof p.v==="number")b.v.push(p.v)});
  return {n,k,ms,gm,q:k+gm,by};
}
function heatHTML(P,big){
  const c={};P.forEach(p=>{const key=p.x+","+p.y;c[key]=(c[key]||0)+1});
  const mx=Math.max(1,...Object.values(c));let h="";
  for(let y=0;y<5;y++)for(let x=0;x<5;x++){const n=c[x+","+y]||0,inZ=x>=1&&x<=3&&y>=1&&y<=3;
    h+=`<div class="hc ${inZ?"in":""}"><span style="opacity:${n?(.18+.82*n/mx).toFixed(2):0}"></span><b>${n||(inZ?holeN(x,y):"")}</b></div>`}
  return `<div class="heatwrap"><div class="zedge"><span>Arm side</span><span>Glove side</span></div><div class="heat ${big?"big":""}">${h}</div><div class="zcap">Catcher's view · inner 9 = the holes · numbers = pitches</div></div>`;
}
function recapHTML(P){
  if(!P.length)return `<div class="empty">No pitches charted yet.</div>`;
  const s=penStats(P);
  const rows=PORDER.filter(t=>s.by[t]).map(t=>{const b=s.by[t];return `<tr><td><i class="pdot" style="background:${PC[t]}"></i>${PT[t]}</td><td>${b.n}</td><td>${pctS(b.k,b.n)}</td><td>${pctS(b.k+b.gm,b.n)}</td><td>${b.v.length?avg(b.v):"–"}</td><td>${b.v.length?Math.max(...b.v):"–"}</td></tr>`}).join("");
  return `<div class="tiles"><div><div class="v">${pctS(s.k,s.n)}</div><div class="t">Strikes · ${s.k}/${s.n}</div></div><div><div class="v">${s.gm}<small>/${s.ms}</small></div><div class="t">Good misses</div></div><div><div class="v hi">${pctS(s.q,s.n)}</div><div class="t">Strike + good miss</div></div></div>
  <div class="tscroll"><table class="pt"><thead><tr><th>Pitch</th><th>#</th><th>Strike</th><th>K + GM</th><th>Avg</th><th>Top</th></tr></thead><tbody>${rows}</tbody></table></div>${heatHTML(P)}`;
}
function progressHTML(pens){
  const L=pens.filter(x=>x.p&&x.p.length).sort((a,b)=>a.d<b.d?-1:1);
  if(!L.length)return `<div class="empty">Shows up after your first charted bullpen.</div>`;
  const pts=L.map(x=>{const s=penStats(x.p);return {d:x.d,k:100*s.k/s.n,q:100*s.q/s.n}});
  const w=520,h=180,p={l:36,r:14,t:14,b:26};
  const X=i=>p.l+(pts.length===1?(w-p.l-p.r)/2:i*(w-p.l-p.r)/(pts.length-1)),Y=v=>p.t+(100-v)*(h-p.t-p.b)/100;
  const line=k=>pts.map((x,i)=>(i?"L":"M")+X(i).toFixed(1)+" "+Y(x[k]).toFixed(1)).join(" ");
  const M=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];const f=d=>M[+d.slice(5,7)-1]+" "+(+d.slice(8));
  const step=Math.max(1,Math.ceil(pts.length/6));
  const svg=`<svg viewBox="0 0 ${w} ${h}" width="100%" role="img" aria-label="Strike percent by bullpen">${[0,50,100].map(t=>`<line x1="${p.l}" x2="${w-p.r}" y1="${Y(t)}" y2="${Y(t)}" stroke="#2d2640"/><text x="${p.l-6}" y="${Y(t)+4}" text-anchor="end">${t}%</text>`).join("")}
  <path d="${line("q")}" fill="none" stroke="#4fc3b0" stroke-width="2.5"/><path d="${line("k")}" fill="none" stroke="#9b6ce0" stroke-width="3.5"/>${pts.map((x,i)=>`<circle cx="${X(i)}" cy="${Y(x.k)}" r="${i===pts.length-1?6:4}" fill="#c3a2f5"/>${i%step===0||i===pts.length-1?`<text x="${X(i)}" y="${h-7}" text-anchor="middle">${f(x.d)}</text>`:""}`).join("")}</svg>`;
  const all=[].concat(...L.map(x=>x.p)),s=penStats(all);
  const bars=PORDER.filter(t=>s.by[t]).map(t=>{const b=s.by[t],v=100*b.k/b.n;return `<div class="pbar"><span><i class="pdot" style="background:${PC[t]}"></i>${PT[t]}</span><div class="track"><div class="fill" style="width:${Math.max(3,v)}%;background:${PC[t]}"></div></div><b>${Math.round(v)}%</b></div>`}).join("");
  return `<div class="sub">Strike % each bullpen</div><div style="overflow-x:auto">${svg}</div><div class="legend"><span><i class="ball" style="background:#9b6ce0"></i>Strike %</span><span><i class="ball" style="background:#4fc3b0"></i>Strike + good miss %</span></div>
  <div class="sub">Strike % by pitch · all bullpens (${all.length} pitches)</div>${bars}<div class="sub">Where it's landing · all bullpens</div>${heatHTML(all)}`;
}
