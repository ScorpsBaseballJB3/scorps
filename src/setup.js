/* Top-down setup diagrams. Wall at top. Drawn for a righty; lefty = mirrored (labels stay readable). */
const SW=320;
function setupSVG(s,L){
  const X=x=>L?SW-x:x, R=r=>L?-r:r, A=a=>L?(a==="start"?"end":a==="end"?"start":a):a;
  const H=s.k==="walk"?250:205;
  const FOOT="M0,-16 C8,-16 9,-6 8,4 C7,14 3,17 0,17 C-3,17 -7,14 -8,4 C-9,-6 -8,-16 0,-16Z";
  const PUR="#9b6ce0",SIL="#cfccd8",TXT="#f2eff8",MUT="#a49eb5";
  let g="";
  const foot=(x,y,r,col,lab,la,ghost)=>{g+=`<g transform="translate(${X(x)},${y}) rotate(${R(r)})"><path d="${FOOT}" fill="${ghost?"none":col}" stroke="${col}" stroke-width="2" ${ghost?'stroke-dasharray="4 3"':""}/><circle cx="-5" cy="-21" r="2.6" fill="${ghost?"none":col}" stroke="${col}" stroke-width="${ghost?1.2:0}"/><circle cx="0" cy="-23.5" r="2.8" fill="${ghost?"none":col}" stroke="${col}" stroke-width="${ghost?1.2:0}"/><circle cx="5" cy="-21" r="2.6" fill="${ghost?"none":col}" stroke="${col}" stroke-width="${ghost?1.2:0}"/></g>`;if(lab){const o=Math.abs(r%180)>45?32:18;g+=txt(x+(la==="start"?o:-o),y+4,lab,la||"end",ghost?MUT:TXT)}};
  const knee=(x,y,lab,la)=>{g+=`<circle cx="${X(x)}" cy="${y}" r="11" fill="${SIL}"/><text x="${X(x)}" y="${y+4}" text-anchor="middle" style="fill:#16131e;font:700 10px var(--body)">K</text>`;if(lab)g+=txt(x+(la==="start"?20:-20),y+4,lab,la||"end",TXT)};
  const txt=(x,y,t,a,c,w)=>`<text x="${X(x)}" y="${y}" text-anchor="${A(a||"middle")}" style="fill:${c||TXT};font:${w||600} 12px var(--body)">${t}</text>`;
  const arrow=(d,col,dash,lab,lx,ly,la)=>{const pts=d;g+=`<path d="${pts}" fill="none" stroke="${col}" stroke-width="3" ${dash?'stroke-dasharray="5 4"':""} marker-end="url(#ah${col===PUR?"p":"s"})"/>`;if(lab)g+=txt(lx,ly,lab,la||"start",col===PUR?"#c3a2f5":MUT,700)};
  const P=pts=>"M"+pts.map(([x,y])=>X(x)+","+y).join(" L");
  const Q=(a,c,b)=>`M${X(a[0])},${a[1]} Q${X(c[0])},${c[1]} ${X(b[0])},${b[1]}`;
  const dim=(y1,y2,lab)=>{const x=46;g+=`<path d="M${X(x)},${y1} L${X(x)},${y2} M${X(x-6)},${y1} L${X(x+6)},${y1} M${X(x-6)},${y2} L${X(x+6)},${y2}" stroke="${MUT}" stroke-width="1.5" fill="none"/>`;g+=`<rect x="${X(x)-26}" y="${(y1+y2)/2-11}" width="52" height="20" rx="6" fill="#1f1a2b" stroke="#2d2640"/>`+txt(x,(y1+y2)/2+3,lab,"middle",TXT,700)};
  // wall / net
  if(s.k!=="slam"){const net=s.w==="net";g+=`<rect x="14" y="8" width="${SW-28}" height="20" rx="4" fill="${net?"none":"#5a556a"}" stroke="${net?SIL:"#5a556a"}" stroke-width="2" ${net?'stroke-dasharray="6 4"':""}/>`+`<text x="${SW/2}" y="22" text-anchor="middle" style="fill:${TXT};font:800 12px var(--body);letter-spacing:.18em">${net?"FIELD NET":"WALL"}</text>`}
  const top=30;
  switch(s.k){
    case "side": case "roll": case "drop": case "kneel": {
      const r=s.k==="roll"?125:90, fy=100, by=165;
      if(s.k==="kneel"){foot(160,fy,90,PUR,"Front foot","start");knee(160,by,"Back knee down","start")}
      else{foot(160,fy,r,PUR,"Front foot (glove side)","start");foot(160,by,r,SIL,s.k==="drop"?"Back foot starts here":"Back foot","start")}
      if(s.k==="drop"){foot(128,128,90,SIL,"",null,true);arrow(Q([152,160],[128,158],[128,148]),SIL,true,"Step behind",100,190,"middle")}
      if(s.k==="roll")g+=txt(160,198,"Turned past sideways, back half toward the wall","middle",MUT,500);
      arrow(P([[160,78],[160,top+4]]),PUR,false,"Throw",170,58);dim(top,fy,s.d);break}
    case "back": {
      foot(135,95,180,SIL,"");foot(185,95,180,SIL,"");g+=txt(160,135,"Toes point away from the wall","middle",TXT,600);
      arrow(Q([118,92],[86,64],[110,top+4]),PUR,false,"Throw back over your throwing shoulder",132,170,"middle");dim(top,95,s.d);break}
    case "face": {
      foot(140,95,0,PUR,"Glove-side foot","end");foot(182,95,0,SIL,"");foot(182,160,90,SIL,"Step back here","end",true);
      arrow(P([[182,116],[182,140]]),SIL,true);arrow(P([[160,74],[160,top+4]]),PUR,false,"Throw",170,58);dim(top,95,s.d);break}
    case "walk": {
      foot(140,215,0,SIL,"",null,true);foot(180,215,0,SIL,"Start here",'start',true);
      arrow(P([[160,198],[160,168]]),SIL,true,"Walk 2 steps",172,186);
      foot(160,95,90,PUR,"Front foot","start");foot(160,150,90,SIL,"Back foot","start");
      arrow(P([[160,74],[160,top+4]]),PUR,false,"Throw",170,58);dim(top,215,s.d);break}
    case "crouch": case "kd": case "jp": {
      if(s.k==="kd"){foot(132,100,-15,PUR,"Glove-side foot","end");knee(188,108,"Knee down","start")}
      else{foot(132,100,-15,PUR,"","");foot(188,100,15,SIL,"");g+=txt(160,s.k==="jp"?196:140,"Catcher's stance, facing the wall","middle",TXT,600)}
      if(s.k==="jp"){foot(196,160,90,SIL,"Jab, pivot","end",true);arrow(Q([190,118],[200,135],[196,148]),SIL,true)}
      arrow(P([[160,82],[160,top+4]]),PUR,false,"Throw",170,58);dim(top,100,s.d);break}
    case "slam": {
      g+=`<circle cx="${SW/2}" cy="55" r="22" fill="none" stroke="${PUR}" stroke-width="3" stroke-dasharray="5 4"/>`+txt(160,59,"Slam","middle","#c3a2f5",700);
      foot(135,120,0,SIL,"");foot(185,120,0,SIL,"");g+=txt(160,165,"Feet shoulder width · no net needed","middle",TXT,600);break}
  }
  return `<svg class="setsvg" viewBox="0 0 ${SW} ${H}" width="100%" role="img" aria-label="Setup: ${esc(s.t)}"><defs><marker id="ahp" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10z" fill="${PUR}"/></marker><marker id="ahs" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10z" fill="${SIL}"/></marker></defs>${g}</svg>`;
}
function setupHTML(g){if(!g.set)return "";return `<div class="setup">${setupSVG(g.set,!!D.lefty)}<div><b>Setup</b> ${esc(g.set.t)}${D.lefty?" <span class=\"lh\">Drawn for a lefty.</span>":""}</div></div>`}
