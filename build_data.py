import json
from pathlib import Path

ROOT = Path(__file__).parent
DATE = '2026-10-29'
drugs = []
sources = {}
def source(key, name, url, section, kind='Institutional guidance'):
    sources[key] = dict(id=key, title=name, url=url, section=section, type=kind, accessed=DATE)
    return key
def u(key, slug):
    return source(key, 'UCSF IDMP · '+key, 'https://idmp.ucsf.edu/content/'+slug, 'Adult non-dialysis and intermittent/continuous haemodialysis tables')
def label(key, sid, section='Dosage and administration; renal impairment'):
    return source(key, 'DailyMed · '+key, 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid='+sid, section, 'US prescribing information')
def table(indication, bands, doses):
    assert len(bands)==len(doses)
    return dict(indication=indication, rows=[dict(context=a, dose=b) for a,b in zip(bands,doses)])
def modality(tables=None, notes='', status=None, refs=None):
    return dict(status=status or ('summarized' if tables else 'not_curated'), tables=tables or [], notes=notes, sourceIds=refs or [])
def single(indication, context, dose):
    return [table(indication,[context],[dose])]
def add(id, name, brands, group, cls, metric, summary, nd, hd=None, cr=None, pd=None, notes='', refs=None, flag='adjust', formulation='See dose rows'):
    drugs.append(dict(id=id, name=name, aliases=brands, category=group, drugClass=cls, formulation=formulation, kidneyMetric=metric, summary=summary, flag=flag,
        modalities=dict(ckd=modality(nd),ihd=hd or modality(),crrt=cr or modality(),pd=pd or modality(),sled=modality()),
        considerations=notes, sourceIds=refs or [id], review=dict(status='clinical_review_pending',sourceCheckedAt=DATE,clinicalReviewer=None,clinicalApprovedAt=None),
        completeness='Selected adult indications only. Full interaction, adverse-effect and contraindication monograph not yet curated.'))

CRCL='CrCl · mL/min (source bands)'
EGFR='eGFR · mL/min/1.73 m²'
AB='Antimicrobials'
u('amoxicillin','amoxicillin')
b=['>30','10–29','<10']
add('amoxicillin','Amoxicillin',['Amoxil'],AB,'Aminopenicillin',CRCL,'Dose interval increases as kidney function falls.',[
 table('Symptomatic Enterococcus UTI',b,['500 mg PO every 8 h','500 mg PO every 12 h','500 mg PO every 24 h']),
 table('Severe infection / selected outpatient CAP',b,['1 g PO every 8 h','1 g PO every 12 h','500 mg PO every 12 h'])],
 modality(single('Enterococcus UTI','High-flux IHD','500 mg PO once now, then every evening')+single('Severe infection / selected CAP','High-flux IHD','500 mg PO every 12 h')),
 modality(single('Enterococcus UTI','CVVHD','500 mg PO every 8 h')+single('Severe infection / selected CAP','CVVHD','1 g PO every 8 h'), 'Limited data; UCSF local expert opinion.'),formulation='Oral')

u('amoxicillin-clavulanate','amoxicillin-clavulanate')
label('augmentin-label','af4c2ea8-73bd-429b-8392-fa20fec6fb3f','2.6 renal impairment; formulation restrictions')
add('amoxicillin-clavulanate','Amoxicillin / clavulanate',['Augmentin','Co-amoxiclav'],AB,'Penicillin + β-lactamase inhibitor',CRCL,'Use the correct amoxicillin/clavulanate strength.',[
 table('Most indications (immediate release)',b,['875/125 mg PO every 12 h','500/125 mg PO every 12 h','500/125 mg PO every 24 h'])],
 modality(single('Most indications','High-flux IHD','500/125 mg PO once now, then every evening'), 'UCSF regimen. Label dialysis supplementation differs; reconcile with local policy.'),
 modality(single('Most indications','CVVHD','500/125 mg PO every 12 h')),
 notes='US label: do not use the 875/125 mg tablet at GFR <30 mL/min. Different clavulanate ratios are not interchangeable. Bloodstream-infection regimens are not included.',refs=['amoxicillin-clavulanate','augmentin-label'],formulation='Immediate-release oral tablets')

u('cefazolin','cefazolin')
add('cefazolin','Cefazolin',['Ancef','Kefzol'],AB,'First-generation cephalosporin',CRCL,'Separate uncomplicated and complicated infections.',[
 table('Uncomplicated Gram-positive infection',b,['1 g IV every 8 h','1 g IV every 12 h','1 g IV every 24 h']),
 table('Complicated Gram-positive / Gram-negative infection',b,['2 g IV every 8 h','2 g IV every 12 h','1 g IV every 24 h'])],
 modality(single('UCSF regimen','High-flux IHD','2 g IV once now and after HD'), 'Alternative for stable three-times-weekly HD: 2 g / 2 g / 3 g after HD; 3 g precedes the 72-hour interval.'),
 modality(single('UCSF regimen','CVVHD','2 g IV every 12 h')),
 notes='Deep-seated MSSA infection or clinical instability may require higher dosing with ID/pharmacy input.',formulation='IV')

u('cefepime','cefepime')
label('cefepime-label','c654ef2e-1067-4026-8931-6a0dc2a17ad1','2.3 renal dosing; 5.2 neurotoxicity')
b4=['>60','30–60','10–29','<10']
add('cefepime','Cefepime',['Maxipime'],AB,'Fourth-generation cephalosporin',CRCL,'Adjust dose and interval. Check the indication and dialysis protocol.',[
 table('Non-severe infection · short infusion',b4,['2 g IV every 12 h','2 g IV every 24 h','1 g IV every 24 h','500 mg IV every 24 h']),
 table('Severe infection / meningitis / febrile neutropenia / Pseudomonas · short infusion',b4,['2 g IV every 8 h','2 g IV every 12 h','2 g IV every 24 h','1 g IV every 24 h'])],
 modality(single('UCSF high-flux regimen','IHD','2 g IV once now and after HD'), 'DIFFERENT SOURCE REGIMENS: US label uses 1 g day 1, then 500 mg every 24 h (1 g every 24 h for febrile neutropenia), after HD on dialysis days. Choose an approved local protocol; do not combine regimens.', refs=['cefepime','cefepime-label']),
 modality(single('UCSF regimen','CVVHD','1 g IV every 8 h'), 'Extended infusion requires ID/pharmacy guidance.'),
 modality(single('Systemic IV therapy · not intraperitoneal','CAPD','Usual indication-specific unit dose (500 mg, 1 g or 2 g) IV every 48 h'), 'US label Table 2; verify the unit dose against the normal-function regimen. APD and intraperitoneal peritonitis dosing are not curated.', refs=['cefepime-label']),
 notes='Neurotoxicity is a labelled risk in renal impairment, including encephalopathy, myoclonus and seizures. UCSF short-infusion bands and US label bands differ; check boundary values in the source.',refs=['cefepime','cefepime-label'],formulation='IV · short infusion')

u('ceftriaxone','ceftriaxone')
ct=[table('Standard systemic dosing',['All renal-function bands'],['2 g IV every 24 h']),table('UTI',['All renal-function bands'],['1 g IV every 24 h']),table('Meningitis / enterococcal endocarditis (with ampicillin)',['All renal-function bands'],['2 g IV every 12 h'])]
add('ceftriaxone','Ceftriaxone',['Rocephin'],AB,'Third-generation cephalosporin','No renal adjustment in cited guidance','No routine renal adjustment in the selected UCSF regimens.',ct,modality(ct,'No haemodialysis adjustment in the cited guidance.'),modality(ct),notes='Obesity may warrant higher doses depending on the clinical setting; discuss with ID/pharmacy.',flag='no_adjust',formulation='IV')

u('cephalexin','cephalexin')
add('cephalexin','Cephalexin',['Cefalexin','Keflex'],AB,'First-generation cephalosporin',CRCL,'This starter entry covers Gram-negative bloodstream infection only.',[
 table('Gram-negative bloodstream infection · selected oral therapy',['>50','30–50','15–29','<15'],['1 g PO every 6 h','1 g PO every 8 h','1 g PO every 12 h','500 mg PO every 8 h'])],
 modality(single('Gram-negative bloodstream infection','IHD','500 mg PO every 12 h')),
 modality(notes='UCSF lists no continuous-HD data.',status='insufficient_data'),
 notes='Common skin-infection and cystitis regimens have not been curated here. Do not apply the bloodstream-infection regimen to those indications.',formulation='Oral')

u('ciprofloxacin','ciprofloxacin')
b3=['>50','30–50','<30']
add('ciprofloxacin','Ciprofloxacin',['Cipro','Ciproxin'],AB,'Fluoroquinolone',CRCL,'Route and indication change the regimen.',[
 table('Standard dosing',b3,['400 mg IV every 12 h OR 500 mg PO every 12 h','400 mg IV every 12 h OR 500 mg PO every 12 h','400 mg IV every 24 h OR 500 mg PO every 24 h']),
 table('Pseudomonas / Gram-negative bloodstream infection',b3,['400 mg IV every 8 h OR 750 mg PO every 12 h','400 mg IV every 12 h OR 500 mg PO every 12 h','400 mg IV every 24 h OR 500 mg PO every 24 h'])],
 modality(single('UCSF regimen','IHD','400 mg IV OR 500 mg PO every evening')),
 modality(single('UCSF regimen','CVVHD','400 mg IV every 8 h OR 500 mg PO every 12 h')),formulation='IV or oral')

u('levofloxacin','levofloxacin')
add('levofloxacin','Levofloxacin',['Levaquin','Tavanic'],AB,'Fluoroquinolone',CRCL,'Preserve the initial dose when the source specifies one.',[
 table('UTI',['>50','20–49','<20'],['500 mg IV/PO every 24 h','500 mg once, then 250 mg IV/PO every 24 h','500 mg once, then 250 mg IV/PO every 48 h']),
 table('Other indications, including Gram-negative bloodstream infection',['>50','20–49','<20'],['750 mg IV/PO every 24 h','750 mg IV/PO every 48 h','750 mg once, then 500 mg IV/PO every 48 h'])],
 modality(single('Standard','IHD','500 mg once, then 250 mg IV/PO every 48 h')+single('Pneumonia / GNR bloodstream / Pseudomonas','IHD','750 mg once, then 500 mg IV/PO every 48 h')),
 modality(single('Standard','CVVHD','750 mg IV/PO once, then 250 mg IV/PO every 24 h')+single('Pneumonia / GNR bloodstream / Pseudomonas','CVVHD','750 mg IV/PO once, then 500 mg IV every 24 h')),
 notes='Separate oral doses from calcium, magnesium and other polyvalent cations by at least 2 hours per UCSF.',formulation='IV or oral')

u('meropenem','meropenem')
add('meropenem','Meropenem',['Merrem','Meronem'],AB,'Carbapenem',CRCL,'Short-infusion regimens shown; extended infusions need a separate protocol.',[
 table('Standard · short infusion',['>50','26–50','10–25','<10'],['1 g IV every 8 h','1 g IV every 12 h','500 mg IV every 12 h','500 mg IV every 24 h']),
 table('Meningitis / cystic fibrosis · short infusion',['>50','26–50','10–25','<10'],['2 g IV every 8 h','2 g IV every 12 h','1 g IV every 12 h','1 g IV every 24 h'])],
 modality(single('Standard','IHD','500 mg IV once now, then every evening')+single('Meningitis / cystic fibrosis','IHD','1 g IV once now, then every evening')),
 modality(single('Standard','CVVHD','1 g IV every 8 h')+single('Meningitis / cystic fibrosis','CVVHD','2 g IV every 12 h'), 'Discuss flow rates >2 L/h with ID/pharmacy.'),formulation='IV · short infusion')

u('ertapenem','ertapenem')
label('ertapenem-label','44496f7c-8407-4765-9cd6-1daa619a6db6','2.4–2.5 renal impairment and haemodialysis')
add('ertapenem','Ertapenem',['Invanz'],AB,'Carbapenem',CRCL,'Reduce maintenance dosing in severe renal impairment.',[
 table('Selected adult infections',['>30','≤30'],['1 g IV every 24 h','500 mg IV every 24 h'])],
 modality(single('UCSF daily regimen','IHD','500 mg IV once now, then every evening'), 'Post-HD-only regimens require specialist approval because of toxicity risk. The US label specifies a 150 mg post-HD supplement if the daily dose was given within 6 hours before HD.'),
 modality(single('UCSF regimen','CVVHD','1 g IV every 24 h')),
 notes='At CrCl exactly 30, the ≤30 band follows the US label; the UCSF page uses >30 / <30. Peritoneal-dialysis and haemofiltration data are absent in the label.',refs=['ertapenem','ertapenem-label'],formulation='IV')

for id,name,brands,cls,dose in [('doxycycline','Doxycycline',['Vibramycin'],'Tetracycline','100 mg IV/PO every 12 h')]:
    u(id,id)
    t=single('UCSF adult regimen','All renal-function bands',dose)
    add(id,name,brands,AB,cls,'No renal adjustment in cited guidance','No renal adjustment in the cited adult regimen.',t,modality(t),modality(t),flag='no_adjust',formulation='IV or oral')

u('azithromycin','azithromycin')
az=[table('Community-acquired pneumonia · ICU',['All renal-function bands'],['500 mg IV/PO every 24 h']),table('Community-acquired pneumonia · non-ICU',['All renal-function bands'],['500 mg IV/PO once, then 250 mg every 24 h'])]
add('azithromycin','Azithromycin',['Zithromax'],AB,'Macrolide','No renal adjustment in cited guidance','Selected CAP regimens; no renal or dialysis adjustment.',az,modality(az),modality(az),flag='no_adjust',formulation='IV or oral')

u('clindamycin','clindamycin')
cl=[table('Uncomplicated infection',['All renal-function bands'],['600 mg IV every 8 h OR 450 mg PO every 8 h']),table('Necrotising soft-tissue / group A streptococcal infection / PID',['All renal-function bands'],['900 mg IV every 8 h'])]
add('clindamycin','Clindamycin',['Dalacin','Cleocin'],AB,'Lincosamide','No renal adjustment in cited guidance','No renal adjustment in the selected adult regimens.',cl,modality(cl),modality(cl),flag='no_adjust',formulation='IV or oral')

u('metronidazole','metronidazole')
md=[table('Standard',['>10','<10'],['500 mg IV/PO every 8 h','500 mg IV/PO every 12 h']),table('Intra-abdominal infection (excluding C. difficile)',['All renal-function bands'],['500 mg IV/PO every 12 h'])]
mt=single('Standard','Dialysis regimen','500 mg IV/PO every 8 h')+single('Intra-abdominal infection (excluding C. difficile)','Dialysis regimen','500 mg IV/PO every 12 h')
add('metronidazole','Metronidazole',['Flagyl'],AB,'Nitroimidazole',CRCL,'Standard and intra-abdominal regimens differ.',md,modality(mt),modality(mt),notes='The source uses >10 / <10; the boundary of exactly 10 requires clarification. Hepatic adjustment is outside this entry.',formulation='IV or oral')

u('linezolid','linezolid')
li=single('Selected systemic bacterial infections','All renal-function bands','600 mg IV/PO every 12 h')
add('linezolid','Linezolid',['Zyvox'],AB,'Oxazolidinone','No routine renal adjustment in cited guidance','No routine adjustment; prolonged courses need additional review.',li,modality(li),modality(li),
 notes='For stable patients with CrCl <30 and a planned course >10 days, UCSF notes some experts consider 300 mg every 12 h after 72 h. This is a specialist decision with possible therapeutic drug monitoring to reduce thrombocytopenia risk. Mycobacterial regimens are not included.',flag='monitor',formulation='IV or oral')

u('fluconazole','fluconazole')
add('fluconazole','Fluconazole',['Diflucan'],AB,'Azole antifungal',CRCL,'Maintenance dosing falls in CKD but may increase during CVVHD.',[
 table('Oropharyngeal infection · maintenance',['>50','10–50','<10'],['100 mg IV/PO every 24 h','50 mg IV/PO every 24 h','25 mg IV/PO every 24 h']),
 table('Oesophageal infection · maintenance',['>50','10–50','<10'],['200 mg IV/PO every 24 h','100 mg IV/PO every 24 h','50 mg IV/PO every 24 h'])],
 modality(single('Oropharyngeal infection','IHD','100 mg IV/PO once now, then after HD')+single('Oesophageal infection','IHD','200 mg IV/PO once now, then after HD')),
 modality(single('Oropharyngeal infection','CVVHD','200 mg IV/PO every 24 h')+single('Oesophageal infection','CVVHD','400 mg IV/PO every 24 h'), 'These recommendations are for CVVHD, not evaluated for CVVH.'),
 notes='This entry covers selected mucosal maintenance regimens only. Loading doses, systemic infection, cryptococcosis and prophylaxis require their own protocols.',formulation='IV or oral')

u('tmp-smx','tmp-smx-trimethoprim-sulfamethoxazole')
add('tmp-smx','Trimethoprim / sulfamethoxazole',['TMP-SMX','Co-trimoxazole','Bactrim','Septrin'],AB,'Folate antagonists',CRCL,'Use the trimethoprim component for weight-based regimens.',[
 table('Skin / soft-tissue infection or UTI',['>30','15–30','<15'],['1 DS tablet PO every 12 h','1 DS tablet PO every 24 h','1 SS tablet PO every 24 h'])],
 modality(single('Skin / soft-tissue infection or UTI','IHD','1 SS tablet PO once now, then every evening')),
 modality(single('Skin / soft-tissue infection or UTI','CVVHD','1 DS tablet PO every 12 h')),
 notes='SS = 80 mg TMP / 400 mg SMX. DS = 160 mg TMP / 800 mg SMX. Pneumocystis treatment, prophylaxis, CNS and other systemic regimens are not included.',formulation='Oral · SS / DS tablets')

u('nitrofurantoin','nitrofurantoin-macrobid')
add('nitrofurantoin','Nitrofurantoin',['Macrobid'],AB,'Urinary antibacterial',CRCL,'The cited UCSF guidance advises alternatives below CrCl 60.',[
 table('Cystitis treatment',['>60','<60'],['100 mg PO every 12 h','Limited data in this source; consider an alternative'])],
 modality(notes='Limited dialysis data in UCSF guidance; consider alternatives.',status='insufficient_data'),
 modality(notes='Limited dialysis data in UCSF guidance; consider alternatives.',status='insufficient_data'),
 notes='Renal thresholds vary between authorities. This is the UCSF position, not a reconciled universal cutoff. Exactly 60 is not assigned in the source. Other authorities must be reconciled before clinical approval.',flag='caution',formulation='Oral · Macrobid')

u('daptomycin','daptomycin')
add('daptomycin','Daptomycin',['Cubicin'],AB,'Lipopeptide',CRCL,'UCSF high-dose strategy; specialist antimicrobial guidance required.',[
 table('UCSF selected adult regimen',['>30','<30'],['8–10 mg/kg IV every 24 h','8–10 mg/kg IV every 48 h'])],
 modality(single('UCSF regimen','High-flux IHD','8–10 mg/kg IV once now and after HD'), 'Unstable HD schedule: UCSF alternative 8–10 mg/kg IV every 48 h.'),
 modality(single('UCSF regimen','CVVHD','6–8 mg/kg IV every 24 h'), 'Not evaluated for CVVH. Flow >2.5 L/h may require higher doses with ID/pharmacy.'),
 notes='Not effective for pneumonia. Use total body weight unless >120% ideal body weight, when UCSF uses adjusted weight. The source leaves exactly 30 unassigned. Some VRE infections need separate specialist regimens.',flag='monitor',formulation='IV')

u('valacyclovir','valacyclovir')
add('valacyclovir','Valacyclovir',['Valaciclovir','Valtrex'],AB,'Antiviral',CRCL,'Select herpes zoster or initial HSV treatment before reading the bands.',[
 table('Primary varicella / herpes zoster',['≥50','30–49','10–29','<10'],['1 g PO every 8 h','1 g PO every 12 h','1 g PO every 24 h','500 mg PO every 24 h']),
 table('Initial orolabial / genital HSV',['≥50','30–49','10–29','<10'],['1 g PO every 12 h','1 g PO every 12 h','1 g PO every 24 h','500 mg PO every 24 h'])],
 modality(single('UCSF regimen','IHD','500 mg PO every evening')),
 modality(notes='UCSF: insufficient data; contact ID pharmacy.',status='insufficient_data'),formulation='Oral')

label('metformin','e1679cfd-6425-440a-8d93-bb0ef78a5631')
add('metformin','Metformin',['Glucophage'], 'Diabetes','Biguanide',EGFR,'Distinguish starting therapy from continuing existing therapy.',[
 table('Renal eligibility · not a titration schedule',['≥45','30 to <45','<30'],['No renal restriction from this threshold alone; use formulation-specific dosing','Do not initiate. If already taking, reassess benefit versus risk','Contraindicated; discontinue'])],
 modality(notes='Contraindicated in kidney failure with eGFR <30. No maintenance-dialysis treatment regimen.',status='avoid'),
 modality(notes='No CRRT treatment regimen curated. RRT does not establish eligibility for metformin.',status='not_curated'),
 modality(notes='Contraindicated in kidney failure with eGFR <30. No PD treatment regimen.',status='avoid'),
 notes='Assess kidney function before treatment and periodically. This entry does not provide sick-day or contrast instructions; consult the full label.',flag='caution',formulation='Oral · immediate release reference')

label('sitagliptin','f85a48d0-0407-4c50-b0fa-7673a160bf01')
add('sitagliptin','Sitagliptin',['Januvia'],'Diabetes','DPP-4 inhibitor',EGFR,'Use eGFR bands; dialysis timing does not change administration.',[
 table('Type 2 diabetes',['≥45','30 to <45','<30'],['100 mg PO once daily','50 mg PO once daily','25 mg PO once daily'])],
 modality(single('Type 2 diabetes','ESRD on HD','25 mg PO once daily'),'May administer without regard to dialysis timing.'),None,
 modality(single('Type 2 diabetes','ESRD on PD','25 mg PO once daily'),'May administer without regard to dialysis timing.'),notes='Assess kidney function before treatment and periodically.',formulation='Oral')

label('linagliptin','dfe327e8-f6ab-41e5-bdef-d520118cd83a')
add('linagliptin','Linagliptin',['Tradjenta','Trajenta'],'Diabetes','DPP-4 inhibitor','No renal adjustment in US label','The US label recommends no renal dose adjustment.',single('Type 2 diabetes','Renal impairment','5 mg PO once daily'),
 notes='Removal by HD or PD is unlikely per the label. Modality-specific dosing has not been separately curated in this starter entry; do not infer a dialysis regimen from an empty tab.',flag='no_adjust',formulation='Oral')

label('empagliflozin','5777b8a8-ada6-4950-8548-43a1de11f075','2.1–2.3 dosing; 8.6 renal impairment (label revised January 2026)')
add('empagliflozin','Empagliflozin',['Jardiance'],'Diabetes','SGLT2 inhibitor',EGFR,'Separate cardiorenal benefit from glucose-lowering eligibility.',[
 table('Adult HF / eligible CKD',['eGFR ≥20','eGFR <20'],['10 mg PO once daily','Not enrolled at initiation in cited efficacy/safety trials; no initiation dose supplied here']),
 table('Glycaemic control in type 2 diabetes',['eGFR ≥30','eGFR <30'],['10 mg PO once daily; may increase to 25 mg if tolerated','Not recommended for glucose lowering'])],
 modality(notes='Trials did not enrol patients already on dialysis. No initiation regimen provided here; specialist review required.',status='specialist'),
 modality(notes='No CRRT regimen curated.',status='not_curated'),
 modality(notes='No PD initiation regimen provided; specialist review required.',status='specialist'),
 notes='Trial participants were not required to stop for eGFR <20 or dialysis initiation; this is not a recommendation to initiate on dialysis. Check volume status. Withhold ≥3 days before surgery/prolonged fasting when possible; restart when stable and eating.',flag='caution',formulation='Oral')

label('gabapentin','2ac0622c-440a-49a0-974f-726e6ac72a0e','2.3 renal adjustment, Table 1')
add('gabapentin','Gabapentin',['Neurontin'],'Neurology & pain','Gabapentinoid',CRCL,'Label total daily ranges are not starting doses.',[
 table('Label renal dose ranges · match indication and titrate',['≥60','>30–59','>15–29','15','<15'],['900–3,600 mg/day PO in 3 doses','400–1,400 mg/day PO in 2 doses','200–700 mg PO once daily','100–300 mg PO once daily','Reduce the 15 mL/min daily dose in proportion to CrCl'])],
 modality(single('Immediate release · label','After each 4-hour HD','Maintenance based on residual CrCl PLUS a matched post-HD supplement'), 'Post-HD supplements of 125 / 150 / 200 / 250 / 350 mg correspond to the label dose columns. Open Table 1 to select the matched dose; these are not interchangeable options.',status='specialist'),
 notes='Immediate-release formulation only. Dose ranges do not select a starting regimen or an indication-specific maximum. The label band notation leaves some exact boundary values unclear; confirm before prescribing.',flag='monitor',formulation='Immediate-release oral')

label('pregabalin','1e6fa742-f658-495f-88bb-8eddf9a45ffe','2.7 renal impairment, Table 2')
add('pregabalin','Pregabalin',['Lyrica'],'Neurology & pain','Gabapentinoid',CRCL,'Map the intended normal-function dose to the matching renal dose.',[
 table('Example ONLY: indication requiring 150 mg/day at normal function',['≥60','30–60','15–30','<15'],['150 mg/day PO in 2–3 doses','75 mg/day PO in 2–3 doses','25–50 mg/day PO in 1–2 doses','25 mg PO once daily'])],
 modality(single('Immediate-release label','After each 4-hour HD','Renally adjusted daily dose PLUS a matched supplemental dose'), 'For a 25 mg once-daily regimen: 25–50 mg supplement; 25–50 mg daily: 50–75 mg supplement; 50–75 mg daily: 75–100 mg supplement; 75 mg daily: 100–150 mg supplement. Confirm Table 2.',status='specialist'),
 notes='Example is not a universal starting dose. Higher indication-specific normal-function targets need their own Table 2 mapping. At shared boundaries 30 or 60, confirm the label interpretation. Extended-release products are excluded.',flag='monitor',formulation='Immediate-release oral')

label('enoxaparin','5017a927-2a24-4f27-89f9-27c805bf7d59','2.2–2.3 adult regimens; 8.7 renal impairment')
add('enoxaparin','Enoxaparin',['Lovenox','Clexane'],'Anticoagulants','Low-molecular-weight heparin',CRCL,'Prophylaxis and treatment require different doses.',[
 table('VTE prophylaxis in acutely ill medical adults',['≥30','<30 · non-dialysis'],['40 mg SC once daily','30 mg SC once daily']),
 table('Inpatient acute DVT ± PE (label regimen with warfarin)',['≥30','<30 · non-dialysis'],['1 mg/kg SC every 12 h OR 1.5 mg/kg SC once daily','1 mg/kg SC once daily'])],
 modality(notes='A routine IHD regimen has not been curated. Do not apply the non-dialysis <30 band as an approved dialysis regimen.',status='specialist'),
 modality(notes='Systemic VTE treatment and circuit anticoagulation are different indications; no CRRT regimen curated.',status='specialist'),
 notes='Observe for bleeding even at CrCl 30–50. ACS, STEMI, orthopaedic prophylaxis and extracorporeal-circuit anticoagulation are outside this entry.',flag='monitor',formulation='Subcutaneous')

label('apixaban','e9481622-7cc6-418a-acb6-c5450daae9b0','2.1 adult dosing; 8.6 renal impairment (US label)')
add('apixaban','Apixaban',['Eliquis'],'Anticoagulants','Direct factor Xa inhibitor','NVAF: age + weight + serum creatinine (US label)','AF dose-reduction criteria do not apply to acute VTE treatment.',[
 table('Stroke prevention in nonvalvular AF · US label',['Fewer than 2 reduction criteria','At least 2 reduction criteria'],['5 mg PO twice daily','2.5 mg PO twice daily']),
 table('Acute adult DVT / PE · US label',['Initial 7 days','After initial 7 days'],['10 mg PO twice daily','5 mg PO twice daily'])],
 modality(notes='US label dialysis recommendations rely on pharmacokinetic data; dialysis patients were not enrolled in efficacy/safety trials. Similar clinical outcomes are unknown. No automatic regimen is assigned; specialist and local-label review required.',status='specialist'),
 modality(notes='No CRRT regimen curated.',status='specialist'),
 modality(notes='Do not extrapolate intermittent-HD pharmacokinetics to PD. No PD regimen curated.',status='specialist'),
 notes='NVAF reduction criteria: age ≥80 years; weight ≤60 kg; serum creatinine ≥1.5 mg/dL. Renal eligibility and interactions still require the full local label; acute VTE rows are not proof of suitability in severe CKD. Jurisdiction-specific labels differ.',flag='monitor',formulation='Oral · adult tablets')

label('allopurinol','19a138b8-d225-03e6-f762-abe71560204b','2.3 and 2.6 gout initiation, Table 1')
add('allopurinol','Allopurinol',['Zyloric','Zyloprim'],'Gout & lipids','Xanthine oxidase inhibitor','eGFR · mL/min as written in cited label','Initial gout doses only; maintenance must be titrated to response.',[
 table('Gout · initial dose',['>60','>30–60','>15–30','5–15','<5'],['100 mg PO daily (usual initial dose)','50 mg PO daily','50 mg PO every other day','50 mg PO twice weekly','50 mg PO once weekly'])],
 notes='In renal impairment the label advises gradual 50 mg/day increases every 2–4 weeks with monitoring. These initial doses are not renal maximum doses. Tumour lysis and stone-prevention regimens are excluded.',formulation='Oral')

label('rosuvastatin','325a5d0e-9a72-4015-9fcd-1655fb504cee','2.2 and 2.5 renal dosing; 8.6')
add('rosuvastatin','Rosuvastatin',['Crestor'],'Gout & lipids','Statin','CLcr · mL/min/1.73 m² as written in US label','Severe non-dialysis renal impairment limits the dose.',[
 table('Adult lipid lowering',['Mild / moderate renal impairment','CLcr <30 · not on HD'],['No renal adjustment; indication-based adult range 5–40 mg PO daily','Start 5 mg PO daily; maximum 10 mg daily'])],
 modality(notes='The label severe-impairment cap explicitly excludes HD. This starter entry does not assign a dialysis dose or determine whether a statin should be initiated.',status='specialist'),
 notes='Other factors, including interacting drugs and Asian ancestry, can require lower doses. Do not substitute ordinary eGFR for the label metric without reviewing the source.',formulation='Oral')

source('rrt-assumptions','UCSF IDMP · Dialysis assumptions','https://idmp.ucsf.edu/antimicrobial-dosing-intermittent-continuous-hemodialysis','Introduction: high-flux IHD; CVVHD 2 L/h; residual native GFR <10 mL/min')
source('kidney-function','NIDDK · Drug dosing in adults with CKD','https://www.niddk.nih.gov/research-funding/research-programs/kidney-clinical-research-epidemiology/laboratory/ckd-drug-dosing-providers','Estimating equations, body surface area and limitations','Government clinical resource')
for drug in drugs:
    drug['addedInVersion']='0.1.0'
exec((ROOT/'expansion_v02.py').read_text(), globals())
assert len(drugs)==70, len(drugs)
exec((ROOT/'expansion_v03.py').read_text(), globals())
assert len(drugs)==100, len(drugs)
exec((ROOT/'catalog_v03.py').read_text(), globals())
exec((ROOT/'expansion_v04.py').read_text(), globals())
for drug in drugs:
    assert all(x in sources for x in drug['sourceIds'])
    for mode, m in drug['modalities'].items():
        if not m['sourceIds'] and m['tables']: m['sourceIds']=drug['sourceIds']
        assert all(x in sources for x in m['sourceIds'])
data=dict(schemaVersion='1.3.0',version='0.4.0',title='RenalRounds',population='Adults only',releaseDate=DATE,
          clinicalStatus=f'Draft inventory and reference. All {len(drugs)} entries await independent nephrologist and renal-pharmacist review. Not approved for bedside prescribing.',
          referenceScope=dict(bnfEdition='92 (September 2026)',bnfStatus='Monographs inaccessible; comparison pending. Edition existence checked with publisher only.',pnfStatus='PNF title/edition not identified; no PNF comparison claimed.',pdrStatus='Continuously updated digital reference; only specifically linked summaries and update material have been accessed.',newEntries=0,updatedEntries=sum(d.get('updatedInVersion')=='0.4.0' for d in drugs)),
          coverage={k:sum(d['entryType']==k for d in drugs) for k in ['renal','safety','catalog']},
          pharmacokineticCoverage=dict(profiles=sum(d['pharmacokinetics']['status']=='source_summary' for d in drugs),
              allFourCoreFields=sum(all(d['pharmacokinetics'][k]['status']=='sourced' for k in ['halfLife','volumeOfDistribution','proteinBinding']) and d['pharmacokinetics']['dialysability']['ihd']['value'] is not None for d in drugs)),
          sharedGuidance=shared_guidance,sources=list(sources.values()),drugs=sorted(drugs,key=lambda x:x['name']))
(ROOT/'dist'/'database.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print(f"Built {len(drugs)} monographs; {len(sources)} sources")
