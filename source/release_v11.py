"""Compact interface release with bounded additions from supplied references.

Online primary-source lookup failed during this batch. No historical dose tables
or unverified dialysis-removal categories are promoted into current prescriptions.
"""
from pathlib import Path
import json
R=Path(__file__).parent;D=R/'dist';DATE='2026-10-30'
data=json.loads((D/'database.json').read_text());assert data['version']=='0.10.0'
drugs={d['id']:d for d in data['drugs']};old=json.loads(json.dumps(drugs));sources={s['id']:s for s in data['sources']}
BOOK='https://www.routledge.com/rsc/downloads/Medicine_-_Bestsellers_and_New_Arrivals_Catalog.pdf'
NM='https://www.unmc.edu/intmed/_documents/id/asp/dose-nm-anti-infective-renal-dosing-guidelines.pdf'
def bookref(ident,page):
 sid='rdh5-v11-'+ident;f=data['sourceAudit'][0]
 sources[sid]=dict(id=sid,title=f'Renal Drug Handbook 5th · {drugs[ident]["name"]} · PDF p{page} (printed {page-19})',url=BOOK,section=f'Historical fifth edition, published 2018 (copyright 2019), supplied PDF p{page}. Publisher-listing link is not this supplied PDF. Selected fields only; current product reconciliation pending.',type='Supplied historical PK reference',accessed=DATE,suppliedDocument=dict(fileName=f['fileName'],sha256=f['sha256'],pdfPage=page,editionOrDate=f['editionOrDate']))
 return sid
def nmref(ident,page):
 sid='nm11-'+ident;f=data['sourceAudit'][4]
 sources[sid]=dict(id=sid,title='Nebraska adult antimicrobial protocol · '+drugs[ident]['name'],url=NM+'#page='+str(page),section=f'Supplied protocol, adult row on PDF p{page}; P&T approval April 2026. No paediatric or unlisted RRT schedule inferred.',type='Supplied institutional protocol',accessed=DATE,suppliedDocument=dict(fileName=f['fileName'],sha256=f['sha256'],pdfPage=page,editionOrDate=f['editionOrDate']))
 return sid
def promote(ident,refs,summary,notes,rows=None):
 d=drugs[ident];assert d['entryType']=='catalog'
 d.update(entryType='renal',summary=summary,considerations=notes,flag='no_adjust' if rows else 'monitor',sourceIds=refs,updatedInVersion='0.11.0',jurisdiction='Selected supplied-source adult statement only; current local product and independent clinical review remain pending.',completeness='The displayed renal statement is partial. A full indication/formulation regimen and missing IHD/PD/CRRT/PIRRT prescriptions are not inferred.',kidneyMetric='CrCl · mL/min as specified in the institutional protocol')
 d['review']['sourceCheckedAt']=DATE
 d['modalities']['ckd']=dict(status='summarized' if rows else 'specialist',tables=[dict(indication='Selected adult renal statement',rows=[dict(context=c,dose=v) for c,v in rows])] if rows else [],notes=notes,sourceIds=refs)
 return d
r=nmref('omadacycline',43)
d=promote('omadacycline',[r],'The selected adult institutional protocol specifies no renal reduction.','Select the full indication, route-specific loading and maintenance regimen with ID/pharmacy. Current product-label reconciliation is pending; no universal dialysis schedule is inferred.',[('Adult renal impairment','No renal dose adjustment specified in this protocol')]);d.update(formulation='Oral / IV · selected adult protocol statement',routes=['Oral','Parenteral'],drugClass='Aminomethylcycline antibiotic')
r=nmref('telavancin',51);b=bookref('telavancin',991)
sources[b]['type']='Supplied historical product comparison';sources[b]['section']='Historical fifth edition (2018, copyright 2019), supplied PDF p991: renal restrictions, dialysis and baseline-AKI mortality warning. Current authorised product not verified.'
d=promote('telavancin',[r,b],'Renal adjustment and product-specific restrictions require reconciliation before selecting a numeric regimen.','The supplied protocol changes dosing at CrCl 30–50 and 10–29, and reports no data below 10 or on HD. The historical 2018 handbook reports a different UK restriction below CrCl 30/dialysis and a mortality signal in patients with baseline AKI. A current indication- and jurisdiction-specific label has not been verified in this batch, so its numeric renal table is withheld.');d.update(formulation='IV telavancin · numeric regimen withheld',routes=['Parenteral'],drugClass='Lipoglycopeptide antibiotic')
conflict=dict(drug='telavancin',issue='Supplied 2026-approved institutional dose bands differ from UK restrictions reported in the historical 2018 handbook. Current authorised product and indication have not been reconciled.',action='Numeric renal and dialysis dosing withheld; review renal safety, mortality warning and current local label before use.',status='clinical_reconciliation_pending')
data['sourceConflicts'].append(conflict);d['evidenceNotes']=[dict(title='Source and jurisdiction limits',text=conflict['issue']+' '+conflict['action'],sourceIds=[r,b])]

# Individually inspected historical PK tables. Superscript reference numbers are
# not appended to numeric values. No dialysis-removal category is imported here.
rows=[
 ('morphine',695,'2–3 h','Unchanged','3–5 L/kg','20–35%','Parent reference only; the monograph describes active morphine metabolites separately. An unchanged parent half-life does not establish unchanged opioid dosing needs.'),
 ('hydromorphone',515,'2.5 h',None,'0.99–1.45 L/kg','7.1%','The binding value is the historical table value, not a contemporary product-specific estimate. Release formulation is not matched.'),
 ('oxycodone',774,'2–4 h; modified release 4.5 h','3–5 h; modified release 5.5 h','1.2–6.31 L/kg','45%','The source distinguishes modified-release half-life. Its Vd is printed as 6.31, not a superscript-reference 6.3.'),
 ('fentanyl',438,'2–7 h','Possibly increased','4 L/kg','80–85%','Formulation and route affect disposition; do not apply this generic reference as a transdermal, transmucosal or infusion prescription.'),
 ('buprenorphine',166,'20–25 h; transdermal 30 h','Unchanged','2.5 L/kg','96%','Mixed formulation reference. The source describes prolonged decline after patch removal; this is not a universal duration of effect or opioid-conversion rule.'),
 ('codeine',267,'2.5–4 h','13 h','3–4 L/kg','7%','Codeine-phosphate monograph; parent and morphine/metabolite kinetics are separate. No renal safety conclusion or regimen is assigned.'),
 ('pethidine-meperidine',811,'3–6 h','7–32 h','4.17 L/kg','60–80%','Parent reference; the monograph describes active norpethidine separately. No opioid regimen or toxicity-clearance conclusion is inferred.'),
 ('methadone',660,'13–47 h',None,'3–6 L/kg','60–90%','Historical reference; wide variability and the selected clinical context require separate dose/titration assessment.'),
 ('lacosamide',585,'13 h',None,'0.6 L/kg','<15%','Historical parent reference; no renal dose or post-HD supplement is calculated from these fields.'),
 ('lamotrigine',588,'24–35 h','Unchanged','0.92–1.22 L/kg','55%','Interactions markedly change half-life in the monograph; the renal-column statement is not an on-dialysis measurement.'),
 ('oxcarbazepine',771,'Parent 1.3–2.3 h; active metabolite 9 h','Parent unchanged; active metabolite 16–19 h','0.7–0.8 L/kg','40–60% (metabolite)','Binding refers to the metabolite. The source distinguishes parent and metabolite half-lives; the Vd row does not further resolve the analyte.'),
 ('topiramate',1036,'20–30 h','48–60 h; source also lists 12–15 h with an enzyme-inducing antiepileptic','0.55–0.8 L/kg','9–17%','The source qualifier about enzyme-inducing antiepileptics must not be discarded or used to calculate a dose ratio.'),
 ('carbamazepine',187,'5–26 h','Unchanged','0.8–1.9 L/kg','70–80%','Historical reference; formulation, induction and active-metabolite exposure require separate assessment.'),
 ('phenytoin',819,'7–42 h','Unchanged','0.52–1.19 L/kg','90%','Historical reference binding does not establish the unbound fraction in an individual patient. No free concentration or renal dose is inferred.'),
 ('valproate',950,'6–15 h','Unchanged','0.1–0.4 L/kg','90–95%','Sodium-valproate reference. The digit after 0.4 in extracted text is superscript reference 1, not a Vd of 0.41. No free concentration is inferred.'),
 ('pramipexole',839,'8–14 h','36 h','400–500 L','<20%','Vd explicitly says total Litres despite the generic L/kg row heading; it is not 400–500 L/kg.'),
 ('ropinirole',915,'6 h',None,'8 L/kg','10–40%','The source contains distinct Parkinson disease, restless-leg and modified-release regimens; none is selected from these PK fields.'),
 ('amantadine',67,'15 h','500 h','5–10 L/kg','67%','Historical ESRF column; this is not an on-dialysis half-life or a modern release-product dose rule.'),
 ('memantine',648,'60–100 h','117–156 h','10 L/kg','45%','The final digit after 156 in extracted text is superscript reference 1. No dialysis clearance estimate is inferred from this historical table.'),
 ('donepezil',354,'70 h','Unchanged','12 L/kg','95%','Historical parent reference. An unchanged table entry does not establish a complete renal prescribing or safety assessment.'),
 ('rivastigmine',911,'1 h',None,'1.8–2.7 L/kg','40%','Reference table is not matched to transdermal kinetics; no patch or oral regimen is selected.'),
 ('clonazepam',251,'20–60 h',None,'3 L/kg','86%','Historical reference; no renal starting dose, titration or sedative safety conclusion is assigned.'),
 ('lorazepam',628,'10–20 h','32–70 h','0.9–1.3 L/kg','85%','Parent reference; formulation/excipient and metabolite assessments are separate. No IV or oral regimen is selected.'),
 ('midazolam',676,'2–7 h','Unchanged','0.7–1.2 L/kg','96–98%','Parent reference only; active-metabolite and infusion disposition are not represented by this half-life alone.'),
 ('diazepam',333,'24–48 h','Increased; no numeric value in table','0.95–2 L/kg','95–99%','The monograph describes prolonged metabolite kinetics separately. Parent half-life is not a dosing interval.'),
 ('tizanidine',1027,'2.4 h','Increased; no numeric value in table','2.4 L/kg','30%','Historical reference; numeric renal dosing and interaction reconciliation remain uncurated.'),
 ('phenobarbital',814,'75–120 h','Unchanged','1 L/kg','45–60%','Historical reference column, not a measured on-dialysis half-life or a toxicity-treatment protocol.'),
 ('brivaracetam',160,'9 h','9.8 h in source table','0.5 L/kg','<20%','The 1 following 9.8 is a superscript reference. The cited renal study described severe impairment without dialysis; the table column must not be treated as an on-HD value.'),
 ('ketamine',572,'2–4 h','Unchanged','4 L/kg','20–50%','The monograph describes IV-bolus disposition; no oral/intranasal product matching or infusion regimen is established.'),
 ('sumatriptan',972,'2 h','Probably unchanged','170 L','14–21%','Vd explicitly says total Litres, not L/kg. Route/formulation-specific PK and renal dosing remain separate.')]
for ident,page,half,renal,vd,binding,note in rows:
 d=drugs[ident];assert d['pharmacokinetics']['status']=='not_curated',ident;sid=bookref(ident,page)
 def fact(v,context,basis=None):
  f=dict(status='sourced' if v is not None else 'not_reported',value=v,context=context,sourceIds=[sid])
  if basis:f['basis']=basis
  return f
 removal={k:dict(status='not_curated',value=None,context='The historical category has not been reconciled with contemporary modality-specific evidence; not imported in this batch.',sourceIds=[]) for k in ['ihd','pd','crrt','sled']}
 d['pharmacokinetics']=dict(status='source_summary',sourceCheckedAt=DATE,historical=True,evidenceDate='2018 (copyright 2019)',halfLife=fact(half,'Historical normal/reference column. '+note),renalHalfLife=fact(renal,'Historical renal/ESRF column; not an on-dialysis estimate. '+note,'handbook_normal_esrf_columns'),volumeOfDistribution=fact(vd,note),proteinBinding=fact(binding,'Historical plasma binding reference. '+note),dialysability=removal,notes='Historical 2018 PK fields only. Renal dose schedules and dialysis-removal categories are withheld pending current-source verification. '+note)
 d['updatedInVersion']='0.11.0'

classes={i:'Opioid analgesic' for i in ['morphine','hydromorphone','oxycodone','fentanyl','buprenorphine','codeine','pethidine-meperidine','methadone']}
classes.update({i:'Antiepileptic' for i in ['lacosamide','lamotrigine','oxcarbazepine','topiramate','carbamazepine','phenytoin','valproate','phenobarbital','brivaracetam']})
classes.update({i:'Benzodiazepine' for i in ['clonazepam','lorazepam','midazolam','diazepam']})
classes.update({'pramipexole':'Dopamine agonist','ropinirole':'Dopamine agonist','amantadine':'Antiparkinson agent','memantine':'NMDA receptor antagonist','donepezil':'Cholinesterase inhibitor','rivastigmine':'Cholinesterase inhibitor','tizanidine':'Alpha-2 agonist · muscle relaxant','ketamine':'Dissociative anaesthetic','sumatriptan':'Triptan'})
for ident,cls in classes.items():drugs[ident]['drugClass']=cls

changed=[d['id'] for d in data['drugs'] if d!=old[d['id']]];newrenal=[i for i in changed if drugs[i]['entryType']=='renal'];assert len(changed)==32
data.update(version='0.11.0',clinicalDataVersion='0.11.0',softwareReleaseDate=DATE)
data['coverage']={k:sum(d['entryType']==k for d in data['drugs']) for k in ['renal','safety','catalog']}
data['pharmacokineticCoverage']=dict(profiles=sum(d['pharmacokinetics']['status']=='source_summary' for d in data['drugs']),allFourCoreFields=sum(all(d['pharmacokinetics'][k]['status']=='sourced' for k in ['halfLife','volumeOfDistribution','proteinBinding']) and d['pharmacokinetics']['dialysability']['ihd']['value'] is not None for d in data['drugs']))
data['clinicalUpdates']=dict(version='0.11.0',changedIds=changed,newRenalIds=newrenal,newPKIds=[r[0] for r in rows],scope='Two partial institutional renal profiles; thirty historical PK panels, with new renal doses and RRT removal withheld pending current-source reconciliation.')
data['researchLimitations']=dict(version='0.11.0',onlinePrimarySourceLookup='Unavailable during this batch; no new current-label verification claimed.',historicalPK='Thirty selected fifth-edition tables checked against supplied PDF pages. No new dialysis-removal category or historical renal-dose table imported.',renalSources='Supplied April-2026-approved adult institutional rows; complete current product reconciliation remains pending.')
data['sources']=list(sources.values());(D/'database.json').write_text(json.dumps(data,ensure_ascii=False,indent=2));(D/'REFERENCE_DIRECTORY.json').write_text(json.dumps(data['referenceResources'],ensure_ascii=False,indent=2))
queue=json.loads((D/'CURATION_QUEUE.json').read_text());queue['version']=data['version']
for q in queue['drugs']:
 d=drugs[q['id']];p=d['pharmacokinetics'];q.update(content=d['entryType'],renalDoseSourceCheckedAt=d['review']['sourceCheckedAt'],pkSourceCheckedAt=p['sourceCheckedAt'],modalities={k:v['status'] for k,v in d['modalities'].items()},pkFields={k:p[k]['status'] for k in ['halfLife','renalHalfLife','volumeOfDistribution','proteinBinding']},removal={k:v['status'] for k,v in p['dialysability'].items()})
(D/'CURATION_QUEUE.json').write_text(json.dumps(queue,ensure_ascii=False,indent=2))
remaining=[dict(id=d['id'],name=d['name'],category=d['category'],reason='Renal-dose curation pending' if d['entryType']=='catalog' else 'Shared safety note only') for d in data['drugs'] if d['entryType']!='renal']
(D/'REMAINING_MEDICATIONS.json').write_text(json.dumps(dict(version=data['version'],notComplete=True,note='PK-only panels do not constitute renal dosing guidance. Renal profiles also retain indication/formulation/RRT gaps; independent clinical approval remains pending.',remaining=remaining),ensure_ascii=False,indent=2))
audit=json.loads((D/'SOURCE_AUDIT.json').read_text());audit['conflicts']=data['sourceConflicts'];audit['v11Changes']=data['clinicalUpdates'];audit['researchLimitations']=data['researchLimitations'];(D/'SOURCE_AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
print(json.dumps(dict(version=data['version'],coverage=data['coverage'],pk=data['pharmacokineticCoverage'],changed=len(changed))))

c=data['coverage'];p=data['pharmacokineticCoverage']
head=f'''# RenalRounds v0.11.0 · 30 October 2026

The upper area is reduced to two compact rows: smaller text/theme/eGFR controls first, then a 40-px search field with Filters and Clear filters beside it. Filter actions use icons on narrow phones and visible labels on larger screens. Clear filters is disabled when no filter is active and does not erase the search query. Filter details remain collapsed until opened. Clinical-review badges and informational missing-data notices follow the clinical findings; explicit do-not-use warnings remain with their relevant setting.

The manual day/night choice, text-size preference, calculator and in-app semicircular back arrows are retained. Clinical text size remains readable and can increase independently of the compact controls.

Medication information is expanded for 32 records: two partial adult institutional renal profiles (omadacycline and telavancin), plus 30 historical PK-only panels in pain/neurology. The 668-entry inventory now has {c['renal']} partial renal profiles, {c['safety']} shared safety notes and {c['catalog']} renal-dose-pending catalog entries. There are {p['profiles']} PK panels; {p['allFourCoreFields']} have all four core items. Thirty new panels contain half-life, Vd and binding; their dialysis removal and dose schedules remain uncurated.

Online primary-source search and retrieval were unavailable during this batch. No new current product-label verification is claimed. The renal additions use the supplied institutional protocol approved April 2026; the PK additions use selected supplied fifth-edition handbook tables published in 2018 (copyright 2019). Historical reference numbers are distinguished from numeric values, and total Litres from L/kg. No historical renal-dose table or new dialysis-removal category is imported. Telavancin's current label, indication and jurisdiction need reconciliation; its numeric renal regimen is withheld.

Coverage remains incomplete. REMAINING_MEDICATIONS.json lists {len(remaining)} records without a drug-specific renal profile ({c['catalog']} catalog entries plus {c['safety']} shared safety notes). PK availability does not establish a dose. Existing renal profiles also retain formulation/indication/RRT gaps. Independent clinical approval and BNF monograph reconciliation remain pending.

'''
(D/'CHANGELOG.md').write_text(head+'## Earlier releases · historical\n\n'+(R/'changelog_v10.md').read_text())
(D/'EDITORIAL_GUIDE.md').write_text(head+'## Existing editorial policy · historical record\n\n'+(R/'editorial_guide_v10.md').read_text())
(D/'SOURCE_AUDIT.md').write_text(head+'## New historical PK page locators\n\n'+'\n'.join(f'- {drugs[i]["name"]}: PDF p{page}, printed p{page-19}.' for i,page,*_ in rows)+'\n\n## Previous audit\n\n'+(R/'source_audit_v10.md').read_text())
(D/'COMPLETION_PLAN.md').write_text(head+'''## Next clinical work

Resume current authorised product verification when online primary sources are available. Prioritise the newly described pain/neurology products for indication/formulation-specific renal dosing, free/metabolite kinetics and measured dialysis removal. Reconcile telavancin source/jurisdiction differences. Complete the remaining local adult formulary and missing prescription-specific IHD/PD/CRRT/PIRRT data; retain explicit gaps and obtain independent nephrology plus renal-pharmacy sign-off before clinical release.
''')
(D/'VERIFICATION.md').write_text('''# v0.11 software and source-integrity verification

Current checks: checks.mjs, checks_v11.mjs, checks_interface.mjs and checks_calculator.mjs. They verify schema/source links, unchanged v0.10 drug regimens and prior PK, PDF page/checksum provenance, historical/normal/renal column distinctions, reference-number parsing, units, explicit new RRT gaps, partial renal profiles, queue/export consistency, actual search filters, compact-control structure, manual theme persistence, in-app back navigation and calculator arithmetic/privacy. Actual service-worker contracts verify offline reopening, explicit update activation, checksum/version rejection and scoped cache isolation.

Browser QA checks the smaller top controls, shorter search field and filter actions on the same line; clear-filter behaviour; lower review/missing-data notices; day/night persistence; text enlargement; back navigation; calculator; and 320/390-px overflow. A clean extracted package is rebuilt and compared byte-for-byte; root SHA256 checksums, ZIP CRC and public-file exclusions are verified.

These are software, arithmetic and source-integrity checks, not clinical validation. Current-source verification was unavailable in this batch. Full clinical coverage, source reconciliation, BNF comparison and independent approval remain pending. Hosted HTTPS update/offline installation and physical-phone testing require verification after GitHub upload.
''')
