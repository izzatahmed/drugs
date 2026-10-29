"""Selected additions from supplied references, with edition and prescription provenance.

Build order: build_data.py, release_v06.py, release_v07.py, build_standalone.py.
Original PDFs are research inputs, not redistributed runtime assets.
"""
from pathlib import Path
import json
ROOT=Path(__file__).parent;DATE='2026-10-29';D=ROOT/'dist'
data=json.loads((D/'database.json').read_text());drugs={d['id']:d for d in data['drugs']}
before=json.loads(json.dumps(drugs));inventory=json.loads((ROOT/'source_inventory_v07.json').read_text())
NM='https://www.unmc.edu/intmed/_documents/id/asp/dose-nm-anti-infective-renal-dosing-guidelines.pdf'
RRT='https://www.unmc.edu/intmed/_documents/id/asp/final_crrt_pirrt_abxrecommendations_2023.pdf'
BOOK='https://www.routledge.com/rsc/downloads/Medicine_-_Bestsellers_and_New_Arrivals_Catalog.pdf'
sources={s['id']:s for s in data['sources']}
def src(ident,title,url,section,kind='Institutional dosing protocol',file=None,page=None):
 s=dict(id=ident,title=title,url=url,section=section,type=kind,accessed=DATE)
 if file:s['suppliedDocument']=dict(fileName=file['fileName'],sha256=file['sha256'],pdfPage=page,editionOrDate=file['editionOrDate'])
 sources[ident]=s;return ident
def dose_ref(ident,page):return src('nm07-'+ident,'Nebraska Medicine · '+drugs[ident]['name']+f' · PDF p{page}',NM+f'#page={page}',f'Adult renal rows; PDF page {page}. P&T approval April 2026; not the paediatric rows.',file=inventory[4],page=page)
def table(title,rows):return dict(indication=title,rows=[dict(context=c,dose=v) for c,v in rows])
def mod(ref,tables=None,notes='',status=None,setting=None):
 m=dict(status=status or ('summarized' if tables else 'not_curated'),tables=tables or [],notes=notes,sourceIds=[ref])
 if setting:m['settingMeasure']=setting
 return m
def one(ref,title,rows,notes='',setting=None):return mod(ref,[table(title,rows)],notes,setting=setting)
def mark(d):d['updatedInVersion']='0.7.0'
def promote(ident,page,cls,summary,ckd=None,ihd=None,pd=None,form='Adult systemic therapy · see route in rows',notes=''):
 d=drugs[ident];r=dose_ref(ident,page);assert d['entryType']=='catalog',ident
 d.update(entryType='renal',sourceIds=[r],drugClass=cls,kidneyMetric='CrCl · mL/min; adult Cockcroft–Gault in Nebraska protocol',summary=summary,flag='adjust',formulation=form,considerations=notes,
   completeness='Selected adult source-specific indications only. Regimens do not cover every infection, formulation, paediatric patient or RRT prescription. PD rows are systemic therapy, not intraperitoneal peritonitis therapy.',jurisdiction='Nebraska institutional adult protocol unless a table explicitly identifies a current product label.')
 d['review']['sourceCheckedAt']=DATE
 for k,v in [('ckd',ckd),('ihd',ihd),('pd',pd)]:
  if v:d['modalities'][k]=v(r)
 mark(d);return d,r

promote('acyclovir',4,'Antiviral','Selected IV HSV/VZV renal regimens; oral acyclovir is not covered by these dose rows.',
 lambda r:mod(r,[table('IV mucocutaneous HSV',[('CrCl >50','5 mg/kg IV every 8 h'),('CrCl 25–50','5 mg/kg IV every 12 h'),('CrCl 10–24','5 mg/kg IV every 24 h'),('CrCl <10','2.5–3.1 mg/kg IV every 24 h')]),table('IV HSV encephalitis / VZV',[('CrCl >50','10 mg/kg IV every 8 h'),('CrCl 25–50','10 mg/kg IV every 12 h'),('CrCl 10–24','10 mg/kg IV every 24 h'),('CrCl <10','5–6.2 mg/kg IV every 24 h')])],'Source uses adjusted body weight in obesity. Verify fractional CrCl gaps and the exact indication; monitor renal function and neurotoxicity.'),
 lambda r:one(r,'IV acyclovir · daily IHD schedule',[('Mucocutaneous HSV','2.5–3.1 mg/kg IV every 24 h'),('Encephalitis / VZV','5–6.2 mg/kg IV every 24 h')],'Give daily, after HD on HD days; not only after dialysis sessions.'),
 lambda r:one(r,'IV acyclovir · systemic PD therapy',[('Mucocutaneous HSV','2.5–3.1 mg/kg IV every 24 h'),('Encephalitis / VZV','5–6.2 mg/kg IV every 24 h')]),form='IV renal tables only · oral dose curation pending',notes='Use an appropriate infusion rate and hydration plan; the obese dosing-weight recommendation is source specific. No oral or intraperitoneal dose is inferred.')
drugs['acyclovir']['aliases']=sorted(set(drugs['acyclovir']['aliases']+['Aciclovir']))

for ident,cls in [('amphotericin-b-deoxycholate','Polyene antifungal · conventional'),('liposomal-amphotericin-b','Polyene antifungal · liposomal')]:
 promote(ident,8,cls,'No renal reduction specified in the institutional protocol; formulation and infection-specific dosing remain essential.',
  lambda r:one(r,'Renal adjustment statement',[('Renal impairment','No renal dose reduction specified; choose the formulation/indication regimen separately')]),
  notes='No numeric antifungal prescription is selected. Conventional and liposomal formulations are not interchangeable; review nephrotoxicity, potassium, magnesium and infusion precautions.',form='IV · formulation-specific; no automatic substitution')

promote('aztreonam',11,'Monobactam','Selected adult IV regimen for moderate/severe infection or Pseudomonas.',
 lambda r:one(r,'Moderate/severe infection · IV',[('CrCl >30','2 g IV every 8 h'),('CrCl 10–30','2 g IV every 12 h'),('CrCl <10','2 g IV every 24 h')]),
 lambda r:one(r,'Adult IHD · daily IV regimen',[('IHD','2 g IV every 24 h; after HD on dialysis days')]),
 lambda r:one(r,'Systemic PD therapy',[('PD','2 g IV every 24 h')]),form='IV · not inhaled aztreonam')

promote('cefadroxil',12,'First-generation cephalosporin','Separate complicated-infection and uncomplicated/suppression regimens.',
 lambda r:mod(r,[table('Complicated infection, e.g. bacteremia/osteomyelitis',[('CrCl >40','1 g PO every 12 h'),('CrCl 20–40','500 mg PO every 12 h'),('CrCl <20','500 mg PO every 24 h')]),table('Uncomplicated infection or suppression',[('CrCl >40','500 mg PO every 12 h'),('CrCl 20–40','500 mg PO every 24 h'),('CrCl <20','500 mg PO every 48 h')])]),
 lambda r:one(r,'Three-times-weekly IHD',[('Complicated infection','1 g PO once, then 1 g after each HD session three times weekly'),('Uncomplicated / suppression','1 g PO once, then 500 mg after each HD session three times weekly')]),
 lambda r:one(r,'Complicated infection · systemic PD',[('PD','1 g PO once, then 500 mg PO daily')],'Uncomplicated-infection PD dosing has not been selected here.'),form='Oral')
promote('cefdinir',14,'Third-generation oral cephalosporin','Reduce frequency below CrCl 30; IHD and PD schedules differ.',
 lambda r:one(r,'Adult oral dosing',[('CrCl ≥30','300 mg PO every 12 h'),('CrCl <30','300 mg PO every 24 h')]),
 lambda r:one(r,'IHD',[('IHD','300 mg PO once, then 300 mg after each HD session three times weekly')]),
 lambda r:one(r,'Systemic PD',[('PD','300 mg PO every 48 h')]),form='Oral')
promote('cefoxitin',16,'Cephamycin','Selected standard adult IV renal regimen.',
 lambda r:one(r,'Standard adult dose',[('CrCl >50','2 g IV every 6 h'),('CrCl 30–50','2 g IV every 8 h'),('CrCl 10–30','2 g IV every 12 h'),('CrCl <10','1 g IV every 24 h')],'Source bands overlap at CrCl 30; verify the boundary.'),
 lambda r:one(r,'IHD',[('IHD','1 g IV every 24 h; after HD on HD days')]),
 lambda r:one(r,'Systemic PD',[('PD','1 g IV every 24 h')]),form='IV')
promote('cefpodoxime',16,'Third-generation oral cephalosporin','Renal interval depends on the selected infection-specific single dose.',
 lambda r:mod(r,[table('Systemic infection',[('CrCl ≥30','400 mg PO every 12 h'),('CrCl <30','400 mg PO every 24 h')]),table('Complicated UTI / pyelonephritis',[('CrCl ≥30','200 mg PO every 12 h'),('CrCl <30','200 mg PO every 24 h')]),table('Uncomplicated cystitis',[('CrCl ≥30','100 mg PO every 12 h'),('CrCl <30','100 mg PO every 24 h')])]),
 lambda r:one(r,'IHD · select the indication',[('Systemic infection','400 mg PO every 24 h'),('Complicated UTI / pyelonephritis','200 mg PO every 24 h'),('Uncomplicated cystitis','100 mg PO every 24 h')],'After HD on dialysis days.'),
 lambda r:one(r,'Systemic PD · select the indication',[('Systemic infection','400 mg PO every 24 h'),('Complicated UTI / pyelonephritis','200 mg PO every 24 h'),('Uncomplicated cystitis','100 mg PO every 24 h')]),form='Oral · source institutional indications')
promote('ceftaroline',17,'Cephalosporin with MRSA activity','Standard and salvage/S. aureus bacteremia schedules are separate.',
 lambda r:mod(r,[table('Standard adult IV regimen',[('CrCl >50','600 mg IV every 12 h'),('CrCl 31–50','400 mg IV every 12 h'),('CrCl 15–30','300 mg IV every 12 h'),('CrCl <15','200 mg IV every 12 h')]),table('Salvage / severe infection / S. aureus bacteremia · institutional regimen',[('CrCl >50','600 mg IV every 8 h'),('CrCl 31–50','400 mg IV every 8 h'),('CrCl 15–30','300 mg IV every 8 h'),('CrCl <15','200 mg IV every 8 h')])],'q8h salvage therapy is an institutional regimen; reconcile indication, local policy and exact boundary gaps.'),
 lambda r:one(r,'IHD',[('Standard','200 mg IV every 12 h'),('Salvage / severe infection','200 mg IV every 8 h')],'On HD days give the appropriate scheduled dose after HD; not a once-per-session-only regimen.'),
 lambda r:one(r,'Systemic PD',[('Standard','200 mg IV every 12 h'),('Salvage / severe infection','200 mg IV every 8 h')]),form='IV')

# Cefuroxime: use the current tablet label, and retain the uploaded-source conflict.
cef_label=src('cefuroxime-label-07','DailyMed · Cefuroxime axetil tablets','https://www.dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=d14d4184-3e29-43cd-8046-658699c70f03','2.5 renal interval table; 12.3 PK','US prescribing information')
d,r=promote('cefuroxime',21,'Second-generation cephalosporin','ORAL TABLET guidance follows the current US label; uploaded institutional and historical sources differ.',form='Oral cefuroxime axetil tablets only · IV not covered by these rows')
d['kidneyMetric']='CrCl · mL/min; current US oral-tablet label'
d['sourceIds']=[cef_label,r];d['jurisdiction']='Current US oral-tablet label selected; Nebraska and historical references differ.'
d['modalities']['ckd']=one(cef_label,'Oral tablets · select standard single dose by indication',[('CrCl ≥30','No renal interval change to the selected single dose'),('CrCl 10 to <30','Selected standard single dose every 24 h'),('CrCl <10 without HD','Selected standard single dose every 48 h')],'Choose the standard individual dose from the complete infection-specific label. Do not apply this oral interval to IV cefuroxime.')
d['modalities']['ihd']=one(cef_label,'Oral tablets · HD supplement',[('At end of each HD session','Give one additional standard individual dose')],'This supplement statement does not itself select the complete maintenance schedule.')
d['modalities']['pd']=mod(cef_label,notes='A PD dose is not selected because the supplied older/institutional sources differ and the current tablet label does not supply a PD regimen.',status='specialist')
d['evidenceNotes']=[dict(title='Cefuroxime source disagreement',text='The 2018 BC sheet and fifth-edition handbook retain more frequent oral schedules than the current US tablet label. Nebraska also uses indication-specific institutional schedules. The active table here follows the tablet label; these alternatives must not be combined.',sourceIds=[cef_label,r])]

promote('clarithromycin',23,'Macrolide','Immediate-release oral regimen; reduce the single dose at CrCl <30.',
 lambda r:one(r,'Adult immediate-release regimen',[('CrCl ≥30','500 mg PO every 12 h'),('CrCl <30','250 mg PO every 12 h')]),
 lambda r:one(r,'IHD · immediate-release',[('IHD','250 mg PO every 12 h; time the relevant dose after HD on dialysis days')]),
 lambda r:mod(r,notes='The Nebraska PD row says no adjustment, while the older BC/handbook sources differ. A fixed PD regimen is withheld pending reconciliation.',status='specialist'),form='Oral immediate release only · not XL',notes='Review major CYP3A interactions, QT risk, colchicine and transplant medicines; the renal reduction is 50% OF the reference single dose, not a further arbitrary subtraction.')
promote('ethambutol',28,'Antimycobacterial','Renal impairment requires intermittent dosing with monitoring.',
 lambda r:one(r,'Adult treatment',[('CrCl ≥30','15–20 mg/kg PO daily, maximum 2.4 g/dose in the source'),('CrCl <30','15–25 mg/kg PO three times weekly')]),
 lambda r:one(r,'IHD',[('IHD','15–25 mg/kg PO three times weekly, after HD')]),
 lambda r:one(r,'Systemic PD',[('PD','15–25 mg/kg PO three times weekly')]),form='Oral',notes='Source uses estimated lean body weight; obese dosing is uncertain. Confirm the full multidrug TB regimen, treatment phase and visual/toxicity monitoring.')
promote('famciclovir',28,'Antiviral','Selected varicella-zoster 500 mg q8h reference regimen only.',
 lambda r:one(r,'Adult VZV reference regimen',[('CrCl ≥60','500 mg PO every 8 h'),('CrCl 40–59','500 mg PO every 12 h'),('CrCl 20–39','500 mg PO every 24 h'),('CrCl <20','250 mg PO every 24 h')]),
 lambda r:one(r,'IHD · selected VZV regimen',[('IHD','250 mg PO after each HD session')]),form='Oral · VZV only',notes='Herpes simplex, single-dose and prophylaxis schedules differ; duration must be selected separately. No clear PD schedule is supplied.')
promote('flucytosine',30,'Antifungal','Interval extension and concentration monitoring are essential.',
 lambda r:one(r,'Adult oral regimen',[('CrCl >40','25 mg/kg PO every 6 h'),('CrCl 21–40','25 mg/kg PO every 12 h'),('CrCl 10–20','25 mg/kg PO every 24 h'),('CrCl <10','25 mg/kg PO every 48 h')],'Source uses ideal body weight; verify fractional boundary gaps and therapeutic concentrations.'),
 lambda r:one(r,'IHD',[('IHD','25 mg/kg PO after HD, three times weekly')],'Individualise by drug concentrations and toxicity monitoring.'),
 lambda r:mod(r,notes='The source groups HD/PD with a three-times-weekly post-dialysis statement. That timing cannot be transferred to continuous PD; no fixed PD schedule is assigned.',status='specialist'),form='Oral',notes='Use TDM and monitor marrow/liver toxicity; do not infer a continuous-PD schedule from HD timing.')
promote('fosfomycin',33,'Urinary antibacterial','Oral cystitis regimens only; IV fosfomycin is not covered.',
 lambda r:mod(r,[table('Uncomplicated cystitis',[('Adult renal impairment','3 g PO once; no renal reduction in the selected protocol')]),table('Complicated cystitis · institutional multidose regimen',[('CrCl ≥50','3 g PO every 48 h for 3 doses'),('CrCl <50','3 g PO every 72 h for 3 doses')])]),form='Oral trometamol · cystitis only',notes='The multidose course is institutional guidance; it is not a regimen for pyelonephritis or systemic infection. Dialysis regimens remain uncurated.')
promote('ganciclovir',33,'CMV antiviral','IV induction and maintenance doses are distinct.',
 lambda r:mod(r,[table('IV induction · non-resistant CMV',[('CrCl ≥70','5 mg/kg IV every 12 h'),('CrCl 50–69','2.5 mg/kg IV every 12 h'),('CrCl 25–49','2.5 mg/kg IV every 24 h'),('CrCl 10–24','1.25 mg/kg IV every 24 h'),('CrCl <10','Specialist schedule; see HD when applicable')]),table('IV maintenance',[('CrCl ≥70','5 mg/kg IV every 24 h'),('CrCl 50–69','2.5 mg/kg IV every 24 h'),('CrCl 25–49','1.25 mg/kg IV every 24 h'),('CrCl 10–24','0.625 mg/kg IV every 24 h'),('CrCl <10','Specialist schedule; see HD when applicable')])]),
 lambda r:one(r,'IHD · three-times-weekly HD',[('Induction','1.25 mg/kg IV after each HD session'),('Maintenance','0.625 mg/kg IV after each HD session')]),form='IV · not oral valganciclovir',notes='Source uses adjusted body weight in obesity. Monitor CBC and renal function; resistant CMV regimens are excluded. No PD dose inferred.')
promote('phenoxymethylpenicillin',46,'Penicillin V','No renal dose reduction specified in the protocol.',
 lambda r:one(r,'Adult oral reference',[('Renal impairment','250–500 mg PO every 6–8 h; select indication and duration separately')]),
 lambda r:one(r,'IHD',[('IHD','No renal reduction; time the appropriate scheduled dose after HD')]),form='Oral')
promote('tigecycline',51,'Glycylcycline','No renal reduction specified; loading and maintenance doses are separate.',
 lambda r:one(r,'Adult IV reference',[('Renal impairment','100 mg IV loading dose, then 50 mg IV every 12 h')]),form='IV',notes='Check infection eligibility, hepatic impairment and the full safety label. The renal statement does not establish suitability for bloodstream or urinary infections.')
promote('valganciclovir',55,'Oral CMV prodrug','Selected non-dialysis induction and maintenance renal table; dialysis regimens are withheld.',
 lambda r:mod(r,[table('CMV induction',[('CrCl ≥60','900 mg PO every 12 h'),('CrCl 40–59','450 mg PO every 12 h'),('CrCl 25–39','450 mg PO every 24 h'),('CrCl 10–24','450 mg PO every 48 h'),('CrCl <10','Specialist review; no tablet prescription assigned')]),table('CMV maintenance',[('CrCl ≥60','900 mg PO every 24 h'),('CrCl 40–59','450 mg PO every 24 h'),('CrCl 25–39','450 mg PO every 48 h'),('CrCl 10–24','450 mg PO twice weekly'),('CrCl <10','Specialist review; no tablet prescription assigned')])]),form='Oral · induction/maintenance only, not transplant prophylaxis',notes='Nebraska includes low-dose dialysis schedules requiring separate formulation/local-protocol review. They are not copied into a routine tablet prescription. Monitor CBC; do not confuse with IV ganciclovir.')
vori_label=src('voriconazole-label-07','DailyMed · Voriconazole tablets','https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=67c174da-41b8-4738-8a22-dd814b8e96b8','2.6 renal impairment; oral versus IV SBECD vehicle','US prescribing information')
d,r=promote('voriconazole',57,'Triazole antifungal','Oral voriconazole needs no renal reduction; IV vehicle exposure requires a separate decision.',form='Oral renal statement only · IV needs separate benefit/risk review')
d['kidneyMetric']='CrCl · mL/min; current US product information'
d['sourceIds']=[vori_label,r];d['modalities']['ckd']=one(vori_label,'Oral renal adjustment',[('Mild to severe renal impairment','No renal reduction to the indication-specific oral regimen')],'At CrCl <50, the IV SBECD vehicle accumulates; use oral therapy unless the individual benefit/risk justifies IV treatment with monitoring.')
d['evidenceNotes']=[dict(title='Route matters for voriconazole',text='The institutional table says no renal adjustment for the drug. Current product information separately addresses IV SBECD accumulation below CrCl 50. The active renal statement here is oral only.',sourceIds=[vori_label,r])]

for ident in ['amphotericin-b-deoxycholate','liposomal-amphotericin-b','phenoxymethylpenicillin','tigecycline']:
 drugs[ident]['flag']='no_adjust'
drugs['voriconazole']['flag']='monitor'

# PIRRT: source-specific schedules, not universal SLED conversions. No old regimen is overwritten.
def pirrt(ident,page,indication,rows,prescription,notes):
 d=drugs[ident];r=src('nm-pirrt-'+ident,'Nebraska · '+d['name']+f' · PIRRT PDF p{page}',RRT+f'#page={page}',f'Table 2, PDF p{page}; read with prescription/timing comments and footnotes on pp2,10–13.',file=inventory[3],page=page)
 assert d['entryType']=='renal',ident
 d['modalities']['sled']=one(r,indication,rows,notes,setting='Nebraska PIRRT · '+prescription)
 d['sourceIds']=list(dict.fromkeys(d['sourceIds']+[r]));mark(d)
pirrt('ampicillin',10,'PIRRT · extrapolated guidance',[('Maintenance','1–2 g IV every 8 h')],'session prescription not specified for this extrapolated row','Source extrapolates from ampicillin/sulbactam. No specific dose timing is supplied; verify the complete delivered prescription.')
pirrt('ampicillin-sulbactam',10,'PIRRT',[('Maintenance','3 g IV every 8 h')],'8-hour sessions','No specific timing recommendation in the source. Dose is total combination amount.')
pirrt('aztreonam',10,'PIRRT',[('Loading','2 g IV once'),('Maintenance','1–2 g IV every 12 h')],'7-hour sessions','At least one scheduled dose should follow the end of daily PIRRT.')
pirrt('cefazolin',10,'PIRRT · expert opinion',[('Alternative maintenance regimens','1 g IV every 8 h OR 2 g IV every 12 h')],'prescription not specified; expert opinion','No specific timing recommendation; alternatives are not additive.')
pirrt('cefepime',10,'PIRRT · standard / neutropenic-fever source rows',[('Alternative maintenance regimens','1 g IV every 6 h OR 2 g IV every 12 h')],'flow 4–5 L/h; 8–10-hour sessions','Source also lists an alternative 2 g pre-session plus 3 g after PIRRT; that higher-dose alternative is not combined with the displayed regimens. Neurotoxicity risk requires close review.')
pirrt('ceftazidime',10,'PIRRT',[('Maintenance','2 g IV every 12 h')],'flow 4–5 L/h; 8–10-hour sessions','No specific timing recommendation in the source.')
pirrt('ceftazidime-avibactam',10,'PIRRT · expert opinion',[('Maintenance','1.25 g IV every 12 h')],'expert opinion; session duration must be checked','Give one scheduled dose after daily PIRRT. The source notes q8h may be needed for sessions longer than 12 h; this is not an automatic change.')
pirrt('ceftaroline',11,'PIRRT · expert opinion',[('Standard','400 mg IV every 12 h'),('Endocarditis / S. aureus bacteremia','400 mg IV every 8 h')],'prescription not specified; expert opinion','No specific timing recommendation; severe-infection dosing is an institutional regimen.')
pirrt('daptomycin',11,'PIRRT',[('Maintenance','6 mg/kg IV every 24 h')],'flow 160 mL/min; 8-hour sessions','Give after daily PIRRT. Match indication, dosing weight and CPK/toxicity monitoring.')
pirrt('ertapenem',11,'PIRRT',[('Loading','500 mg IV once'),('After daily PIRRT','500 mg IV after the session')],'flow 4–5 L/h; 8–10-hour sessions','Source wording is a loading dose followed by a post-PIRRT dose; do not add a separate inferred q24h dose. Review neurotoxicity and session interruptions.')
pirrt('fluconazole',11,'PIRRT',[('Maintenance','400 mg PO/IV every 24 h')],'flow 4–5 L/h; 8–10-hour sessions','No specific timing recommendation. Select infection, loading strategy and susceptibility separately.')
pirrt('ganciclovir',11,'PIRRT · expert opinion',[('Induction','2.5 mg/kg IV every 24 h'),('Maintenance / prophylaxis','1.25 mg/kg IV every 24 h')],'prescription not specified; expert opinion','Administer after daily PIRRT. Confirm dosing weight, indication and CBC monitoring.')
pirrt('meropenem',12,'PIRRT · standard-dose row only',[('Maintenance','1 g IV by extended infusion every 12 h')],'flow 4–5 L/h; 8–10-hour sessions','Give one scheduled dose after daily PIRRT. EI means 3–4 hours in this source. Meningitis/CF/MIC 4 requires a separate reviewed high-dose protocol.')
pirrt('oseltamivir',12,'PIRRT · influenza treatment only',[('Maintenance','75 mg PO every 24 h')],'prescription not specified; expert opinion','Give after daily PIRRT. Prophylaxis has no data in the source; select full treatment duration separately.')
pirrt('piperacillin-tazobactam',12,'PIRRT · extended infusion only',[('Maintenance','4.5 g IV by extended infusion every 8 h')],'flow 6 L/h; 6-hour sessions','Give one scheduled dose after daily PIRRT. EI means 3–4 hours. Do not transfer the existing short-infusion CKD table into this regimen.')
# Locate the existing combination ID without creating a duplicate.
tmp=next(d['id'] for d in data['drugs'] if 'trimethoprim' in d['name'].lower() and 'sulfamethoxazole' in d['name'].lower())
pirrt(tmp,13,'PIRRT · high-dose indications only',[('Stenotrophomonas / Pneumocystis pneumonia','10–15 mg/kg/day of TMP component, divided every 8 h')],'blood and dialysate flow 170 mL/min; 6–8-hour sessions','Amounts are TMP component, not total combination. Prophylaxis and systemic GNR rows have no data. Monitor potassium, marrow and toxicity.')

# Source gaps are explicit, not equivalent to missing curation or contraindication.
for ident in ['acyclovir','cefiderocol','cefoxitin']:
 d=drugs[ident];r=src('nm-pirrt-gap-'+ident,'Nebraska · '+d['name']+' · PIRRT no-data row',RRT+'#page=10','Table 2, PDF p10 explicitly says no data.',file=inventory[3],page=10)
 d['modalities']['sled']=mod(r,notes='The reviewed PIRRT source explicitly reports no data. No dose is inferred from CKD, IHD or CRRT.',status='insufficient_data');mark(d)
valg_rrt=src('nm-pirrt-valganciclovir','Nebraska · Valganciclovir · PIRRT PDF p13',RRT+'#page=13','Table 2; use IV ganciclovir instead.',file=inventory[3],page=13)
drugs['valganciclovir']['modalities']['sled']=mod(valg_rrt,notes='The Nebraska PIRRT/CRRT guide recommends using IV ganciclovir instead. No valganciclovir PIRRT dose is assigned.',status='not_indicated');mark(drugs['valganciclovir'])

# New CRRT profiles use CVVHD flow columns only; never the adjacent anephric column.
for ident,page,loading,profiles in [
 ('acyclovir',4,None,[('IV mucocutaneous HSV',['5 mg/kg IV every 24 h','5 mg/kg IV every 24 h','5 mg/kg IV every 12 h']),('IV VZV / HSV encephalitis',['7.5 mg/kg IV every 24 h','10 mg/kg IV every 24 h','10 mg/kg IV every 12 h'])]),
 ('aztreonam',4,'2 g IV once',[('Systemic infection',['2 g IV every 8 h','2 g IV every 8 h','2 g IV every 6 h'])]),
 ('ceftaroline',6,None,[('Standard',['400 mg IV every 12 h']*3),('Endocarditis / S. aureus bacteremia',['400 mg IV every 8 h']*3)]),
 ('ganciclovir',7,None,[('IV induction',['2.5 mg/kg IV every 24 h','2.5 mg/kg IV every 12 h','2.5 mg/kg IV every 12 h']),('IV maintenance / prophylaxis',['1.25 mg/kg IV every 24 h','1.25 mg/kg IV every 12 h','1.25 mg/kg IV every 12 h'])])]:
 d=drugs[ident];assert d['modalities']['crrt']['status']=='not_curated'
 r=src('nm-cvvhd-'+ident,'Nebraska · '+d['name']+f' · CVVHD PDF p{page}',RRT+f'#page={page}',f'Table 1; PDF p{page}; dialysate flow 1,2,3–4 L/h; footnotes PDF p9.',file=inventory[3],page=page)
 tables=[table(title,list(zip(['CVVHD dialysate 1 L/h','CVVHD dialysate 2 L/h','CVVHD dialysate 3–4 L/h'],values))) for title,values in profiles]
 if loading:tables.insert(0,table('Loading dose',[('CVVHD initiation',loading)]))
 note='CVVHD only, not CVVH/CVVHDF or a universal CRRT regimen. Reassess residual function, treatment interruptions and actual delivered flow. '
 note+=('Evidence above 2 L/h is limited.' if ident=='acyclovir' else 'Higher-flow aztreonam interval is empirical in the source.' if ident=='aztreonam' else 'Ganciclovir flow data above 1–1.5 L/h are limited; verify indication and TDM/toxicity.' if ident=='ganciclovir' else 'Indication-specific institutional recommendations.')
 d['modalities']['crrt']=mod(r,tables,note,setting='Nebraska CVVHD · dialysate flow 1, 2 or 3–4 L/h');d['sourceIds'].append(r);mark(d)

# Historical PK summaries: the source age and dialysis method stay visible.
def fact(value,ref,context,basis=None):
 x=dict(status='sourced',value=value,context=context,sourceIds=[ref])
 if basis:x['basis']=basis
 return x
def missing():return dict(status='not_curated',value=None,context='No prescription-specific removal value curated.',sourceIds=[])
def removal(ref,value,status,context):return dict(status=status,value=value,context=context,sourceIds=[ref])
pk_rows=[
 ('acyclovir',33,'2.9 h','19.5 h','0.7 L/kg','9–33%','removed','Not removed','IV aciclovir; the separate on-dialysis half-life 5.7 h is not the ESRF baseline.'),
 ('amoxicillin',80,'1–1.5 h','7–20 h','0.3 L/kg','20%','removed','Not removed','Parent amoxicillin; no clavulanate PK is implied.'),
 ('aztreonam',124,'1.7 h','6–8 h','0.5–1 L/kg','60%','removed','Not removed','Systemic aztreonam reference; not an inhaled-formulation dosing recommendation.'),
 ('cephalexin',197,'1 h','16 h','0.35 L/kg','15%','removed','Removed','Book uses the spelling cefalexin.'),
 ('cefixime',198,'3–4 h','11.5 h','0.11–0.6 L/kg','65%','conventional_no_highflux_unknown','Not removed','Historical conventional-HD and high-flux statements differ in certainty.'),
 ('ceftaroline',201,'2.5 h','Increased; no numeric ESRF value supplied','20.3 L','20%','removed','Removed','Active ceftaroline. The book value explicitly says Litres despite an L/kg row heading; it is retained as total L.'),
 ('ceftazidime',202,'2 h','13–25 h','0.28–0.4 L/kg','<10%','removed','Removed','Parent ceftazidime; not the avibactam combination.'),
 ('cefuroxime',206,'1.2 h','17 h','0.13–1.8 L/kg','50%','removed','Removed','Oral cefuroxime-axetil monograph. Broad historical Vd range is retained without choosing one value.'),
 ('ciprofloxacin',235,'3–5 h','8 h','2.5 L/kg','20–40%','conventional_no_highflux_unknown','Not removed','Method-specific removal uncertainty is retained.'),
 ('clarithromycin',242,'3–7 h','Prolonged; no numeric ESRF value supplied','2–4 L/kg','80%','conventional_no_highflux_unknown','Not removed','Reference parent-drug values; active-metabolite handling differs.'),
 ('clindamycin',245,'2–3 h','3–5 h','0.6–1.2 L/kg','>90%','conventional_no_highflux_unknown','Not removed','No dialysis supplement is calculated.'),
 ('doxycycline',365,'18 h','Unchanged in the cited table','0.7 L/kg','>90%','conventional_no_highflux_unknown','Not removed','Reference values from the fifth-edition table.'),
 ('ertapenem',402,'4 h','14 h','0.1 L/kg','85–95%','removed','Removed','Protein binding and exposure can vary in critical illness.'),
 ('fluconazole',453,'30 h','98 h','0.65–0.7 L/kg','11–12%','removed','Removed','Reference parent-drug values.'),
 ('ganciclovir',492,'2.9 h','28.5 h','0.54–0.87 L/kg','<2%','removed','Removed','IV ganciclovir monograph; not valganciclovir parent-drug PK.'),
 ('levofloxacin',603,'6–8 h','35 h','1.1–1.5 L/kg','30–40%','not_removed','Not removed','Systemic reference; the book separately lists nebulised half-life 5–7 h.'),
 ('linezolid',611,'5–7 h','Unchanged in the cited table','0.6 L/kg','31%','removed','Possibly removed','PD removal is described as likely, not measured removal extent.'),
 ('meropenem',654,'1 h','6–13.7 h','0.35 L/kg','2%','removed','Removed','Historical reference values; ESRF half-life is a range and is not the on-dialysis elimination half-life.'),
 ('metronidazole',671,'5.6–11.4 h','7–21 h','0.7–1.5 L/kg','10–20%','removed','Not removed','Reference parent-drug values; metabolite accumulation is a separate issue.'),
 ('moxifloxacin',698,'12 h','Unchanged in the cited table','2 L/kg','30–50%','unknown','Unknown','This book reports unknown dialysis removal; no removal value is inferred from a no-adjustment regimen.'),
 ('rifampicin',898,'2–5 h','1.8–11 h','0.64–0.66 L/kg','80%','not_removed','Not removed','Reference range from the fifth edition; induction and repeated dosing can alter kinetics.'),
 ('piperacillin-tazobactam',981,'Piperacillin 1 h; tazobactam 1 h','Piperacillin 4–6 h; tazobactam 7 h','Piperacillin 0.18–0.3 L/kg; tazobactam 0.18–0.33 L/kg','20–30% each','removed','Source differences','Book APD/CAPD category says not dialysed but its other-information text reports 6–21% PD removal; do not treat that category as zero clearance.'),
 ('teicoplanin',987,'150 h','62–230 h','0.94–1.4 L/kg','90–95%','method_dependent','Not removed','Historical reference half-life; conventional HD and high-flux removal categories differ.'),
 ('tigecycline',1017,'42 h','Probably unchanged in the cited table','7–9 L/kg','71–89%','conventional_no_highflux_unknown','Not removed','The ESRF statement is qualified as probable in the source.'),
 ('vancomycin',1066,'6 h','120–216 h','0.47–1.1 L/kg; CKD5 0.88 L/kg','10–50%; CKD5 19%','method_dependent','Not removed','Systemic/IV PK only. Oral vancomycin systemic exposure cannot be assumed from these values.'),
 ('voriconazole',1089,'About 6 h; dose dependent','Unchanged in the cited table','4.6 L/kg','58%','removed','Possibly removed','Nonlinear and dose-dependent PK; a historical removal category is not evidence that HD requires a replacement dose.')]
for ident,page,half,renal,vd,pb,hd,pd,note in pk_rows:
 d=drugs[ident];assert d['pharmacokinetics']['status']=='not_curated',ident
 r=src('rdh5-'+ident,f'Renal Drug Handbook 5th · {d["name"]} · supplied PDF p{page} (printed {page-19})',BOOK,f'Supplied fifth edition, published 2018 (©2019), PK/removal fields; PDF p{page}, printed p{page-19}. Link opens publisher listing, not the uploaded book.','Supplied handbook · historical PK reference',inventory[0],page)
 hs={'removed':('Removed in book HD/high-flux categories','removed'),'not_removed':('Not removed in book HD/high-flux categories','not_removed'),'unknown':(None,'unknown'),'conventional_no_highflux_unknown':('Conventional HD: not removed; high-flux: unknown','limited'),'method_dependent':('Conventional HD: not removed; high-flux: removed','limited')}[hd]
 pdstatus='unknown' if pd=='Unknown' else 'source_difference' if pd=='Source differences' else 'limited' if pd=='Possibly removed' else 'not_removed' if pd=='Not removed' else 'removed'
 d['pharmacokinetics']=dict(status='source_summary',sourceCheckedAt=DATE,evidenceDate='2018 (©2019)',historical=True,
 halfLife=fact(half,r,'Reference/normal-function column; '+note),renalHalfLife=fact(renal,r,'ESRF column, not an on-dialysis half-life.','handbook_normal_esrf_columns'),volumeOfDistribution=fact(vd,r,note),proteinBinding=fact(pb,r,'Historical plasma binding reference; disease state and assay can change the unbound fraction.'),
 dialysability=dict(ihd=removal(r,hs[0],hs[1],'Historical book categories; membrane/method and modern clearance extent are not independently verified. '+note),pd=removal(r,None if pd=='Unknown' else pd,pdstatus,'Historical APD/CAPD category. This does not establish a PD dose or quantitative clearance. '+note),crrt=missing(),sled=missing()),
 notes='Historical PK reference: Renal Drug Handbook, 5th edition, published 2018 (©2019). Source checked today does not mean a new PK study or independent clinical approval. '+note)
 mark(d)

drugs['meropenem']['formulation']='IV · existing short-infusion tables; PIRRT extended infusion'
drugs['meropenem']['summary']='Select the treatment setting: existing tables use short infusion; the new PIRRT row uses a 3–4-hour extended infusion.'
drugs['piperacillin-tazobactam']['formulation']='IV · short infusion in existing tables; PIRRT extended infusion'
drugs['piperacillin-tazobactam']['summary']='Existing short-infusion/non-Pseudomonas tables and the new extended-infusion PIRRT regimen are separate; select the setting and indication.'
bc_ref=src('bc-oral-2018-comparison','BC Renal · supplied oral antimicrobial sheet · PDF p1','https://www.bcrenal.ca/','Supplied February 2018 sheet, PDF p1: cefuroxime and clarithromycin comparisons. Public link is the organisation homepage, not this supplied file.','Supplied institutional sheet · historical comparison',inventory[2],1)
drugs['cefuroxime']['evidenceNotes'][0]['sourceIds'] += [bc_ref,'rdh5-cefuroxime']

# Audited source differences/gaps are part of the release, not silently resolved.
for ident,pages in {'aztreonam':[11,12],'cefpodoxime':[16,17],'ganciclovir':[33,34]}.items():
 r=sources['nm07-'+ident];r['suppliedDocument']['additionalPdfPages']=pages[1:];r['section']+=' Continued adult rows on PDF pages '+', '.join(map(str,pages))+'.'
data['sourceAudit']=inventory
data['sourceConflicts']=[
 dict(drug='cefuroxime',issue='Oral renal intervals differ between current tablet label, Nebraska protocol, BC 2018 sheet and handbook fifth edition.',action='Active oral table follows the current tablet label; IV and PD are not inferred.',status='source_difference_retained'),
 dict(drug='clarithromycin',issue='Nebraska PD no-adjustment row differs from older source reductions.',action='Numeric PD regimen withheld; immediate-release CKD/IHD source retained.',status='clinical_reconciliation_pending'),
 dict(drug='flucytosine',issue='Nebraska HD/PD grouped post-dialysis three-times-weekly wording does not define a continuous-PD schedule.',action='Only IHD schedule displayed; PD requires specialist review.',status='source_ambiguity_retained'),
 dict(drug='valganciclovir',issue='Institutional very-low-dose HD schedules and mixed-analyte handbook PK need formulation/analyte reconciliation.',action='Non-dialysis induction/maintenance only. No numeric HD/PD dose or mixed-analyte PK profile imported.',status='clinical_reconciliation_pending'),
 dict(drug='levofloxacin',issue='PIRRT row lacks an unambiguous interval in its main dose cell; comments refer to different reference regimens.',action='PIRRT numeric regimen not imported. Existing CKD/IHD remains unchanged.',status='source_ambiguity_retained'),
 dict(drug='piperacillin-tazobactam',issue='Book PD categorical statement and reported removal percentage differ in the same monograph.',action='Both are qualified in PK evidence; no PD regimen inferred.',status='source_difference_retained')]
data.update(version='0.7.0',schemaVersion='1.5.0',softwareReleaseDate=DATE)
data['coverage']={k:sum(d['entryType']==k for d in data['drugs']) for k in ['renal','safety','catalog']}
data['pharmacokineticCoverage']=dict(profiles=sum(d['pharmacokinetics']['status']=='source_summary' for d in data['drugs']),allFourCoreFields=sum(all(d['pharmacokinetics'][k]['status']=='sourced' for k in ['halfLife','volumeOfDistribution','proteinBinding']) and d['pharmacokinetics']['dialysability']['ihd']['value'] is not None for d in data['drugs']))
changed=[d['id'] for d in data['drugs'] if d!=before[d['id']]]
data['referenceScope'].update(newEntries=0,updatedEntries=len(changed));data['sources']=list(sources.values())
data['releaseChanges']=dict(version='0.7.0',changedIds=changed,newRenalIds=[d['id'] for d in data['drugs'] if before[d['id']]['entryType']=='catalog' and d['entryType']=='renal'],newPKIds=[r[0] for r in pk_rows],pirrtSummaryIds=[d['id'] for d in data['drugs'] if d['modalities']['sled']['status']=='summarized'])
for ident in ['cefuroxime','clarithromycin','flucytosine','valganciclovir']:
 if not drugs[ident].get('evidenceNotes'):drugs[ident]['evidenceNotes']=[]
 for c in data['sourceConflicts']:
  if c['drug']==ident and ident!='cefuroxime':drugs[ident]['evidenceNotes'].append(dict(title='Source reconciliation',text=c['issue']+' '+c['action'],sourceIds=drugs[ident]['sourceIds']))
for item in inventory:
 data['referenceResources'].append(dict(id='upload-'+str(inventory.index(item)),organisation='User-supplied reference',title=item['title'],url=NM if item is inventory[4] else RRT if item is inventory[3] else BOOK if item is inventory[0] else 'https://doi.org/10.1038/ki.2011.322' if item is inventory[1] else 'https://www.bcrenal.ca/',role=item['selectedUse'],access=item['editionOrDate']+'. Selected sections reviewed; full-file clinical review not claimed.',use='Original PDF remains a research input. Citations use page locators and the supplied-file checksum; original PDF is not in the GitHub package.',sourceCheckedAt=DATE))
(D/'database.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
(D/'REFERENCE_DIRECTORY.json').write_text(json.dumps(data['referenceResources'],ensure_ascii=False,indent=2))
(D/'SOURCE_AUDIT.json').write_text(json.dumps(dict(files=inventory,conflicts=data['sourceConflicts'],changes=data['releaseChanges']),ensure_ascii=False,indent=2))
queue=[]
for d in data['drugs']:
 p=d['pharmacokinetics'];queue.append(dict(id=d['id'],name=d['name'],category=d['category'],routes=d['routes'],content=d['entryType'],renalDoseSourceCheckedAt=d['review']['sourceCheckedAt'],pkSourceCheckedAt=p['sourceCheckedAt'],modalities={k:v['status'] for k,v in d['modalities'].items()},pkFields={k:p[k]['status'] for k in ['halfLife','renalHalfLife','volumeOfDistribution','proteinBinding']},removal={k:v['status'] for k,v in p['dialysability'].items()},independentClinicalReview=d['review']['status'],priority='1: common rounds classes' if d['category'] in ['Cardiovascular','Antimicrobials','Diabetes & endocrine','Anticoagulation & haematology','Pain & neurology','OTC & medicine safety'] else '2: remaining formulary'))
(D/'CURATION_QUEUE.json').write_text(json.dumps(dict(version=data['version'],generatedAt=DATE,note='Statuses describe curation coverage, not suitability for an individual patient. Summarized does not mean clinically approved or complete for every indication.',drugs=queue),ensure_ascii=False,indent=2))
print(json.dumps(dict(version=data['version'],coverage=data['coverage'],pk=data['pharmacokineticCoverage'],changed=len(changed),newRenal=len(data['releaseChanges']['newRenalIds']),pirrt=len(data['releaseChanges']['pirrtSummaryIds']))))

# Current documentation is generated from the same final data as the application.
counts=data['coverage'];pk=data['pharmacokineticCoverage']
head=f'''# Changelog

## v0.7.0 — 29 October 2026

- Reviewed selected sections of five supplied references; original PDFs are not redistributed.
- Promoted 20 existing catalog entries to selected adult renal profiles: {', '.join(data['releaseChanges']['newRenalIds'])}.
- Added 26 historical fifth-edition handbook PK/removal summaries with individual PDF page locators and visible 2018 (©2019) labels. Modern high-flux removal and continuous therapies are not inferred from historical conventional-HD categories.
- Added 16 prescription-specific PIRRT summaries and four CVVHD profiles. Retained session/flow assumptions, indication, infusion and dose timing. Existing CKD/IHD/PD/CRRT tables on previously curated renal entries are unchanged.
- Retained six source disagreements/ambiguities, including oral cefuroxime label intervals, clarithromycin PD, flucytosine PD timing, valganciclovir formulation/analyte issues, levofloxacin PIRRT and piperacillin/tazobactam PD removal.
- 668 indexed entries: {counts['renal']} renal profiles, {counts['safety']} shared safety notes and {counts['catalog']} renal-dose-pending catalog records. {pk['profiles']} PK profiles; {pk['allFourCoreFields']} contain all four core items.
- These are selected source summaries. Independent clinical approval and BNF monograph reconciliation remain pending.

'''
(D/'CHANGELOG.md').write_text(head+(ROOT/'changelog_v06.md').read_text())
plan=f'''# Clinical completion plan · v0.7.0

668 indexed drug/formulation entries: {counts['renal']} renal profiles, {counts['safety']} shared safety notes and {counts['catalog']} renal-dose-pending catalog entries. {pk['profiles']} source-based PK profiles, including 26 historical handbook summaries. No entry has independent clinical approval.

## Next clinical work

1. Confirm the local adult formulary and prioritise common rounds drugs, oral/parenteral formulations and OTC products.
2. Complete each indication/route-specific kidney-function table using current product information and licensed references. CrCl, indexed eGFR and CKD stage are not substitutes for each other.
3. Reconcile the six issues in SOURCE_AUDIT.json with a renal pharmacist. Do not fill continuous-PD schedules from intermittent-HD wording or mix parent/prodrug analytes.
4. Replace or corroborate historical handbook PK with contemporary measured evidence. Preserve analyte, Vd units, conventional versus high-flux HD and within/between-session half-lives.
5. Complete IHD, systemic PD and CRRT/PIRRT evidence separately. Record delivered modality, session length, dialysate/effluent flows, residual function, loading, infusion duration, timing and TDM requirements. No intraperitoneal peritonitis regimen is implied.
6. Obtain authorised BNF (British National Formulary) and PDR monograph access for comparison. BNF verification is not claimed; the supplied handbook is a different reference.
7. Record independent nephrologist and renal-pharmacist review, names, dates and resolution of source conflicts before a clinical release.
8. After GitHub upload, verify HTTPS offline reopen and update activation on a physical phone.

CURATION_QUEUE.json records field/modality gaps for every entry. “Summarized” means a selected source summary, potentially nonnumeric; it does not mean a complete or approved prescribing monograph. Unknown, not reported and not curated remain separate.
'''
(D/'COMPLETION_PLAN.md').write_text(plan)
guide=D/'EDITORIAL_GUIDE.md';g=guide.read_text().split('\n## v0.7 supplied-reference rules')[0].replace('113 sourced renal profiles','133 sourced renal profiles').replace('527 renal-dose-pending','507 renal-dose-pending')
g=g.replace('Version 0.4.0 ·','Version 0.7.0 ·').replace('Most PD and all SLED entries remain gaps.','Most PD and PIRRT/SLED entries remain gaps; 16 selected prescription-specific PIRRT summaries are included.').replace('Run `python3 build_data.py` and `python3 build_standalone.py` to rebuild the bundled application, then `node checks.mjs`', 'Run `python3 build_data.py`, `python3 release_v06.py`, `python3 release_v07.py` and `python3 build_standalone.py` in order, then `node checks.mjs` and `node checks_v07.mjs`').replace('27 cardiovascular/BP medicines have PK summaries; 15 have all four core reference items', 'At the v0.4 release, 27 cardiovascular/BP medicines had PK summaries; 15 had all four core reference items')
g+='''\n## v0.7 supplied-reference rules\n\nUse SOURCE_AUDIT.json for file hashes, edition dates, review scope and conflicts. PDF metadata is not a clinical revision date. Each imported numeric table has an individual source/page record; continued pages are retained. Handbook PK is historical and cannot establish a current dialysis replacement dose. Do not collapse “not dialysed” into measured zero clearance or carry conventional-HD conclusions into modern high-flux therapy. Categorical removal is not a numeric supplemental-dose recommendation. Read product route and analyte before using PK. The supplied PDFs remain research inputs outside the public package. Selected summaries are original condensations; full monographs are not republished.\n'''
guide.write_text(g)
audit='# Supplied-source audit · v0.7.0\n\nSelected sections reviewed on '+DATE+'. This is not a full clinical review of all five documents. Metadata dates do not establish clinical currency. Original PDFs are excluded from this package.\n\n'
for f in inventory:
 audit+=f"## {f['title']}\n\n- Edition/date: {f['editionOrDate']}\n- Supplied filename: {f['fileName']}\n- PDF pages: {f['pages']}\n- SHA-256: `{f['sha256']}`\n- Use: {f['selectedUse']}\n- Scope: {f['reviewScope']}\n\n"
audit+='## Source disagreements and gaps\n\n'
for c in data['sourceConflicts']:audit+=f"### {c['drug']}\n\n{c['issue']}\n\nAction: {c['action']}\n\nStatus: {c['status']}\n\n"
audit+='See database.json sources[].suppliedDocument for per-drug PDF pages, continuation pages and checksums. Public publisher/organisation links are identified as listings where they do not provide the exact supplied PDF. Source access is separate from independent clinical approval.\n'
(D/'SOURCE_AUDIT.md').write_text(audit)
(D/'VERIFICATION.md').write_text('''# v0.7.0 verification — 29 October 2026

668 indexed records: 133 selected renal profiles, 28 shared safety notes and 507 renal-dose-pending catalog records. 53 source-based PK profiles; 40 contain all four core items. Every entry remains independently unapproved.

## Source review scope

Selected sections of five supplied PDFs were reviewed, not every monograph in the handbook. Individual imported source pages, continued pages, file hashes, edition/date and six source disagreements are recorded in SOURCE_AUDIT.json and sources[].suppliedDocument. PK table crops were visually inspected for all 26 handbook additions; dialysis-category text was checked separately. Superscript references were distinguished from digits, ceftaroline total-L Vd from L/kg, conventional HD from high-flux, and the adjacent anephric column from CVVHD flow columns. Current oral cefuroxime and oral/IV voriconazole labels were checked to reconcile specific source differences. A source check is not independent clinical validation.

## Automated checks

- checks.mjs checks all drug/source IDs, approved-review state, schema, embedded data/document equality, unchanged pre-existing CKD/IHD/PD/CRRT tables and clinically important original edge cases.
- checks_v07.mjs compares against the full v0.6 baseline: 621 unrelated records and all 27 existing PK summaries are unchanged; the 47 changed records cover the declared additions. Existing source records and shared guidance remain unchanged.
- Specific regressions cover Vd units/superscripts, high-flux uncertainty, unknown versus not-curated removal, oral versus IV restrictions, daily versus post-session HD, withheld continuous-PD schedules, TMP component units, PIRRT source/page/session/timing and CVVHD flow columns.
- Actual app search functions cover brand/exact-name ordering, spelling suggestions, setting/PK/latest filters and queue/reference exports. The 668-drug completion queue matches the final data.
- Actual service-worker logic is exercised with simulated network/caches: install, offline reopen, deliberate update activation, wrong-release/checksum/404 rejection and per-path cache isolation.
- ZIP CRC and root SHA-256 checksums are verified. A fresh extraction rebuild is compared with the packaged runtime/data/documents.

## Browser checks

The managed HTTP preview displayed the final release. Cefuroxime showed the current oral-label table and source-disagreement notice. At 320- and 390-pixel iframe widths, ceftaroline/meropenem search, PK and PIRRT sections had no horizontal page overflow. Ceftaroline Vd displayed 20.3 L; meropenem displayed the 3–4-hour infusion/timing note and prescription conditions. These are responsive-browser checks, not physical-phone performance or bedside validation.

## Remaining checks and limitations

Independent nephrologist and renal-pharmacist review, full formulary/indication coverage, authorised BNF monograph comparison and resolution of retained source conflicts remain incomplete. The historical PK additions are clearly dated 2018 (©2019). No modern circuit clearance or supplemental dose was calculated from PK properties. No intraperitoneal peritonitis regimen is implied.

The internal HTTP preview cannot activate the offline worker. Check HTTPS installation, airplane-mode reopen, update activation and storage persistence on a physical phone after GitHub upload. External clinical source links need internet. Software checks cannot establish clinical validity.
''')
