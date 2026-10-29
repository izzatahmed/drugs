"""Twelve sourced cardiovascular renal profiles and a role-labelled source directory.

Run after build_data.py. No clinical approval or cross-modality extrapolation.
"""
from pathlib import Path
import json

ROOT=Path(__file__).parent
path=ROOT/'dist/database.json';data=json.loads(path.read_text())
drugs={d['id']:d for d in data['drugs']};DATE='2026-10-29'
def table(indication,rows):return dict(indication=indication,rows=[dict(context=c,dose=v) for c,v in rows])
def modality(tables=None,notes='',status=None,refs=None):return dict(status=status or ('summarized' if tables else 'not_curated'),tables=tables or [],notes=notes,sourceIds=refs or [])
def summary(ref,indication,rows,notes=''):return modality([table(indication,rows)],notes,refs=[ref])
def gap(ref,note):return modality(notes=note,status='specialist',refs=[ref])
def source(ident,title,product):
    data['sources'].append(dict(id=ident,title='UK SmPC · '+title,url=f'https://www.medicines.org.uk/emc/product/{product}/smpc',section='4.2: adult indication and renal doses; 4.3–4.4: restrictions and monitoring',type='UK product information',accessed=DATE))
source('bisoprolol-renal-uk','Bisoprolol fumarate tablets · renal dosing','13705')
source('valsartan-hypertension-uk','Valsartan tablets · adult hypertension','8181')
def promote(ident,cls,ref,metric,text,ckd,ihd=None,notes='',form='Oral'):
    d=drugs[ident];assert d['entryType']=='catalog',ident
    d.update(entryType='renal',drugClass=cls,sourceIds=[ref],kidneyMetric=metric,summary=text,flag='adjust',formulation=form,
        considerations=notes,jurisdiction='Selected UK product information; verify local product instructions and authorised indications.',
        completeness='Selected adult oral renal guidance only. Source summaries may be monitoring advice rather than numeric doses. Other indications, routes, interactions and RRT prescriptions require separate review.',
        updatedInVersion='0.6.0')
    d['review']['sourceCheckedAt']=DATE
    d['modalities']['ckd']=ckd
    if ihd:d['modalities']['ihd']=ihd
    return d

r='losartan-pk'
promote('losartan','Angiotensin II receptor blocker',r,'No initial renal adjustment in checked UK SmPC',
 'Adult hypertension: usual 50 mg once daily; initial renal reduction is not required, including HD. Volume depletion can require a lower start.',
 summary(r,'Adult hypertension · initial renal adjustment',[('Renal impairment','Usual start 50 mg PO once daily; titrate to 100 mg once daily by response'),('Intravascular volume depletion','Consider starting 25 mg PO once daily')]),
 summary(r,'Adult hypertension · IHD',[('IHD','No initial renal dose reduction; use the individually titrated once-daily regimen')], 'No post-HD replacement amount is assigned.'),
 notes='Correct volume depletion and monitor BP, potassium and kidney function. Heart-failure titration differs. Do not combine routinely with ACE inhibitors; review potassium-raising drugs. This is not a complete contraindication list.')

r='valsartan-hypertension-uk'
promote('valsartan','Angiotensin II receptor blocker',r,'CrCl · mL/min; >10 restriction in checked UK SmPC',
 'Adult hypertension dosing is unchanged at CrCl >10. Evidence in CrCl <10 and dialysis is limited in the selected label.',
 summary(r,'Adult hypertension · tablets',[('CrCl >10','Start 80 mg PO once daily; titrate to 160 mg, then maximum 320 mg once daily if needed'),('CrCl <10','Use cautiously; no validated numeric renal regimen supplied here')], 'The label does not explicitly allocate exact CrCl 10. Confirm the boundary. This table is not the heart-failure or post-MI regimen.'),
 gap(r,'The SmPC describes insufficient experience in dialysis and advises caution. No numeric IHD dose is selected.'),
 notes='Monitor BP, potassium and renal function; correct sodium/volume depletion. Hepatic impairment has separate limits. Avoid dual RAAS blockade unless specifically reviewed.',form='Oral · tablets, adult hypertension only')

r='candesartan-pk'
promote('candesartan','Angiotensin II receptor blocker',r,'Renal impairment; limited experience at CrCl <15 mL/min',
 'For adult hypertension with renal impairment, including HD, start 4 mg once daily and titrate carefully.',
 summary(r,'Adult hypertension · renal starting dose',[('Renal impairment, including very severe impairment','Initial 4 mg PO once daily; titrate to BP response')], 'General hypertension maximum is 32 mg daily; it is not a renal target. Experience at CrCl <15 is limited.'),
 summary(r,'Adult hypertension · IHD',[('IHD','Initial 4 mg PO once daily; titrate with close BP monitoring')], 'HD may increase sensitivity to BP lowering; no supplemental amount is assigned.'),
 notes='Monitor creatinine and potassium. Heart-failure use follows a separate titration/eligibility assessment. The 8 mg source tablet score is not intended to make equal doses; use a suitable strength.')

r='irbesartan-pk'
promote('irbesartan','Angiotensin II receptor blocker',r,'No renal reduction; lower initial dose considered in HD',
 'No CKD dose reduction is required in the label; consider a 75 mg starting dose in HD.',
 summary(r,'Adult hypertension · CKD',[('Renal impairment, not HD','Usual 150 mg PO once daily; may increase to 300 mg once daily by response')]),
 summary(r,'Adult hypertension · IHD starting dose',[('IHD','Consider initial 75 mg PO once daily; individualise subsequent titration')]),
 notes='Review volume status and monitor BP, potassium and renal function. The diabetic renal-disease indication has its own treatment context; no PD/CRRT regimen is inferred.')

r='telmisartan-pk'
promote('telmisartan','Angiotensin II receptor blocker',r,'Mild/moderate versus severe renal impairment; no numeric boundary supplied',
 'Mild/moderate renal impairment needs no adjustment; severe impairment or HD warrants a lower 20 mg starting dose.',
 summary(r,'Adult hypertension · renal adjustment',[('Mild or moderate renal impairment','Usual effective 40 mg PO once daily; some respond to 20 mg; maximum 80 mg daily'),('Severe renal impairment','Recommended lower start: 20 mg PO once daily; individualise titration')]),
 summary(r,'Adult hypertension · IHD',[('IHD','Recommended lower start: 20 mg PO once daily')], 'Experience is limited. A non-removal statement is not a CRRT maintenance regimen.'),
 notes='Monitor BP, creatinine and potassium. Cardiovascular prevention uses a different indication-specific dose. Hepatic impairment has separate limits.')

r='bisoprolol-renal-uk'
promote('bisoprolol','Beta-1 selective blocker',r,'CrCl · mL/min; severe renal threshold <20 for hypertension/angina',
 'Hypertension/angina and heart failure have different initiation schedules. At CrCl <20, the hypertension/angina dose must not exceed 10 mg daily.',
 summary(r,'Hypertension / stable angina · renal limit',[('Adult reference regimen','Usually start 5 mg PO once daily; usual 10 mg daily, general maximum 20 mg/day'),('CrCl <20','Individualise starting dose and titration; maximum 10 mg/day')], 'Stable HFrEF instead starts at 1.25 mg daily with its own slow titration, maximum 10 mg daily; additional renal caution is required. Do not use the hypertension start for HFrEF.'),
 gap(r,'Measured high-flux removal is retained in the PK panel, but the study does not define a universal IHD dose or supplement.'),
 notes='Monitor pulse, BP and conduction. Initiation requires clinical stability; severe renal HFrEF experience is limited. Avoid abrupt withdrawal.')

r='enalapril-pk'
promote('enalapril','ACE inhibitor',r,'CrCl · mL/min; exact source inequalities retained',
 'The selected renal table gives initial TOTAL daily amounts. Dialysis and non-dialysis days need distinct assessment.',
 summary(r,'Adult renal table · INITIAL TOTAL daily amount',[('30 < CrCl <80','Initial total 5–10 mg/day PO'),('10 < CrCl ≤30','Initial total 2.5 mg/day PO'),('CrCl ≤10, not on dialysis','The source row specifies dialysis-day dosing; no non-dialysis prescription is inferred')], 'The upper band excludes exact CrCl 80; verify the full source at boundaries. Reduce dose and/or extend interval according to response.'),
 summary(r,'Adult renal table · dialysis-day INITIAL amount',[('Haemodialysis','Initial total 2.5 mg PO on dialysis days')], 'Adjust non-dialysis-day dosing to BP response. Enalaprilat is dialysable. The table does not specify a universal post-HD supplement or a dialysis-day-only maintenance plan.'),
 notes='Monitor BP, potassium and renal function; check membrane-related reactions. Full hypertension/HF titration differs. This is oral enalapril, not IV enalaprilat.')

r='ramipril-pk'
promote('ramipril','ACE inhibitor',r,'CrCl · mL/min; source range boundaries overlap at 30 and 60',
 'Starting and maximum DAILY amounts fall with renal impairment; the label supplies a separate regimen for haemodialysed hypertension.',
 summary(r,'Adult renal table · DAILY amounts',[('CrCl ≥60','Initial 2.5 mg/day PO; maximum 10 mg/day'),('CrCl 30–60 (source wording)','Initial 2.5 mg/day PO; maximum 5 mg/day'),('CrCl 10–30 (source wording)','Initial 1.25 mg/day PO; maximum 5 mg/day')], 'Source bands overlap at 30 and 60; check the original/local rule before selecting a boundary. No CrCl <10 non-dialysis dose is assigned.'),
 summary(r,'Hypertension in haemodialysed adults',[('IHD','Initial 1.25 mg/day PO; maximum 5 mg/day; give a few hours after HD on treatment days')], 'This is a daily regimen, not a thrice-weekly-only prescription. Preserve the parent/metabolite removal distinctions in the PK panel.'),
 notes='Monitor BP, potassium and renal function; check extracorporeal membrane compatibility. Other indications and hepatic impairment have separate initiation/limits.')

r='clonidine-pk'
promote('clonidine','Central alpha-2 agonist',r,'Individual response and degree of renal impairment; no fixed CrCl table',
 'Oral clonidine needs individual renal adjustment and monitoring. Routine HD does not require a replacement dose.',
 gap(r,'The label requires dose adjustment to renal impairment and BP response but does not supply numeric CKD bands. No fixed renal starting dose is assigned.'),
 summary(r,'Oral clonidine · IHD supplement only',[('Routine IHD','No routine post-HD supplemental dose; maintenance remains individually adjusted')]),
 notes='Monitor BP, pulse and sedation. Abrupt withdrawal can cause rebound hypertension. These oral recommendations do not apply to a transdermal patch.',form='Oral tablets only · transdermal dosing not curated')

r='hydralazine-pk'
promote('hydralazine','Direct arterial vasodilator',r,'CrCl <30 mL/min or serum creatinine >2.5 mg/dL (221 micromol/L)',
 'In moderate/severe renal impairment, adjust the oral dose or interval to avoid accumulation; the label provides no fixed reduction factor.',
 gap(r,'For CrCl <30 mL/min or creatinine >2.5 mg/dL, adapt dose or interval to clinical response. A numeric renal regimen has not been established by this source summary.'),
 notes='Oral source only; IV regimens remain uncurated. Monitor BP/tachycardia and fluid retention. Review lupus/ANCA vasculitis risk and the full product-specific dose limits.',form='Oral tablets only · IV dosing not curated')

r='methyldopa-pk'
promote('methyldopa','Central antihypertensive',r,'Renal elimination; no numeric CrCl bands in checked SmPC',
 'Renal impairment may require smaller doses. Dialysis removal can allow hypertension to recur after treatment.',
 gap(r,'Reduced kidney function can increase response to smaller doses; the source does not provide numeric renal bands or a fixed reduction factor.'),
 gap(r,'Dialysis removes methyldopa and BP may rise afterward; no numeric replacement or maintenance schedule is supplied here.'),
 notes='Review BP, sedation, blood counts and liver function according to the full label. Product contraindications include active liver disease; a dialysis replacement dose is not guessed.')

r='indapamide-pk'
promote('indapamide','Thiazide-like diuretic',r,'CrCl · mL/min; checked 2.5 mg tablet contraindicated below 30',
 'The selected 2.5 mg tablet is contraindicated at CrCl <30 mL/min. Do not transfer its dose to the 1.5 mg sustained-release product.',
 summary(r,'Adult hypertension · 2.5 mg tablet only',[('Normal or only minimally impaired renal function','2.5 mg PO once daily in the morning; do not increase above 2.5 mg/day'),('CrCl <30','Contraindicated in the selected UK product information')], 'Intermediate CKD eligibility requires review of the full source; no band-wide safety claim is made for CrCl ≥30.'),
 modality(notes='Severe renal failure is contraindicated in the checked product. No IHD regimen is supplied.',status='avoid',refs=[r]),
 notes='Check sodium, potassium, magnesium and kidney function. Do not generalise this product restriction to every thiazide-like drug.',form='Oral · 2.5 mg tablet only, not 1.5 mg SR')

data.update(version='0.6.0',schemaVersion='1.4.0',softwareReleaseDate=DATE)
data['coverage']={k:sum(d['entryType']==k for d in data['drugs']) for k in ['renal','safety','catalog']}
data['referenceScope'].update(pnfStatus='Clarified by the user: the intended reference is the British National Formulary (BNF), not a separate PNF.',newEntries=0,updatedEntries=12)
data['referenceResources']=[
 dict(id='bnf',organisation='BNF · British National Formulary',title='BNF on NICE',url='https://bnf.nice.org.uk/',role='Licensed medicines reference',access='Monograph access blocked in this environment; reconciliation pending.',use='UK prescribing/renal information where accessible. Product SmPCs are identified separately and are not labelled BNF-verified.',sourceCheckedAt=DATE),
 dict(id='kdigo',organisation='KDIGO',title='2024 CKD guideline · Chapter 4',url='https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf',role='Clinical guideline',access='Medication-management practice points reviewed.',use='GFR-based adjustment, monitoring, OTC review and medication reconciliation. Does not supply every drug-specific RRT regimen.',sourceCheckedAt=DATE),
 dict(id='asn',organisation='ASN · American Society of Nephrology',title='Kidney News · Pharmacokinetics and Kidney Clearance: A Nephrologist’s Role in Drug Safety and Toxicology',url='https://www.asn-online.org/publications/kidneynews/archives/2024/KN_2024_08_aug.pdf',role='Professional education',access='Linda Awdishu, August 2024, pages 13–14; reviewed for principles.',use='Explains altered disposition and prescription-dependent dialysis removal; not a comprehensive drug-by-drug dosing formulary.',sourceCheckedAt=DATE),
 dict(id='era',organisation='ERA · European Renal Association',title='ERA Guidance and ERBP practice documents',url='https://www.era-online.org/era-guidance/',role='Guideline and practice-document directory',access='Indexed directory reviewed; direct portal access blocked. Linked documents are not all reviewed.',use='Find topic-specific guidelines, practice documents and journal guidance; individual recommendations require source-level checking.',sourceCheckedAt=DATE),
 dict(id='nkf',organisation='NKF · National Kidney Foundation',title='Medication dosing and kidney disease',url='https://www.kidney.org/kidney-topics/medication-dosing-and-kidney-disease',role='Patient medication education',access='Page updated 26 June 2026; reviewed.',use='Safety education and reasons for dose review; not a numerical dialysis dosing table.',sourceCheckedAt=DATE),
 dict(id='nkf-otc',organisation='NKF · National Kidney Foundation',title='Safe medicine use with CKD',url='https://www.kidney.org/kidney-topics/safe-medicine-use-chronic-kidney-disease',role='Patient / OTC safety guidance',access='Page updated 21 April 2025; reviewed.',use='Supports shared medicine-safety notes. Drug-specific doses and RRT removal need additional evidence.',sourceCheckedAt=DATE),
 dict(id='ukka',organisation='UK Kidney Association',title='Blood pressure on dialysis · 2025 guideline',url='https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20Management%20of%20blood%20pressure%20guideline-Jan%202025_4.pdf',role='Dialysis clinical guideline',access='Selected Appendix D PK/removal material reviewed for v0.4.',use='Selected ESRF half-lives and modality-specific removal categories; analytes, dialysis methods and source disagreement remain explicit.',sourceCheckedAt=DATE),
 dict(id='ucsf',organisation='UCSF Infectious Diseases Management Program',title='Antimicrobial dosing in IHD and continuous HD',url='https://idmp.ucsf.edu/antimicrobial-dosing-intermittent-continuous-hemodialysis',role='Institutional dosing protocol',access='Prescription assumptions and selected drug tables reviewed.',use='IHD assumes high-flux; continuous-HD recommendations assume CVVHD at 2 L/h and residual native GFR <10. Do not apply universally to CRRT/PD/SLED.',sourceCheckedAt=DATE),
 dict(id='labels',organisation='Product information · emc / DailyMed',title='UK SmPC and US label sources',url='https://www.medicines.org.uk/emc/',role='Product-specific prescribing information',access='Individual checked documents are linked on each drug.',use='Indication, formulation, renal limits, PK and label removal statements. Local authorisations and renal protocols can differ.',sourceCheckedAt=DATE)]
data['drugStewardship']=dict(sourceIds=['kdigo-2024-medications'],text='Review kidney function, indication, interactions and OTC products; monitor relevant electrolytes and drug levels. When creatinine estimates are unreliable or precision is critical, consider creatinine–cystatin C estimates or measured GFR. Adjust decisions when kidney function or distribution volume is changing.')
data['sources'].append(dict(id='kdigo-2024-medications',title='KDIGO 2024 · Medication management and stewardship',url=data['referenceResources'][1]['url'],section='Chapter 4; practice points 4.1.2–4.1.3, 4.2.1–4.2.5 and 4.3.1',type='International clinical practice guideline',accessed=DATE))
path.write_text(json.dumps(data,ensure_ascii=False,indent=2))

# Regenerate the coverage queue from final data using the existing exact schema.
queue=[]
for d in data['drugs']:
 p=d['pharmacokinetics'];queue.append(dict(id=d['id'],name=d['name'],category=d['category'],routes=d['routes'],content=d['entryType'],renalDoseSourceCheckedAt=d['review']['sourceCheckedAt'],pkSourceCheckedAt=p['sourceCheckedAt'],modalities={k:v['status'] for k,v in d['modalities'].items()},pkFields={k:p[k]['status'] for k in ['halfLife','renalHalfLife','volumeOfDistribution','proteinBinding']},removal={k:v['status'] for k,v in p['dialysability'].items()},independentClinicalReview=d['review']['status'],priority='1: common rounds classes' if d['category'] in ['Cardiovascular','Antimicrobials','Diabetes & endocrine','Anticoagulation & haematology','Pain & neurology','OTC & medicine safety'] else '2: remaining formulary'))
(ROOT/'dist/CURATION_QUEUE.json').write_text(json.dumps(dict(version=data['version'],generatedAt=DATE,note='Statuses describe curation coverage, not suitability for an individual patient. Summarized does not mean clinically approved or complete for every indication.',drugs=queue),ensure_ascii=False,indent=2))
(ROOT/'dist/REFERENCE_DIRECTORY.json').write_text(json.dumps(data['referenceResources'],ensure_ascii=False,indent=2))
(ROOT/'dist/CHANGELOG.md').write_text('''# Changelog

## v0.6.0 — 29 October 2026

- Corrected the reference clarification: BNF means British National Formulary. No separate PNF reference remains requested; BNF monograph reconciliation is still pending access.
- Expanded 12 existing catalog entries: bisoprolol, candesartan, clonidine, enalapril, hydralazine, indapamide, irbesartan, losartan, methyldopa, ramipril, telmisartan and valsartan. They are source-based drafts, not independently approved monographs.
- 113 renal profiles, 28 shared safety notes and 527 renal-dose-pending catalog records; total remains 668. PK coverage remains 27 profiles, with 15 having four core PK items.
- Added explicit HD advice where supplied by the cited label. No new PD, CRRT or SLED regimen was inferred. Clonidine, hydralazine and methyldopa retain nonnumeric renal guidance where the label gives no fixed regimen.
- Kept indication/route differences, source cutoff gaps and initial-versus-maximum daily amounts visible. Existing drug/PK data outside the 12 promoted entries are unchanged.
- Added a role-labelled directory of BNF, KDIGO, ASN, ERA, NKF, UKKA, UCSF and product-information resources. Portal discovery and patient education are distinguished from drug-specific prescribing evidence.

'''+(ROOT/'changelog_v05.md').read_text())
plan=(ROOT/'completion_plan_v05.md').read_text().replace('v0.5.0','v0.6.0').replace('This release adds no clinical claims or dosing regimens.','This release expands 12 existing cardiovascular entries with selected UK-label renal guidance.').replace('101 renal profiles','113 renal profiles').replace('539 renal-dose-pending','527 renal-dose-pending').replace('Identify the requested PNF title and edition; obtain authorized monograph access for PNF/BNF/PDR as appropriate.','BNF has been clarified as the British National Formulary; obtain authorised BNF/PDR monograph access as appropriate. Use the role-labelled reference directory for additional renal evidence.').replace('v0.6.0 passes software/data checks only.','v0.6.0 passes software/data checks only; the new clinical summaries still require independent review.')
(ROOT/'dist/COMPLETION_PLAN.md').write_text(plan)
guide=ROOT/'dist/EDITORIAL_GUIDE.md'
text=guide.read_text().replace('101 sourced renal profiles','113 sourced renal profiles').replace('539 renal-dose-pending','527 renal-dose-pending').replace('The requested PNF title/edition has not been identified. No PNF verification is claimed.','The user clarified that the intended reference is the British National Formulary (BNF), not a separate PNF.')
if '## v0.6 source selection' not in text:
 text+='''\n## v0.6 source selection\n\nUse REFERENCE_DIRECTORY.json and the in-app References view. BNF/labels support product-specific prescribing; professional guidelines and measured PK studies support renal decisions; institutional protocols retain their dialysis assumptions; ASN education and NKF patient pages provide context or safety information. An ERA directory listing is not evidence that every linked guideline has been reviewed. New cardiovascular renal tables cite the individual SmPCs, not a blanket ASN/ERA/NKF endorsement. No source type automatically establishes clinical approval.\n'''
guide.write_text(text)
print(f"Prepared v0.6.0: {data['coverage']}, 12 expanded profiles, 9 reference resources")
