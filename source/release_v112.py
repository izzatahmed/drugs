"""Selected factual summaries of the supplied fifth-edition handbook (2018).

Edition-based advice is identified at the point of use. Existing label-based
regimens are not overwritten. No unparameterised continuous-therapy table is
converted into a universal modern CRRT prescription.
"""
from pathlib import Path
import json,hashlib
R=Path(__file__).parent;D=R/'dist';DATE='2026-10-30';VERSION='0.11.2'
data=json.loads((D/'database.json').read_text());assert data['version']=='0.11.1'
drugs={d['id']:d for d in data['drugs']};old=json.loads(json.dumps(drugs));sources={s['id']:s for s in data['sources']}
facts=json.loads((R/'book_facts_v112.json').read_text());F={f['id']:f for f in facts}
BOOK=next(s['url'] for s in data['sources'] if s['id'].startswith('rdh5-v11-'))
EDITION='Handbook 5th ed · 2018 (copyright 2019)'
# Short selected-regimen references, not a reproduction of full monographs.
# None means that no universal numeric adult regimen is selected.
reference={
 'acetazolamide':None,'adenosine':'PSVT: 6 mg rapid IV with ECG monitoring, then 12 mg after 1–2 min if needed; a further 12 mg may follow after another 1–2 min',
 'amiodarone':'Selected oral maintenance reference: 200 mg daily or the lowest effective dose; initiation/loading is separate',
 'dobutamine':'Selected monitored IV infusion reference: 2.5–10 micrograms/kg/min, titrated to haemodynamic response',
 'dopamine':'Selected initial monitored IV infusion: 2–5 micrograms/kg/min; titrate for the haemodynamic indication',
 'esmolol':'Selected IV maintenance reference: 50–200 micrograms/kg/min; use the product-specific loading/titration protocol',
 'flecainide':None,'isosorbide-dinitrate':'Selected oral angina reference: total 30–120 mg/day in divided doses',
 'isosorbide-mononitrate':'Selected oral reference: total 20–120 mg/day in divided doses; match release formulation',
 'ivabradine':'Selected oral reference: 2.5–7.5 mg twice daily, adjusted to heart rate and tolerability',
 'metolazone':None,'midodrine':None,'minoxidil-systemic':None,'nicardipine':None,
 'nitroglycerin':'Selected monitored IV reference: 10–200 micrograms/min, titrated to response; other formulations require their own regimen',
 'prazosin':None,'propafenone':None,'terazosin':'Initial oral reference: 1 mg at bedtime, then indication-specific titration',
 'verapamil':None,'carbimazole':'Selected oral reference: total 5–60 mg/day, titrated to thyroid response',
 'dexamethasone':None,'fludrocortisone':'Selected oral replacement reference: 50–300 micrograms daily; individualise to clinical/electrolyte response',
 'hydrocortisone':'Selected oral replacement reference: total 20–30 mg/day in divided doses; stress-dose/IV regimens are separate',
 'levothyroxine':None,'liothyronine':None,'methylprednisolone':None,'prednisolone':None,'repaglinide':None,
 'vildagliptin':None,'alfacalcidol':'Selected reference: 0.25–1 microgram daily, adjusted to calcium/PTH response',
 'calcitriol':'Selected oral reference: begin 0.25 microgram daily or on alternate days; increase by 0.25 microgram every 2–4 weeks if indicated',
 'calcium-acetate':None,'cholecalciferol':None,'lanthanum-carbonate':'Selected oral phosphate-binder reference: 500–1,000 mg with each of three daily meals; handbook maximum total 3,750 mg/day',
 'paricalcitol':None,'sodium-bicarbonate':'Selected oral reference: 0.5–1.5 g three times daily; individualise to bicarbonate, sodium and volume status',
 'bisacodyl':'Selected oral constipation reference: 5–10 mg at night; rectal 10 mg is a separate option',
 'domperidone':None,'granisetron':'Selected chemotherapy oral reference: 1–2 mg before treatment, then total 2 mg/day in one or two doses during treatment',
 'hyoscine-butylbromide':'Selected oral IBS reference: 10 mg three times daily, increasing if required up to 20 mg four times daily',
 'prochlorperazine':'Selected oral antiemetic reference: 5–10 mg two or three times daily',
 'promethazine':'Selected oral reference: 25 mg at night; use the lowest tolerated dose',
 'ursodeoxycholic-acid':'Selected gallstone-dissolution reference: total 8–12 mg/kg/day in one or two doses; biliary-disease protocols differ',
 'acetylcysteine':'Selected oral mucolytic reference: 600 mg once daily; poisoning and inhaled protocols are separate',
 'aminophylline':None,'chlorphenamine':'Selected oral reference: 4 mg four to six times daily, maximum 24 mg/day; renal patients may tolerate less',
 'ipratropium':'Selected nebulised reference: 250–500 micrograms three or four times daily; inhaler strengths differ',
 'salbutamol-albuterol':'Selected nebulised airway reference: 2.5–5 mg four times daily, individualised to respiratory response',
 'theophylline':None,'terbutaline':None,'folic-acid':None,'clopidogrel':'Selected maintenance reference: 75 mg orally once daily; ACS/PCI loading and combination therapy are separate',
 'aprepitant':'Selected oral chemotherapy schedule: 125 mg on day 1, then 80 mg once daily on days 2 and 3',
 'palonosetron':'Selected chemotherapy reference: 250 micrograms IV once about 30 min before treatment OR 500 micrograms orally once about 60 min beforehand',
 'misoprostol':'Selected ulcer-prevention reference: 200 micrograms orally two to four times daily; reduce if not tolerated',
 'formoterol':None,'nystatin':'Select the oral-suspension or topical product regimen; do not use as treatment for systemic fungal infection',
 'hydroxychloroquine':None,'mesalazine':None,'sulfasalazine':None}
assert set(reference)==set(F)
notes={
 'acetazolamide':'The handbook reports manufacturer avoidance in severe renal failure and warns of acidosis and neurological toxicity in dialysis. Numeric GFR bands do not override a contraindication in the authorised product.',
 'adenosine':'Only monitored IV treatment of an appropriate supraventricular tachycardia is described. Dipyridamole increases effect; theophylline antagonises it. Do not treat the renal statement as an arrhythmia diagnosis or a stress-test protocol.',
 'amiodarone':'No renal loading or maintenance reduction in this edition. IV emergency algorithms, QT/electrolytes, interactions and organ monitoring require the relevant current protocol; historical resuscitation doses are not imported.',
 'dobutamine':'Use continuous haemodynamic/ECG monitoring; hypotension, arrhythmia and hypokalaemia require review. This is monitored inotropic support, not a kidney-function-based prescription.',
 'dopamine':'The handbook gives little support for a renal-protective effect. No AKI-prevention indication is created by this entry. Monitor haemodynamics, rhythm and infusion extravasation.',
 'esmolol':'Titrate to BP and heart rate under monitoring; review potassium in advanced CKD. Renal impairment and clearance of the metabolite do not select the loading protocol.',
 'flecainide':'Narrow therapeutic margin: monitor ECG and plasma levels in severe impairment and correct electrolytes. The oral starting dose and IV percentage are separate; do not interpret the initial dose as a universal maintenance dose.',
 'isosorbide-dinitrate':'Match indication, route and nitrate-free interval. Check hypotension and contraindicated PDE5-inhibitor/riociguat combinations; dialysis removal alone does not establish a supplement.',
 'isosorbide-mononitrate':'Match IR/MR formulation, response and nitrate-free interval. Avoid contraindicated PDE5-inhibitor/riociguat combinations; no automatic post-HD replacement is given.',
 'ivabradine':'The handbook cautions below GFR 15 because manufacturer data were lacking. Individualise eligibility, heart rate and interacting drugs; its historical ESRD use is not a current product authorisation.',
 'metolazone':'No fixed renal reduction in this edition. Dose to diuresis and residual urine, with close volume/electrolyte monitoring; profound diuresis and hypokalaemia can occur. The old very high maximum is not imported.',
 'midodrine':'Handbook dialysis-related hypotension reference only; verify local authorisation and selection. Give about 30 min before HD in the cited approach and avoid late dosing near bedtime. Supine hypertension, coronary ischaemia, urinary retention and organic heart disease require review. No historic high maximum or automatic post-HD replacement is selected.',
 'minoxidil-systemic':'Oral systemic product only. Start lower or use a longer interval in significant impairment; titrate BP/volume. Review beta-blocker/diuretic co-therapy and residual urine. Topical hair-loss doses are excluded.',
 'nicardipine':'Oral and IV recommendations are separate. The handbook IV titration uses 0.5 mg/hour increments at 30-minute intervals, maximum 15 mg/hour; specialist monitoring is required. Verify the local product and current infusion protocol.',
 'nitroglycerin':'Systemic/IV selected reference only; SL, patches and rectal preparations are not interchanged. Monitor BP and review PDE5-inhibitor/riociguat contraindications. Do not infer a renal dose from concentration alone.',
 'prazosin':'No fixed renal reduction in this edition; select a low initial dose and titrate for the indication. Review first-dose/postural hypotension, especially with volume shifts.',
 'propafenone':'Use cautiously at GFR <10; select indication, weight and metabolic/interacting-drug context. Correct electrolytes and monitor ECG. No renal percentage is supplied by the handbook.',
 'terazosin':'First-dose/postural hypotension warrants slow titration; the 1 mg bedtime dose is an initiation reference, not a complete BP/BPH protocol.',
 'verapamil':'No fixed renal reduction in this edition, but monitor carefully. Oral IR/MR and IV regimens differ. Review heart rate, conduction, hypotension and interacting medicines.',
 'carbimazole':'Titrate to thyroid function. The PK table includes methimazole/thiamazole values and cannot be treated as parent-carbimazole kinetics or a strength conversion.',
 'dexamethasone':'Select the exact indication, preparation and route; this entry supplies renal-adjustment advice rather than a universal steroid dose. Monitor glucose, infection and electrolytes.',
 'fludrocortisone':'Renal non-reduction does not remove mineralocorticoid toxicity. Monitor oedema/BP, sodium and potassium; biological and plasma half-lives are distinct.',
 'hydrocortisone':'The source includes oral replacement and injectable products. Increases in free hydrocortisone clearance during HD have been reported without an established replacement-dose recommendation. No stress-dose, shock or adrenal-crisis regimen is selected here.',
 'levothyroxine':'Titrate to thyroid tests and clinical state, not GFR alone. Review separation from phosphate binders and other absorption interactions. The handbook Vd units require reconciliation, so its numeric Vd is withheld.',
 'liothyronine':'Use the intended thyroid indication and monitor clinical/cardiac response. No levothyroxine conversion or myxoedema-emergency protocol is inferred from the renal non-reduction statement.',
 'methylprednisolone':'Dose by indication, route and transplant/inflammatory protocol; monitor glucose, infection, BP and electrolytes. Historical pulse/depot regimens are not imported as a universal dose.',
 'prednisolone':'Dose by indication and response; no fixed renal reduction in this edition. Monitor glucose, infection, BP, fluid status and electrolytes. Renal half-life is not a tapering schedule.',
 'repaglinide':'Start low and titrate cautiously in advanced renal failure, matching food intake and glucose. Omit meal-related doses when meals are omitted according to the local product. Gemfibrozil and other interacting medicines need review; no fixed dialysis dose is given.',
 'vildagliptin':'Use cautiously in ESRD because experience was limited; review liver function. The handbook reports about 3% parent removal by 3–4 h HD and removal of its main metabolite. No extra post-HD dose is inferred.',
 'alfacalcidol':'Dose to calcium/phosphate/PTH and the intended indication; hypercalcaemia can limit treatment. The daily reference is not a peri-parathyroidectomy or universal IV schedule.',
 'calcitriol':'Monitor calcium closely during titration and reassess phosphate-binder requirements. Oral micrograms and nanograms must not be confused; no universal IV regimen is selected.',
 'calcium-acetate':'Dose with meals to phosphate and calcium response. Tablet elemental calcium varies substantially by brand (e.g. Phosex versus PhosLo), so the book’s tablet-count range is not imported as a universal prescription.',
 'cholecalciferol':'The 2018 table suggests normal dosing but its other-information section reports severe-impairment manufacturer restrictions and senior renal review for higher doses. These product-dependent statements need reconciliation; no universal loading or dialysis regimen is selected.',
 'lanthanum-carbonate':'Chew the selected tablets fully and take with food; match local formulation. Review drug binding/spacing and GI risk. PK of the small absorbed fraction is distinct from intestinal phosphate binding.',
 'paricalcitol':'Initial/maintenance doses depend on PTH, calcium, phosphate, route and product. The book’s oral range is not a substitute for the current initial-dose/titration algorithm; no fixed numeric regimen is selected.',
 'sodium-bicarbonate':'Individualise to bicarbonate, potassium, sodium and volume, especially alongside dialysate alkali. Do not infer a post-HD replacement dose or an acute IV/contrast-prophylaxis regimen.',
 'bisacodyl':'Selected constipation guidance only; bowel-preparation protocols are separate. Review diarrhoea, dehydration and electrolyte effects. Minimal absorption does not mean every combination laxative is appropriate.',
 'domperidone':'The handbook’s older high-dose and prolonged-use schedules are not selected. MHRA restricts use to nausea/vomiting, lowest effective dose, adult maximum 30 mg/day and usually no more than one week. Do not use with impaired cardiac conduction, cardiac disease such as heart failure, QT-prolonging drugs/potent CYP3A4 inhibitors or severe hepatic impairment. Review electrolyte disturbance. Repeated dosing in severe renal impairment may need once/twice-daily frequency per the handbook note.',
 'granisetron':'Match route, indication and formulation; no fixed renal reduction in this edition. The book reports a company suggestion to schedule HD >2 h after a dose, with unknown dialysability; verify this against the local product.',
 'hyoscine-butylbromide':'Butylbromide only, not hydrobromide. Review anticholinergic effects, urinary retention and cardiac risk; parenteral and palliative-care infusion regimens are not inferred from the oral IBS reference.',
 'prochlorperazine':'Selected oral antiemetic reference only; review sedation, extrapyramidal effects, QT and hypotension. Buccal, injectable and psychiatric regimens differ.',
 'promethazine':'Excess sedation can occur in CKD 5. This entry selects oral guidance; older injection doses are not imported. Review anticholinergic effects, hypotension and co-sedatives.',
 'ursodeoxycholic-acid':'Dose by the specific hepatobiliary indication and product. The gallstone reference does not select a cholestatic-liver-disease regimen.',
 'acetylcysteine':'Oral mucolytic and paracetamol-poisoning protocols are different. The book notes that manufacturer/poisons-centre advice did not reduce poisoning doses for renal failure. A general renal percentage or a historical contrast-prophylaxis regimen is not imported; poisoning plus extracorporeal therapy requires toxicology advice.',
 'aminophylline':'The source continuation explains rapid release of theophylline: “not dialysed” for aminophylline must not be read as lack of active-drug removal. Measure theophylline and individualise HD timing/dose; 80% theophylline content is not a free interchangeability rule.',
 'chlorphenamine':'Increased CNS sensitivity is reported in renal impairment. Use the lowest tolerated dose; injection/anaphylaxis protocols are separate. The handbook’s HD categories are historical, not modern quantitative clearance measurements.',
 'ipratropium':'Selected inhaled formulation only. Inhaler/nebuliser strengths differ; nasal products are not covered by this regimen. Review anticholinergic effects and eye exposure.',
 'salbutamol-albuterol':'Airway-treatment reference only; it does not establish a hyperkalaemia regimen. Monitor heart rate, BP, ECG and potassium; systemic IV/oral and inhaled formulations differ.',
 'theophylline':'Use formulation-specific dosing and serum-level monitoring because of the narrow therapeutic window and interactions. HD removes theophylline; no fixed supplement is derived from an old clearance percentage.',
 'terbutaline':'No fixed renal reduction in this edition; select inhaled versus systemic product and titrate to response. Monitor cardiovascular effects and potassium. No obstetric/tocology regimen is supplied.',
 'folic-acid':'Treat deficiency and routine dialysis supplementation separately. Check B12 and the local renal-vitamin policy. The handbook describes varying supplementation schedules; no universal high-dose replacement after every HD is selected.',
 'clopidogrel':'Renal non-reduction does not remove bleeding risk. Select the antiplatelet indication, duration and interacting medicines. The table’s half-life/analyte attribution requires reconciliation and is withheld.',
 'aprepitant':'Selected three-day oral chemotherapy regimen only, not IV fosaprepitant or a different antiemetic schedule. Review CYP3A4 interactions and concomitant steroid/cancer-drug doses.',
 'palonosetron':'Selected single-agent chemotherapy formulations only. Combination products and PONV doses differ. Review the local regimen and QT-risk medicines.',
 'misoprostol':'Selected GI ulcer-prevention use only. The active acid, not parent drug, determines the PK reference. Lower the dose if poorly tolerated; this entry gives no obstetric regimen and does not authorise use in pregnancy.',
 'formoterol':'Match inhaler strength and combination product; the book’s puff count does not identify a strength. No universal high-dose or single-agent asthma schedule is selected.',
 'nystatin':'Oral/topical local therapy with negligible systemic absorption; source strengths vary. No renal dose reduction in this edition does not make nystatin effective for systemic infection.',
 'hydroxychloroquine':'The book derives unusual small renal doses from Seyffart and itself notes practical problems. Its older weight ceiling/renal schedule is not selected as a current lupus/rheumatology protocol. Dose, interval, actual-weight target and retinal surveillance require current indication-specific reconciliation.',
 'mesalazine':'The book’s cautious-use table conflicts with its reported manufacturer restriction below GFR 20, and nephrotoxicity is described. Numeric renal/dialysis dosing is withheld pending the exact current product and gastroenterology/renal review.',
 'sulfasalazine':'At very low GFR, start very low and monitor. Review metabolite toxicity, urine/crystal risk and renal/CBC/liver monitoring; hydration advice must respect an individual fluid restriction. Different indications/formulations need separate regimens.'}
assert set(notes)==set(F)
def tbl(title,rows):return dict(indication=title,rows=[dict(context=c,dose=v) for c,v in rows])
def normdose(ident):
 return ('No fixed renal reduction in this edition. '+reference[ident]) if reference[ident] else 'No fixed renal reduction in this edition; select and titrate the indication/formulation-specific dose'
def module(sid,title,rows=None,*,status='summarized',note='',measure=None):
 m=dict(status=status,tables=[tbl(EDITION+' · '+title,rows)] if rows else [],notes=note,sourceIds=[sid],historical=True,evidenceDate='2018 (copyright 2019)')
 if measure:m['settingMeasure']=measure
 return m
def fact(v,context,sid,withheld=False,basis=None):
 f=dict(status='not_curated' if withheld else 'sourced' if v is not None else 'not_reported',value=v,context=context,sourceIds=[sid])
 if basis:f['basis']=basis
 return f
def category(v):
 # Do not import the adjacent dose statement into the PK category.
 v=v.split('Dose as')[0].split('Initial dose')[0].strip(' .')
 if v.startswith('Unknown'):return ('unknown',None)
 if v.startswith('Not dialysed'):return ('not_removed','Not removed in the historical book category')
 if v.startswith('Unlikely'):return ('limited','Removal described as unlikely in the historical book')
 if v.startswith('Probably'):return ('limited','Removal described as probable, not quantified or independently verified')
 if v.startswith('Likely'):return ('limited','Removal described as likely, not quantified or independently verified')
 if v.startswith('≈1%'):return ('limited','About 1% removed in the historical reference')
 if v.startswith('Dialysed'):return ('removed','Removed in the historical book category; extent unspecified')
 raise ValueError(v)
for f in facts:
 ident=f['id'];d=drugs[ident];assert d['entryType']=='catalog',ident;sid='rdh5-v112-'+ident;page=f['pdfPage'];audit=data['sourceAudit'][0]
 sources[sid]=dict(id=sid,title=f'Renal Drug Handbook 5th · {d["name"]} · PDF p{page} (printed p{page-19})',url=BOOK,section='Selected factual renal/PK summary from the supplied fifth edition, published 2018 (copyright 2019). Publisher-listing link is not the supplied PDF. Additional source pages: '+(', '.join(map(str,f['additionalPdfPages'])) or 'none')+'. Current local product and independent clinical reconciliation remain pending.',type='Supplied fifth-edition renal reference',accessed=DATE,suppliedDocument=dict(fileName=audit['fileName'],sha256=audit['sha256'],pdfPage=page,additionalPdfPages=f['additionalPdfPages'],editionOrDate=audit['editionOrDate']))
 d.update(entryType='renal',flag='no_adjust',kidneyMetric='Handbook GFR · mL/min (not stated as indexed eGFR or Cockcroft–Gault CrCl)',summary='Handbook 5th edition: no fixed renal reduction; match indication and formulation.',considerations=notes[ident],sourceIds=[sid],updatedInVersion=VERSION,jurisdiction='Selected fifth-edition UK-oriented reference, 2018 (copyright 2019); current local authorisation is not established.',completeness='Selected adult edition-based renal instructions. Full indication/formulation coverage, current-label reconciliation, quantified modern circuit clearance and independent clinical approval remain incomplete.',doseEvidence=dict(historical=True,edition='5th',publicationYear=2018,copyrightYear=2019,sourceCheckedAt=DATE,sourceIds=[sid]))
 if ident in ['flecainide','nicardipine','palonosetron','aminophylline']:
  d['routes']=['Oral','Parenteral'];d['formulation']='Oral / Parenteral · separate handbook regimens; verify exact local product'
 d['review']['sourceCheckedAt']=DATE
 common='Edition-based reference; verify the local product, indication, residual function and response. No post-dialysis supplement is calculated from a removal category.'
 ckd=[('Source GFR bands: 20–50, 10–20 and <10 mL/min',normdose(ident))]
 advanced=normdose(ident);hd=advanced;pd=advanced
 if ident=='acetazolamide':
  ckd=[('GFR 20–50','250 mg up to twice daily in the handbook; confirm manufacturer restrictions'),('GFR 10–20','250 mg up to twice daily in the handbook; confirm manufacturer restrictions'),('GFR <10','Avoid in this handbook')];advanced='Avoid in this handbook';hd=pd=advanced;d['flag']='caution';d['summary']='Handbook renal reduction; avoid below GFR 10 and review severe-impairment restrictions.'
 if ident=='flecainide':
  ckd=[('GFR 35–50','Usual indication-specific regimen with ECG monitoring'),('GFR 10–35','Oral initial total 100 mg/day (100 mg daily OR 50 mg twice daily); IV: reduce by 50%'),('GFR <10','Oral initial total 100 mg/day (100 mg daily OR 50 mg twice daily); IV: reduce by 50%')];hd=pd='Oral initial total 100 mg/day (100 mg daily OR 50 mg twice daily); IV: reduce by 50%; monitor ECG/plasma levels';d['flag']='adjust';d['summary']='Handbook renal initial dose: oral total 100 mg/day; IV reduction is separate.'
 if ident=='ivabradine':
  ckd=[('GFR 20–50 or 15–20',normdose(ident)),('GFR <15',normdose(ident)+'; use cautiously because data were lacking')];hd=pd=normdose(ident)+'; use cautiously because ESRD data were lacking';d['flag']='monitor'
 if ident=='midodrine':
  ckd=[('GFR 20–50','No fixed renal reduction; select the orthostatic-hypotension regimen'),('GFR 10–20 or <10','Begin at a lower dose and titrate cautiously to response')];hd='Initial pre-HD reference: 2.5 mg if weight <70 kg, 5 mg if >70 kg; the book assigns no rule at exactly 70 kg';pd='Begin at a lower dose and titrate cautiously; no fixed PD milligram dose is given';d['flag']='monitor';d['summary']='Handbook low-dose titration; selected HD initiation reference, with an unresolved weight boundary.'
 if ident=='minoxidil-systemic':
  ckd=[('Source GFR bands: 20–50, 10–20 and <10','Begin with smaller oral doses or a longer interval; titrate BP and volume response')];hd=pd=ckd[0][1];d['flag']='monitor';d['summary']='Use smaller oral starting doses or longer intervals in significant renal impairment.';d['formulation']='Oral systemic minoxidil only';d['routes']=['Oral']
 if ident=='nicardipine':
  ckd=[('GFR 20–50 · oral','Usual indication/formulation regimen'),('GFR 10–20 or <10 · oral','Start with smaller doses and titrate cautiously'),('GFR 20–50, 10–20 or <10 · IV','Begin 1–5 mg/hour; if needed increase by 0.5 mg/hour every 30 min as tolerated; maximum 15 mg/hour')];hd=pd='Oral: start with smaller doses. IV: begin 1–5 mg/hour; increase by 0.5 mg/hour every 30 min if tolerated, maximum 15 mg/hour';d['flag']='adjust';d['summary']='Handbook oral caution and separately specified IV renal titration.'
 if ident in ['propafenone','verapamil']:
  ckd=[('Source GFR bands: 20–50, 10–20 and <10',normdose(ident)+'; monitor carefully'+(' and use caution below GFR 10' if ident=='propafenone' else ''))];hd=pd=ckd[0][1];d['flag']='monitor'
 if ident=='repaglinide':
  ckd=[('GFR 20–50','Usual indication-specific regimen; monitor glucose'),('GFR 10–20 or <10','Start with a low dose and increase cautiously to glucose/meal response')];hd=pd=ckd[1][1];d['flag']='monitor';d['summary']='Handbook cautious low-dose titration in advanced renal impairment.'
 if ident=='vildagliptin':
  ckd=[('Source GFR bands: 20–50, 10–20 and <10','50 mg orally once daily')];hd=pd='50 mg orally once daily; use cautiously in ESRD';d['flag']='adjust';d['summary']='Handbook renal regimen: 50 mg once daily, including its dialysis categories.'
 if ident=='calcium-acetate':ckd=[('Source GFR bands: 20–50, 10–20 and <10','No fixed GFR reduction; titrate the product-specific elemental-calcium dose to phosphate/calcium response')];hd=pd=ckd[0][1];d['flag']='monitor';d['summary']='Titrate phosphate binding to response; tablet elemental calcium varies by product.'
 if ident=='paricalcitol':ckd=[('Source GFR bands: 20–50, 10–20 and <10','No fixed renal reduction; select the route/product-specific PTH-based initial and titration algorithm')];hd=pd=ckd[0][1];d['flag']='monitor';d['summary']='Select the PTH-, calcium-, phosphate- and route-specific regimen.'
 if ident=='domperidone':
  ckd=[('Nausea/vomiting · adult ≥35 kg · MHRA oral limit','At most 10 mg orally three times daily (maximum 30 mg/day), usually for no longer than one week'),('Repeated treatment in severe renal impairment · handbook note','Reduce frequency to once or twice daily; select the lowest effective dose and review ongoing need')];hd=pd='Repeated treatment may require once- or twice-daily frequency; respect the 10 mg single-dose / 30 mg daily adult limits and cardiac/interaction restrictions';d['flag']='caution';d['summary']='Use the MHRA adult limit, not the older handbook high-dose schedule.'
 if ident in ['aminophylline','theophylline']:
  ckd=[('Source GFR bands: 20–50, 10–20 and <10','No automatic renal reduction; choose the formulation-specific regimen and adjust to measured theophylline levels')];pd=ckd[0][1];hd=ckd[0][1]+'; account for theophylline removal by HD';d['flag']='monitor';d['summary']='Dose to theophylline levels; distinguish the active drug from aminophylline.'
 if ident=='folic-acid':
  ckd=[('Folate deficiency · selected oral reference','5 mg daily for about 4 months, then maintenance by response; exclude B12 deficiency first')];hd=pd='Routine supplementation is local-protocol dependent; the handbook notes 0.5–1 mg/day and unit schedules ranging from 5 mg weekly to daily';d['flag']='monitor';d['summary']='Separate deficiency treatment from routine dialysis supplementation.'
 if ident=='sulfasalazine':
  ckd=[('GFR 20–50 or 10–20','Usual indication-specific dose with caution and monitoring'),('GFR <10','Start at a very low dose; titrate only with close monitoring')];hd=pd=ckd[1][1];d['flag']='monitor';d['summary']='Use cautiously; start very low in the handbook’s <10/dialysis categories.'
 if ident in ['promethazine','chlorphenamine','fludrocortisone','hydrocortisone','sodium-bicarbonate','metolazone']:d['flag']='monitor'
 d['modalities']['ckd']=module(sid,'selected adult renal guidance',ckd,note=common)
 d['modalities']['ihd']=module(sid,'HD / HDF-high-flux reference',[('HD (historical category)',hd),('HDF / high-flux (historical category)',hd)],note=common,measure='2018 handbook HD and HDF/high-flux categories; current circuit prescription not specified')
 d['modalities']['pd']=module(sid,'APD/CAPD combined reference',[('Book APD/CAPD category',pd)],note=common+' Systemic dosing only; not an intraperitoneal-peritonitis prescription.',measure='2018 APD/CAPD combined category; individualise PD prescription and residual function')
 if ident=='acetazolamide':
  for key in ['ihd','pd']:d['modalities'][key]=module(sid,'renal safety',status='avoid',note='The handbook maps this setting to GFR <10 and advises avoidance. '+notes[ident])
 if ident in ['cholecalciferol','hydroxychloroquine','mesalazine']:
  for key in ['ckd','ihd','pd']:d['modalities'][key]=module(sid,'source reconciliation',status='specialist',note=notes[ident]+' Numeric regimen selection remains withheld.')
  d['flag']='caution';d['summary']='Handbook cautions require current product/indication reconciliation; numeric dosing withheld.'
 cont=F[ident]['removalReference']['continuous']
 if 'GFR=' in cont:context='The historical CAV/VVHD row refers to '+cont.split('Dose as in ')[-1].rstrip('.')+'. '
 else:context='The historical CAV/VVHD row refers to the usual indication-specific regimen. '
 d['modalities']['crrt']=module(sid,'continuous-therapy scope',status='specialist',note=context+'No delivered effluent, flow, downtime or residual-clearance settings are supplied. A universal modern CVVH/CVVHD/CVVHDF prescription is therefore not selected.')
 # SLED is deliberately left at its previous explicit gap.
 p=d['pharmacokinetics']
 basis='Historical fifth-edition reference table; normal/reference versus ESRF columns, not measured on-dialysis half-lives.'
 context=notes[ident] if ident in ['carbimazole','aminophylline','lanthanum-carbonate','misoprostol','levothyroxine','clopidogrel','hydroxychloroquine'] else ''
 p.update(status='source_summary',sourceCheckedAt=DATE,historical=True,evidenceDate='2018 (copyright 2019)',halfLife=fact(f['halfLife'],basis+' '+context,sid,'halfLife' in f['withheldFields']),renalHalfLife=fact(f['renalHalfLife'],basis,sid,basis='handbook_normal_esrf_columns'),volumeOfDistribution=fact(f['volumeOfDistribution'],'Only explicit units retained; L and L/kg are not interchanged. '+context,sid,'volumeOfDistribution' in f['withheldFields']),proteinBinding=fact(f['proteinBinding'],'Historical table reference, not an individual patient’s free fraction. '+context,sid),notes='Selected fifth-edition PK facts, with missing/withheld values left blank. Modern circuit clearance and a replacement prescription cannot be inferred. '+context)
 for key,refkey in [('ihd','hd'),('pd','pd')]:
  st,val=category(f['removalReference'][refkey]);ctx='Historical book category only; membrane, quantitative clearance, timing and analyte may differ from current practice.'
  if key=='ihd':
   hst,hval=category(f['removalReference']['highFlux']);ctx+=' HDF/high-flux category: '+(hval or 'unknown in the source')+'.'
  p['dialysability'][key]=dict(status=st,value=val,context=ctx,sourceIds=[sid])
 if ident=='aminophylline':p['dialysability']['ihd']=dict(status='removed',value='Theophylline is removed; aminophylline rapidly dissociates',context='Supplied PDF pp72–73 explain the distinction; p1012 confirms theophylline removal. Do not read the parent “not dialysed” category as no active-drug clearance.',sourceIds=[sid])
 if ident=='hydrocortisone':p['dialysability']['ihd']=dict(status='source_difference',value='Table: removal unlikely; note: unbound hydrocortisone is removed',context='The same source reports increased HD clearance without an established dosing-change recommendation. No fixed replacement dose is inferred.',sourceIds=[sid])
 if ident=='vildagliptin':p['dialysability']['ihd']=dict(status='limited',value='About 3% parent removed over 3–4 h in the cited study',context='Other-information note is more specific than the table’s “not dialysed” category; the main metabolite is also removed. No automatic supplement.',sourceIds=[sid])
 if ident=='aprepitant':p['dialysability']['ihd']=dict(status='negligible',value='<0.2% of dose recovered in HD dialysate',context='Historical handbook cited study; no quantified high-flux conversion or supplement inferred.',sourceIds=[sid])
 if not any(p[k]['value'] is not None for k in ['halfLife','renalHalfLife','volumeOfDistribution','proteinBinding']) and not any(p['dialysability'][k]['value'] is not None for k in ['ihd','pd']):p['status']='not_reported'
 if old[ident]['pharmacokinetics']['status']=='source_summary':d['pharmacokinetics']=old[ident]['pharmacokinetics']
 d['handbookSource']=dict(edition='5th',publicationYear=2018,pdfPage=page,additionalPdfPages=f['additionalPdfPages'],sourceIds=[sid])

mhra='mhra-domperidone-v112'
sources[mhra]=dict(id=mhra,title='MHRA · Domperidone: risks of cardiac side effects',url='https://www.gov.uk/drug-safety-update/domperidone-risks-of-cardiac-side-effects',section='Adult dose/duration and cardiac-risk restrictions; viewed directly on the regulator page. This regulatory notice does not supply a full renal monograph.',type='UK regulator drug-safety notice',accessed=DATE)
drugs['domperidone']['sourceIds'].append(mhra)
for m in ['ckd','ihd','pd']:drugs['domperidone']['modalities'][m]['sourceIds'].append(mhra)
conflicts=[
 ('domperidone','Older handbook normal-dose/duration wording conflicts with MHRA cardiac-risk restrictions.','Older high-dose/prolonged schedules excluded; regulator adult maximum/duration retained with the handbook renal-frequency caution.'),
 ('mesalazine','The handbook cautious-use table and its reported manufacturer restriction below GFR 20 do not select one safe regimen.','Numeric renal and dialysis prescription withheld pending exact current product review.'),
 ('cholecalciferol','Normal-dose table and product-dependent severe-impairment cautions require reconciliation.','No universal loading or dialysis regimen selected.'),
 ('hydroxychloroquine','Historical Seyffart-derived small doses/older weight target are not selected as a current indication-specific regimen.','Renal dosing and ambiguous historical half-life withheld for current-source reconciliation.'),
 ('levothyroxine','The Vd table’s numeric/unit basis needs confirmation.','Numeric Vd left blank; no L/kg-to-L correction guessed.'),
 ('clopidogrel','Historical half-life/analyte attribution needs confirmation.','Half-life left blank; no parent/active-metabolite value inferred.')]
data['sourceConflicts'].extend(dict(drug=i,issue=issue,action=action,status='clinical_reconciliation_pending') for i,issue,action in conflicts)
data.update(version=VERSION,clinicalDataVersion=VERSION,softwareReleaseDate=DATE)
data['coverage']={k:sum(d['entryType']==k for d in data['drugs']) for k in ['renal','safety','catalog']}
data['pharmacokineticCoverage']=dict(profiles=sum(d['pharmacokinetics']['status']=='source_summary' for d in data['drugs']),allFourCoreFields=sum(all(d['pharmacokinetics'][k]['status']=='sourced' for k in ['halfLife','volumeOfDistribution','proteinBinding']) and d['pharmacokinetics']['dialysability']['ihd']['value'] is not None for d in data['drugs']))
changed=[d['id'] for d in data['drugs'] if d!=old[d['id']]];assert len(changed)==60
data['clinicalUpdates']=dict(version=VERSION,changedIds=changed,newRenalIds=changed,newPKIds=[i for i in changed if drugs[i]['pharmacokinetics']['status']=='source_summary' and old[i]['pharmacokinetics']['status']=='not_curated'],newPDIds=[i for i in changed if drugs[i]['modalities']['pd']['tables']],scope='60 selected fifth-edition renal profiles, with dated HD/HDF/PD categories and available PK; three numeric renal regimens withheld, no unparameterised modern CRRT or SLED prescription inferred.')
data['researchLimitations']=dict(onlinePrimarySourceLookup='Search service unavailable. Supplied fifth-edition PDF and a directly retrieved MHRA safety page used for this batch.',scope='Selected edition-based summaries, not current BNF comparison or full clinical approval. Existing current-label regimens retained unchanged.')
data['sourceAudit'][0]['selectedUse']='Selected renal-dose, monitoring, PK and removal summaries; fifth edition is a historical reference, not a current formulary'
data['sources']=list(sources.values());(D/'database.json').write_text(json.dumps(data,ensure_ascii=False,indent=2));(D/'REFERENCE_DIRECTORY.json').write_text(json.dumps(data['referenceResources'],ensure_ascii=False,indent=2))
queue=json.loads((D/'CURATION_QUEUE.json').read_text());queue['version']=VERSION
for q in queue['drugs']:
 d=drugs[q['id']];p=d['pharmacokinetics'];q.update(content=d['entryType'],renalDoseSourceCheckedAt=d['review']['sourceCheckedAt'],pkSourceCheckedAt=p['sourceCheckedAt'],modalities={k:v['status'] for k,v in d['modalities'].items()},pkFields={k:p[k]['status'] for k in ['halfLife','renalHalfLife','volumeOfDistribution','proteinBinding']},removal={k:v['status'] for k,v in p['dialysability'].items()})
(D/'CURATION_QUEUE.json').write_text(json.dumps(queue,ensure_ascii=False,indent=2))
remaining=[dict(id=d['id'],name=d['name'],category=d['category'],reason='Renal-dose curation pending' if d['entryType']=='catalog' else 'Shared safety note only') for d in data['drugs'] if d['entryType']!='renal']
(D/'REMAINING_MEDICATIONS.json').write_text(json.dumps(dict(version=VERSION,notComplete=True,note='Renal profiles also retain indication/product/RRT gaps; clinical approval remains pending.',remaining=remaining),ensure_ascii=False,indent=2))
audit=json.loads((D/'SOURCE_AUDIT.json').read_text());audit['files']=data['sourceAudit'];audit.update(v112Changes=data['clinicalUpdates'],conflicts=data['sourceConflicts'],researchLimitations=data['researchLimitations']);(D/'SOURCE_AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
c=data['coverage'];p=data['pharmacokineticCoverage'];header=f'''# RenalRounds v{VERSION} · 30 October 2026

The top program title is a semantic Home link. It clears the query, selected drug, category/content/route/setting/OTC filters and returns to non-dialysis search at the top, closing open panels. Reader theme/font and favourites remain saved. The in-app back arrow can restore the previous browsing context; calculator values remain excluded and clear on close.

This batch adds 60 selected adult renal profiles from the supplied Renal Drug Handbook fifth edition (published 2018, copyright 2019). They cover cardiovascular, endocrine/steroid, phosphate/vitamin, respiratory, GI and common-medicine entries. There are {c['renal']} partial renal profiles, {c['safety']} shared safety notes and {c['catalog']} catalog entries among 668 indexed medicines. {len(remaining)} entries still lack a drug-specific renal profile. Existing current-label dosing and PK records are retained unchanged.

Edition/year appear at the point of each new dose table. The book GFR bands are not silently relabelled Cockcroft–Gault CrCl or indexed eGFR. Historical HD and HDF/high-flux categories remain separate; APD/CAPD is identified as a combined source category, not an intraperitoneal peritonitis protocol. Source CAV/VVHD rows have no delivered settings, so no universal modern CRRT regimen is assigned. SLED gaps remain explicit. No supplemental dose is calculated from a removal category.

The new profiles include numeric selected references and adjustments where support exists (e.g. flecainide oral initial total versus IV reduction, nicardipine IV titration, vildagliptin 50 mg/day, midodrine initial pre-HD weight bands with exact 70 kg unassigned, calcitriol micrograms, and selected oral/infusion regimens). Many drugs require no fixed renal reduction, while others require response/level-based titration. Three profiles withhold numeric renal selection: hydroxychloroquine, mesalazine and cholecalciferol, because their older/product-dependent guidance needs reconciliation.

Domperidone's older high-dose/prolonged schedules are excluded in favour of the directly retrieved MHRA adult dose/duration restrictions, alongside the handbook renal-frequency note. Aminophylline's continuation explains that the active theophylline is dialysable; the parent category is not a no-clearance rule. Vildagliptin and hydrocortisone preserve the differences between table categories and explanatory notes. Levothyroxine Vd and clopidogrel/hydroxychloroquine half-life fields are withheld where units/analytes need confirmation.

PK coverage is {p['profiles']} source-summary profiles, of which {p['allFourCoreFields']} have all four core items (including qualified qualitative removal statements and historical data). A checked source can have missing parameters: partial panels leave those fields blank; calcium acetate has an explicit source-checked no-parameters-reported state and is not counted as a PK profile. Total L, L/kg, minutes, hours, days, parent and active-metabolite qualifications remain distinct.

Source metadata records exact supplied-PDF page, continuation pages, edition and original file checksum. The original PDF is not redistributed. Source check is not a new study, current product approval, completed BNF comparison or independent clinical sign-off. This remains a reference in development; verify current local products and obtain nephrology/renal-pharmacy review before clinical release.

Both cumulative and modified-file ZIPs include the same target release. The modified-file ZIP compares against the exact v0.10 cumulative package and includes intervening v0.11/v0.11.1 changes, including source paths. It can be overlaid on those retained packages; no original PDFs, credentials or preview files are distributed.

'''
for target,base in [('CHANGELOG.md','changelog_v111.md'),('EDITORIAL_GUIDE.md','editorial_guide_v111.md'),('SOURCE_AUDIT.md','source_audit_v111.md')]: (D/target).write_text(header+'## Earlier release record\n\n'+(R/base).read_text())
(D/'COMPLETION_PLAN.md').write_text(header+'## Remaining clinical work\n\nFinish the local adult formulary and reconcile current products/indications and every remaining dialysis prescription. Source quality, clinically relevant interactions and independent approval matter in addition to inventory counts.\n')
(D/'VERIFICATION.md').write_text('''# v0.11.2 verification

Current suites: checks.mjs, checks_v112.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v112.py. Checks cover exact preservation of v0.11.1 records, 60 edition-based additions, source checksum/page references, dose units and special cases, partial PK/absent versus withheld fields, clear continuous/SLED gaps, live Home/filter/back/theme/font logic, calculator arithmetic/privacy, embedded documents and actual service-worker offline/update integrity. Cumulative extraction/rebuild and byte-level patch overlays are verified. Browser QA checks Home at phone widths, preserved reader settings, in-app back, and dated dose displays.

These are software/source-integrity checks, not clinical validation. Current product reconciliation, BNF comparison, independent approval and physical-phone HTTPS integration remain pending.
''')
print(json.dumps(dict(version=VERSION,coverage=c,pk=p,changed=len(changed),newRenal=60,selectedHD=sum(bool(drugs[i]['modalities']['ihd']['tables']) for i in changed),selectedPD=sum(bool(drugs[i]['modalities']['pd']['tables']) for i in changed))))
