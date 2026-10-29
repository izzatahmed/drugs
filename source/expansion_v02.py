"""Source-grounded expansion executed by build_data.py. No clinical approval implied."""
def pdr(key, slug):
    return source(key, 'PDR · '+slug.rsplit('-',1)[0].replace('-', ' '), 'https://www.pdr.net/drug-summary/?drugLabelId='+slug,
                  'Adult dosing considerations; selected renal impairment and dialysis sections', 'PDR digital monograph')
def smpc(key, name, product):
    return source(key, 'UK SmPC · '+name, 'https://www.medicines.org.uk/emc/product/'+product+'/smpc',
                  '4.2–4.4 and 5.2: dosing, renal precautions and pharmacokinetics', 'UK product information')
def put(*args, **kwargs):
    add(*args, **kwargs)
    d=drugs[-1]
    d['addedInVersion']='0.2.0'
    d['jurisdiction']='US source unless a table or note explicitly identifies UK guidance'
    d['referenceChecks']={'bnf':{'edition':'92 (September 2026)','status':'comparison_pending','reason':'Monograph text inaccessible in this environment; presence in BNF 92 is not asserted.'},
                          'pdr':{'status':'accessed' if any(sources[x]['type']=='PDR digital monograph' for x in d['sourceIds']) else 'not_checked'}}
    return d
def restricted(note): return modality(notes=note,status='specialist')
def not_indicated(note): return modality(notes=note,status='not_indicated')
def non_dialysis_only(d, note='No dialysis regimen established in the curated sources. Do not extrapolate from non-dialysis dosing.'):
    d['modalities']['ihd']=restricted(note)
    d['modalities']['pd']=restricted(note)
    return d
DI='Diabetes';CV='Cardiovascular';KD='Specialist kidney therapies';EL='Electrolytes & phosphate';AN='Renal anaemia'
source('bnf-edition','BNF publisher · current print edition','https://www.pharmaceuticalpress.com/bnf-and-bnfc/books/','BNF 92 listed; monograph content not accessed','Bibliographic record only')
source('pdr-current','PDR · digital reference','https://www.pdr.net/','Continuously updated prescribing information; not a numbered print edition','Reference description')
source('pdr-oct2026','PDR · October 2026 updates','https://www.pdr.net/edrug-updates/oct2026','Finerenone new US indication; label independently checked','PDR update bulletin')

pdr('dapagliflozin-pdr','Farxiga-dapagliflozin-3427')
smpc('dapagliflozin-uk','dapagliflozin 5 mg (product-specific)','102189')
put('dapagliflozin','Dapagliflozin',['Farxiga','Forxiga'],DI,'SGLT2 inhibitor',EGFR,'Initiation thresholds differ by jurisdiction and product; separate glycaemic and cardiorenal use.',[
 table('US PDR · HF / CKD',['≥25','<25'],['10 mg PO once daily','Do not initiate; established therapy may continue at 10 mg daily under the source conditions']),
 table('UK product SmPC · initiation eligibility',['≥15','<15'],['No renal dose reduction; usual regimen 10 mg PO daily. Experience starting below 25 is limited','Do not initiate'])],
 restricted('PDR: no dialysis efficacy/safety trial data; no routine dialysis regimen assigned.'),None,restricted('No PD regimen curated.'),
 notes='US PDR: not recommended for glucose lowering at eGFR <45. Its continuation advice stops at kidney replacement therapy. The checked UK generic SmPC uses a different initiation threshold; verify the exact local product. Do not merge the two rules.',refs=['dapagliflozin-pdr','dapagliflozin-uk'],flag='caution',formulation='Oral')

label('canagliflozin-label','4e946ba3-02c4-4a10-9d5e-f2d87b534dc3','2.2–2.4 renal dosing; renal impairment (2026 label)')
put('canagliflozin','Canagliflozin',['Invokana'],DI,'SGLT2 inhibitor',EGFR,'Renal eligibility and maximum dose depend on eGFR.',[
 table('US renal dosing',['≥60','30 to <60','<30'],['Usual initiation 100 mg PO daily; product-specific escalation requires eligibility','Maximum 100 mg PO daily','Do not initiate. Adults already taking it with albuminuria >300 mg/day may continue 100 mg daily for labelled cardiorenal benefit'])],
 restricted('Dialysis patients were not enrolled in efficacy/safety trials; no regimen assigned.'),
 notes='UGT-inducing medicines require separate dosing instructions. Assess renal function and volume status; do not use glycaemic thresholds interchangeably with cardiorenal indications.',refs=['canagliflozin-label'],flag='caution',formulation='Oral')

pdr('ertugliflozin-pdr','Steglatro-ertugliflozin-24174')
put('ertugliflozin','Ertugliflozin',['Steglatro'],DI,'SGLT2 inhibitor',EGFR,'The renal threshold differs from other SGLT2 inhibitors.',[
 table('Type 2 diabetes · US PDR',['≥45','<45'],['5 mg PO once daily initially; may increase to 15 mg daily','Use not recommended'])],restricted('Not recommended in kidney failure; no HD dose assigned.'),
 notes='Do not transfer dapagliflozin or empagliflozin CKD/HF eligibility to ertugliflozin.',refs=['ertugliflozin-pdr'],flag='caution',formulation='Oral')

label('finerenone-label','fc726765-5d5a-4d6e-b037-b847bda9fb7c','US label revised September 2026: 1, 2.1–2.3, monitoring tables')
smpc('finerenone-uk','Kerendia 20 mg','13438')
d=put('finerenone','Finerenone',['Kerendia'],KD,'Nonsteroidal mineralocorticoid antagonist',EGFR,'Starting dose, target dose and potassium algorithm depend on the indication.',[
 table('US starting dose · eligible CKD with T2DM/T1DM or HF with LVEF ≥40%',['≥60','25 to <60','<25'],['20 mg PO once daily','10 mg PO once daily','Initiation not recommended']),
 table('US target dose · after monitoring and titration',['CKD with T2DM / T1DM','HF · eGFR ≥60 at initiation','HF · eGFR 25 to <60 at initiation'],['20 mg PO daily','40 mg PO daily','20 mg PO daily'])],
 restricted('No dialysis initiation regimen assigned; specialist review required.'),None,restricted('No PD regimen assigned.'),
 notes='Do not start if K >5.0 mEq/L. Recheck K/eGFR at 4 weeks and after dose changes; follow the indication-specific withholding/restart table. Strong CYP3A4 inhibitors and adrenal insufficiency are contraindications. UK SmPC differs in indications/continuation: do not assume the new US T1DM indication is UK approved.',refs=['finerenone-label','finerenone-uk','pdr-oct2026'],flag='monitor',formulation='Oral · 10 / 20 / 40 mg US tablets')
d['updateNote']='US label September 2026 adds CKD associated with T1DM; its claim is UACR reduction with expected kidney benefit. HF target dosing is distinct. PDR October 2026 bulletin checked against the label.'
d['referenceChecks']['pdr']['status']='update_bulletin_checked'

label('semaglutide-label','42bdd912-2393-44c4-b7e0-47672ca28991','Ozempic injection: 2, 8.6; kidney outcomes indication')
source('semaglutide-maker','Novo Nordisk · semaglutide special populations','https://www.novomedlink.com/diabetes/products/treatments/ozempic/efficacy-safety/special-populations.html','No renal adjustment; volume-depletion monitoring','Manufacturer clinical information')
put('semaglutide-sc','Semaglutide (Ozempic injection)',['Ozempic','Semaglutide'],DI,'GLP-1 receptor agonist','No renal dose adjustment in US product information','Renal impairment does not require dose reduction; formulation and indication still determine titration.',single('Ozempic SC only','Renal impairment, including kidney failure','No renal adjustment; follow the injection-specific initiation and titration schedule'),
 restricted('US renal PK includes kidney failure; this does not establish all dialysis outcomes or an automatic patient-specific dose. Use the product titration with specialist review.'),
 notes='Monitor renal function with severe GI reactions or dehydration. Oral semaglutide and obesity products are not interchangeable with this entry.',refs=['semaglutide-label','semaglutide-maker'],flag='no_adjust',formulation='Subcutaneous · Ozempic')

label('tirzepatide-label','d2d7da5d-ad07-4228-955f-cf7e355c8cc0','Mounjaro: 8.6 and GI/volume-depletion precautions')
smpc('tirzepatide-uk','Mounjaro KwikPen','15483')
put('tirzepatide','Tirzepatide',['Mounjaro','Zepbound'],DI,'Dual GIP / GLP-1 receptor agonist','No renal dose adjustment in cited labels','No renal reduction is required, including ESRD; clinical experience remains limited.',single('Mounjaro · renal adjustment only','Renal impairment, including ESRD','Use usual product-specific titration without a renal dose reduction'),
 restricted('No renal PK adjustment including ESRD in US/UK information; severe-impairment experience is limited. Dialysis care needs individual tolerability review.'),
 notes='Monitor hydration and kidney function when severe vomiting/diarrhoea occurs, especially at initiation/escalation. This entry does not substitute Mounjaro dosing for other branded indications.',refs=['tirzepatide-label','tirzepatide-uk'],flag='no_adjust',formulation='Subcutaneous · weekly, product-specific titration')

label('dulaglutide-label','af4e38a6-ad3f-480c-ae82-5ac6c7735b99','Trulicity 8.6: renal impairment and ESRD')
put('dulaglutide','Dulaglutide',['Trulicity'],DI,'GLP-1 receptor agonist','No renal adjustment in US label','Renal impairment including ESRD does not require dose reduction.',single('Renal adjustment only','Renal impairment / ESRD','No adjustment; use the usual product-specific initiation and titration'),
 restricted('No renal adjustment is recommended in ESRD, but US label advises caution. No dialysis-outcome claim is made.'),
 notes='Monitor kidney function if severe adverse GI reactions occur. Do not treat “no adjustment” as absence of dehydration-related AKI risk.',refs=['dulaglutide-label'],flag='no_adjust',formulation='Weekly subcutaneous')

label('liraglutide-label','5a9ef4ea-c76a-4d34-a604-27c5b505f5a4','Victoza 8.6 renal impairment')
put('liraglutide','Liraglutide (Victoza)',['Victoza','Liraglutide'],DI,'GLP-1 receptor agonist','No renal adjustment in US label','No renal reduction in the US Victoza label; ESRD experience is limited.',single('Victoza renal adjustment only','Renal impairment','No adjustment; use product-specific usual titration'),
 restricted('Limited ESRD experience; no dialysis regimen is automatically assigned.'),
 notes='This is the diabetes product entry. Do not extrapolate to obesity-dose products or regard limited ESRD evidence as proven dialysis benefit.',refs=['liraglutide-label'],flag='no_adjust',formulation='Daily subcutaneous · Victoza')

pdr('exenatide-pdr','Bydureon-exenatide-60')
source('exenatide-label','AstraZeneca · Byetta US prescribing information','https://medicalinformation.astrazeneca-us.com/prescribing-information/byetta.html','5.4 and 8.6 severe renal impairment, ESRD and transplantation','US prescribing information')
put('exenatide-ir','Exenatide (immediate release)',['Byetta','Exenatide'],DI,'GLP-1 receptor agonist',CRCL,'Immediate-release and extended-release products have different renal restrictions.',[
 table('Byetta only',['>50','30–50','<30 / ESRD'],['No renal adjustment; usual product titration','Use cautiously, especially when increasing 5 to 10 micrograms','Not recommended'])],
 modality(notes='Byetta is not recommended in ESRD on HD.',status='avoid'),None,modality(notes='Not recommended in ESRD.',status='avoid'),
 notes='The extended-release formulation is not covered: PDR uses eGFR <45 as its not-recommended threshold. Use caution after kidney transplantation and monitor for dehydration-related AKI.',refs=['exenatide-pdr','exenatide-label'],flag='caution',formulation='Immediate-release subcutaneous · Byetta')

pdr('saxagliptin-pdr','Onglyza-saxagliptin-111')
put('saxagliptin','Saxagliptin',['Onglyza'],DI,'DPP-4 inhibitor',EGFR,'Reduce to 2.5 mg daily below eGFR 45.',[
 table('Type 2 diabetes · US PDR',['≥45','<45'],['2.5 or 5 mg PO daily according to the usual regimen','2.5 mg PO once daily'])],
 modality(single('Type 2 diabetes','IHD','2.5 mg PO once daily; give after HD')),
 notes='Check CYP3A interactions and the full heart-failure precautions. PD dosing is not curated.',refs=['saxagliptin-pdr'],formulation='Oral')

label('alogliptin-label','a3768c7e-aa4c-44d3-bc53-43bb7346c0b0','Nesina 2.2 renal impairment and HD/PD evidence')
put('alogliptin','Alogliptin',['Nesina','Vipidia'],DI,'DPP-4 inhibitor',CRCL,'Uses CrCl rather than the eGFR thresholds of some other DPP-4 inhibitors.',[
 table('Type 2 diabetes',['≥60','30 to <60','<30'],['25 mg PO once daily','12.5 mg PO once daily','6.25 mg PO once daily'])],
 modality(single('Type 2 diabetes','ESRD on HD','6.25 mg PO once daily'),'No relationship to HD timing required.'),None,
 modality(notes='US label: not studied in patients undergoing PD.',status='insufficient_data'),
 notes='Assess kidney function before starting and periodically; review the full heart-failure precautions.',refs=['alogliptin-label'],formulation='Oral')

pdr('sacubitril-valsartan-pdr','Entresto-sacubitril-valsartan-3756')
label('sacubitril-valsartan-label','000dc81d-ab91-450c-8eae-8eb74e72296f','2.7 and 8.7 severe renal impairment')
put('sacubitril-valsartan','Sacubitril / valsartan',['Entresto'],CV,'Angiotensin receptor–neprilysin inhibitor',EGFR,'Severe renal impairment halves the usual starting dose.',[
 table('Adult HF · initial renal adjustment',['≥30','<30'],['No renal reduction to the usual starting dose','Start at half the usual recommended starting dose; use the full adult product algorithm'])],
 restricted('Unlikely to be removed by HD because of protein binding; this does not establish a validated dialysis dose.'),
 notes='Initial dose also depends on prior ACE inhibitor/ARB therapy. Titration, blood pressure, potassium, renal function and ACE-inhibitor washout need the full protocol.',refs=['sacubitril-valsartan-pdr','sacubitril-valsartan-label'],flag='monitor',formulation='Oral · combination strengths')

pdr('lisinopril-pdr','Zestril-lisinopril-2456')
label('lisinopril-label','f5db9549-e179-3db6-e053-2995a90a1544','2.4 initial renal doses')
put('lisinopril','Lisinopril',['Zestril','Prinivil'],CV,'ACE inhibitor',CRCL,'These are initial-dose adjustments, not a universal maintenance cap.',[
 table('Initial adult dose',['>30','10–30 · hypertension','10–30 · HF / acute MI','<10'],['No renal adjustment to usual initiation','5 mg PO daily','2.5 mg PO daily','2.5 mg PO daily'])],
 modality(single('Initial adult dose','HD','2.5 mg PO once daily; titrate individually')),
 notes='Monitor blood pressure, potassium and renal function. Acute MI has additional haemodynamic restrictions; this summary does not replace that protocol.',refs=['lisinopril-pdr','lisinopril-label'],formulation='Oral')

pdr('atenolol-pdr','Tenormin-atenolol-1128')
label('atenolol-label','6e850b1e-28a4-4ff8-8ed7-bb0b29faa28a','Elderly/renal impairment: maximum oral doses; HD dosing')
put('atenolol','Atenolol',['Tenormin'],CV,'Beta blocker','CrCl · mL/min/1.73 m² as US label','Renal impairment limits the maximum oral dose.',[
 table('Maximum oral dose · not starting doses',['15–35','<15'],['Maximum 50 mg PO daily','Maximum 25 mg PO daily'])],
 modality(single('US label · supervised dosing','After each HD session','25 or 50 mg PO after HD'),'Hospital supervision advised: marked falls in blood pressure can occur.'),
 notes='Initial doses may need to be lower. Assess heart rate, blood pressure and response before titration.',refs=['atenolol-label','atenolol-pdr'],flag='monitor',formulation='Oral')

source('spironolactone-label','DailyMed · spironolactone','https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=bd5ec154-b092-4c4d-8e72-ca2a2ef71a6d','2.2 heart-failure initiation; potassium and renal precautions','US prescribing information')
put('spironolactone','Spironolactone',['Aldactone'],CV,'Steroidal mineralocorticoid antagonist',EGFR,'HF initiation depends on kidney function and potassium.',[
 table('HF initial dosing · selected US label guidance',['>50 and K ≤5.0 mEq/L','30–50','<30'],['25 mg PO once daily initially','Consider 25 mg PO every other day initially','No regimen assigned here; specialist risk assessment required'])],
 restricted('Do not derive a routine HD regimen from these non-dialysis HF starting doses.'),
 notes='Hyperkalaemia risk requires potassium/renal monitoring. This entry does not cover cirrhotic oedema, hyperaldosteronism or a dialysis trial protocol.',refs=['spironolactone-label'],flag='monitor',formulation='Oral')

pdr('eplerenone-pdr','Inspra-eplerenone-1817')
label('eplerenone-label','1a52bedc-8e2c-4116-a296-a87770676b4a','4 contraindications by indication')
put('eplerenone','Eplerenone',['Inspra'],CV,'Steroidal mineralocorticoid antagonist',CRCL,'Hypertension and HF have different renal restrictions.',[
 table('US renal eligibility',['≤30 · all indications','>30 to <50 · hypertension','>30 to <50 · HF','≥50'],['Contraindicated','Contraindicated','PDR guideline regimen: 25 mg PO every other day for first 4 weeks, then 25 mg daily if appropriate','No renal adjustment; use indication-specific regimen'])],
 modality(notes='Contraindicated at CrCl ≤30. HD does not remove eplerenone.',status='avoid'),
 notes='Additional hypertension contraindications include T2DM with microalbuminuria and specified serum-creatinine limits. Check potassium, strong CYP3A inhibitors and the full label.',refs=['eplerenone-pdr','eplerenone-label'],flag='caution',formulation='Oral')

pdr('rivaroxaban-pdr','Xarelto-rivaroxaban-278')
label('rivaroxaban-label','10db92f9-2300-4a80-836b-673e1ae91610','2.1, 5.4, 8.6 adult indications and renal impairment')
put('rivaroxaban','Rivaroxaban',['Xarelto'], 'Anticoagulants','Direct factor Xa inhibitor',CRCL,'AF and VTE regimens must remain separate.',[
 table('US NVAF · selected non-dialysis dosing',['>50','15–50','<15'],['20 mg PO daily with evening meal','15 mg PO daily with evening meal','No automatic regimen assigned; specialist/local-label review']),
 table('US acute DVT/PE',['CrCl ≥15','CrCl <15'],['15 mg PO twice daily for 21 days, then 20 mg daily; take with food','Avoid use'])],
 restricted('Clinical outcomes in ESRD/HD are uncertain and indication dependent. No automatic HD dose assigned.'),
 notes='At CrCl 15–29, VTE evidence is limited: monitor closely for bleeding. Review P-gp/CYP3A interactions. Do not extrapolate US NVAF advice to VTE or to UK/local labels.',refs=['rivaroxaban-pdr','rivaroxaban-label'],flag='monitor',formulation='Oral · adult tablets')

pdr('dabigatran-pdr','Pradaxa-dabigatran-etexilate-mesylate-100')
smpc('dabigatran-uk','Pradaxa 75 mg','6228')
put('dabigatran','Dabigatran etexilate',['Pradaxa'], 'Anticoagulants','Direct thrombin inhibitor',CRCL,'US and UK severe-renal-impairment rules differ.',[
 table('US NVAF · renal adjustment',['>30','15–30','<15'],['Usual indication-specific regimen; check interactions','75 mg PO twice daily under US guidance','Manufacturer provides no dose']),
 table('UK adult renal restriction',['CrCl <30'],['Contraindicated; US 75 mg twice-daily advice must not be transferred to UK prescribing'])],
 restricted('No manufacturer dialysis dose supplied. Dialysis removal in overdose is not a maintenance regimen.'),
 notes='US DVT/PE treatment/prophylaxis: no dose recommendation at CrCl ≤30. P-gp inhibitors can require dose changes or avoidance at higher CrCl; review the full interaction-specific guidance.',refs=['dabigatran-pdr','dabigatran-uk'],flag='caution',formulation='Oral capsules · adult indications')

pdr('edoxaban-pdr','Savaysa-edoxaban-3667')
put('edoxaban','Edoxaban',['Savaysa','Lixiana'], 'Anticoagulants','Direct factor Xa inhibitor',CRCL,'US AF guidance has both a lower and an upper CrCl restriction.',[
 table('US NVAF',['>95','>50 to 95','15–50','<15'],['Do not use for NVAF; reduced efficacy','60 mg PO once daily','30 mg PO once daily','Use not recommended'])],
 restricted('Use is not recommended at CrCl <15; no HD regimen assigned.'),
 notes='VTE treatment requires initial parenteral anticoagulation and separate weight/P-gp dose criteria. This entry curates the US NVAF regimen only; do not automatically apply it to Lixiana in another jurisdiction.',refs=['edoxaban-pdr'],flag='caution',formulation='Oral')

pdr('duloxetine-pdr','Cymbalta-duloxetine-288')
put('duloxetine','Duloxetine',['Cymbalta'], 'Neurology & pain','SNRI',CRCL,'Avoid below CrCl 30 in the cited PDR guidance.',[
 table('Renal eligibility',['≥30','<30'],['No renal adjustment; use indication-specific dose','Avoid use'])],
 modality(notes='Avoid in kidney failure under the cited guidance; no HD regimen.',status='avoid'),None,modality(notes='No PD regimen assigned; avoid in severe renal impairment under this source.',status='avoid'),
 notes='PDR also advises avoiding chronic liver disease/cirrhosis. Full serotonergic-interaction and withdrawal guidance is outside this summary.',refs=['duloxetine-pdr'],flag='caution',formulation='Oral delayed-release capsules')

pdr('tramadol-pdr','Ultram-tramadol-hydrochloride-950')
put('tramadol-ir','Tramadol (immediate release)',['Ultram','Tramadol'], 'Neurology & pain','Opioid analgesic',CRCL,'Prolong the interval below CrCl 30; extended-release products are excluded.',[
 table('Immediate-release renal adjustment',['≥30','<30'],['No renal adjustment to usual regimen; use the lowest appropriate dose','Interval every 12 h; maximum 200 mg/day'])],
 modality(single('Immediate-release only','IHD','Use the renally adjusted regimen; no routine dialysis-day replacement dose'), 'Only about 7% is removed by HD in cited PDR guidance.'),
 notes='Avoid extended-release tramadol at CrCl <30. Renal advice does not replace opioid, seizure, serotonergic interaction, age or hepatic precautions.',refs=['tramadol-pdr'],flag='monitor',formulation='Immediate-release oral only')

pdr('levetiracetam-pdr','Levetiracetam-Injection-levetiracetam-23988')
put('levetiracetam','Levetiracetam (immediate release)',['Keppra','Levetiracetam'], 'Neurology & pain','Antiseizure drug','CrCl · mL/min/1.73 m² as cited PDR','Renal maintenance ranges are separate from emergency loading protocols.',[
 table('Adult maintenance · IR oral / IV',['>80','50–80','30–49','<30'],['Usual indication-specific maintenance','500–1,000 mg every 12 h','250–750 mg every 12 h','250–500 mg every 12 h'])],
 modality(single('Adult maintenance · IR / IV','IHD','500–1,000 mg every 24 h PLUS 250–500 mg after HD')),
 restricted('PDR provides a generic CRRT range without delivered-treatment settings. No universal CRRT dose assigned here.'),
 modality(single('PDR adult maintenance · IR / IV','PD','500–1,000 mg every 24 h'),'Individualise to residual function and seizure control; this is not a loading dose.'),
 notes='Extended-release formulations are excluded. PDR advises against XR in ESRD on dialysis. Confirm the unusual indexed CrCl units in the original source.',refs=['levetiracetam-pdr'],flag='monitor',formulation='Immediate-release oral or IV')

pdr('colchicine-pdr','Colcrys-colchicine-592')
label('colchicine-label','d6adc880-5499-4691-93f3-27c87902d5fc','2.5 renal dosing; 4 contraindicated inhibitor combinations')
put('colchicine','Colchicine',['Colcrys'], 'Gout & lipids','Anti-inflammatory antigout drug',CRCL,'Gout prophylaxis, flare treatment and FMF are different regimens.',[
 table('Gout prophylaxis · selected US tablet guidance',['CrCl ≥30','CrCl <30'],['No routine renal reduction; monitor closely','Start 0.3 mg PO daily; any increase requires monitoring'])],
 modality(single('Gout prophylaxis','IHD','0.3 mg PO twice weekly')+single('Gout flare treatment','IHD','0.6 mg PO once; do not repeat within 2 weeks'), 'Do not use flare treatment if already receiving colchicine prophylaxis in renal impairment.'),
 notes='In renal or hepatic impairment, combination with P-gp or strong CYP3A4 inhibitors is contraindicated because of potentially fatal toxicity. Colchicine is not effectively removed by dialysis. FMF dosing is not curated.',refs=['colchicine-pdr','colchicine-label'],flag='monitor',formulation='Oral · 0.6 mg US tablets')

pdr('febuxostat-pdr','Uloric-febuxostat-563')
label('febuxostat-label','54de10ef-fe5f-4930-b91d-6bbb04c664bd','2.2, 8.6; boxed cardiovascular warning')
put('febuxostat','Febuxostat',['Uloric','Adenuric'], 'Gout & lipids','Xanthine oxidase inhibitor',CRCL,'US renal maximum differs from products and strengths used elsewhere.',[
 table('US gout renal dosing',['≥30','15–29'],['No renal adjustment to usual 40/80 mg daily regimen','Maximum 40 mg PO once daily'])],
 modality(notes='US label: not studied in end-stage renal impairment on dialysis.',status='insufficient_data'),
 notes='Review the US boxed cardiovascular warning, intended allopurinol-related eligibility and contraindicated azathioprine/mercaptopurine interactions in the full label. Do not use this US dose cap as an unqualified UK/local rule.',refs=['febuxostat-pdr','febuxostat-label'],flag='monitor',formulation='Oral · US regimen')

source('paxlovid-label','Pfizer · Paxlovid US prescribing information','https://www.pfizermedical.com/paxlovid','2.2–2.3, 8.6: 5-day renal and HD regimens','US prescribing information')
d=put('nirmatrelvir-ritonavir','Nirmatrelvir / ritonavir',['Paxlovid'],AB,'Protease inhibitor combination','eGFR · mL/min as US label table','The current US label includes severe renal impairment and haemodialysis.',[
 table('Eligible adult COVID-19 · 5-day course · US label',['≥60','30 to <60','<30 · day 1','<30 · days 2–5'],['300 mg nirmatrelvir + 100 mg ritonavir PO twice daily','150 mg nirmatrelvir + 100 mg ritonavir PO twice daily','300 mg nirmatrelvir + 100 mg ritonavir PO ONCE','150 mg nirmatrelvir + 100 mg ritonavir PO once daily'])],
 modality(single('Day 1','HD','300 mg nirmatrelvir + 100 mg ritonavir PO once')+single('Days 2–5','HD','150 mg nirmatrelvir + 100 mg ritonavir PO once daily'),'On HD days administer after the session. This is a 5-day total course, not a recurring HD regimen.'),
 notes='Major CYP3A interactions can preclude therapy even with the correct renal dose; complete a current interaction check, especially for transplant immunosuppressants. Eligibility, symptom-onset window and hepatic restrictions remain essential.',refs=['paxlovid-label'],flag='monitor',formulation='Co-packaged oral tablets · 5-day course')
d['updateNote']='US severe-renal-impairment/HD dosing is now present in the checked label; older references may state it is not recommended. Do not transfer this update to another jurisdiction without checking.'

label('cefiderocol-label','75c0c785-38e0-4049-a6fb-b77581f5b35c','2.1–2.2 renal/HD/CRRT tables; March 2026 label')
d=put('cefiderocol','Cefiderocol',['Fetroja','Fetcroja'],AB,'Siderophore cephalosporin',CRCL,'Use the label effluent-based CRRT table; it is not the UCSF generic CVVHD assumption.',[
 table('US adult regimen · all infusions over 3 h',['≥120','60–119','30–59','15–29','<15'],['2 g IV every 6 h','2 g IV every 8 h','1.5 g IV every 8 h','1 g IV every 8 h','0.75 g IV every 12 h'])],
 modality(single('US label · 3 h infusion','IHD','0.75 g IV every 12 h'),'Give immediately after HD on dialysis days.'),
 modality([table('US CRRT initial dosing · 3 h infusions',['Effluent ≤2 L/h','2.1–3 L/h','3.1–4 L/h','≥4.1 L/h'],['1.5 g IV every 12 h','2 g IV every 12 h','1.5 g IV every 8 h','2 g IV every 8 h'])], 'CVVH/CVVHD/CVVHDF; residual renal function may require individualisation. Verify exact flow boundaries in source.'),
 notes='Monitor changing renal function and treatment settings. Specialist microbiology/susceptibility review and full safety warnings remain necessary.',refs=['cefiderocol-label'],flag='monitor',formulation='IV · 3-hour infusion')
d['modalities']['crrt']['settingMeasure']='US label · CVVH/CVVHD/CVVHDF · delivered effluent flow in L/h'

pdr('ceftazidime-avibactam-pdr','Avycaz-avibactam-ceftazidime-3692')
source('ceftazidime-avibactam-maker','AbbVie · Avycaz renal dosing','https://www.avycaz.com/dosing-renal-impairment','Adult renal dosing, 2 h infusions and post-HD timing','Manufacturer clinical information')
put('ceftazidime-avibactam','Ceftazidime / avibactam',['Avycaz','Zavicefta'],AB,'Cephalosporin + β-lactamase inhibitor',CRCL,'Amounts below are the total combination dose.',[
 table('US adult renal adjustment · 2 h infusion',['>50','31–50','16–30','6–15','≤5'],['Usual adult regimen; see full label','1.25 g IV every 8 h','0.94 g IV every 12 h','0.94 g IV every 24 h','0.94 g IV every 48 h'])],
 restricted('PDR: use the estimated-CrCl regimen and give after HD on dialysis days. Residual CrCl is needed; no single dose is selected automatically.'),
 notes='0.94 g is the rounded combination amount (0.75 g ceftazidime + 0.1875 g avibactam). With changing function, check CrCl at least daily. CRRT needs a separate prescription-specific protocol.',refs=['ceftazidime-avibactam-pdr','ceftazidime-avibactam-maker'],flag='monitor',formulation='IV · 2-hour infusion')

label('sparsentan-label','d7354af1-f304-f4d9-e053-2995a90ab219','US adult IgAN initiation; new FSGS section distinct')
smpc('sparsentan-uk','Filspari 400 mg','100611')
put('sparsentan','Sparsentan',['Filspari'],KD,'Dual endothelin / angiotensin receptor antagonist',EGFR,'Specialist IgAN therapy; do not combine with existing RAAS inhibitors.',[
 table('Adult IgAN · selected regimen',['eGFR ≥30','eGFR <30'],['200 mg PO daily for 14 days, then 400 mg daily as tolerated','UK SmPC: not recommended; limited clinical experience'])],
 restricted('No dialysis regimen curated; do not extrapolate from the IgAN trial.'),
 notes='Stop RAAS inhibitors and endothelin antagonists before initiating per US label. Liver, pregnancy, potassium, BP and fluid-retention precautions are essential. The newer US FSGS dosing differs and is not included here.',refs=['sparsentan-label','sparsentan-uk'],flag='monitor',formulation='Oral · IgAN regimen only')

label('atrasentan-label','9a7e7f85-bfd0-44a0-beda-3bcfa8215c64','1–2, 12.3; US IgAN label updated June 2026')
put('atrasentan','Atrasentan',['Vanrafia'],KD,'Selective endothelin A receptor antagonist',EGFR,'Specialist primary IgAN treatment; severe-CKD evidence must be assessed separately.',[
 table('US primary IgAN · selected adult regimen',['Eligible non-dialysis patient','eGFR <30'],['0.75 mg PO once daily','No automatic regimen: specialist assessment of limited clinical evidence'])],
 restricted('ESRD pharmacokinetics are unknown in the checked US label; no dialysis regimen assigned.'),
 notes='Checked US indication is accelerated approval for proteinuria reduction in patients at risk of rapid progression, generally UPCR ≥1.5 g/g; kidney-function benefit is not yet established in that label. Pregnancy, liver and fluid-retention precautions apply.',refs=['atrasentan-label'],flag='monitor',formulation='Oral · 0.75 mg')

label('voclosporin-label','9f489295-1156-52c7-5fd0-5c4c52f9b813','2.2–2.4 renal dosing, eGFR change algorithm')
smpc('voclosporin-uk','Lupkynis','14381')
put('voclosporin','Voclosporin',['Lupkynis'],KD,'Calcineurin inhibitor',EGFR,'Lupus nephritis dosing depends on baseline and change in eGFR.',[
 table('US lupus nephritis · initial dosing',['Baseline eGFR >45','Baseline eGFR ≤45','Severe baseline impairment, if specialist elects use'],['23.7 mg PO twice daily with MMF and corticosteroids','Not recommended unless benefit exceeds risk','US starting dose 15.8 mg PO twice daily; specialist decision only'])],
 restricted('No dialysis regimen curated; toxicity monitoring cannot be replaced by an eGFR band.'),
 notes='If eGFR <60 with >20% to <30% decline, reduce by 7.9 mg twice daily; ≥30% decline requires discontinuation and reassessment. Check eGFR every 2 weeks initially and follow the full re-initiation algorithm. UK SmPC separates baseline 30–<45 from <30; do not merge thresholds.',refs=['voclosporin-label','voclosporin-uk'],flag='monitor',formulation='Oral · 7.9 mg capsules')

label('daprodustat-label','d82aa06e-5a33-4844-99b7-4701313455a4','Historical US label: dialysis ≥4 months; initiation table')
source('daprodustat-market','GSK · Jesduvroq discontinuation','https://www.gsk-ecs.com/gskstorefront/gskEcs/en_US/USD/RootCategory/Vaccines/JESDUVROQ-TABLET-1MG-1X30/p/60000000135324','Manufacturer states product no longer sold; discontinued December 19, 2024','Manufacturer market-status record')
d=put('daprodustat','Daprodustat (historical US product)',['Jesduvroq','Daprodustat'],AN,'HIF prolyl hydroxylase inhibitor','Haemoglobin / ESA history · not eGFR band dosing','US Jesduvroq was discontinued; retained as a labelled historical reference.',[],
 modality([table('Historical US start · on dialysis ≥4 months, not receiving ESA',['Hb <9 g/dL','Hb 9–10 g/dL','Hb >10 g/dL'],['4 mg PO daily','2 mg PO daily','1 mg PO daily'])], 'Prior ESA treatment needs a different conversion table; do not use this table for conversion.'),
 notes='US product no longer sold by GSK (December 2024). These historical doses do not establish current availability or local approval. Full HIF-PHI cardiovascular/thrombotic warnings, Hb monitoring and interaction adjustments are required.',refs=['daprodustat-label','daprodustat-market'],flag='caution',formulation='Historical US oral product')
d['modalities']['ckd']=not_indicated('Historical US label was not indicated for CKD anaemia in patients not on dialysis.')
d['marketStatus']='US Jesduvroq discontinued by GSK; not a newly marketed medicine.'

label('vadadustat-label','ac9da724-5a62-4ab6-a89c-376a25f6195b','1–2, 5: adult dialysis duration and Hb-based dosing')
d=put('vadadustat','Vadadustat',['Vafseo'],AN,'HIF prolyl hydroxylase inhibitor','Haemoglobin / clinical response · not eGFR bands','US eligibility requires dialysis for at least 3 months.',[],
 modality(single('US anaemia of CKD · dialysis ≥3 months','Initial dose','300 mg PO once daily'),'May give without regard to dialysis type or timing. Titrate by Hb using the full label.'),None,
 modality(single('US anaemia of CKD · dialysis ≥3 months','PD initial dose','300 mg PO once daily'),'Label states dosing is independent of dialysis type/timing.'),
 notes='Use the lowest dose to reduce transfusions; do not target Hb >11 g/dL. Boxed cardiovascular/thrombotic risks, hypertension, liver monitoring and oral-drug separation require the full label.',refs=['vadadustat-label'],flag='monitor',formulation='Oral')
d['modalities']['ckd']=not_indicated('US label: not indicated for CKD anaemia in patients not on dialysis.')

label('difelikefalin-label','0c7b81f2-0fd3-47cb-8b0f-185e07f19c87','1–2: post-HD administration; July 2025 revision')
d=put('difelikefalin','Difelikefalin',['Korsuva','Kapruvia'],KD,'Kappa opioid receptor agonist','Target dry body weight · micrograms/kg','Administer after dialysis; this product is removed by the dialyser.',[],
 modality(single('Adult moderate/severe CKD-associated pruritus','At end of each HD treatment','0.5 micrograms/kg IV bolus using target dry body weight'), 'Give into the venous line after blood is no longer circulating through the dialyser; follow rinse-back/flush instructions.'),None,
 modality(notes='Not studied in PD; US label does not recommend use in this population.',status='avoid'),
 notes='Dose is in micrograms, not milligrams. Watch for dizziness, sedation, mental-status changes and falls; review other CNS depressants.',refs=['difelikefalin-label'],flag='monitor',formulation='IV · end of HD')
d['modalities']['ckd']=not_indicated('The curated injectable product is indicated for adults undergoing HD, not non-dialysis CKD.')

label('tenapanor-label','c57e279c-0f1b-4238-81b7-4e0dc0cc60c5','Xphozah: 1–2, 5.1, 7; revised May 2025')
d=put('tenapanor-phosphate','Tenapanor (Xphozah)',['Xphozah','Tenapanor'],EL,'Intestinal NHE3 inhibitor','Serum phosphate / tolerability · not eGFR band dosing','Phosphate-lowering product and indication; separate from IBS formulations.',[],
 modality(single('Adult dialysis hyperphosphataemia · labelled add-on setting','Initial dose','30 mg PO twice daily just before first and last meals'), 'Do not take immediately before HD; take before the next meal after dialysis.'),None,
 modality(single('Adult CKD on dialysis · labelled add-on setting','PD initial dose','30 mg PO twice daily just before first and last meals'),'Monitor phosphate and GI tolerability; label indication is CKD on dialysis.'),
 notes='For inadequate binder response or intolerance of any binder dose. Severe diarrhoea may require dose adjustment. Mechanical GI obstruction is a contraindication. This is not the IBS-C product dosing entry.',refs=['tenapanor-label'],flag='monitor',formulation='Oral · Xphozah phosphate indication')
d['modalities']['ckd']=not_indicated('The curated US phosphate indication is CKD on dialysis; non-dialysis phosphate use is not included.')

label('patiromer-label','bf002984-d6c9-46df-aecb-a07733f763c1','2 and 5–7: adult starting dose, separation and monitoring')
put('patiromer','Patiromer',['Veltassa'],EL,'Potassium binder','Serum potassium / response · not eGFR bands','Titrate to potassium rather than reducing dose by CKD stage.',single('Adult hyperkalaemia · initial regimen','Serum-potassium guided','8.4 g PO once daily initially; maximum 25.2 g daily'),
 restricted('No HD-specific protocol curated; do not replace urgent dialysis or emergency hyperkalaemia care with this entry.'),
 notes='Not an emergency treatment for life-threatening hyperkalaemia. Separate most other oral medicines by ≥3 h unless shown not to interact. Monitor potassium, magnesium and GI tolerability.',refs=['patiromer-label'],flag='monitor',formulation='Oral suspension')

label('szc-label','90bf8e28-748d-4e4b-a19f-9cf483370eff','2.1–2.2 chronic-HD schedule; limitations and interactions')
put('sodium-zirconium-cyclosilicate','Sodium zirconium cyclosilicate',['Lokelma','SZC'],EL,'Potassium binder','Serum potassium / dialysis schedule','The chronic-HD schedule differs from non-dialysis correction dosing.',[
 table('US non-dialysis adult regimen',['Initial correction','Maintenance'],['10 g PO three times daily for up to 48 h','Usually 10 g daily; titrate per potassium and full label'])],
 modality(single('US chronic haemodialysis','Initial regimen','5 g PO once daily on NON-dialysis days only'), 'Consider 10 g initial dose on non-dialysis days if K >6.5 mEq/L; this does not replace emergency management. Reassess pre-HD potassium after the long interval.'),
 notes='Not an emergency treatment for life-threatening hyperkalaemia. Monitor potassium and oedema/sodium burden. Other oral medicines generally require ≥2 h separation; check label exceptions.',refs=['szc-label'],flag='monitor',formulation='Oral suspension')

label('sevelamer-label','e6328460-a57b-450b-a48c-6dcd4b476360','Renvela: 1–2.1 binder-naive adult dialysis starting table')
sv=[table('US binder-naive adult dialysis patient',['Phosphate >5.5 to <7.5 mg/dL','Phosphate ≥7.5 mg/dL'],['0.8 g PO three times daily with meals','1.6 g PO three times daily with meals'])]
d=put('sevelamer-carbonate','Sevelamer carbonate',['Renvela','Sevelamer'],EL,'Non-calcium phosphate binder','Serum phosphate / meal intake','Dose follows phosphate and meals, not a creatinine-clearance band.',[],modality(sv),None,modality(sv),
 notes='Titrate by phosphate; switching from another binder needs a separate conversion. Contraindicated in bowel obstruction. Review separation/monitoring of concomitant oral drugs. Carbonate is the formulation curated here.',refs=['sevelamer-label'],flag='monitor',formulation='Oral · carbonate tablets or suspension')
d['modalities']['ckd']=not_indicated('This US Renvela indication is CKD on dialysis. Non-dialysis uses require separate jurisdiction-specific guidance.')

label('sucroferric-label','237da26c-f38c-4faa-93ad-735e71c9d0c1','Velphoro: adult dosing and administration; 2026 label')
sf=single('Adult CKD on dialysis · initial dose','With meals','One 500 mg iron chewable tablet PO three times daily')
d=put('sucroferric-oxyhydroxide','Sucroferric oxyhydroxide',['Velphoro'],EL,'Iron-based phosphate binder','Serum phosphate / meal intake','The labelled 500 mg strength refers to iron, not total compound mass.',[],modality(sf),None,modality(sf),
 notes='Chew or crush; do not swallow whole. Each tablet contains 500 mg iron equivalent to 2,500 mg sucroferric oxyhydroxide. Titrate by phosphate. Review drug-specific separation and iron/GI precautions.',refs=['sucroferric-label'],flag='monitor',formulation='Oral chewable · 500 mg iron per tablet')
d['modalities']['ckd']=not_indicated('The curated adult US indication is CKD on dialysis.')

label('ferric-citrate-label','aadd18e0-3752-11e4-8510-0800200c9a66','Auryxia: separate dialysis phosphate and non-dialysis iron indications')
fc=single('Hyperphosphataemia · adult CKD on dialysis','Initial dose','2 tablets PO three times daily with meals')
put('ferric-citrate','Ferric citrate',['Auryxia'],EL,'Phosphate binder / oral iron', 'Indication, phosphate and iron indices','The dose differs between dialysis phosphate control and non-dialysis iron treatment.',
 single('Iron-deficiency anaemia · adult CKD not on dialysis','Initial dose','1 tablet PO three times daily with meals'),modality(fc),None,modality(fc),
 notes='Auryxia tablet = 210 mg ferric iron, equivalent to 1 g ferric citrate. Swallow whole. Maximum 12 tablets/day; titrate by indication. Monitor iron indices and phosphate. Contraindicated in iron-overload syndromes.',refs=['ferric-citrate-label'],flag='monitor',formulation='Oral · Auryxia tablets')

label('budesonide-igan-label','938cada4-d6bf-4252-836f-dd40f9eadb4d','Tarpeyo: adult primary IgAN, 9-month course and taper')
put('budesonide-targeted','Budesonide (IgAN targeted release)',['Tarpeyo','Kinpeygo','Budesonide'],KD,'Targeted-release corticosteroid','Disease eligibility / trial population; not a renal dose band','Formulation-specific IgAN regimen; do not substitute other budesonide products.',[
 table('US Tarpeyo · eligible primary IgAN',['Treatment course','Final 2 weeks on discontinuation'],['16 mg PO once daily for a 9-month course','Reduce to 8 mg PO once daily for final 2 weeks'])],
 restricted('No HD regimen curated; the pivotal trial enrolled non-dialysis patients with eGFR ≥35.'),
 notes='Swallow whole in the morning ≥1 h before food. Trial eGFR ≥35 is an evidence boundary, not a universal contraindication cutoff. Adrenal suppression, infections, liver impairment and CYP3A4 inhibitors require full review. Kinpeygo local product instructions need separate confirmation.',refs=['budesonide-igan-label'],flag='monitor',formulation='Oral · US Tarpeyo delayed-release 4 mg capsules')

# Preserve source provenance for the original collection without claiming a BNF comparison.
for d in drugs:
    if 'referenceChecks' not in d:
        d['referenceChecks']={'bnf':{'edition':'92 (September 2026)','status':'comparison_pending','reason':'Monograph text inaccessible; not independently checked.'},'pdr':{'status':'not_checked'}}
    d.setdefault('jurisdiction','Selected UCSF institutional guidance / US labels; see the linked sources')
