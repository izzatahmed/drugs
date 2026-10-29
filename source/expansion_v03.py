"""Additional source summaries. Each entry remains an unapproved clinical draft."""
def put3(*args, **kwargs):
    d=put(*args, **kwargs)
    d['addedInVersion']='0.3.0'
    return d
def noadj(text='No renal dose adjustment specified; use the indication-specific regimen.'):
    return single('Renal adjustment only · not a complete prescription','Renal impairment',text)

u('ampicillin','ampicillin-0')
put3('ampicillin','Ampicillin',['Principen'],AB,'Aminopenicillin',CRCL,'The selected IV regimen is for infections other than the separate UCSF UTI regimen.',[
 table('Other infections · IV',['>50','30–49','15–29','<15'],['2 g IV every 4 h','2 g IV every 6 h','2 g IV every 8 h','2 g IV every 12 h'])],
 modality(single('Other infections','High-flux IHD','2 g IV every 12 h')),
 modality(single('Other infections','CVVHD','2 g IV every 6 h')),
 notes='UTI dosing differs. Exact CrCl 50 is not assigned in the source bands; confirm the original/local protocol.',formulation='IV')
u('ampicillin-sulbactam','ampicillin-sulbactam-unasyn')
put3('ampicillin-sulbactam','Ampicillin / sulbactam',['Unasyn'],AB,'Penicillin + β-lactamase inhibitor',CRCL,'Doses refer to the total combination amount.',[
 table('Standard adult dosing',['>30','15–30','<15'],['3 g IV every 6 h','3 g IV every 12 h','3 g IV every 24 h'])],
 modality(single('Standard adult dosing','High-flux IHD','3 g IV every 12 h')),
 modality(single('Standard adult dosing','CVVHD','3 g IV every 6 h')),
 notes='Carbapenem-resistant Acinetobacter regimens require a separate high-dose specialist protocol.',formulation='IV')
u('piperacillin-tazobactam','piperacillin-tazobactam-zosyn')
source('piptazo-protocol','UCSF IDMP · Piperacillin/tazobactam infusion protocol','https://idmp.ucsf.edu/piptazoextendedinfusion','Short-infusion renal dosing; HD and CVVHD tables')
put3('piperacillin-tazobactam','Piperacillin / tazobactam',['Zosyn','Tazocin'],AB,'Penicillin + β-lactamase inhibitor',CRCL,'Short-infusion, non-Pseudomonas table only; extended infusion and Pseudomonas regimens differ.',[
 table('Non-Pseudomonas infection · short infusion',['>50','10–50','<10'],['3.375 g IV every 6 h','3.375 g IV every 8 h','2.25 g IV every 8 h'])],
 modality(single('UCSF short-infusion regimen','High-flux IHD','2.25 g IV every 8 h'),refs=['piptazo-protocol']),
 restricted('Select an approved CRRT infusion protocol matched to the delivered prescription; no automatic CRRT dose assigned.'),
 notes='Do not use this table for Pseudomonas or convert a short infusion to an extended infusion without its full loading/maintenance protocol.',refs=['piperacillin-tazobactam','piptazo-protocol'],formulation='IV · short infusion only')
u('ceftazidime','ceftazidime')
put3('ceftazidime','Ceftazidime',['Fortaz','Fortum','Tazicef'],AB,'Third-generation cephalosporin',CRCL,'Selected short-infusion adult regimen.',[
 table('Short infusion',['>50','31–50','15–30','<15'],['2 g IV every 8 h','2 g IV every 12 h','2 g IV every 24 h','1 g IV every 24 h'])],
 modality(single('UCSF regimen','High-flux IHD','1 g IV once now and after HD')),
 modality(single('UCSF regimen','CVVHD','2 g IV every 12 h')),formulation='IV · short infusion')
u('oseltamivir','oseltamivir')
put3('oseltamivir','Oseltamivir',['Tamiflu'],AB,'Influenza neuraminidase inhibitor',CRCL,'Treatment doses only; prophylaxis uses a different schedule.',[
 table('Influenza treatment',['>60','31–60','10–30'],['75 mg PO twice daily','30 mg PO twice daily','30 mg PO once daily'])],
 modality(single('Influenza treatment','High-flux IHD','30 mg PO once now, then after each HD session')),
 modality(single('Influenza treatment','CVVHD','75 mg PO twice daily')),
 notes='Choose the complete treatment duration and eligibility separately; post-HD dosing is not indefinite prophylaxis. Non-dialysis CrCl <10 is not assigned here.',formulation='Oral')
label('remdesivir-label','c0978fa8-53ff-4ca2-82a7-567fd3e958ca','2, 8.6: no renal adjustment including dialysis')
put3('remdesivir','Remdesivir',['Veklury'],AB,'Antiviral RNA polymerase inhibitor','No renal dose adjustment in checked US label','The checked label allows use across renal impairment, including dialysis.',
 noadj(),modality(noadj('No renal adjustment, including dialysis; administration need not be timed to HD.')),
 notes='Eligibility, loading dose, course duration and hepatic monitoring must follow the complete current label. Older renal restrictions should not be substituted for this checked label.',refs=['remdesivir-label'],flag='no_adjust',formulation='IV')

pdr('famotidine-pdr','Pepcid-AC-Maximum-Strength-famotidine-3585')
label('famotidine-label','cd95271c-cf39-47fb-97a6-f6ee1e619e4a','2.2, Table 2; renal/CNS/QT precautions')
put3('famotidine','Famotidine',['Pepcid','Pepcid AC'], 'Gastrointestinal','H2 receptor antagonist',CRCL,'Oral non-erosive GERD maximum doses below are indication-specific.',[
 table('Symptomatic non-erosive GERD · oral maximum',['CrCl 30–60','CrCl <30'],['20 mg PO once daily','20 mg PO every other day'])],
 restricted('PDR advises administration after HD; a dialysis dose is not selected automatically from this GERD table.'),
 notes='Other ulcer/erosive indications and IV dosing differ. Renal accumulation can increase CNS effects and QT risk. Confirm the exact CrCl 60 boundary in the original product guidance.',refs=['famotidine-pdr','famotidine-label'],formulation='Oral · non-erosive GERD only')
pdr('cetirizine-pdr','Cetirizine-Hydrochloride-Tablets-cetirizine-hydrochloride-2934')
put3('cetirizine-oral','Cetirizine (oral)',['Zyrtec','Cetirizine'], 'Allergy & respiratory','Second-generation antihistamine',CRCL,'This entry covers oral products; IV cetirizine has different renal guidance.',[
 table('US PDR · adult oral renal adjustment',['CrCl >31','CrCl ≤31'],['No renal adjustment to the usual oral regimen','No more than 5 mg PO once daily'])],
 modality(single('Adult oral product','IHD','No more than 5 mg PO once daily'),'Not removed by HD in the cited PDR summary.'),
 notes='Do not apply the oral reduction to IV cetirizine. Monitor antihistamine effects.',refs=['cetirizine-pdr'],formulation='Oral')
pdr('loratadine-pdr','Claritin-loratadine-1039')
put3('loratadine','Loratadine',['Claritin','Clarityn'], 'Allergy & respiratory','Second-generation antihistamine',CRCL,'Reduced initial frequency for severe impairment.',[
 table('Adult initial regimen',['CrCl ≥30','CrCl <30'],['No renal adjustment','10 mg PO every other day initially'])],
 modality(single('Adult initial regimen','IHD','10 mg PO every other day initially'),'Not removed by HD.'),refs=['loratadine-pdr'],formulation='Oral')
label('fexofenadine-label','e5a207e4-472b-4bf9-8cd3-a018ef3a82bb','Adult dosing in decreased renal function')
put3('fexofenadine','Fexofenadine',['Allegra','Telfast'], 'Allergy & respiratory','Second-generation antihistamine','Decreased renal function · label terminology','The label recommends a lower initial adult dose with decreased renal function.',
 single('Adult initial dose · decreased renal function','Non-dialysis renal impairment','60 mg PO once daily initially'),
 restricted('Do not assume the non-dialysis initial dose is a validated HD prescription; reconcile product guidance with renal pharmacy.'),
 refs=['fexofenadine-label'],formulation='Oral')

pdr('metoclopramide-pdr','Reglan-Tablets-metoclopramide-956')
put3('metoclopramide','Metoclopramide',['Reglan','Maxolon'], 'Gastrointestinal','Dopamine antagonist / prokinetic',CRCL,'Diabetic gastroparesis oral dosing only; GERD and injection regimens differ.',[
 table('Diabetic gastroparesis · oral',['CrCl >60','CrCl ≤60'],['Usual indication-specific oral regimen','5 mg PO four times daily; maximum 20 mg/day'])],
 modality(single('Diabetic gastroparesis · oral','ESRD on HD','5 mg PO twice daily; maximum 10 mg/day')),None,
 modality(single('Diabetic gastroparesis · oral','ESRD on CAPD','5 mg PO twice daily; maximum 10 mg/day')),
 notes='Review full duration limits, movement-disorder warnings and interactions; this is not an IV antiemetic protocol.',refs=['metoclopramide-pdr'],formulation='Oral · diabetic gastroparesis')
label('ondansetron-label','4dcd1e4c-6a9c-7ac6-e063-6394a90a39bf','8.7: renal impairment; oral product')
put3('ondansetron','Ondansetron',['Zofran'], 'Gastrointestinal','5-HT3 antagonist','No renal adjustment in checked oral label','The renal statement does not select the dose for a specific antiemetic indication.',
 noadj(),notes='The checked oral label notes limited experience beyond first-day administration in renal impairment. Use the full product label for indication, duration and precautions.',refs=['ondansetron-label'],flag='no_adjust',formulation='Oral')
pdr('omeprazole-pdr','Omeprazole-omeprazole-24360')
put3('omeprazole','Omeprazole',['Prilosec','Losec'], 'Gastrointestinal','Proton pump inhibitor','No renal dose adjustment in checked source','Renal adjustment and the need for long-term acid suppression are separate decisions.',
 noadj(),modality(noadj('No dose adjustment for HD in the checked PDR summary.')),
 refs=['omeprazole-pdr'],flag='no_adjust',formulation='Oral')
pdr('baclofen-pdr','Baclofen-baclofen-1058')
label('baclofen-label','4585aafe-0af8-4786-a419-6a7e76671ca2','Renal impairment and caution with reduced renal function')
d=put3('baclofen','Baclofen',['Lioresal'], 'Pain & neurology','GABA-B agonist','Renal function and toxicity risk','Renal impairment requires special caution; this entry deliberately assigns no numeric dose.',[],
 restricted('Consider an alternative in HD because of serious adverse effects reported with baclofen. No routine dialysis dose assigned.'),
 notes='The label advises caution and possible dose reduction in renal impairment. Do not treat a small empiric dose as established safe dosing in advanced CKD.',refs=['baclofen-pdr','baclofen-label'],flag='caution',formulation='Oral · intrathecal dosing excluded')
d['modalities']['ckd']=restricted('Renal-pharmacy/nephrology assessment required. No numeric CKD regimen curated.')

pdr('amlodipine-pdr','Norvasc-amlodipine-besylate-1853')
put3('amlodipine','Amlodipine',['Norvasc'],CV,'Dihydropyridine calcium-channel blocker','No renal dose adjustment in checked source','Titrate the indication-specific dose by clinical response.',
 noadj(),modality(noadj('No renal adjustment; not meaningfully removed by HD in the cited summary.')),
 refs=['amlodipine-pdr'],flag='no_adjust',formulation='Oral')
source('kdigo-bp-dialysis','KDIGO conference report · CKD and arrhythmias','https://doi.org/10.1093/eurheartj/ehy060','Beta-blocker pharmacokinetics and renal dosing table','Specialist consensus report')
put3('metoprolol','Metoprolol',['Lopressor','Toprol XL','Betaloc'],CV,'Beta blocker','Clinical response / formulation','The consensus table does not require a renal dose reduction.',
 noadj(),restricted('Metoprolol is dialyzable; assess timing, blood pressure and indication with the dialysis team.'),
 notes='Immediate-release and extended-release products require their own regimens. This is a renal-adjustment summary, not a formulation conversion.',refs=['kdigo-bp-dialysis'],flag='monitor',formulation='Oral · IR and ER distinct')
label('carvedilol-label','e5e766e3-ef75-4100-e053-2995a90a510f','Renal impairment pharmacokinetics; haemodialysis')
put3('carvedilol','Carvedilol',['Coreg','Dilatrend'],CV,'Alpha/beta blocker','Clinical response / tolerability','Renal impairment can increase exposure; clinical titration and monitoring remain necessary.',
 noadj('No fixed eGFR-based regimen is selected here. Titrate the labelled indication-specific regimen by clinical response.'),
 modality(noadj('The checked label states carvedilol is not significantly cleared by HD; dosing still follows clinical tolerance.')),
 refs=['carvedilol-label'],flag='monitor',formulation='Oral')
label('furosemide-label','ede9846b-b4c5-4be2-9188-fd65e66cd893','Dosage individualisation; renal/electrolyte and parenteral precautions')
d=put3('furosemide','Furosemide',['Lasix','Frusemide'],CV,'Loop diuretic','Urine output / volume response / electrolytes','The dose is individualised by response; an eGFR band does not choose a useful dose.',[],
 restricted('Residual urine output and volume status are required. No automatic HD diuretic dose assigned.'),
 notes='Monitor fluid balance and electrolytes. IV administration has rate-related precautions; do not substitute oral and IV doses without a conversion protocol.',refs=['furosemide-label'],flag='monitor',formulation='Oral or IV')
d['modalities']['ckd']=restricted('Individualise dose and route by indication, response and fluid/electrolyte monitoring. No numeric renal-band table curated.')

label('atorvastatin-label','74d03dfe-6fe1-42e4-8048-b5b42874da96','Atorvastatin component: 8.6 renal impairment')
put3('atorvastatin','Atorvastatin',['Lipitor'], 'Gout & lipids','Statin','No renal dose adjustment in checked label','No renal adjustment is required for the atorvastatin component.',noadj(),
 notes='Renal impairment increases myopathy risk. This adjustment statement does not determine whether to initiate a statin on dialysis.',refs=['atorvastatin-label'],flag='no_adjust',formulation='Oral')
pdr('pravastatin-pdr','Pravastatin-Sodium-pravastatin-sodium-3511')
put3('pravastatin','Pravastatin',['Pravachol'], 'Gout & lipids','Statin',CRCL,'Severe renal impairment changes the starting dose and maximum.',[
 table('Adult renal adjustment',['Mild/moderate impairment','CrCl <30'],['No renal adjustment','Start 10 mg PO once daily; maximum 40 mg/day'])],
 notes='Dialysis statin initiation and interactions need separate review.',refs=['pravastatin-pdr'],formulation='Oral')
pdr('ezetimibe-pdr','Zetia-ezetimibe-401')
put3('ezetimibe','Ezetimibe',['Zetia','Ezetrol'], 'Gout & lipids','Cholesterol absorption inhibitor','No renal dose adjustment in checked source','Combination-product dosing restrictions may come from the accompanying statin.',noadj(),
 refs=['ezetimibe-pdr'],flag='no_adjust',formulation='Oral')

pdr('tacrolimus-pdr','Prograf-tacrolimus-1331')
d=put3('tacrolimus','Tacrolimus',['Prograf','Advagraf','Envarsus','Astagraf XL'], 'Transplant & immunology','Calcineurin inhibitor','Trough concentration / transplant protocol','Use transplant-specific therapeutic monitoring; no generic CKD-band dose is assigned.',[],
 restricted('Specialist transplant dosing and therapeutic drug monitoring are required; no automatic dialysis prescription.'),
 notes='Nephrotoxicity, trough concentration and interactions guide dose changes. Immediate- and extended-release products are not freely interchangeable.',refs=['tacrolimus-pdr'],flag='monitor',formulation='Systemic · formulation-specific oral or IV')
d['modalities']['ckd']=restricted('Use the lower end of the therapeutic range where the source advises it; follow the transplant protocol and trough targets.')
label('cyclosporine-label','c36132b2-3ec7-4c43-a25e-75cbdbe3d88d','Renal impairment; transplant versus non-transplant indications')
d=put3('cyclosporine','Ciclosporin / cyclosporine',['Neoral','Sandimmune','Gengraf','Ciclosporin','Cyclosporine'], 'Transplant & immunology','Calcineurin inhibitor','Trough concentration / renal toxicity','Indication and formulation are essential to interpreting renal restrictions.',[],
 restricted('HD does not establish a standard dose. Transplant protocol, levels and nephrotoxicity monitoring are required.'),
 notes='The checked label restricts use in renal impairment for rheumatoid arthritis/psoriasis. Transplant use is a separate monitored setting. Modified and non-modified formulations are distinct.',refs=['cyclosporine-label'],flag='caution',formulation='Systemic · product-specific')
d['modalities']['ckd']=restricted('No universal renal dose: separate transplant therapeutic monitoring from non-transplant renal restrictions in the full label.')
label('mycophenolate-label','c3ded171-89da-4644-9ee8-dbcf6258036f','Kidney transplant: severe chronic graft impairment and delayed graft function')
put3('mycophenolate-mofetil','Mycophenolate mofetil',['CellCept','MMF'], 'Transplant & immunology','Antimetabolite immunosuppressant','GFR · mL/min/1.73 m² as label','Selected renal-transplant guidance only; do not transfer this maximum to every indication.',
 single('Kidney transplant · severe chronic graft impairment','GFR <25','Avoid doses greater than 1 g PO twice daily'),
 restricted('Use transplant protocol and close monitoring; no automatic dialysis dose assigned.'),
 notes='Delayed graft function does not itself require adjustment in the checked label, but monitoring is necessary. Mycophenolate sodium is a separate formulation.',refs=['mycophenolate-label'],flag='monitor',formulation='Oral · mofetil renal-transplant setting')
pdr('azathioprine-pdr','Azasan-azathioprine-1892')
d=put3('azathioprine','Azathioprine',['Imuran','Azasan'], 'Transplant & immunology','Thiopurine antimetabolite','Clinical response / blood counts / renal function','A single quantitative renal algorithm is not provided in the cited PDR summary.',[],
 notes='Oliguric patients early after transplantation may be more sensitive. Dose individualisation and monitoring are required; use the full label and interaction guidance.',refs=['azathioprine-pdr'],flag='monitor',formulation='Oral')
d['modalities']['ckd']=restricted('Modify according to clinical response and renal function; no numeric CKD regimen curated.')

label('cinacalcet-label','55f95ae0-84ac-4ae4-b7a0-7590ab919ae1','Adult secondary hyperparathyroidism on dialysis; initial dosing and monitoring')
ci=single('Adult secondary hyperparathyroidism · CKD on dialysis','Initial regimen','30 mg PO once daily with food')
d=put3('cinacalcet','Cinacalcet',['Sensipar','Mimpara'],EL,'Calcimimetic','Calcium / phosphorus / PTH','The curated secondary-hyperparathyroidism indication requires dialysis.',[],
 modality(ci),None,modality(ci),notes='Check calcium/phosphorus within 1 week and PTH 1–4 weeks after initiation or adjustment; titrate with the full label and hypocalcaemia precautions.',refs=['cinacalcet-label'],flag='monitor',formulation='Oral')
d['modalities']['ckd']=not_indicated('The selected US secondary-hyperparathyroidism indication is not for CKD patients who are not on dialysis. Other indications are not curated.')
label('etelcalcetide-label','cd270093-c6a8-4596-a4ab-e6aa0a2c8a0c','Adult HD secondary hyperparathyroidism; calcium requirements and cinacalcet switch')
d=put3('etelcalcetide','Etelcalcetide',['Parsabiv'],EL,'IV calcimimetic','Calcium / PTH / HD schedule','This IV product is for adults receiving haemodialysis.',[],
 modality(single('Adult HD secondary hyperparathyroidism','Initial regimen','5 mg IV three times weekly at the end of HD'),'Corrected calcium must be at or above the lower normal limit before initiation. Follow full administration instructions.'),
 notes='Check calcium within 1 week of initiation/adjustment. Stop cinacalcet at least 7 days before starting; follow the full calcium and PTH titration algorithm.',refs=['etelcalcetide-label'],flag='monitor',formulation='IV · end of HD')
d['modalities']['ckd']=not_indicated('Curated indication requires HD.')
d['modalities']['pd']=not_indicated('Curated indication requires HD; not a PD regimen.')

u('micafungin','micafungin')
mi=single('Invasive candidiasis · selected adult regimen','Renal impairment','100 mg IV every 24 h; no renal adjustment')
put3('micafungin','Micafungin',['Mycamine'],AB,'Echinocandin antifungal','No renal adjustment in cited regimen','Other indications can use a different dose.',mi,modality(mi),modality(mi),
 notes='Obesity or elevated MIC may require specialist review. The selected dose is not the endocarditis/esophageal regimen.',flag='no_adjust',formulation='IV')
label('caspofungin-label','08fb61ee-a05a-4ce1-934c-8cd26c5733db','8.7 renal impairment and haemodialysis')
put3('caspofungin','Caspofungin',['Cancidas'],AB,'Echinocandin antifungal','No renal dose adjustment in checked label','Renal adjustment does not specify the loading or indication-specific maintenance dose.',
 noadj(),modality(noadj('No renal adjustment. Not dialyzable; no post-HD supplemental dose is required.')),
 notes='Hepatic impairment and interactions have separate instructions.',refs=['caspofungin-label'],flag='no_adjust',formulation='IV')
label('anidulafungin-label','a88d9010-55fb-4a02-baff-042cd27688ea','8.7 renal insufficiency and haemodialysis')
put3('anidulafungin','Anidulafungin',['Eraxis','Ecalta'],AB,'Echinocandin antifungal','No renal dose adjustment in checked label','Use the indication-specific loading and maintenance regimen from the full label.',
 noadj(),modality(noadj('No renal adjustment including HD; administration need not be timed to HD.')),
 refs=['anidulafungin-label'],flag='no_adjust',formulation='IV')
