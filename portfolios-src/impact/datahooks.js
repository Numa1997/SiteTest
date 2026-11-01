// Inserted into the page by build.py after the page script. The panel (scripts/datalog.js) only reads the store; these hooks say
// what lies at a point of the figure, how to recompute every value from stored inputs, and how to read it back from the picture.
const NAME={iron:"iron",cot:"cotton"},WHAT={iron:"atom",cot:"bead"};
const stageBox={canvas:cv,ctx:cx,get dpr(){return DPR}};
const plotBox=id=>{const c=document.getElementById(id);return {canvas:c,ctx:c.getContext("2d"),dpr:DPR}};
const colOf=s=>RTL?(s==="cot"?0:1):(s==="iron"?0:1);

// ---- reruns for Check: a second pair of balls, built afresh by makeIron() and makeCotton(), stepped by the same step() ----
const FB={};                                    // built afresh and never stepped: shapes, bonds, rest lengths
const fresh=s=>FB[s]||(FB[s]=s==="iron"?makeIron():makeCotton());
const RB={},runs=new Map();                     // RB: a second ball of each kind, built once and reloaded from checkpoints; runs: the last results
function run(s,from,k){                         // the state of ball s at sample k, rerun from checkpoint `from` (−1: from a fresh build at t = 0)
  const key=s+"|"+from+"|"+k;if(runs.has(key))return runs.get(key);
  const build=()=>s==="iron"?makeIron():makeCotton(),b=from>=0?(RB[s]||(RB[s]=build())):build(),N=b.N,ns=ds.get("nstep");let todo=ns[k];
  if(from>=0){const ck=n=>ds.get("ck_"+n+"_"+s);
    for(let i=0;i<N;i++){b.x[i]=ck("x")[from*N+i];b.y[i]=ck("y")[from*N+i];b.u[i]=ck("u")[from*N+i];b.v[i]=ck("v")[from*N+i]}
    b.alive.set(ck("alive").subarray(from*b.nb,(from+1)*b.nb));
    b.t=ck("t")[from];b.yp=ck("yp")[from];b.vp=ck("vp")[from];b.Fmax=ck("Fmax")[from];b.heatBall=ck("Qb")[from];b.heatHead=ck("Qh")[from];b.heatAir=ck("Qa")[from];b.heat=b.heatBall+b.heatHead;
    const ti=ck("ti")[from];b.tImpact=ti===ti?ti:null;todo=ns[k]-ds.get("ck_step")[from]}
  for(let q=0;q<todo;q++)b.Fs=step(b);
  const snap={x:Float64Array.from(b.x),y:Float64Array.from(b.y),u:Float64Array.from(b.u),v:Float64Array.from(b.v),alive:Uint8Array.from(b.alive),
    t:b.t,yp:b.yp,vp:b.vp,Fmax:b.Fmax,heatBall:b.heatBall,heatHead:b.heatHead,heatAir:b.heatAir,tImpact:b.tImpact,E:Object.assign({},b.E)};
  const r={key,from,k,steps:todo,b:snap};runs.set(key,r);if(runs.size>24)runs.delete(runs.keys().next().value);return r;
}
const fromFor=k=>k%CK===0?k/CK-1:Math.floor(k/CK);        // the checkpoint before sample k (never k itself)
const replay=(s,k)=>run(s,fromFor(k),k);
const replayCk=(s,c)=>run(s,c-1,c*CK);
const howRerun=(r,s)=>r.from<0?"the same model, built afresh and stepped "+r.steps+" times from t = 0":"the same model, rerun "+r.steps+" steps of Δt from checkpoint "+r.from+" (sample "+r.from*CK+")";
let NSTEP=null;
function recount(){                             // the frame steps per sample, counted again by adding the sub-steps exactly as the model does
  if(NSTEP)return NSTEP;NSTEP=new Int32Array(NF);let t=0,S=0;const h=P.dt/P.iron.sub,st=()=>{for(let q=0;q<P.iron.sub;q++)t+=h;S++};
  st();NSTEP[0]=S;for(let k=1;k<NF;k++){while(t<tOf(k)-1e-9)st();NSTEP[k]=S}return NSTEP;
}

// ---- read-back from the picture ----
const dark=c=>c[3]>200&&c[0]<110&&c[1]<110&&c[2]<110;
const light=c=>c[3]>=230&&c[0]>=200&&c[1]>=195&&c[2]>=185;
const blue=c=>c[3]>0&&c[2]>c[0]+40&&c[2]<220;
const plateFill=c=>c[3]>250&&Math.abs(c[0]-227)<14&&Math.abs(c[1]-207)<14&&Math.abs(c[2]-174)<14;
function readBack(box,what,pt,r,test,expected,note){
  const q=Sim.readPixel(box,pt.x,pt.y,r,test);
  return {what:what+", ("+Sim.fmt(pt.x,1)+", "+Sim.fmt(pt.y,1)+") css px",drawn:q.text,expected:expected,ok:q.found,note:note};
}
function partDrawn(s,idx){
  const N=D[s].N,n=Math.floor(idx/N),i=idx%N;
  if(n!==ds.get("i_now"))return {what:NAME[s]+" "+WHAT[s]+" "+i+" at sample "+n,drawn:"not drawn now",expected:"drawn only while the playback shows sample "+n,ok:null,note:"The figure shows one stored sample at a time, n<sub>now</sub> = "+ds.get("i_now")+"."};
  const p=partXY(s,n,i);
  if(p.y<ds.get("top_px")||p.y>ds.get("bottom_px")+2)return {what:NAME[s]+" "+WHAT[s]+" "+i,drawn:"outside the scene",expected:"cut off by the scene's edge",ok:null,note:"The scene shows "+Sim.fmt(ds.get("view_m"),2)+" m of height; this "+WHAT[s]+" is outside it."};
  return s==="iron"?readBack(stageBox,"centre of iron atom "+i,p,1,dark,"the dark atom disc","Drawn at x<sub>col</sub> + x·s, y<sub>bottom</sub> − (y + (G − 1) y<sub>p</sub> − y<sub>cam</sub>)·s.")
    :readBack(stageBox,"centre of cotton bead "+i,p,1,light,"the pale bead core","Drawn at x<sub>col</sub> + x·s, y<sub>bottom</sub> − (y + (G − 1) y<sub>p</sub> − y<sub>cam</sub>)·s; the fibre is a smooth curve through the beads.");
}
function plateRow(s){
  const top=ds.get("plate_px_"+s),bx=ds.get("bx_"+s),pw=Math.min(2.9*ds.get("sc"),ds.get("col_w")-14);
  if(top>ds.get("bottom_px")+18)return {what:"the "+NAME[s]+" plate",drawn:"below the scene",expected:"not drawn",ok:null,note:"The camera follows the iron ball; the plate is out of view."};
  let found=null;                               // scan whole device-pixel rows: Sim.readPixel reads device row round(y·dpr), so y = r/dpr reads row r
  for(const x of [bx-pw/2+5,bx+pw/2-5])for(let r=Math.floor((top-6)*DPR);r<=Math.ceil((top+12)*DPR);r++){const q=Sim.readPixel(stageBox,x,r/DPR,0);if(plateFill(q.rgba)){if(found===null||r<found.r)found={x,r};break}}
  // the 1.4 px outline is centred on the edge, so it ends at y_plate + 0.7; the row it ends in is a blend of outline and fill,
  // so the first row of pure fill is the next whole device row
  const expRow=Math.ceil((top+0.7)*DPR);
  return {what:"first device-pixel row of pure plate fill, scanned down two columns near the plate's ends",drawn:found?"row "+found.r+" ("+Sim.fmt(found.r/DPR,2)+" css px)":"no plate fill found",expected:"row "+expRow+" ("+Sim.fmt(expRow/DPR,2)+" css px), the first whole row under the outline that ends at y_plate + 0.7 = "+Sim.fmt(top+0.7,2)+" css px",
    ok:!!found&&Math.abs(found.r-expRow)<=1,note:"The plate's top edge is drawn at y<sub>plate</sub>; its travel, and the ball resting on it, are drawn G = 10 times larger than computed."};
}
const gaugeAt=(s,deg,r)=>({x:ds.get("bx_"+s)+r*Math.cos(deg*Math.PI/180),y:ds.get("gauge_cy")+r*Math.sin(deg*Math.PI/180)});
const needleBack=s=>readBack(stageBox,"the black needle, 0.3 R from the hub",gaugeAt(s,ds.get("needle_"+s),0.3*ds.get("gauge_R")),1,dark,"the dark needle",
  "The dial is square-root: the needle stands at −225° + 270°·√(F/700 N), clockwise from the right, so 9.81 N and 640 N both read clearly.");
const peakBack=s=>readBack(stageBox,"tip of the red peak-hold needle",gaugeAt(s,ds.get("peakneedle_"+s),ds.get("gauge_R")-6.5),1,Sim.isBurgundy,"the red needle tip",
  "The red needle reaches 3 px beyond the black one, so its tip shows even when both point the same way.");
function curveBack(s,n){
  if(n>ds.get("i_now"))return {what:"F of sample "+n+" on the whole-run plot",drawn:"not drawn yet",expected:"the curve is drawn up to the sample on screen",ok:null,note:"The plots grow with the playback."};
  const G=plotGeom("pAll",0,P.tmax),t=ds.get("ts")[n],p={x:G.X(t),y:G.Y(D[s].F[n])};
  if(s==="cot"&&Math.abs(G.Y(D.iron.F[n])-p.y)<2.5)return {what:"F of sample "+n+", cotton, on the whole-run plot",drawn:"under the iron curve",expected:"hidden: the iron curve is drawn over it here",ok:null,note:"Both balls read nearly the same force here, within 2.5 px of the plot."};
  const r=readBack(plotBox("pAll"),"F of sample "+n+" on the whole-run plot",p,2,s==="iron"?Sim.isBurgundy:blue,s==="iron"?"the wine curve":"the blue curve","x ∝ t from 0 to 9 s, y ∝ F from 0 to 700 N; every stored sample up to the one on screen is joined by straight lines.");
  if(s==="cot"&&!r.ok&&Sim.readPixel(plotBox("pAll"),p.x,p.y,2,Sim.isBurgundy).found)return {what:r.what,drawn:"the wine iron curve",expected:"hidden: the iron curve, drawn after it, covers it here",ok:null,note:"Near the impact the iron spike crosses the cotton curve; on a narrow plot it covers it."};
  return r;
}

// ---- Check: recompute from the stored inputs ----
const PMAP={g:"g",h:"h",M:"M",dt:"dt",tmax:"tmax",a_iron:"iron.a",R_iron:"iron.R",k_iron:"iron.k",ar0:"iron.ar0",c_iron:"iron.c",rad_iron:"iron.rad",sub_iron:"iron.sub",
  R_cot:"cot.R",nf:"cot.nf",nb:"cot.nb",s_cot:"cot.s",turn:"cot.turn",kax:"cot.kax",kb:"cot.kb",cb:"cot.cb",c_cot:"cot.c",jr:"cot.jr",kj:"cot.kj",Fj:"cot.Fj",drep:"cot.drep",krep:"cot.krep",crep:"cot.crep",
  rad_cot:"cot.rad",seed:"cot.seed",sub_cot:"cot.sub",mp:"head.mp",kh:"head.kh",ch:"head.ch",wc:"head.wc",zc:"head.zc",
  air_k:"air.k",rho_air:"air.rho",Cd:"air.Cd",dens_iron:"air.dens.iron",dens_cot:"air.dens.cot"};
const G=n=>ds.get(n),I=(sy,v,u,d)=>[sy,v,u||"",d===undefined?6:d];
const check={};
for(const n in PMAP)check[n]=()=>({formula:"the constant P."+PMAP[n]+" in the model",inputs:[],value:PMAP[n].split(".").reduce((o,k)=>o[k],P)});
const fromBuild=(s,f,txt)=>()=>({formula:txt+", from "+(s==="iron"?"makeIron()":"makeCotton()")+" run again",inputs:[],value:f(fresh(s))});
const atNow=(arr,sy)=>()=>{const n=G("i_now");return {formula:sy+"<sub>n</sub> at n = n<sub>now</sub>",inputs:[I("n<sub>now</sub>",n,"",0)],value:G(arr)[n]}};
function meanF(s,n){const F=D[s].F;let sum=0,c=0;for(let j=KW0;j<=n;j++){sum+=F[j];c++}return c?sum/c:NaN}
for(const s of BALLS){
  const d=D[s],N=d.N,nn=idx=>Math.floor(idx/N);
  Object.assign(check,{
    ["N_"+s]:fromBuild(s,b=>b.N,"particles"),["nbond_"+s]:fromBuild(s,b=>b.nb,"bonds"),["y00_"+s]:fromBuild(s,b=>b.y00,"mean starting height minus h"),
    ["m_"+s]:()=>({formula:"M / N",inputs:[I("M",G("M"),"kg",3),I("N",G("N_"+s),"",0)],value:G("M")/G("N_"+s)}),
    ["kc_"+s]:()=>({formula:"m ω<sub>c</sub>²",inputs:[I("m",G("m_"+s),"kg"),I("ω<sub>c</sub>",G("wc"),"rad/s",0)],value:G("m_"+s)*G("wc")*G("wc")}),
    ["cc_"+s]:()=>({formula:"2 ζ<sub>c</sub> m ω<sub>c</sub>",inputs:[I("ζ<sub>c</sub>",G("zc"),"",2),I("m",G("m_"+s),"kg"),I("ω<sub>c</sub>",G("wc"),"rad/s",0)],value:2*G("zc")*G("m_"+s)*G("wc")}),
    ["E0_"+s]:()=>({formula:"K + V + E<sub>el</sub> + E<sub>head</sub> + Q<sub>ball</sub> + Q<sub>head</sub> + Q<sub>air</sub> at n = 0, from the stored arrays",inputs:[I("K<sub>0</sub>",d.KE[0],"J"),I("V<sub>0</sub>",d.PE[0],"J")],value:d.KE[0]+d.PE[0]+d.El[0]+d.Eh[0]+d.Qb[0]+d.Qh[0]+d.Qa[0]}),
    ["t_touch_"+s]:()=>{const ti=G("ck_ti_"+s);let c=0;while(c<NCK&&!(ti[c]===ti[c]))c++;if(c>=NCK)return {formula:"not touched yet in the computed part of the run",inputs:[],value:NaN};
      const r=run(s,c-1,c*CK),b=r.b;   // run() stops at the checkpoint; the touch happened inside these steps
      return {formula:howRerun(r,s)+"; the model notes the time of the first step with a contact force",inputs:[I("checkpoint",c-1,"",0)],value:b.tImpact===null?NaN:b.tImpact}},
    ["Fpeak_"+s]:()=>{const r=replay(s,NF-1);return {formula:howRerun(r,s)+": the peak hold at the end",inputs:[I("steps",r.steps,"",0)],value:r.b.Fmax}},
    ["W_end_"+s]:()=>({formula:"mean of the stored F<sub>n</sub>, 4 s ≤ t<sub>n</sub> ≤ 9 s",inputs:[I("samples",NF-KW0,"",0)],value:meanF(s,NF-1)}),
    ["w_rel_"+s]:()=>({formula:"(W − Mg) / Mg",inputs:[I("W",G("W_end_"+s),"N"),I("Mg",G("Mg"),"N")],value:(G("W_end_"+s)-G("Mg"))/G("Mg")}),
    ["books_max_"+s]:()=>{let m=0;for(let k=0;k<NF;k++)m=Math.max(m,Math.abs(d.Esum[k]-d.Ein[k]));return {formula:"max over n of |E<sub>now</sub> − E<sub>in</sub>|, from the stored arrays",inputs:[I("samples",NF,"",0)],value:m}},
    ["x_"+s]:idx=>{const r=replay(s,nn(idx));return {formula:howRerun(r,s),inputs:[I("n",nn(idx),"",0),I("i",idx%N,"",0)],value:r.b.x[idx%N]}},
    ["y_"+s]:idx=>{const r=replay(s,nn(idx));return {formula:howRerun(r,s),inputs:[I("n",nn(idx),"",0),I("i",idx%N,"",0)],value:r.b.y[idx%N]}},
    ["sp_"+s]:idx=>{const r=replay(s,nn(idx)),i=idx%N;return {formula:"√(u² + v²) after "+howRerun(r,s),inputs:[I("u",r.b.u[i],"m/s"),I("v",r.b.v[i],"m/s")],value:Math.sqrt(r.b.u[i]*r.b.u[i]+r.b.v[i]*r.b.v[i])}},
    ["yp_"+s]:n=>{const r=replay(s,n);return {formula:howRerun(r,s),inputs:[I("n",n,"",0)],value:r.b.yp}},
    ["vp_"+s]:n=>{const r=replay(s,n);return {formula:howRerun(r,s),inputs:[I("n",n,"",0)],value:r.b.vp}},
    ["F_"+s]:n=>({formula:"F = −k<sub>h</sub> y<sub>p</sub>: the head spring times its compression",inputs:[I("k<sub>h</sub>",G("kh"),"N/m",0),I("y<sub>p</sub>",d.yp[n],"m",9)],value:-G("kh")*d.yp[n]}),
    ["Fmax_"+s]:n=>{const r=replay(s,n);return {formula:howRerun(r,s)+"; the peak hold sees every step",inputs:[I("n",n,"",0)],value:r.b.Fmax}},
    ["KE_"+s]:n=>{const r=replay(s,n);return {formula:howRerun(r,s),inputs:[I("n",n,"",0)],value:r.b.E.KE}},
    ["PE_"+s]:n=>{const r=replay(s,n);return {formula:howRerun(r,s),inputs:[I("n",n,"",0)],value:r.b.E.PE}},
    ["El_"+s]:n=>{const r=replay(s,n);return {formula:howRerun(r,s),inputs:[I("n",n,"",0)],value:r.b.E.elastic}},
    ["Eh_"+s]:n=>{const r=replay(s,n);return {formula:howRerun(r,s),inputs:[I("n",n,"",0)],value:r.b.E.head}},
    ["Qb_"+s]:n=>{const r=replay(s,n);return {formula:howRerun(r,s),inputs:[I("n",n,"",0)],value:r.b.E.heatBall}},
    ["Qh_"+s]:n=>{const r=replay(s,n);return {formula:howRerun(r,s),inputs:[I("n",n,"",0)],value:r.b.E.heatHead}},
    ["Qa_"+s]:n=>{const r=replay(s,n);return {formula:howRerun(r,s),inputs:[I("n",n,"",0)],value:r.b.E.heatAir}},
    ["Ein_"+s]:n=>({formula:"E<sub>0</sub> − V<sub>n</sub>",inputs:[I("E<sub>0</sub>",G("E0_"+s),"J"),I("V<sub>n</sub>",d.PE[n],"J")],value:G("E0_"+s)-d.PE[n]}),
    ["Esum_"+s]:n=>({formula:"K + E<sub>el</sub> + E<sub>head</sub> + Q<sub>ball</sub> + Q<sub>head</sub> + Q<sub>air</sub>",inputs:[I("K",d.KE[n],"J"),I("E<sub>el</sub>",d.El[n],"J"),I("E<sub>head</sub>",d.Eh[n],"J"),I("Q<sub>ball</sub>",d.Qb[n],"J"),I("Q<sub>head</sub>",d.Qh[n],"J"),I("Q<sub>air</sub>",d.Qa[n],"J")],value:d.KE[n]+d.El[n]+d.Eh[n]+d.Qb[n]+d.Qh[n]+d.Qa[n]}),
    ["books_"+s]:n=>({formula:"E<sub>now</sub> − E<sub>in</sub>",inputs:[I("E<sub>now</sub>",d.Esum[n],"J"),I("E<sub>in</sub>",d.Ein[n],"J")],value:d.Esum[n]-d.Ein[n]}),
    ["W_"+s]:n=>({formula:"mean of the stored F<sub>j</sub>, 4 s ≤ t<sub>j</sub> ≤ t<sub>n</sub>",inputs:[I("t<sub>n</sub>",G("ts")[n],"s",3)],value:n<KW0?NaN:meanF(s,n)}),
    ["bi_"+s]:q=>({formula:"bond list of a fresh build",inputs:[I("bond",q,"",0)],value:fresh(s).bi[q]}),
    ["bj_"+s]:q=>({formula:"bond list of a fresh build",inputs:[I("bond",q,"",0)],value:fresh(s).bj[q]}),
    ["l0_"+s]:q=>({formula:"rest length in a fresh build",inputs:[I("bond",q,"",0)],value:fresh(s).l0[q]}),
    ["ck_t_"+s]:c=>{const r=replayCk(s,c);return {formula:howRerun(r,s),inputs:[I("c",c,"",0)],value:r.b.t}},
    ["ck_yp_"+s]:c=>{const r=replayCk(s,c);return {formula:howRerun(r,s),inputs:[I("c",c,"",0)],value:r.b.yp}},
    ["ck_vp_"+s]:c=>{const r=replayCk(s,c);return {formula:howRerun(r,s),inputs:[I("c",c,"",0)],value:r.b.vp}},
    ["ck_Fmax_"+s]:c=>{const r=replayCk(s,c);return {formula:howRerun(r,s),inputs:[I("c",c,"",0)],value:r.b.Fmax}},
    ["ck_Qb_"+s]:c=>{const r=replayCk(s,c);return {formula:howRerun(r,s),inputs:[I("c",c,"",0)],value:r.b.heatBall}},
    ["ck_Qh_"+s]:c=>{const r=replayCk(s,c);return {formula:howRerun(r,s),inputs:[I("c",c,"",0)],value:r.b.heatHead}},
    ["ck_Qa_"+s]:c=>{const r=replayCk(s,c);return {formula:howRerun(r,s),inputs:[I("c",c,"",0)],value:r.b.heatAir}},
    ["A_"+s]:fromBuild(s,b=>b.Aair,"cross-section of a real 1 kg ball, π (3M / 4πρ)^(2/3)"),
    ["vt_"+s]:()=>({formula:"√(2Mg / (k<sub>air</sub> ρ<sub>air</sub> C<sub>d</sub> A))",inputs:[I("M",G("M"),"kg",3),I("g",G("g"),"m/s²",2),I("k<sub>air</sub>",G("air_k"),"",0),I("ρ<sub>air</sub>",G("rho_air"),"kg/m³",2),I("C<sub>d</sub>",G("Cd"),"",2),I("A",G("A_"+s),"m²")],value:Math.sqrt(2*G("M")*G("g")/(G("air_k")*G("rho_air")*G("Cd")*G("A_"+s)))}),
    ["t_air_"+s]:()=>{const vt=G("vt_"+s),g=G("g"),h=G("h");return {formula:"(v<sub>t</sub>/g) arcosh(e<sup>gh/v<sub>t</sub>²</sup>); √(2h/g) with air off",inputs:[I("v<sub>t</sub>",vt,"m/s",3),I("g",g,"m/s²",2),I("h",h,"m",2)],value:G("air_k")?vt/g*Math.acosh(Math.exp(g*h/vt/vt)):Math.sqrt(2*h/g)}},
    ["v_air_"+s]:()=>{const vt=G("vt_"+s),g=G("g"),h=G("h");return {formula:"v<sub>t</sub> √(1 − e<sup>−2gh/v<sub>t</sub>²</sup>); √(2gh) with air off",inputs:[I("v<sub>t</sub>",vt,"m/s",3),I("g",g,"m/s²",2),I("h",h,"m",2)],value:G("air_k")?vt*Math.sqrt(1-Math.exp(-2*g*h/vt/vt)):Math.sqrt(2*g*h)}},
    ["ck_ti_"+s]:c=>{const r=replayCk(s,c);return {formula:howRerun(r,s),inputs:[I("c",c,"",0)],value:r.b.tImpact===null?NaN:r.b.tImpact}},
    ["ck_alive_"+s]:idx=>{const nb=G("nbond_"+s),r=replayCk(s,Math.floor(idx/nb));return {formula:howRerun(r,s),inputs:[I("bond",idx%nb,"",0)],value:r.b.alive[idx%nb]}},
    ["F_now_"+s]:atNow("F_"+s,"F"),["Fmax_now_"+s]:atNow("Fmax_"+s,"F<sub>peak</sub>"),["yp_now_"+s]:atNow("yp_"+s,"y<sub>p</sub>"),["KE_now_"+s]:atNow("KE_"+s,"K"),["books_now_"+s]:atNow("books_"+s,"Δ"),
    ["W_now_"+s]:()=>{const n=G("i_now");return {formula:"W<sub>n</sub> at n = n<sub>now</sub>, once t<sub>n</sub> ≥ 6.5 s",inputs:[I("t<sub>n</sub>",G("ts")[n],"s",3)],value:G("ts")[n]>=WSHOW?d.W[n]:NaN}},
    ["kgpeak_now_"+s]:()=>({formula:"F<sub>peak</sub> / g",inputs:[I("F<sub>peak</sub>",G("Fmax_now_"+s),"N",3),I("g",G("g"),"m/s²",2)],value:G("Fmax_now_"+s)/G("g")}),
    ["kgw_now_"+s]:()=>({formula:"W / g",inputs:[I("W",G("W_now_"+s),"N",4),I("g",G("g"),"m/s²",2)],value:G("W_now_"+s)/G("g")}),
    ["bx_"+s]:()=>({formula:"w<sub>ruler</sub> + column · w<sub>col</sub> + w<sub>col</sub>/2"+(RTL?" (the Arabic page puts cotton on the right-hand start)":""),inputs:[I("column",colOf(s),"",0),I("w<sub>col</sub>",G("col_w"),"css px",3)],value:G("ruler_px")+colOf(s)*G("col_w")+G("col_w")/2}),
    ["shift_"+s]:()=>({formula:"(G − 1) · y<sub>p</sub>",inputs:[I("G",G("gain"),"",0),I("y<sub>p</sub>",d.yp[G("i_now")],"m",9)],value:(G("gain")-1)*d.yp[G("i_now")]}),
    ["plate_px_"+s]:()=>({formula:"y<sub>bottom</sub> − ((G − 1) y<sub>p</sub> − y<sub>cam</sub>) · s",inputs:[I("y<sub>bottom</sub>",G("bottom_px"),"css px",1),I("(G − 1) y<sub>p</sub>",G("shift_"+s),"m",9),I("y<sub>cam</sub>",G("cam_y"),"m"),I("s",G("sc"),"px/m",4)],value:G("bottom_px")-(G("shift_"+s)-G("cam_y"))*G("sc")}),
    ["needle_"+s]:()=>({formula:"−225° + 270° √(max(0, F)/F<sub>FS</sub>)",inputs:[I("F",G("F_now_"+s),"N",3),I("F<sub>FS</sub>",G("gauge_FS"),"N",0)],value:-225+270*Math.sqrt(Math.max(0,Math.min(G("F_now_"+s),FS))/G("gauge_FS"))}),
    ["peakneedle_"+s]:()=>({formula:"−225° + 270° √(F<sub>peak</sub>/F<sub>FS</sub>)",inputs:[I("F<sub>peak</sub>",G("Fmax_now_"+s),"N",3),I("F<sub>FS</sub>",G("gauge_FS"),"N",0)],value:-225+270*Math.sqrt(Math.max(0,Math.min(G("Fmax_now_"+s),FS))/G("gauge_FS"))})
  });
  for(const q of ["x","y","u","v"])check["ck_"+q+"_"+s]=idx=>{const r=replayCk(s,Math.floor(idx/N));return {formula:howRerun(r,s),inputs:[I("c",Math.floor(idx/N),"",0),I("i",idx%N,"",0)],value:r.b[q][idx%N]}};
}
Object.assign(check,{
  alpha_iron:()=>({formula:"αr<sub>0</sub> / a",inputs:[I("αr<sub>0</sub>",G("ar0"),"",2),I("a",G("a_iron"),"m",3)],value:G("ar0")/G("a_iron")}),
  D_iron:()=>({formula:"k / (2α²)",inputs:[I("k",G("k_iron"),"N/m",0),I("α",G("alpha_iron"),"1/m",4)],value:G("k_iron")/(2*G("alpha_iron")*G("alpha_iron"))}),
  nj_cot:fromBuild("cot",b=>b.nj,"junctions"),ntri_cot:fromBuild("cot",b=>b.ntri,"bending joints"),
  aj_cot:()=>({formula:"k<sub>j</sub> / (4F<sub>j</sub>)",inputs:[I("k<sub>j</sub>",G("kj"),"N/m",0),I("F<sub>j</sub>",G("Fj"),"N",1)],value:G("kj")/(4*G("Fj"))}),
  Dj_cot:()=>({formula:"2F<sub>j</sub> / α<sub>j</sub>",inputs:[I("F<sub>j</sub>",G("Fj"),"N",1),I("α<sub>j</sub>",G("aj_cot"),"1/m",4)],value:2*G("Fj")/G("aj_cot")}),
  t_star:()=>({formula:"√(2h/g)",inputs:[I("h",G("h"),"m",1),I("g",G("g"),"m/s²",2)],value:Math.sqrt(2*G("h")/G("g"))}),
  v_star:()=>({formula:"√(2gh)",inputs:[I("h",G("h"),"m",1),I("g",G("g"),"m/s²",2)],value:Math.sqrt(2*G("g")*G("h"))}),
  Mg:()=>({formula:"M g",inputs:[I("M",G("M"),"kg",3),I("g",G("g"),"m/s²",2)],value:G("M")*G("g")}),
  CK:()=>({formula:"the constant CK in the page",inputs:[],value:CK}),NF:()=>({formula:"the constant NF in the page",inputs:[],value:NF}),
  steps:()=>({formula:"steps<sub>n</sub> at the last computed sample",inputs:[I("n<sub>done</sub>",G("computed"),"",0)],value:G("nstep")[G("computed")-1]}),
  done:()=>({formula:"n<sub>done</sub> = N<sub>s</sub>",inputs:[I("n<sub>done</sub>",G("computed"),"",0),I("N<sub>s</sub>",NF,"",0)],value:G("computed")===NF}),
  ts:n=>({formula:"n · 1 ms up to n = 2500, then 2.5 s + (n − 2500) · 2 ms",inputs:[I("n",n,"",0)],value:tOf(n)}),
  nstep:n=>({formula:"the sub-steps Δt/5 added up again until the model time reaches t<sub>n</sub> − 10<sup>−9</sup> s",inputs:[I("t<sub>n</sub>",G("ts")[n],"s",3)],value:recount()[n]}),
  ck_n:c=>({formula:"c · Δn<sub>ck</sub>",inputs:[I("c",c,"",0),I("Δn<sub>ck</sub>",CK,"",0)],value:c*CK}),
  ck_step:c=>({formula:"the frame steps counted again up to sample c · Δn<sub>ck</sub>",inputs:[I("c",c,"",0)],value:recount()[c*CK]}),
  type_cot:q=>({formula:"bond kind in a fresh build",inputs:[I("bond",q,"",0)],value:fresh("cot").type[q]}),
  fibre_cot:i=>({formula:"fibre of each bead in a fresh build",inputs:[I("bead",i,"",0)],value:fresh("cot").fib[i]}),
  i_now:()=>({formula:"nearest stored sample to t<sub>play</sub>, at most n<sub>done</sub> − 1",inputs:[I("t<sub>play</sub>",G("t_play"),"s",4)],value:Math.min(G("computed")-1,kOf(G("t_play")))}),
  t_now:()=>({formula:"t<sub>n</sub> at n = n<sub>now</sub>",inputs:[I("n<sub>now</sub>",G("i_now"),"",0)],value:G("ts")[G("i_now")]}),
  slow:()=>({formula:"the speed button that is pressed",inputs:[],value:+({s1:1,s4:4,s20:20})[(document.querySelector(".bar button.on:not(#drop)")||{}).id]}),
  W_px:()=>({formula:"width of the canvas on your screen",inputs:[],value:cv.getBoundingClientRect().width}),
  HS_px:()=>({formula:"430 if W < 640 css px, else 470",inputs:[I("W",G("W_px"),"css px",1)],value:G("W_px")<640?430:470}),
  H_px:()=>({formula:"H<sub>scene</sub> + 214 (the gauge strip)",inputs:[I("H<sub>scene</sub>",G("HS_px"),"css px",0)],value:G("HS_px")+214}),
  dpr:()=>({formula:"window.devicePixelRatio",inputs:[],value:devicePixelRatio||1}),
  ruler_px:()=>({formula:"the constant RULER",inputs:[],value:RULER}),gain:()=>({formula:"the constant GAIN",inputs:[],value:GAIN}),gauge_FS:()=>({formula:"the constant FS",inputs:[],value:FS}),
  top_px:()=>({formula:"the constant 40 in drawSim()",inputs:[],value:40}),
  bottom_px:()=>({formula:"H<sub>scene</sub> − 6",inputs:[I("H<sub>scene</sub>",G("HS_px"),"css px",0)],value:G("HS_px")-6}),
  col_w:()=>({formula:"(W − w<sub>ruler</sub> − 6) / 2",inputs:[I("W",G("W_px"),"css px",2),I("w<sub>ruler</sub>",G("ruler_px"),"css px",0)],value:(G("W_px")-G("ruler_px")-6)/2}),
  sc:()=>({formula:"min((y<sub>bottom</sub> − y<sub>top</sub>) / 6.6 m, w<sub>col</sub> / 3.3 m)",inputs:[I("y<sub>bottom</sub>",G("bottom_px"),"css px",1),I("y<sub>top</sub>",G("top_px"),"css px",0),I("w<sub>col</sub>",G("col_w"),"css px",3)],value:Math.min((G("bottom_px")-G("top_px"))/6.6,G("col_w")/3.3)}),
  view_m:()=>({formula:"(y<sub>bottom</sub> − y<sub>top</sub>) / s",inputs:[I("s",G("sc"),"px/m",4)],value:(G("bottom_px")-G("top_px"))/G("sc")}),
  cam_y:()=>{const n=G("i_now"),y=D.iron.y,N=D.iron.N;let lo=Infinity;for(let i=0;i<N;i++)lo=Math.min(lo,y[n*N+i]);
    return {formula:"max(−2.3 m, lowest stored iron y<sub>i</sub> at n<sub>now</sub> − 0.42 h<sub>view</sub>)",inputs:[I("min y<sub>i</sub>",lo,"m"),I("h<sub>view</sub>",G("view_m"),"m",4)],value:Math.max(-2.3,lo-0.42*G("view_m"))}},
  gauge_R:()=>({formula:"min(58, 0.3 w<sub>col</sub>)",inputs:[I("w<sub>col</sub>",G("col_w"),"css px",3)],value:Math.min(58,G("col_w")*0.3)}),
  gauge_cy:()=>({formula:"H<sub>scene</sub> + 8 + R<sub>g</sub> + 8",inputs:[I("H<sub>scene</sub>",G("HS_px"),"css px",0),I("R<sub>g</sub>",G("gauge_R"),"css px",3)],value:G("HS_px")+8+G("gauge_R")+8})
});

const drawn={};
for(const s of BALLS)Object.assign(drawn,{
  ["x_"+s]:idx=>partDrawn(s,idx),["y_"+s]:idx=>partDrawn(s,idx),["sp_"+s]:idx=>partDrawn(s,idx),
  ["plate_px_"+s]:()=>plateRow(s),["yp_now_"+s]:()=>plateRow(s),["shift_"+s]:()=>plateRow(s),
  ["needle_"+s]:()=>needleBack(s),["F_now_"+s]:()=>needleBack(s),["peakneedle_"+s]:()=>peakBack(s),["Fmax_now_"+s]:()=>peakBack(s),
  ["F_"+s]:n=>curveBack(s,n),["yp_"+s]:n=>n===ds.get("i_now")?plateRow(s):{what:"plate at sample "+n,drawn:"not drawn now",expected:"drawn only while the playback shows sample "+n,ok:null,note:""}
});

// ---- what lies at a point of the figure ----
function probe(x,y){
  if(!(G("sc")>0))return null;
  const R=G("gauge_R"),gcy=G("gauge_cy"),HSp=G("HS_px"),k=G("i_now");
  for(const s of BALLS){const bx=G("bx_"+s),pwid=Math.min(G("col_w")-12,170),py=HSp+8+2*R+22,pw=Math.min(2.9*G("sc"),G("col_w")-14),pt=G("plate_px_"+s);
    if(Math.hypot(x-bx,y-gcy)<=R+5)return {what:"scale",s,part:"gauge"};
    if(Math.abs(x-bx)<=pwid/2&&y>=py&&y<=py+62)return {what:"scale",s,part:"panel"};
    if(Math.abs(x-bx)<=pw/2&&y>=pt-2&&y<=pt+12&&pt<G("bottom_px")+20)return {what:"scale",s,part:"plate"}}
  if(y<G("top_px")||y>G("bottom_px")+2)return null;
  let best=null,bd=9;
  for(const s of BALLS)for(let i=0;i<D[s].N;i++){const p=partXY(s,k,i),dd=Math.hypot(x-p.x,y-p.y);if(dd<bd){bd=dd;best={what:"part",s,i}}}
  return best;
}
function inspect(ref){
  const n=G("i_now"),s=ref.s,d=D[s],ts=G("ts");
  if(ref.what==="part"){const N=d.N,i=ref.i,idx=n*N+i,rows=[["n",n,"","i_now",null],["t",ts[n],"s","ts",n],["x",d.x[idx],"m","x_"+s,idx],["y",d.y[idx],"m","y_"+s,idx],["|v|",d.sp[idx],"m/s","sp_"+s,idx]];
    if(s==="cot")rows.push(["fibre",G("fibre_cot")[i],"","fibre_cot",i]);
    return {title:s==="iron"?"iron atom "+i:"cotton bead "+i+", fibre "+G("fibre_cot")[i],at:partXY(s,n,i),rows}}
  const bx=G("bx_"+s),R=G("gauge_R"),at=ref.part==="gauge"?{x:bx,y:G("gauge_cy")}:ref.part==="panel"?{x:bx,y:G("HS_px")+8+2*R+22+31}:{x:bx,y:G("plate_px_"+s)+5};
  return {title:"the scale under the "+NAME[s]+" ball ("+(ref.part==="gauge"?"its gauge":ref.part==="panel"?"its digital panel":"the plate")+")",at,
    rows:[["t",G("t_now"),"s","t_now",null],["F",G("F_now_"+s),"N","F_now_"+s,null],["F<sub>peak</sub>",G("Fmax_now_"+s),"N","Fmax_now_"+s,null],["W",G("W_now_"+s),"N","W_now_"+s,null],["y<sub>p</sub>",G("yp_now_"+s),"m","yp_now_"+s,null],["θ<sub>needle</sub>",G("needle_"+s),"°","needle_"+s,null]]};
}
function locate(name,idx){
  const m=/^(x|y|sp)_(iron|cot)$/.exec(name);
  if(m){const N=D[m[2]].N;return Math.floor(idx/N)===G("i_now")?partXY(m[2],G("i_now"),idx%N):null}
  const q=/^(F|Fmax|W|yp|vp)_(iron|cot)$/.exec(name);
  if(q&&idx===G("i_now"))return q[1]==="yp"||q[1]==="vp"?{x:G("bx_"+q[2]),y:G("plate_px_"+q[2])+5}:{x:G("bx_"+q[2]),y:G("gauge_cy")};
  const r=/^(F_now|Fmax_now|needle|peakneedle|W_now|kgpeak_now|kgw_now)_(iron|cot)$/.exec(name);if(r)return {x:G("bx_"+r[2]),y:G("gauge_cy")};
  const p=/^(yp_now|plate_px|shift)_(iron|cot)$/.exec(name);if(p)return {x:G("bx_"+p[2]),y:G("plate_px_"+p[2])+5};
  return null;
}

const ball=s=>["x_"+s,"y_"+s,"sp_"+s,"yp_"+s,"vp_"+s,"F_"+s,"Fmax_"+s,"W_"+s,"KE_"+s,"PE_"+s,"El_"+s,"Eh_"+s,"Qb_"+s,"Qh_"+s,"Qa_"+s,"Ein_"+s,"Esum_"+s,"books_"+s];
const cks=s=>["ck_x_"+s,"ck_y_"+s,"ck_u_"+s,"ck_v_"+s,"ck_t_"+s,"ck_yp_"+s,"ck_vp_"+s,"ck_Fmax_"+s,"ck_Qb_"+s,"ck_Qh_"+s,"ck_Qa_"+s,"ck_ti_"+s,"ck_alive_"+s];
const both=f=>BALLS.map(f).flat();
Sim.data={
  ds:ds,kicker:"Portfolios 04 · data",file:"impact-iron-cotton",
  playing:()=>playing,play:startDrop,
  groups:[
    {title:"Parameters",note:"the constants of the model, P",vars:Object.keys(PMAP)},
    {title:"Derived physics",note:"computed once, when the two balls are built",vars:["N_iron","N_cot","m_iron","m_cot","nbond_iron","nbond_cot","alpha_iron","D_iron","nj_cot","ntri_cot","aj_cot","Dj_cot","kc_iron","cc_iron","kc_cot","cc_cot","y00_iron","y00_cot","E0_iron","E0_cot","t_star","v_star","Mg","A_iron","A_cot","vt_iron","vt_cot","t_air_iron","t_air_cot","v_air_iron","v_air_cot"]},
    {title:"Solver",note:"how the run is computed and stored",vars:["NF","CK","computed","steps","compute_ms","done"]},
    {title:"Results",note:"written when the run is complete",vars:both(s=>["t_touch_"+s,"Fpeak_"+s,"W_end_"+s,"w_rel_"+s,"books_max_"+s])},
    {title:"Stored run",note:"one row per stored sample: every 1 ms to 2.5 s, every 2 ms to 9 s",vars:["ts","nstep"].concat(ball("iron"),ball("cot"))},
    {title:"Shape of the balls",note:"bonds and fibres, made once",vars:["bi_iron","bj_iron","l0_iron","bi_cot","bj_cot","l0_cot","type_cot","fibre_cot"]},
    {title:"Checkpoints",note:"the full state every 125 samples, so Check can rerun the model to any sample in under a second",vars:["ck_n","ck_step"].concat(cks("iron"),cks("cot"))},
    {title:"Playback",note:"the sample on screen now",vars:["t_play","i_now","t_now","slow","playing"].concat(both(s=>["F_now_"+s,"Fmax_now_"+s,"W_now_"+s,"kgpeak_now_"+s,"kgw_now_"+s,"yp_now_"+s,"KE_now_"+s,"books_now_"+s]))},
    {title:"Drawing",note:"how stored values become pixels",vars:["W_px","H_px","HS_px","dpr","ruler_px","top_px","bottom_px","col_w","sc","view_m","cam_y","gain","gauge_R","gauge_cy","gauge_FS"].concat(both(s=>["bx_"+s,"shift_"+s,"plate_px_"+s,"needle_"+s,"peakneedle_"+s]))}
  ],
  rowLabel:{n:j=>"t = "+G("ts")[j].toFixed(3)+" s",c:j=>"n = "+j*CK},
  probe,inspect,locate,check,drawn,
  round:{time:"t_play",label:()=>"one drop, t = 0 to 9 s of the stored run",length:()=>P.tmax,
    columns:both(s=>["F_now_"+s,"yp_now_"+s,"KE_now_"+s]),point:()=>({what:"scale",s:"iron",part:"gauge"}),
    blocked:()=>playing&&tPlay>0.02?"a drop is under way; when it ends, Record starts a new one from t = 0":null},
  about:"Nothing here is computed while you watch. The drop is computed once when the page opens and every sample is stored: every 1 ms up to 2.5 s, every 2 ms after. "+
    "Each frame draws the stored sample nearest to the playback time, without interpolation. Positions and speeds of the 91 atoms and 612 beads are stored as float32 to keep the store near 50 MB, so their checks agree to about seven figures; everything else is float64. "+
    "The plate's travel is drawn G = 10 times larger than computed, and the ball resting on it is shifted with it by (G − 1) y<sub>p</sub>, so you can see the head give; the scale reading uses the true travel. "+
    "The camera follows the lowest iron atom, for both columns. Bond colours (wine squeezed, blue stretched, saturated at 0.7 % strain for iron; cotton fibres darken above 1.2 % squeeze) are worked out at drawing time from the stored positions and are not stored themselves. "+
    "The cotton fibres are drawn as smooth curves through the beads, so a fibre passes near, not exactly through, each bead. The gauges have a square-root dial with full scale 700 N; the weight is the mean reading from 4 s on and appears on the panel from 6.5 s. "+
    "A checkpoint of the full state every 125 samples lets Check rerun the model from the one before any sample; the first checkpoint is itself checked against a fresh build stepped from t = 0."
};
