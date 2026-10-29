"""Broad inventory and shared OTC safety notes. Inventory is NOT renal guidance."""
source('otc-nkf-pain','National Kidney Foundation · Pain medicines and kidney disease','https://www.kidney.org/kidney-topics/pain-medicines-and-kidney-disease','Patient education: acetaminophen, systemic NSAIDs and topical medicines','Kidney charity patient guidance')
source('otc-nkf-safety','National Kidney Foundation · Safe medicine use in CKD','https://www.kidney.org/kidney-topics/safe-medicine-use-chronic-kidney-disease','Patient education: H2 blockers, antacids, PPIs and sodium phosphate','Kidney charity patient guidance')
source('otc-kcuk','Kidney Care UK · Over-the-counter medicines','https://kidneycareuk.org/kidney-disease-information/treatments/medication-for-kidney-disease/patient-info-over-the-counter-medicines/','Patient education: cold remedies, laxatives, diarrhoea and combination products','Kidney charity patient guidance')
shared_guidance={
 'acetaminophen':dict(title='Acetaminophen / paracetamol',text='Generally kidney-safe at recommended doses. Check combination cold/pain products to prevent duplicate dosing. Liver disease requires separate advice. No numeric CKD or dialysis regimen is curated here.',sourceIds=['otc-nkf-pain']),
 'systemic-nsaid':dict(title='Systemic NSAID safety',text='Systemic NSAIDs can cause AKI and worsen CKD. NKF advises avoidance in CKD, especially eGFR <60; do not self-treat. If a clinician selects one, use an individual risk assessment, the lowest dose and shortest duration. This is a class warning, not a dialysis dosing protocol.',sourceIds=['otc-nkf-pain']),
 'topical-pain':dict(title='Topical pain products',text='Label-directed topical pain products generally have lower kidney risk. Diclofenac gel has less systemic exposure than oral diclofenac. Do not exceed application limits. Lower systemic exposure does not establish safety for every product or patient.',sourceIds=['otc-nkf-pain']),
 'aspirin':dict(title='Distinguish aspirin indications',text='Analgesic/high-dose aspirin carries NSAID kidney risks. Do not use this warning to stop prescribed low-dose antiplatelet aspirin; verify the indication and exact product with the treating team.',sourceIds=['otc-nkf-pain']),
 'antacid':dict(title='Antacid ingredients in CKD',text='Calcium, magnesium, bismuth and aluminium ingredients can accumulate in CKD. Check the exact combination and renal-team advice. NKF advises avoiding aluminium-containing products because of brain toxicity. This does not define prescribed phosphate-binder dosing.',sourceIds=['otc-nkf-safety']),
 'h2':dict(title='H2 blocker accumulation',text='H2 blockers such as cimetidine and nizatidine are renally cleared and may require lower doses or longer intervals. This safety note does not provide a renal regimen; obtain a product-specific recommendation.',sourceIds=['otc-nkf-safety']),
 'ppi':dict(title='OTC proton pump inhibitors',text='Discuss OTC PPI use with the kidney team. Reassess prolonged treatment and potential kidney/mineral adverse effects. An absence of renal dose reduction does not justify unsupervised long-term use.',sourceIds=['otc-nkf-safety']),
 'phosphate':dict(title='Sodium phosphate bowel preparations',text='Oral sodium phosphate bowel preparations can cause kidney injury and should be avoided in CKD. Do not extrapolate an alternative bowel-preparation prescription from this warning.',sourceIds=['otc-nkf-safety']),
 'decongestant':dict(title='Cold remedies and decongestants',text='Kidney Care UK advises avoiding decongestant-containing cold remedies, including pseudoephedrine and phenylephrine, especially with hypertension. Check all active ingredients in combination products.',sourceIds=['otc-kcuk']),
 'constipation':dict(title='Constipation products',text='Kidney Care UK lists senna as an option. Bulk-forming ispaghula/psyllium may be unsuitable with fluid restriction. Persistent constipation and PD-related constipation need renal-team advice; no dose is selected here.',sourceIds=['otc-kcuk']),
 'diarrhoea':dict(title='Diarrhoea and rehydration',text='Kidney Care UK lists loperamide as an option for selected minor diarrhoea. Severe illness needs assessment. Use oral rehydration salts only if the treating team recommends them; fluid and electrolyte restrictions matter.',sourceIds=['otc-kcuk'])
}

def catalog_entry(name, category, routes, aliases=(), ident=None, guidance=None, otc=False):
    import re
    ident=ident or re.sub('[^a-z0-9]+','-',name.lower()).strip('-')
    assert not any(d['id']==ident for d in drugs),ident
    refs=shared_guidance[guidance]['sourceIds'] if guidance else []
    note='No drug-specific renal dose or dialysis schedule has been curated. Open a current product label and consult renal pharmacy.'
    drugs.append(dict(id=ident,name=name,aliases=list(aliases),category=category,drugClass=category,
        formulation=' / '.join(routes)+' · verify exact local product',routes=routes,otc=otc,
        kidneyMetric='Not yet curated',summary='Shared safety note available; numeric renal dosing is not curated.' if guidance else 'Catalog entry only — renal adjustment and dialysis dosing have not been curated.',
        flag='caution' if guidance else 'catalog',entryType='safety' if guidance else 'catalog',sharedGuidanceId=guidance,
        modalities={k:modality(notes=note,status='not_curated') for k in ['ckd','ihd','crrt','pd','sled']},
        considerations='',sourceIds=refs,
        labelSearchUrl='https://dailymed.nlm.nih.gov/dailymed/search.cfm?query='+__import__('urllib.parse',fromlist=['quote']).quote(name),
        review=dict(status='clinical_review_pending',sourceCheckedAt=DATE if guidance else None,clinicalReviewer=None,clinicalApprovedAt=None),
        completeness='Inventory metadata is provisional. Product identity, formulation, local availability, indications, renal guidance and all RRT settings need drug-specific verification.',
        addedInVersion='0.3.0',jurisdiction='OTC availability varies by country and strength; the OTC filter is an inventory aid, not a local supply classification.',
        referenceChecks={'bnf':{'edition':'92 (September 2026)','status':'comparison_pending','reason':'No monograph comparison completed.'},'pdr':{'status':'not_checked'}}))

# Shared notes are stored once, not copied as apparent drug-specific renal tables.
for name,ident,aliases,route,guide,otc in [
 ('Paracetamol / acetaminophen','paracetamol',['Acetaminophen','Paracetamol','Panadol','Tylenol'],'Oral','acetaminophen',True),
 ('Ibuprofen','ibuprofen',['Advil','Brufen','Nurofen'],'Oral','systemic-nsaid',True),
 ('Naproxen','naproxen',['Aleve','Naprosyn'],'Oral','systemic-nsaid',True),
 ('Aspirin','aspirin',['Acetylsalicylic acid','ASA','Bayer'],'Oral','aspirin',True),
 ('Diclofenac (systemic)','diclofenac-systemic',['Voltaren tablets','Cataflam','Diclofenac oral'],'Oral','systemic-nsaid',False),
 ('Celecoxib','celecoxib',['Celebrex'],'Oral','systemic-nsaid',False),
 ('Meloxicam','meloxicam',['Mobic'],'Oral','systemic-nsaid',False),
 ('Ketorolac','ketorolac',['Toradol'],'Parenteral','systemic-nsaid',False),
 ('Diclofenac gel','diclofenac-gel',['Voltaren gel','Voltarol gel'],'Topical','topical-pain',True),
 ('Lidocaine (topical)','lidocaine-topical',['Lidoderm','Lignocaine cream'],'Topical','topical-pain',True),
 ('Capsaicin','capsaicin',['Zostrix'],'Topical','topical-pain',True),
 ('Menthol (topical)','menthol-topical',['Biofreeze'],'Topical','topical-pain',True),
 ('Magnesium hydroxide','magnesium-hydroxide',['Milk of magnesia'],'Oral','antacid',True),
 ('Magnesium citrate','magnesium-citrate',[],'Oral','antacid',True),
 ('Aluminium hydroxide','aluminium-hydroxide',['Aluminum hydroxide'],'Oral','antacid',True),
 ('Calcium carbonate','calcium-carbonate',['Tums','Rennie'],'Oral','antacid',True),
 ('Bismuth subsalicylate','bismuth-subsalicylate',['Pepto-Bismol'],'Oral','antacid',True),
 ('Cimetidine','cimetidine',['Tagamet'],'Oral','h2',True),
 ('Nizatidine','nizatidine',['Axid'],'Oral','h2',True),
 ('Esomeprazole','esomeprazole',['Nexium'],'Oral','ppi',True),
 ('Lansoprazole','lansoprazole',['Prevacid'],'Oral','ppi',True),
 ('Sodium phosphate (oral bowel preparation)','sodium-phosphate-oral',['OsmoPrep','Visicol'],'Oral','phosphate',False),
 ('Pseudoephedrine','pseudoephedrine',['Sudafed'],'Oral','decongestant',True),
 ('Phenylephrine (oral)','phenylephrine-oral',['Oral decongestant'],'Oral','decongestant',True),
 ('Senna / sennosides','senna',['Senokot','Sennosides'],'Oral','constipation',True),
 ('Ispaghula / psyllium','psyllium',['Fybogel','Metamucil','Ispaghula'],'Oral','constipation',True),
 ('Loperamide','loperamide',['Imodium'],'Oral','diarrhoea',True),
 ('Oral rehydration salts','oral-rehydration-salts',['ORS','Dioralyte'],'Oral','diarrhoea',True),
]:
    catalog_entry(name,'OTC & medicine safety',[route],aliases,ident,guide,otc)

# A broad hospital/ambulatory inventory, not a claim of worldwide completeness.
# Rows: generic/product distinction | routes | selected aliases. No dosing is inferred.
inventory={
'Antimicrobials':'''Benzylpenicillin|Parenteral|Penicillin G
Phenoxymethylpenicillin|Oral|Penicillin V
Flucloxacillin|Oral,Parenteral|Floxapen
Dicloxacillin|Oral|
Nafcillin|Parenteral|
Oxacillin|Parenteral|
Piperacillin|Parenteral|
Cefadroxil|Oral|Duricef
Cefuroxime|Oral,Parenteral|Zinnat,Zinacef
Cefaclor|Oral|Ceclor
Cefdinir|Oral|Omnicef
Cefixime|Oral|Suprax
Cefpodoxime|Oral|Vantin
Cefotaxime|Parenteral|Claforan
Cefoxitin|Parenteral|Mefoxin
Cefotetan|Parenteral|
Cefoperazone / sulbactam|Parenteral|Sulperazon
Ceftaroline|Parenteral|Teflaro,Zinforo
Ceftobiprole|Parenteral|Zevtera
Ceftolozane / tazobactam|Parenteral|Zerbaxa
Cefepime / enmetazobactam|Parenteral|Exblifep
Sulbactam / durlobactam|Parenteral|Xacduro
Meropenem / vaborbactam|Parenteral|Vabomere,Vaborem
Imipenem / cilastatin|Parenteral|Primaxin,Tienam
Imipenem / cilastatin / relebactam|Parenteral|Recarbrio
Doripenem|Parenteral|Doribax
Aztreonam|Parenteral|Azactam
Aztreonam / avibactam|Parenteral|Emblaveo
Vancomycin|Oral,Parenteral|Vancocin
Teicoplanin|Parenteral|Targocid
Dalbavancin|Parenteral|Dalvance,Xydalba
Oritavancin|Parenteral|Orbactiv,Kimyrsa
Telavancin|Parenteral|Vibativ
Tedizolid|Oral,Parenteral|Sivextro
Gentamicin|Parenteral|
Tobramycin|Parenteral,Inhaled|
Amikacin|Parenteral,Inhaled|Amikin
Plazomicin|Parenteral|Zemdri
Streptomycin|Parenteral|
Colistimethate sodium|Parenteral,Inhaled|Colistin,Colomycin
Polymyxin B|Parenteral|
Tigecycline|Parenteral|Tygacil
Eravacycline|Parenteral|Xerava
Omadacycline|Oral,Parenteral|Nuzyra
Minocycline|Oral,Parenteral|Minocin
Tetracycline|Oral|
Clarithromycin|Oral,Parenteral|Klacid,Biaxin
Erythromycin|Oral,Parenteral|Erythrocin
Roxithromycin|Oral|Rulid
Moxifloxacin|Oral,Parenteral|Avelox
Ofloxacin|Oral,Parenteral|
Delafloxacin|Oral,Parenteral|Baxdela
Fosfomycin|Oral,Parenteral|Monuril,Monurol
Trimethoprim|Oral|
Sulfadiazine|Oral|
Dapsone|Oral|
Rifampicin|Oral,Parenteral|Rifampin,Rifadin
Rifabutin|Oral|Mycobutin
Isoniazid|Oral,Parenteral|INH
Pyrazinamide|Oral|
Ethambutol|Oral|Myambutol
Bedaquiline|Oral|Sirturo
Pretomanid|Oral|
Rifaximin|Oral|Xifaxan
Fidaxomicin|Oral|Dificid
Tinidazole|Oral|Fasigyn,Tindamax
Secnidazole|Oral|Solosec
Acyclovir|Oral,Parenteral|Aciclovir,Zovirax
Ganciclovir|Parenteral|Cytovene
Valganciclovir|Oral|Valcyte
Famciclovir|Oral|Famvir
Foscarnet|Parenteral|Foscavir
Cidofovir|Parenteral|Vistide
Letermovir|Oral,Parenteral|Prevymis
Maribavir|Oral|Livtencity
Entecavir|Oral|Baraclude
Tenofovir disoproxil|Oral|TDF,Viread
Tenofovir alafenamide|Oral|TAF,Vemlidy
Lamivudine|Oral|Epivir,Zeffix
Emtricitabine|Oral|Emtriva
Abacavir|Oral|Ziagen
Zidovudine|Oral,Parenteral|Retrovir
Dolutegravir|Oral|Tivicay
Bictegravir / emtricitabine / tenofovir alafenamide|Oral|Biktarvy
Raltegravir|Oral|Isentress
Darunavir|Oral|Prezista
Ritonavir|Oral|Norvir
Sofosbuvir / velpatasvir|Oral|Epclusa
Glecaprevir / pibrentasvir|Oral|Mavyret,Maviret
Molnupiravir|Oral|Lagevrio
Baloxavir|Oral|Xofluza
Itraconazole|Oral|Sporanox
Voriconazole|Oral,Parenteral|Vfend
Posaconazole|Oral,Parenteral|Noxafil
Isavuconazonium|Oral,Parenteral|Cresemba
Amphotericin B deoxycholate|Parenteral|Fungizone
Liposomal amphotericin B|Parenteral|AmBisome
Flucytosine|Oral|Ancobon
Nystatin|Oral,Topical|Mycostatin
Terbinafine|Oral,Topical|Lamisil
Ibrexafungerp|Oral|Brexafemme
Rezafungin|Parenteral|Rezzayo
Atovaquone|Oral|Mepron
Pentamidine|Parenteral,Inhaled|Pentam
Albendazole|Oral|Zentel,Albenza
Mebendazole|Oral|Vermox
Ivermectin|Oral,Topical|Stromectol
Praziquantel|Oral|Biltricide
Hydroxychloroquine|Oral|Plaquenil
Chloroquine|Oral|Aralen
Artesunate|Parenteral|
Artemether / lumefantrine|Oral|Coartem,Riamet''',
'Cardiovascular':'''Enalapril|Oral|Renitec,Vasotec
Enalaprilat|Parenteral|Vasotec injection
Ramipril|Oral|Tritace,Altace
Perindopril|Oral|Coversyl
Captopril|Oral|Capoten
Losartan|Oral|Cozaar
Valsartan|Oral|Diovan
Candesartan|Oral|Atacand
Irbesartan|Oral|Aprovel,Avapro
Telmisartan|Oral|Micardis
Olmesartan|Oral|Benicar,Olmetec
Aliskiren|Oral|Tekturna,Rasilez
Nifedipine|Oral|Adalat,Procardia
Felodipine|Oral|Plendil
Nicardipine|Parenteral|Cardene
Clevidipine|Parenteral|Cleviprex
Diltiazem|Oral,Parenteral|Cardizem,Tildiem
Verapamil|Oral,Parenteral|Isoptin,Calan
Bisoprolol|Oral|Concor,Zebeta
Nebivolol|Oral|Nebilet,Bystolic
Propranolol|Oral,Parenteral|Inderal
Labetalol|Oral,Parenteral|Trandate
Esmolol|Parenteral|Brevibloc
Sotalol|Oral,Parenteral|Betapace
Clonidine|Oral,Transdermal|Catapres
Methyldopa|Oral|Aldomet
Hydralazine|Oral,Parenteral|Apresoline
Minoxidil (systemic)|Oral|Loniten
Doxazosin|Oral|Cardura
Prazosin|Oral|Minipress
Tamsulosin|Oral|Flomax,Omnic
Terazosin|Oral|Hytrin
Bumetanide|Oral,Parenteral|Bumex,Burinex
Torsemide|Oral,Parenteral|Torasemide,Demadex
Hydrochlorothiazide|Oral|HCTZ
Chlorthalidone|Oral|Hygroton
Indapamide|Oral|Natrilix
Metolazone|Oral|Zaroxolyn
Acetazolamide|Oral,Parenteral|Diamox
Amiloride|Oral|Midamor
Triamterene|Oral|Dyrenium
Tolvaptan|Oral|Jinarc,Jynarque,Samsca
Digoxin|Oral,Parenteral|Lanoxin
Amiodarone|Oral,Parenteral|Cordarone
Dronedarone|Oral|Multaq
Flecainide|Oral|Tambocor
Propafenone|Oral|Rythmol
Procainamide|Parenteral|Pronestyl
Disopyramide|Oral|Norpace
Ibutilide|Parenteral|Corvert
Dofetilide|Oral|Tikosyn
Adenosine|Parenteral|Adenocard
Ivabradine|Oral|Procoralan,Corlanor
Ranolazine|Oral|Ranexa
Isosorbide mononitrate|Oral|Imdur
Isosorbide dinitrate|Oral|Isordil
Nitroglycerin|Oral,Parenteral,Transdermal|Glyceryl trinitrate,GTN
Sodium nitroprusside|Parenteral|Nipride
Milrinone|Parenteral|Primacor
Dobutamine|Parenteral|Dobutrex
Dopamine|Parenteral|
Norepinephrine|Parenteral|Noradrenaline,Levophed
Epinephrine|Parenteral|Adrenaline,EpiPen
Vasopressin|Parenteral|Pitressin
Midodrine|Oral|ProAmatine
Fenofibrate|Oral|Tricor,Lipanthyl
Gemfibrozil|Oral|Lopid
Simvastatin|Oral|Zocor
Pitavastatin|Oral|Livalo
Fluvastatin|Oral|Lescol
Evolocumab|Parenteral|Repatha
Alirocumab|Parenteral|Praluent
Inclisiran|Parenteral|Leqvio
Bempedoic acid|Oral|Nexletol,Nilemdo
Icosapent ethyl|Oral|Vascepa''',
'Anticoagulation & haematology':'''Warfarin|Oral|Coumadin,Marevan
Unfractionated heparin|Parenteral|Heparin
Dalteparin|Parenteral|Fragmin
Tinzaparin|Parenteral|Innohep
Fondaparinux|Parenteral|Arixtra
Argatroban|Parenteral|Acova
Bivalirudin|Parenteral|Angiomax
Clopidogrel|Oral|Plavix
Prasugrel|Oral|Effient,Efient
Ticagrelor|Oral|Brilinta,Brilique
Dipyridamole|Oral,Parenteral|Persantine
Cangrelor|Parenteral|Kengreal
Eptifibatide|Parenteral|Integrilin
Tirofiban|Parenteral|Aggrastat
Tranexamic acid|Oral,Parenteral|Cyklokapron
Aminocaproic acid|Oral,Parenteral|Amicar
Desmopressin|Oral,Parenteral,Nasal|DDAVP
Alteplase|Parenteral|Actilyse,Cathflo
Tenecteplase|Parenteral|Metalyse,TNKase
Protamine|Parenteral|
Idarucizumab|Parenteral|Praxbind
Andexanet alfa|Parenteral|Andexxa,Ondexxya
Epoetin alfa|Parenteral|Eprex,Epogen,Procrit
Darbepoetin alfa|Parenteral|Aranesp
Methoxy polyethylene glycol-epoetin beta|Parenteral|Mircera
Iron sucrose|Parenteral|Venofer
Ferric carboxymaltose|Parenteral|Ferinject,Injectafer
Ferric derisomaltose|Parenteral|Monofer,Monoferric
Ferumoxytol|Parenteral|Feraheme
Iron dextran|Parenteral|INFeD
Ferrous sulfate|Oral|Iron sulphate
Ferrous fumarate|Oral|
Ferrous gluconate|Oral|
Folic acid|Oral,Parenteral|
Cyanocobalamin|Oral,Parenteral|Vitamin B12
Hydroxocobalamin|Parenteral|Cyanokit
Filgrastim|Parenteral|Neupogen
Pegfilgrastim|Parenteral|Neulasta
Eltrombopag|Oral|Revolade,Promacta
Romiplostim|Parenteral|Nplate''',
'Diabetes & endocrine':'''Insulin regular|Parenteral|Actrapid,Humulin R
Insulin NPH|Parenteral|Isophane,Insulatard,Humulin N
Insulin aspart|Parenteral|NovoRapid,NovoLog,Fiasp
Insulin lispro|Parenteral|Humalog,Lyumjev
Insulin glulisine|Parenteral|Apidra
Insulin glargine|Parenteral|Lantus,Toujeo,Basaglar
Insulin degludec|Parenteral|Tresiba
Insulin detemir|Parenteral|Levemir
Glipizide|Oral|Glucotrol
Gliclazide|Oral|Diamicron
Glimepiride|Oral|Amaryl
Glibenclamide / glyburide|Oral|Daonil,Diabeta
Repaglinide|Oral|NovoNorm,Prandin
Nateglinide|Oral|Starlix
Pioglitazone|Oral|Actos
Acarbose|Oral|Glucobay,Precose
Miglitol|Oral|Glyset
Vildagliptin|Oral|Galvus
Semaglutide (oral)|Oral|Rybelsus
Exenatide (extended release)|Parenteral|Bydureon
Lixisenatide|Parenteral|Lyxumia,Adlyxin
Levothyroxine|Oral,Parenteral|Synthroid,Euthyrox
Liothyronine|Oral,Parenteral|Cytomel
Carbimazole|Oral|Neo-Mercazole
Methimazole|Oral|Thiamazole,Tapazole
Propylthiouracil|Oral|PTU
Hydrocortisone|Oral,Parenteral|Solu-Cortef
Prednisone|Oral|Deltasone
Prednisolone|Oral|Orapred
Methylprednisolone|Oral,Parenteral|Medrol,Solu-Medrol
Dexamethasone|Oral,Parenteral|Decadron
Fludrocortisone|Oral|Florinef
Octreotide|Parenteral|Sandostatin
Glucagon|Parenteral,Nasal|Baqsimi
Alendronate|Oral|Fosamax
Risedronate|Oral|Actonel
Ibandronate|Oral,Parenteral|Boniva
Zoledronic acid|Parenteral|Zometa,Reclast,Aclasta
Pamidronate|Parenteral|Aredia
Denosumab|Parenteral|Prolia,Xgeva
Teriparatide|Parenteral|Forteo,Forsteo
Romosozumab|Parenteral|Evenity
Calcitonin|Parenteral,Nasal|Miacalcin''',
'Electrolytes & phosphate':'''Calcitriol|Oral,Parenteral|Rocaltrol,Calcijex
Alfacalcidol|Oral,Parenteral|One-Alpha
Paricalcitol|Oral,Parenteral|Zemplar
Doxercalciferol|Oral,Parenteral|Hectorol
Cholecalciferol|Oral|Vitamin D3
Ergocalciferol|Oral|Vitamin D2
Calcium acetate|Oral|PhosLo,Phoslyra
Lanthanum carbonate|Oral|Fosrenol
Sevelamer hydrochloride|Oral|Renagel
Sodium bicarbonate|Oral,Parenteral|Baking soda tablets
Potassium chloride|Oral,Parenteral|KCl,Slow-K
Potassium citrate|Oral|Urocit-K
Potassium phosphate|Oral,Parenteral|
Sodium phosphate (IV)|Parenteral|Intravenous phosphate
Magnesium sulfate|Parenteral|Magnesium sulphate
Calcium gluconate|Parenteral|
Calcium chloride|Parenteral|
Sodium polystyrene sulfonate|Oral,Rectal|Kayexalate,Resonium A
Calcium polystyrene sulfonate|Oral,Rectal|Calcium Resonium
Urea (oral)|Oral|Ure-Na
Levocarnitine|Oral,Parenteral|Carnitor''',
'Pain & neurology':'''Morphine|Oral,Parenteral|MST,Oramorph
Codeine|Oral|
Oxycodone|Oral|OxyContin,Oxynorm
Hydromorphone|Oral,Parenteral|Dilaudid
Fentanyl|Parenteral,Transdermal|Duragesic
Buprenorphine|Oral,Parenteral,Transdermal|Subutex,Butrans
Methadone|Oral,Parenteral|
Pethidine / meperidine|Oral,Parenteral|Demerol
Tapentadol|Oral|Nucynta,Palexia
Tramadol (extended release)|Oral|Ultram ER
Naloxone|Parenteral,Nasal|Narcan
Paracetamol (IV)|Parenteral|Acetaminophen IV,Perfalgan,Ofirmev
Indomethacin|Oral,Rectal|Indocin
Etoricoxib|Oral|Arcoxia
Tizanidine|Oral|Sirdalud,Zanaflex
Cyclobenzaprine|Oral|Flexeril
Methocarbamol|Oral,Parenteral|Robaxin
Carbamazepine|Oral|Tegretol
Oxcarbazepine|Oral|Trileptal
Valproate|Oral,Parenteral|Valproic acid,Depakote,Epilim
Phenytoin|Oral,Parenteral|Dilantin,Epanutin
Fosphenytoin|Parenteral|Cerebyx
Lamotrigine|Oral|Lamictal
Topiramate|Oral|Topamax
Lacosamide|Oral,Parenteral|Vimpat
Brivaracetam|Oral,Parenteral|Briviact
Phenobarbital|Oral,Parenteral|Phenobarbitone
Clonazepam|Oral|Rivotril,Klonopin
Diazepam|Oral,Parenteral,Rectal|Valium
Lorazepam|Oral,Parenteral|Ativan
Midazolam|Oral,Parenteral,Nasal|Dormicum,Versed
Propofol|Parenteral|Diprivan
Dexmedetomidine|Parenteral|Precedex
Ketamine|Parenteral|Ketalar
Donepezil|Oral|Aricept
Memantine|Oral|Namenda,Ebixa
Rivastigmine|Oral,Transdermal|Exelon
Levodopa / carbidopa|Oral|Sinemet
Pramipexole|Oral|Mirapex
Ropinirole|Oral|Requip
Amantadine|Oral|Symmetrel
Sumatriptan|Oral,Parenteral,Nasal|Imigran,Imitrex
Rizatriptan|Oral|Maxalt
Rimegepant|Oral|Nurtec,Vydura
Ubrogepant|Oral|Ubrelvy
Atogepant|Oral|Qulipta,Aquipta
Erenumab|Parenteral|Aimovig''',
'Psychiatry':'''Sertraline|Oral|Zoloft,Lustral
Escitalopram|Oral|Cipralex,Lexapro
Citalopram|Oral|Cipramil,Celexa
Fluoxetine|Oral|Prozac
Paroxetine|Oral|Seroxat,Paxil
Venlafaxine|Oral|Effexor
Desvenlafaxine|Oral|Pristiq
Mirtazapine|Oral|Remeron
Bupropion|Oral|Wellbutrin,Zyban
Amitriptyline|Oral|Tryptizol,Elavil
Nortriptyline|Oral|Pamelor
Trazodone|Oral|Desyrel
Lithium|Oral|Priadel,Lithobid
Quetiapine|Oral|Seroquel
Olanzapine|Oral,Parenteral|Zyprexa
Risperidone|Oral,Parenteral|Risperdal
Paliperidone|Oral,Parenteral|Invega
Aripiprazole|Oral,Parenteral|Abilify
Haloperidol|Oral,Parenteral|Haldol
Clozapine|Oral|Clozaril
Buspirone|Oral|Buspar
Zolpidem|Oral|Stilnox,Ambien
Zopiclone|Oral|Imovane
Melatonin|Oral|Circadin''',
'Gastrointestinal':'''Pantoprazole|Oral,Parenteral|Protonix,Controloc
Rabeprazole|Oral|Pariet,Aciphex
Dexlansoprazole|Oral|Dexilant
Sucralfate|Oral|Carafate
Misoprostol|Oral|Cytotec
Domperidone|Oral|Motilium
Prochlorperazine|Oral,Parenteral,Rectal|Stemetil,Compazine
Promethazine|Oral,Parenteral|Phenergan
Granisetron|Oral,Parenteral|Kytril
Palonosetron|Parenteral|Aloxi
Aprepitant|Oral|Emend
Fosaprepitant|Parenteral|Ivemend
Lactulose|Oral,Rectal|Duphalac
Macrogol / polyethylene glycol|Oral|PEG,Movicol,MiraLAX
Bisacodyl|Oral,Rectal|Dulcolax
Sodium picosulfate|Oral|Picolax,Dulcolax Pico
Docusate|Oral,Rectal|Colace
Glycerol (rectal)|Rectal|Glycerin suppository
Linaclotide|Oral|Linzess,Constella
Lubiprostone|Oral|Amitiza
Prucalopride|Oral|Resolor,Motegrity
Diphenoxylate / atropine|Oral|Lomotil
Hyoscine butylbromide|Oral,Parenteral|Buscopan
Dicyclomine|Oral,Parenteral|Bentyl
Mebeverine|Oral|Duspatalin,Colofac
Mesalazine|Oral,Rectal|Mesalamine,Asacol,Pentasa
Sulfasalazine|Oral|Salazopyrin,Azulfidine
Ursodeoxycholic acid|Oral|Ursodiol,Ursofalk
Pancrelipase|Oral|Creon
Cholestyramine|Oral|Questran''',
'Allergy & respiratory':'''Levocetirizine|Oral|Xyzal
Desloratadine|Oral|Aerius,Clarinex
Chlorphenamine|Oral,Parenteral|Chlorpheniramine,Piriton
Diphenhydramine|Oral,Parenteral|Benadryl
Hydroxyzine|Oral|Atarax,Vistaril
Salbutamol / albuterol|Inhaled|Ventolin,ProAir
Terbutaline|Oral,Parenteral,Inhaled|Bricanyl
Formoterol|Inhaled|Foradil,Oxis
Salmeterol|Inhaled|Serevent
Ipratropium|Inhaled,Nasal|Atrovent
Tiotropium|Inhaled|Spiriva
Umeclidinium|Inhaled|Incruse
Glycopyrronium (inhaled)|Inhaled|Glycopyrrolate inhaled,Seebri
Budesonide (inhaled)|Inhaled|Pulmicort
Beclometasone|Inhaled,Nasal|Beclomethasone,Qvar
Fluticasone|Inhaled,Nasal|Flixotide,Flonase
Montelukast|Oral|Singulair
Theophylline|Oral|Uniphyllin
Aminophylline|Parenteral|
Roflumilast|Oral|Daxas,Daliresp
Acetylcysteine|Oral,Parenteral,Inhaled|N-acetylcysteine,NAC
Dextromethorphan|Oral|Delsym
Guaifenesin|Oral|Mucinex
Benzonatate|Oral|Tessalon
Omalizumab|Parenteral|Xolair
Mepolizumab|Parenteral|Nucala
Benralizumab|Parenteral|Fasenra
Dupilumab|Parenteral|Dupixent''',
'Transplant & immunology':'''Mycophenolate sodium|Oral|Myfortic
Sirolimus|Oral|Rapamune
Everolimus|Oral|Certican,Zortress,Afinitor
Belatacept|Parenteral|Nulojix
Basiliximab|Parenteral|Simulect
Antithymocyte globulin (rabbit)|Parenteral|Thymoglobulin
Rituximab|Parenteral|MabThera,Rituxan
Obinutuzumab|Parenteral|Gazyva,Gazyvaro
Cyclophosphamide|Oral,Parenteral|Endoxan,Cytoxan
Methotrexate|Oral,Parenteral|Trexall
Leflunomide|Oral|Arava
Adalimumab|Parenteral|Humira
Infliximab|Parenteral|Remicade
Etanercept|Parenteral|Enbrel
Tocilizumab|Parenteral|Actemra,RoActemra
Abatacept|Parenteral|Orencia
Anakinra|Parenteral|Kineret
Tofacitinib|Oral|Xeljanz
Baricitinib|Oral|Olumiant
Upadacitinib|Oral|Rinvoq
Apremilast|Oral|Otezla
Belimumab|Parenteral|Benlysta
Anifrolumab|Parenteral|Saphnelo
Avacopan|Oral|Tavneos
Iptacopan|Oral|Fabhalta
Eculizumab|Parenteral|Soliris
Ravulizumab|Parenteral|Ultomiris
Pegcetacoplan|Parenteral|Empaveli,Aspaveli
Inebilizumab|Parenteral|Uplizna
Efgartigimod|Parenteral|Vyvgart
Intravenous immunoglobulin|Parenteral|IVIG,Privigen,Gamunex''',
'Oncology':'''Cisplatin|Parenteral|Platinol
Carboplatin|Parenteral|Paraplatin
Oxaliplatin|Parenteral|Eloxatin
Pemetrexed|Parenteral|Alimta
Capecitabine|Oral|Xeloda
Fluorouracil|Parenteral|5-FU
Gemcitabine|Parenteral|Gemzar
Etoposide|Oral,Parenteral|Vepesid
Doxorubicin|Parenteral|Adriamycin
Paclitaxel|Parenteral|Taxol
Docetaxel|Parenteral|Taxotere
Vincristine|Parenteral|Oncovin
Bleomycin|Parenteral|Blenoxane
Melphalan|Oral,Parenteral|Alkeran
Lenalidomide|Oral|Revlimid
Pomalidomide|Oral|Pomalyst,Imnovid
Bortezomib|Parenteral|Velcade
Carfilzomib|Parenteral|Kyprolis
Daratumumab|Parenteral|Darzalex
Imatinib|Oral|Glivec,Gleevec
Dasatinib|Oral|Sprycel
Nilotinib|Oral|Tasigna
Osimertinib|Oral|Tagrisso
Olaparib|Oral|Lynparza
Rucaparib|Oral|Rubraca
Abemaciclib|Oral|Verzenio
Palbociclib|Oral|Ibrance
Ribociclib|Oral|Kisqali
Venetoclax|Oral|Venclexta,Venclyxto
Ibrutinib|Oral|Imbruvica
Acalabrutinib|Oral|Calquence
Zanubrutinib|Oral|Brukinsa
Pembrolizumab|Parenteral|Keytruda
Nivolumab|Parenteral|Opdivo
Atezolizumab|Parenteral|Tecentriq
Bevacizumab|Parenteral|Avastin
Trastuzumab|Parenteral|Herceptin
Cetuximab|Parenteral|Erbitux
Tamoxifen|Oral|Nolvadex
Anastrozole|Oral|Arimidex
Letrozole|Oral|Femara
Abiraterone|Oral|Zytiga
Enzalutamide|Oral|Xtandi
Hydroxyurea|Oral|Hydroxycarbamide,Hydrea
Rasburicase|Parenteral|Fasturtec,Elitek''',
'OTC & medicine safety':'''Simeticone|Oral|Simethicone,Gas-X
Sodium alginate combinations|Oral|Gaviscon
Sodium bicarbonate antacid combinations|Oral|Alka-Seltzer formulations vary
Potassium-containing salt substitutes|Oral|Low-sodium salt
Magnesium oxide|Oral|Mag-Ox
Vitamin C / ascorbic acid|Oral|Ascorbic acid
Vitamin A / retinol|Oral|Retinol
Multivitamins|Oral|Vitamin supplements
Zinc supplements|Oral|Zinc sulfate
St John's wort|Oral|Hypericum
Ginkgo biloba|Oral|Ginkgo
Turmeric / curcumin supplements|Oral|Curcumin
Creatine supplements|Oral|Creatine
Fluticasone nasal|Nasal|Flonase nasal
Oxymetazoline nasal|Nasal|Afrin
Xylometazoline nasal|Nasal|Otrivine
Saline nasal spray|Nasal|Sodium chloride nasal
Hydrocortisone topical|Topical|Hydrocortisone cream
Clotrimazole topical|Topical|Canesten,Lotrimin
Miconazole topical|Topical|Daktarin
Zinc oxide topical|Topical|Barrier cream
Artificial tears|Ophthalmic|Lubricating eye drops''',
'Urology & other medicines':'''Finasteride|Oral|Proscar,Propecia
Dutasteride|Oral|Avodart
Silodosin|Oral|Rapaflo,Urorec
Alfuzosin|Oral|Xatral,Uroxatral
Oxybutynin|Oral,Transdermal|Ditropan
Tolterodine|Oral|Detrusitol,Detrol
Solifenacin|Oral|Vesicare
Trospium|Oral|Sanctura
Mirabegron|Oral|Betmiga,Myrbetriq
Vibegron|Oral|Gemtesa
Sildenafil|Oral,Parenteral|Viagra,Revatio
Tadalafil|Oral|Cialis,Adcirca
Bosentan|Oral|Tracleer
Ambrisentan|Oral|Letairis,Volibris
Macitentan|Oral|Opsumit
Selexipag|Oral|Uptravi
Iloprost|Inhaled,Parenteral|Ventavis
Treprostinil|Oral,Inhaled,Parenteral|Remodulin,Tyvaso
Allopurinol (IV)|Parenteral|Aloprim
Probenecid|Oral|Benemid
Pegloticase|Parenteral|Krystexxa
Roxadustat|Oral|Evrenzo'''
}
for group, rows in inventory.items():
    for row in rows.strip().splitlines():
        name,route,aliases=row.split('|')
        catalog_entry(name,group,route.split(','),[a for a in aliases.split(',') if a],otc=group=='OTC & medicine safety')

# Explicit metadata on source profiles. Route metadata never generates a renal dose.
for d in drugs:
    d['category']={'Neurology & pain':'Pain & neurology','Anticoagulants':'Anticoagulation & haematology','Diabetes':'Diabetes & endocrine'}.get(d['category'],d['category'])
    if d.get('entryType'): continue
    d['entryType']='renal'
    text=d['formulation'].lower()
    d['routes']=[]
    if 'oral' in text or 'tablet' in text or 'capsule' in text or 'suspension' in text: d['routes'].append('Oral')
    if __import__('re').search(r'\biv\b|\bsc\b|injection|subcutaneous|intravenous',text): d['routes'].append('Parenteral')
    if d['id'] in ['semaglutide-sc','dulaglutide','liraglutide','tirzepatide','exenatide-ir','enoxaparin']: d['routes']=['Parenteral']
    if d['id']=='cyclosporine': d['routes']=['Oral','Parenteral']
    d['otc']=d['id'] in ['famotidine','cetirizine-oral','loratadine','fexofenadine','omeprazole']
    if d['id']=='omeprazole': d['sharedGuidanceId']='ppi'
    if not d['routes']: d['routes']=['Verify product']
