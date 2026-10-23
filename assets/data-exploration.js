/* Curated case collection. Generated evidence lives in data/ and assets/exploration-previews/. */
'use strict';
const $ = s => document.querySelector(s);
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt = value => value == null || !Number.isFinite(Number(value)) ? '—' : Number(value).toLocaleString(undefined,{maximumFractionDigits:3});
const colab = 'https://colab.research.google.com/github/cmg777/intro2causal/blob/main/notebooks_colab/';
const chapterInfo = {
  1:['Randomized trials','Health, insurance, and the comparisons we trust.'],
  2:['Regression','Six worlds to explore selection and confounding.'],
  3:['Instrumental variables','When an assignment and an action are different.'],
  4:['Regression discontinuity','A birthday creates a boundary.'],
  5:['Differences in differences','Follow places and policies through time.'],
  6:['The wages of schooling','Different comparisons. One persistent question.']
};
const keyLabels = {health:'Self-reported health',insurance:'Insurance coverage',education:'Years of education',family_income:'Family income',weight:'Survey weight',plan_type:'Insurance plan',age:'Age',health_index:'Health index',visits:'Medical visits',total_expenses:'Annual spending',admissions:'Hospital admissions',blood_pressure:'Blood pressure',cholesterol:'Cholesterol',assigned:'Assigned response',delivered:'Delivered response',agecell:'Actual age',all:'All-cause mortality',mva:'Motor-vehicle mortality',suicide:'Suicide mortality',over21:'Age-21 threshold',year:'Year',bib6:'6th-district banks',bib8:'8th-district banks',counterfactual:'Constructed path',state:'State',dtype:'Cause of death',mrate:'Death rate',legal:'Legal access',s:'Schooling',lnw:'Log weekly earnings',qob:'Birth quarter',yob:'Birth year',educ:'Schooling',lwage:'Log wage',first:'One record per pair',deduc:'Schooling difference',dlwage:'Log-wage difference',indEduc:'Cell mean schooling',lnwkwage:'Cell mean log wages',cl7:'7-year requirement',cl8:'8-year requirement',cl9:'9+ year requirement',minscore:'Exam score',receivehsd:'Diploma receipt',avgearnings:'Later earnings',n:'Students per bin',schooling:'Schooling',earnings:'Log earnings',ability:'Ability',occupation:'Occupation',scholarship:'Scholarship offer',treated:'Reform group',post:'Reform period',avg_schooling:'Mean schooling',avg_earnings:'Mean log earnings'};
let cases=[], summaries=new Map(), simulations=[], observer, plotlyPromise;
const previewCache=new Map();
function loadPlotly(){
  if(window.Plotly)return Promise.resolve(window.Plotly);
  if(!plotlyPromise)plotlyPromise=new Promise((resolve,reject)=>{
    const s=document.createElement('script');s.src='assets/vendor/plotly.min.js';s.onload=()=>resolve(window.Plotly);s.onerror=()=>{plotlyPromise=null;reject(Error('Chart library unavailable'))};document.head.append(s);
  });
  return plotlyPromise;
}
async function chartData(file){
  if(!previewCache.has(file)){
    const r=await fetch(file);if(!r.ok)throw Error('Preview unavailable');previewCache.set(file,await r.json());
  }
  return structuredClone(previewCache.get(file));
}
function chartTheme(){
  const css=getComputedStyle(document.documentElement);
  return {paper_bgcolor:'rgba(0,0,0,0)',plot_bgcolor:'rgba(0,0,0,0)',font:{family:'Inter, system-ui, sans-serif',size:11,color:css.getPropertyValue('--text').trim()},colorway:document.documentElement.classList.contains('light')?['#2563eb','#7c3aed','#059669','#64748b']:['#38bdf8','#a78bfa','#34d399','#94a3b8']};
}
async function drawChart(element,file,hero=false){
  if(element.dataset.loading || element.dataset.rendered)return;
  element.dataset.loading='true';
  try{
    const [P,spec]=await Promise.all([loadPlotly(),chartData(file)]);
    if(!element.isConnected)return;
    const theme=chartTheme();const light=document.documentElement.classList.contains('light');
    const remap={'#2563eb':theme.colorway[0],'#7c3aed':theme.colorway[1],'#059669':theme.colorway[2],'#64748b':theme.colorway[3]};
    spec.data.forEach(t=>{
      if(t.marker && typeof t.marker.color==='string' && remap[t.marker.color])t.marker.color=remap[t.marker.color];
      if(t.line && remap[t.line.color])t.line.color=remap[t.line.color];
      // SVG previews avoid exhausting browser WebGL contexts across many cases.
      if(t.type==='scattergl')t.type='scatter';
    });
    const layout={...spec.layout,...theme,autosize:true,height:hero?240:element.clientHeight,margin:{l:54,r:15,t:20,b:85},legend:{orientation:'h',x:0,y:-.25,font:{size:10},title:{text:''}},hoverlabel:{bgcolor:light?'#fff':'#1e293b',font:{color:light?'#1e293b':'#e2e8f0'}}};
    for(const axis of ['xaxis','yaxis'])layout[axis]={...layout[axis],gridcolor:light?'#e2e8f0':'#334155',zerolinecolor:light?'#cbd5e1':'#475569',automargin:true,title:{...layout[axis]?.title,font:{size:11}}};
    if(hero){layout.margin={l:42,r:12,t:8,b:48};layout.xaxis.title={text:''};layout.yaxis.title={text:''};layout.legend={orientation:'h',x:0,y:-.2,font:{size:9}};}
    element.replaceChildren();
    await P.newPlot(element,spec.data,layout,{responsive:true,displaylogo:false,scrollZoom:false,modeBarButtonsToRemove:['lasso2d','select2d','toImage']});
    element.dataset.rendered='true';element.dataset.file=file;element.dataset.hero=String(hero);element.removeAttribute('role');
  }catch(e){element.innerHTML='<p class="chart-loading">Preview unavailable. The notebook and readable values below are still available.</p>';}finally{delete element.dataset.loading;}
}
function profiles(fields){
  const headers=['Variable','Meaning & role','Type','Available N','Missing %','Mean','SD','Median','Min','Max','Distribution'];
  return `<div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable variable dictionary"><table><thead><tr>${headers.map((h,i)=>`<th scope="col" aria-sort="none"><button data-sort="${i}" type="button" aria-label="Sort by ${h}">${h} ↕</button></th>`).join('')}</tr></thead><tbody>${fields.map(f=>{
    const stats=f.type==='numeric'?f.stats:null;
    let distribution='—';
    if(f.categories){const count=f.categories.length;const items=f.categories.map(c=>`<div class="category-row">${esc(c.value)} · ${fmt(c.count)} (${fmt(c.share*100)}%)<div class="mini-bar" aria-hidden="true"><i style="width:${Math.max(1,c.share*100)}%"></i></div></div>`);distribution=items.slice(0,5).join('')+(count>5?`<details><summary>All ${count} values</summary>${items.slice(5).join('')}</details>`:'');}
    else if(f.bins){const top=Math.max(...f.bins);distribution=`<div class="mini-hist" role="img" aria-label="Histogram with 12 equal-width bins; counts ${f.bins.join(', ')}">${f.bins.map(n=>`<i style="height:${Math.max(2,n/top*100)}%" title="${n} rows"></i>`).join('')}</div><small>12 equal-width bins</small>`;}
    return `<tr><td><code>${esc(f.name)}</code></td><td class="definition">${esc(f.meaning)}<br><small>${esc(f.role)}</small></td><td><span class="type-badge">${esc(f.type)}</span></td><td>${fmt(f.n)}</td><td>${fmt(f.missingPct)}%</td>${['mean','sd','median','min','max'].map(k=>`<td>${fmt(stats?.[k])}</td>`).join('')}<td class="categories">${distribution}</td></tr>`;
  }).join('')}</tbody></table></div>`;
}
function readablePreview(c){return `<details class="evidence-table"><summary>Read the preview as a table</summary><p>${esc(c.preview.tableNote)}</p><table><caption>${esc(c.preview.question)}</caption><thead><tr><th scope="col">Group / observation</th><th scope="col">${esc(c.preview.valueLabel)}</th></tr></thead><tbody>${c.preview.table.map(r=>`<tr><td>${esc(r[0])}</td><td>${fmt(r[1])}</td></tr>`).join('')}</tbody></table></details>`;}
function article(c,fields){
  const d=summaries.get(c.id);const kind=c.kind.startsWith('Simulated')?'Teaching simulation':'Empirical case study';
  const source=c.sourceUrl?`<a href="${esc(c.sourceUrl)}">${esc(c.source)} ↗</a>`:`<span>${esc(c.source)} · Citation only</span>`;
  return `<article class="case" id="${esc(c.id)}" aria-labelledby="title-${esc(c.id)}"><div class="case-inner"><div class="case-topline"><span class="case-kicker">${kind} / Chapter ${String(c.chapter).padStart(2,'0')}</span><a class="case-id" href="#${esc(c.id)}" aria-label="Permanent link to ${esc(c.title)}">${esc(c.file.split('/')[1])} ↗</a></div><h3 id="title-${esc(c.id)}">${esc(c.title)}</h3><div class="case-grid"><div class="case-copy"><p class="research-question"><span class="label">Research question</span>${esc(c.question)}</p><div class="key-variables" aria-label="Key variables">${c.keys.map(k=>`<span title="${esc(k+': '+c.definitions[k])}">${esc(keyLabels[k]||k)}</span>`).join('')}</div><p class="case-story">${esc(c.story)}</p><p class="takeaway"><strong>You will investigate</strong>${esc(c.takeaway)}</p></div><figure class="case-visual"><h4>${esc(c.preview.question)}</h4><p class="chart-hint">A first look · hover to explore, double-click to reset</p><div class="preview-chart" data-preview="${esc(c.preview.file)}" role="img" aria-label="${esc(c.preview.question)}"><span class="chart-loading">Preparing the evidence…</span></div><figcaption>${esc(c.preview.caption)}</figcaption>${readablePreview(c)}</figure></div><div class="case-bottom"><div><div class="case-facts"><span><strong>${fmt(c.rows)}</strong> rows</span><span><strong>${c.columns}</strong> variables</span><span><strong>30–45</strong> minutes</span><span>Beginner · guided</span></div><p class="unit-note"><strong>One row:</strong> ${esc(c.unit)}</p></div><a class="button primary colab-link" href="${colab}${esc(c.notebook)}" aria-label="Open ${esc(c.title)} in Colab">Open in Colab <span aria-hidden="true">↗</span></a></div></div><div class="case-reference"><details class="dictionary"><summary>Inside the data · variable dictionary & source notes <span>${fields.length} variables</span></summary><div class="dictionary-body"><p class="reference-note">${esc(c.caution)}</p><p class="profile-meta">Profiles use the full stored CSV with equal row weights. SD is the sample standard deviation. Numeric summaries are hidden for category codes and identifiers. Filters affect visible fields, not these calculations.</p>${profiles(fields)}<p class="reference-note" style="margin-top:20px"><strong>Preparation and provenance.</strong> ${esc(d.provenance)}</p><div class="reference-links"><a href="data/${esc(c.file)}" download>Download CSV ↓</a><a href="${esc(c.guide)}">Read the chapter ↗</a><a href="notebooks_colab/${esc(c.notebook)}" download>Download notebook ↓</a>${source}</div></div></details></div></article>`;
}
function simulationArticle(){
  const names=['Baseline selection','No treatment effect','Stronger selection','Add family income','Reverse selection','Three confounders'];
  return `<article class="case simulation" id="chapter-2-simulations"><div class="case-inner"><div class="case-topline"><span class="case-kicker">A simulation lab / Chapter 02</span><span class="tiny-tag">Six worlds. One question.</span></div><h3>One earnings gap. Six different stories.</h3><div class="simulation-grid"><div class="simulation-story"><p class="research-question"><span class="label">Research question</span>Can a school appear to raise earnings even when its true effect is zero?</p><div class="key-variables"><span>School attendance</span><span>Ability</span><span>Annual earnings</span></div><p>Imagine comparing earnings of people who attended private and other schools. Attendance may reflect ability, family resources, and motivation—all of which could also affect earnings. In real observational data, we do not know the true school effect. In this lab, you construct six worlds and choose that effect yourself. Each world contains 1,000 simulated students and changes a specific feature of selection or confounding. The scenarios follow the Chapter 2 exercises, including a world with no school effect and a world where selection runs in the opposite direction. None is a real student dataset, and none randomizes school attendance. Comparing the patterns with the known effects gives you something observational data cannot: a direct view of why an earnings gap and a causal effect may be different.</p><p class="takeaway"><strong>You will investigate</strong>Compare observed gaps with known effects, then uncover the role of selection.</p></div><div><div class="worlds">${names.map((n,i)=>`<div class="world"><span>WORLD 0${i+1}</span><strong>${n}</strong><small>Known school effect: ${i===1?'$0':'$5,000'}</small></div>`).join('')}</div><p class="simulation-note">Generated data · seed 42 reset in each world · no survey weights. Earnings here are in simulated dollars, not logs.</p><details class="evidence-table"><summary>Preview the observed and known differences</summary><table><thead><tr><th>Scenario</th><th>Observed gap ($)</th><th>Known effect ($)</th></tr></thead><tbody>${simulations.map(s=>`<tr><td>${esc(s.scenario)}</td><td>${fmt(s['Observed gap'])}</td><td>${fmt(s['Known effect'])}</td></tr>`).join('')}</tbody></table></details></div></div><div class="case-bottom"><div class="case-facts"><span><strong>6</strong> scenarios</span><span><strong>1,000</strong> students each</span><span><strong>30–45</strong> minutes</span><span>Beginner · guided</span></div><a class="button primary colab-link" href="${colab}explore-chapter-2-simulations.ipynb">Open lab in Colab <span aria-hidden="true">↗</span></a></div></div></article>`;
}
function matches(c,q,type){
  const d=summaries.get(c.id);const caseText=[c.title,c.question,c.story,c.takeaway,c.file,c.source].join(' ').toLowerCase();
  const caseMatch=!q||caseText.includes(q);
  const fields=d.fields.filter(f=>(type==='all'||f.type===type)&&(caseMatch||[f.name,f.meaning,f.role].join(' ').toLowerCase().includes(q)));
  return fields;
}
function render(){
  if(!cases.length)return;
  if(observer)observer.disconnect();
  if(window.Plotly)document.querySelectorAll('.preview-chart[data-rendered]').forEach(e=>Plotly.purge(e));
  const q=$('#search').value.trim().toLowerCase(),chapter=$('#chapter').value,type=$('#type').value;
  const visible=cases.map(c=>({c,fields:matches(c,q,type)})).filter(x=>(chapter==='all'||String(x.c.chapter)===chapter)&&x.fields.length);
  const simulationText='chapter 2 regression simulation private school earnings ability income motivation selection confounding bias zero effect reverse';
  const showSimulation=(chapter==='all'||chapter==='2')&&(!q||simulationText.includes(q))&&type!=='identifier';
  $('#status').textContent=`${visible.length} of 15 data stories${showSimulation?' + 1 simulation lab':''} · ${visible.reduce((n,x)=>n+x.fields.length,0)} dictionary variables shown`;
  const chapters=[...new Set(visible.map(x=>x.c.chapter).concat(showSimulation?[2]:[]))].sort();
  $('#chapter-nav').innerHTML=chapters.map(n=>`<a href="#chapter-${n}">${String(n).padStart(2,'0')} · ${chapterInfo[n][0]}</a>`).join('');
  $('#datasets').innerHTML=chapters.length?chapters.map(n=>`<section class="chapter-section" id="chapter-${n}" aria-labelledby="chapter-title-${n}"><header class="chapter-heading"><span class="chapter-number" aria-hidden="true">${String(n).padStart(2,'0')}</span><div><h2 id="chapter-title-${n}">${chapterInfo[n][0]}</h2><p>${chapterInfo[n][1]}</p></div></header>${n===2?simulationArticle():visible.filter(x=>x.c.chapter===n).map(x=>article(x.c,x.fields)).join('')}</section>`).join(''):'<div class="empty-state"><h3>No cases match those filters.</h3><p>Try a broader word or explore all chapters.</p><button id="empty-reset">Show all cases</button></div>';
  if($('#empty-reset'))$('#empty-reset').onclick=reset;
  observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){drawChart(entry.target,entry.target.dataset.preview);observer.unobserve(entry.target);}}),{rootMargin:'350px'});
  document.querySelectorAll('[data-preview]').forEach(e=>observer.observe(e));
  document.querySelectorAll('[data-sort]').forEach(button=>button.onclick=()=>{
    const th=button.closest('th'),table=button.closest('table'),body=table.tBodies[0],i=+button.dataset.sort;
    const ascending=th.getAttribute('aria-sort')!=='ascending';
    table.querySelectorAll('th').forEach(t=>t.setAttribute('aria-sort','none'));th.setAttribute('aria-sort',ascending?'ascending':'descending');
    [...body.rows].sort((a,b)=>a.cells[i].innerText.localeCompare(b.cells[i].innerText,undefined,{numeric:true})*(ascending?1:-1)).forEach(row=>body.append(row));
  });
}
function reset(){$('#search').value='';$('#chapter').value='all';$('#type').value='all';render();}
function scrollToHash(){
  if(!location.hash)return;
  let id;try{id=decodeURIComponent(location.hash.slice(1))}catch(e){return}
  let target=document.getElementById(id);
  if(!target&&(cases.some(c=>c.id===id)||id==='chapter-2-simulations'||/^chapter-[1-6]$/.test(id))){reset();target=document.getElementById(id);}
  if(target)target.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'});
}
document.addEventListener('site:themechange',()=>{
  document.querySelectorAll('[data-rendered]').forEach(el=>{const file=el.dataset.file,hero=el.dataset.hero==='true';Plotly.purge(el);delete el.dataset.rendered;drawChart(el,file,hero);});
});
['search','chapter','type'].forEach(id=>$('#'+id).addEventListener(id==='search'?'input':'change',render));
$('#reset').onclick=reset;$('#expand').onclick=()=>document.querySelectorAll('.dictionary').forEach(d=>d.open=true);$('#collapse').onclick=()=>document.querySelectorAll('.dictionary').forEach(d=>d.open=false);$('#print').onclick=()=>window.print();
window.addEventListener('hashchange',scrollToHash);
Promise.all(['data/exploration-cases.json','data/dictionary-summary.json'].map(async url=>{const r=await fetch(url);if(!r.ok)throw Error(url);return r.json()})).then(([content,profiles])=>{
  cases=content.cases;simulations=content.simulations;summaries=new Map(profiles.datasets.map(d=>[d.id,d]));
  for(const [n,info] of Object.entries(chapterInfo))$('#chapter').insertAdjacentHTML('beforeend',`<option value="${n}">Chapter ${n}: ${info[0]}</option>`);
  render();drawChart($('#hero-chart'),'assets/exploration-previews/banks_clean.json',true);requestAnimationFrame(scrollToHash);
}).catch(()=>{$('#status').textContent='The case collection could not load.';$('#datasets').innerHTML='<div class="empty-state"><h3>The collection is temporarily unavailable.</h3><p>Please reload the page, or browse the <a href="https://github.com/cmg777/intro2causal/tree/main/notebooks_colab">Colab notebook files</a>.</p></div>';});
