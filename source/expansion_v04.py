"""Sourced cardiovascular pharmacokinetics and two requested renal profiles.

Unknown values are explicit. Dialysability is evidence by modality, never inferred
from protein binding or Vd. Source checks are not independent clinical approval.
"""
def find_drug(ident): return next(d for d in drugs if d['id']==ident)
def pk_smpc(ident,product):
    return source(ident+'-pk', 'UK SmPC · '+find_drug(ident)['name'],
        'https://www.medicines.org.uk/emc/product/'+product+'/smpc',
        '4.2, 4.9 and 5.2: selected adult pharmacokinetics, renal impairment and dialysis', 'UK product information')
def fact(value=None,context='',refs=None,status=None):
    return dict(status=status or ('sourced' if value else 'not_reported'),value=value,
        context=context or ('No numeric value reported in the checked source.' if not value else ''),sourceIds=refs or [])
def missing_fact(): return fact(context='Not yet curated. No value is inferred.',status='not_curated')
def missing_dialysis(): return dict(status='not_curated',value=None,context='Modality-specific removal data have not been curated.',sourceIds=[])
def dial(value,refs,status='removed',context=''):
    return dict(status=status,value=value,context=context,sourceIds=refs)
def pk(ident,ref,half,vd,pb,hd=None,renal=None,half_context='',vd_context='',pb_context='',notes=''):
    d=find_drug(ident);r=[ref]
    d['pharmacokinetics']=dict(status='source_summary',sourceCheckedAt=DATE,
        halfLife=fact(half,half_context,r),renalHalfLife=fact(renal,'Renal impairment / ESKD; not an on-dialysis half-life.',r) if renal else fact(None,'A separate numeric half-life in renal impairment/ESKD is not reported in the checked source.',r),
        volumeOfDistribution=fact(vd,vd_context,r),proteinBinding=fact(pb,pb_context,r),
        dialysability={'ihd':hd or dict(status='not_reported',value=None,context='Removal is not specified in the checked PK source. No inference from binding or Vd.',sourceIds=r),
            'pd':missing_dialysis(),'crrt':missing_dialysis(),'sled':missing_dialysis()},notes=notes)
    d['updatedInVersion']='0.4.0'

# Captopril: promote the existing inventory ID rather than adding a duplicate.
smpc('captopril-uk','Captopril 25 mg/5 mL oral solution','5250')
label('captopril-label','607687f4-63cf-411c-a20b-21d238a6b7a7','Pharmacokinetics; renal adjustment; adult HD and PD removal statements')
source('captopril-vss-study','Captopril kinetics · healthy-volunteer study',
       'https://pubmed.ncbi.nlm.nih.gov/7037265/',
       'Five healthy subjects, 10 mg oral/IV: steady-state versus central/terminal distribution volumes', 'Primary pharmacokinetic study')
cap=find_drug('captopril')
cap.update(entryType='renal',drugClass='ACE inhibitor',aliases=['Capoten'],flag='adjust',
    formulation='Oral · UK solution renal table; doses are mg, not mL',
    kidneyMetric='CrCl · mL/min/1.73 m² as written in the UK product table',
    summary='Renally eliminated and removable by HD. The UK table gives TOTAL daily starting and maximum amounts, not amounts per dose.',
    sourceIds=['captopril-uk','captopril-label'],
    considerations='Individualise the divided-dose schedule and titrate slowly; monitor BP, potassium and renal function. Confirm the local formulation/concentration. ACE inhibitors can cause membrane-associated anaphylactoid reactions; check the dialysis membrane and full label. Do not infer a post-HD supplemental dose from the removal statement.',
    jurisdiction='UK oral-solution renal table; US tablet label supports PK/removal statements. Local product instructions must be checked.',
    completeness='Selected adult renal starting/maximum total daily amounts and PK only. The renal table does not define the frequency or an RRT regimen. Full indication, interaction and contraindication review is required.',
    updatedInVersion='0.4.0')
cap['review']['sourceCheckedAt']=DATE
cap['modalities']['ckd']=modality([table('UK renal table · TOTAL daily amounts, not per-dose amounts',
    ['>40','21–40','10–20','<10'],[
        'Initial total 25–50 mg/day; maximum total 150 mg/day',
        'Initial total 25 mg/day; maximum total 100 mg/day',
        'Initial total 12.5 mg/day; maximum total 75 mg/day',
        'Initial total 6.25 mg/day; maximum total 37.5 mg/day'])],
    'Select the dosing frequency separately. These maxima are limits, not treatment targets. Preserve the indexed source metric and verify gaps at fractional CrCl boundaries.',refs=['captopril-uk'])
cap['modalities']['ihd']=restricted('Captopril is removable from adult circulation by HD. An individual dose, session timing and any supplement require an approved renal protocol; the non-dialysis table is not an HD prescription.')
cap['modalities']['ihd']['sourceIds']=['captopril-label']
cap['modalities']['pd']=restricted('The US label states that PD does not effectively remove captopril. This does not establish a PD maintenance dose.')
cap['modalities']['pd']['sourceIds']=['captopril-label']
for key in ['crrt','sled']: cap['modalities'][key]=modality(notes='No prescription-specific regimen curated. Do not extrapolate from IHD or CKD.')

smpc('amlodipine-uk','Amlodipine tablets','13534')
am=find_drug('amlodipine')
am['aliases']=sorted(set(am['aliases']+['Istin','Amlor']))
am['summary']='Usual adult hypertension starting dose 5 mg once daily; titrate to a maximum 10 mg daily. No renal dose reduction; not dialysable in the checked SmPC.'
am['sourceIds'].append('amlodipine-uk')
am['modalities']['ckd']=modality(single('Adult hypertension · UK SmPC','Renal impairment','5 mg PO once daily initially; titrate by response to a maximum 10 mg daily'),
    'Renal impairment does not require a dose reduction. Hepatic impairment and individual tolerance require separate assessment.',refs=['amlodipine-uk'])
am['modalities']['ihd']=modality(single('Adult hypertension · renal adjustment statement','IHD','No renal dose reduction; use the individually titrated once-daily regimen'),
    'Amlodipine is not dialysable in the checked product information.',refs=['amlodipine-uk'])
am['updatedInVersion']='0.4.0'

source('beta-hd-trial','Beta-blocker dialysability · high-flux crossover trial (2018)',
       'https://pubmed.ncbi.nlm.nih.gov/29519953/',
       'Eight adults on maintenance HD; atenolol, metoprolol, bisoprolol, carvedilol. Recovery-clearance and arterial–venous methods differ.', 'Primary dialysis pharmacokinetic study')

pk('captopril','captopril-uk','About 2 h',None,'25–30%',
   dial('Removed by HD',['captopril-label'],context='Adult circulation. The checked label does not supply a universal removal percentage.'),
   half_context='Unchanged parent drug. Half-life of total captopril/disulfide material is a different measure.',
   notes='Renal impairment causes accumulation; the checked label does not give a separate numeric ESKD half-life.')
cap['pharmacokinetics']['volumeOfDistribution']=fact('0.7 L/kg','Steady-state Vss after IV dosing in five healthy subjects; central Vd 0.2 L/kg and terminal-phase Vd 2 L/kg are different measures.',['captopril-vss-study'])
cap['pharmacokinetics']['dialysability']['pd']=dial('Not effectively removed by PD',['captopril-label'],'not_removed','US label removal statement; not a PD dose recommendation.')
pk('amlodipine','amlodipine-uk','35–50 h','About 21 L/kg','About 97.5%',
   dial('Not dialysable',['amlodipine-uk'],'not_removed','Product-information statement; no universal PD/CRRT removal estimate is supplied.'),
   half_context='Terminal plasma elimination half-life.',vd_context='Adult reference distribution volume.',pb_context='In-vitro plasma protein binding.',
   notes='Renal impairment does not correlate with plasma concentration in the checked SmPC; hepatic impairment can prolong half-life.')

r=pk_smpc('lisinopril','15574')
pk('lisinopril',r,'12.6 h',None,'No serum protein binding other than circulating ACE',
   dial('Removed by HD',[r],context='Label: mean plasma concentration decrease about 60% over 4 h; dialysis clearance 40–55 mL/min. This is not 60% of the administered dose.'),
   half_context='Effective accumulation half-life; prolonged terminal ACE-binding phase is a different measure.',
   notes='Elimination slows in renal impairment, particularly GFR <30 mL/min; no single numeric ESKD half-life is assigned.')
r=pk_smpc('atenolol','14699')
pk('atenolol',r,'About 6 h',None,'About 3%',
   dial('Readily removed by high-flux HD',['beta-hd-trial'],context='n=8 crossover trial; recovery-method dialysis clearance 72 mL/min. Not a removal percentage.'),
   notes='The SmPC states half-life increases in severe renal impairment; a separate ESKD value and Vd are not reported here. Binding estimates differ between products/sources.')
source('metoprolol-pk','Medsafe · IPCA metoprolol tartrate datasheet',
       'https://medsafe.govt.nz/profs/Datasheet/i/IPCA-Metoprololtab.pdf','5.2: adult parent-drug half-life, Vd, binding and renal impairment','Regulator-hosted product information')
pk('metoprolol','metoprolol-pk','3–4 h; 7–9 h in poor metabolisers','3.2–5.6 L/kg','About 10%',
   dial('Readily removed by high-flux HD',['beta-hd-trial'],context='n=8 crossover trial; recovery-method dialysis clearance 87 mL/min. Not a removal percentage.'),
   half_context='Parent-drug elimination in the tartrate datasheet; not the dosing interval of an extended-release product.',
   notes='Parent-drug PK is not materially affected by renal impairment in this datasheet. CYP2D6 phenotype and hepatic impairment affect elimination.')
r=pk_smpc('carvedilol','3106')
pk('carvedilol',r,'About 6 h','About 2 L/kg','98–99%',
   dial('Negligible removal in high-flux HD',['beta-hd-trial'],'negligible',context='n=8 crossover trial; recovery-method dialysis clearance 0.2 mL/min. Other clearance methods gave a different value.'),
   half_context='Average oral elimination half-life in this SmPC.',
   notes='Exposure can increase in renal impairment despite little renal elimination. Liver disease alters distribution and clearance.')
r=pk_smpc('bisoprolol','101897')
pk('bisoprolol',r,'10–12 h','3.5 L/kg','About 30%',
   dial('Removed by high-flux HD',['beta-hd-trial'],context='n=8 crossover trial; recovery-method clearance 44 mL/min, less than atenolol/metoprolol. Older non-dialysable classifications should not replace this measured result.'),
   notes='This study does not define a universal supplement or PD/CRRT prescription.')

r=pk_smpc('losartan','14493')
pk('losartan',r,'Parent about 2 h; active metabolite 6–9 h','34 L (parent)','≥99% (parent and active metabolite)',
   dial('Neither parent nor active metabolite removed by HD',[r],'not_removed'),
   notes='Parent and active-metabolite kinetics differ; do not use the parent half-life as the duration of effect.')
r=pk_smpc('valsartan','8184')
pk('valsartan',r,'About 6 h','About 17 L','94–97%',
   dial('Unlikely to be removed by dialysis',[r],'unlikely','Label prediction, not a measured removal percentage.'),
   half_context='Label general elimination half-life; the same label separately reports a terminal beta phase about 9 h.',vd_context='Steady-state volume after IV administration.',
   notes='The checked SmPC identifies limited safe-use experience at CrCl <10 mL/min or on dialysis; non-removal is not evidence of eligibility.')
r=pk_smpc('candesartan','14555')
source('candesartan-hd-study','Candesartan in regular HD · primary PK study',
       'https://pmc.ncbi.nlm.nih.gov/articles/PMC2014260/',
       'Negligible HD elimination; about 0.2% of an 8 mg cilexetil dose recovered as unchanged candesartan in dialysate', 'Primary dialysis pharmacokinetic study')
pk('candesartan',r,'About 9 h','0.1 L/kg','>99%',
   dial('Negligible removal in the cited HD study',['candesartan-hd-study'],'negligible','Study-specific result, not a modern-circuit removal percentage.'),
   renal='Approximately doubled in severe renal impairment',half_context='Active candesartan, not the cilexetil prodrug.',vd_context='Apparent distribution volume.')
r=pk_smpc('irbesartan','14518')
pk('irbesartan',r,'11–15 h','53–93 L','About 96%',dial('Not removed by HD',[r],'not_removed'),half_context='Terminal elimination half-life.',notes='The checked SmPC reports no significant PK change in renal impairment or HD.')
r=pk_smpc('telmisartan','5386')
pk('telmisartan',r,'>20 h','About 500 L','>99.5%',dial('Not dialysable',[r],'not_removed','The product also states it is not removed by haemofiltration, without a circuit-specific CRRT clearance.'),
   half_context='Terminal elimination half-life.',vd_context='Apparent steady-state volume.',notes='The checked label states elimination half-life is unchanged in renal impairment. No CRRT dose is inferred from the haemofiltration statement.')
r=pk_smpc('enalapril','2672')
pk('enalapril',r,'About 11 h (enalaprilat)',None,'≤60% (enalaprilat)',
   dial('Enalaprilat is removed by HD',[r],context='Active metabolite; confirm session-specific dose/timing separately.'),
   half_context='Effective accumulation half-life of the active metabolite after repeated oral enalapril; not the prodrug half-life.',
   notes='Enalaprilat exposure and effective half-life increase with significant renal impairment. Vd is not reported in this checked SmPC.')
r=pk_smpc('ramipril','14718')
pk('ramipril',r,'13–17 h (ramiprilat)',None,'Ramipril about 73%; ramiprilat about 56%',
   dial('Ramiprilat is poorly removed by HD',[r],'limited','The SmPC also describes ramipril as slightly dialysable; parent and active metabolite must be distinguished.'),
   half_context='Effective active-metabolite half-life after repeated 5–10 mg doses; longer at 1.25–2.5 mg. Terminal enzyme-binding phase differs.',
   notes='Renal impairment reduces ramiprilat clearance. A separate numeric ESKD half-life and Vd are not provided here.')

r=pk_smpc('nifedipine','11473')
pk('nifedipine',r,'1.7–3.4 h (conventional formulation)',None,'About 95%',
   dial('Label states not dialysable',[r],'not_removed','Statement appears in the overdose section; no quantitative therapeutic-circuit study is supplied.'),
   half_context='Intrinsic terminal elimination after conventional capsules; modified-release exposure is release-limited and is not represented by this value.',
   notes='Formulation matters. The conventional-formulation half-life does not select a modified-release dosing interval.')
r=pk_smpc('diltiazem','14')
pk('diltiazem',r,'About 5–7 h','About 5 L/kg','80–85%',
   half_context='VIAZEM XL product information; other formulations and repeated dosing can differ.',
   notes='This product-specific PK summary does not supply a dialysis dose or a measured dialytic removal value.')
r=pk_smpc('verapamil','11475')
pk('verapamil',r,'3–7 h','1.8–6.8 L/kg','About 90%',
   dial('Verapamil and norverapamil not significantly removed by HD',['verapamil-iv-pk'],'negligible'),
   half_context='Oral elimination half-life reported in this SmPC; IV and repeated/modified-release dosing can differ.',
   notes='Parent and norverapamil differ; hepatic impairment prolongs elimination. Distribution range is from healthy subjects.')
source('verapamil-iv-pk','UK SmPC · Verapamil injection','https://www.medicines.org.uk/emc/product/979/smpc','5.2: ESRD comparison and HD removal of verapamil/norverapamil','UK product information')
r=pk_smpc('furosemide','12129')
label('furosemide-hd-label','d07ff11c-c1ab-41e6-a455-f2b89340106e','Overdose: HD does not accelerate elimination')
pk('furosemide',r,'About 1–1.5 h','0.1–1.2 L/kg','>98%',
   dial('HD does not accelerate elimination',['furosemide-hd-label'],'negligible','Label statement in overdose; no therapeutic-circuit removal percentage is given.'),
   half_context='Terminal half-life after IV administration as reported within the tablet SmPC.',
   notes='Distribution and protein binding are illness-dependent; the broad Vd range is preserved from this source.')
r=pk_smpc('hydrochlorothiazide','7746')
pk('hydrochlorothiazide',r,'6–15 h','4–8 L/kg','40–70%',half_context='Terminal plasma elimination.',vd_context='Apparent volume reported for the HCTZ component of Co-Diovan.',
   notes='The HCTZ component accumulates in erythrocytes. Other labels report different distribution/binding estimates; retain this source and do not silently combine ranges.')
r=pk_smpc('chlorthalidone','11981')
pk('chlorthalidone',r,'About 50 h',None,'About 76% (plasma)',
   half_context='Elimination from whole blood/plasma.',pb_context='Plasma binding is distinct from extensive erythrocyte carbonic-anhydrase binding.',
   notes='The checked label states renal dysfunction does not alter PK, but this is not a drug-eligibility or CKD dosing statement. No removal inference is made from erythrocyte binding.')
find_drug('chlorthalidone')['aliases'].append('Chlortalidone')
r=pk_smpc('indapamide','14345')
pk('indapamide',r,'15–18 h',None,'About 79% · plasma/RBC binding description',half_context='Beta-phase elimination in the 2.5 mg tablet SmPC.',
   pb_context='Source describes binding to plasma protein and erythrocytes; not a free-fraction estimate in CKD.',notes='Vd and dialytic removal are not reported in this checked source.')
r=pk_smpc('hydralazine','2604')
pk('hydralazine',r,'Average 2–3 h','1.5 ± 1.0 L/kg','88–90%',renal='Up to 16 h in severe renal failure (CrCl <20 mL/min)',
   half_context='Reference plasma value; acetylator status and conjugate measurement affect interpretation.',
   notes='No dialysis-removal estimate is assigned from protein binding or distribution.')
r=pk_smpc('clonidine','102313')
pk('clonidine',r,'5–25.5 h',None,'30–40%',
   dial('Only minimally removed during routine HD',[r],'limited','Label states post-HD supplemental clonidine is not needed. This is not a complete maintenance regimen.'),
   renal='Up to 41 h in severe renal impairment',half_context='Terminal half-life in the checked oral-tablet SmPC.')
r=pk_smpc('methyldopa','4667')
pk('methyldopa',r,'1.8 ± 0.2 h',None,None,
   dial('Dialysable',[r],context='Product-information statement; method and percentage are not provided.'),
   notes='Renal clearance matters. Vd, protein-binding percentage and a numeric ESKD half-life are not reported in this checked SmPC.')
r=pk_smpc('spironolactone','12015')
pk('spironolactone',r,'Parent 1.4 h; canrenone 16.5 h',None,None,
   half_context='Repeated oral 100 mg in non-fasted healthy volunteers; 7-alpha-thiomethyl metabolite 13.8 h.',
   notes='Active metabolites have longer half-lives than the parent. This PK information does not remove the existing hyperkalaemia and renal-eligibility restrictions.')
r=pk_smpc('eplerenone','15373')
pk('eplerenone',r,'3–6 h','42–90 L','About 50%',dial('Not removed by HD',[r],'not_removed'),vd_context='Apparent steady-state volume.',
   notes='Existing severe-renal-impairment and potassium restrictions still apply; lack of dialytic removal does not establish suitability.')
source('sacubitril-valsartan-pk','EMA · Entresto product information',
       'https://www.ema.europa.eu/en/documents/product-information/entresto-epar-product-information_en.pdf',
       '5.2: separate parent, active metabolite, apparent volumes and binding; 4.9 dialysis statement','Regulator product information')
pk('sacubitril-valsartan','sacubitril-valsartan-pk','Sacubitril 1.43 h; LBQ657 11.48 h; valsartan 9.90 h',
   'Sacubitril 103 L; valsartan 75 L','94–97% (all three analytes)',
   dial('Unlikely to be removed by HD',['sacubitril-valsartan-pk'],'unlikely','EMA product information, overdose section: prediction based on binding, not a measured clearance.'),
   half_context='Separate mean elimination half-lives; LBQ657 is the active neprilysin-inhibiting metabolite.',vd_context='Apparent volumes in the combination; not interchangeable with IV valsartan Vss.',
   notes='Use the existing indication-specific renal guidance separately; non-removal does not establish eligibility.')

# Current renal-society table supplies ESRF/PD information where product labels
# do not. Keep its analyte/method limitations separate from parent-drug data.
source('ukka-bp-2025','UK Kidney Association · Dialysis BP guideline (January 2025)',
       'https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20Management%20of%20blood%20pressure%20guideline-Jan%202025_4.pdf',
       'Appendix D, printed p.76: HDF/high-flux, PD and ESRF half-life columns; reviewed against page image', 'Renal society clinical guideline')
uk_renal={
    'atenolol':'15–35 h','bisoprolol':'18–24 h','carvedilol':'Unchanged','metoprolol':'Unchanged',
    'amlodipine':'50 h','diltiazem':'Unchanged','nifedipine':'Unchanged','verapamil':'Increased',
    'captopril':'21–32 h','enalapril':'34–60 h','lisinopril':'40–50 h','ramipril':'Increased',
    'spironolactone':'Parent: unchanged','candesartan':'18 h','irbesartan':'Unchanged',
    'losartan':'4–6 h','telmisartan':'Unchanged','valsartan':'Unchanged'
}
uk_pd={
    'atenolol':'not_removed','bisoprolol':'not_removed','carvedilol':'unlikely','metoprolol':'not_removed',
    'amlodipine':'not_removed','diltiazem':'not_removed','nifedipine':'not_removed','verapamil':'not_removed',
    'captopril':'not_removed','enalapril':'removed','lisinopril':'unknown','ramipril':'unknown',
    'eplerenone':'unknown','spironolactone':'not_removed','candesartan':'unlikely','irbesartan':'not_removed',
    'losartan':'not_removed','telmisartan':'not_removed','valsartan':'not_removed'
}
for ident,value in uk_renal.items():
    p=find_drug(ident)['pharmacokinetics']
    p['renalHalfLife']=fact(value,'',['ukka-bp-2025'])
    p['renalHalfLife']['basis']='guideline_esrf_column'
for ident,status in uk_pd.items():
    p=find_drug(ident)['pharmacokinetics']
    p['dialysability']['pd']=dial({'not_removed':'Not dialysed','removed':'Dialysed','unlikely':'Unlikely','unknown':'Unknown'}[status],['ukka-bp-2025'],status)
p=find_drug('diltiazem')['pharmacokinetics']
p['dialysability']['ihd']=dial('Not dialysed',['ukka-bp-2025'],'not_removed','UKKA HDF/high-flux column.')
find_drug('captopril')['pharmacokinetics']['notes']='Renal impairment causes accumulation. UKKA ESRF half-life 21–32 h is a reference-table value; the table does not specify free parent versus total captopril/disulfide material. Do not calculate a dose ratio from the two half-lives.'
p=find_drug('ramipril')['pharmacokinetics']['dialysability']['ihd']
p['sourceIds'].append('ukka-bp-2025')
p['context']='SmPC: active ramiprilat poorly removed; ramipril slightly dialysable. UKKA classifies ramipril as dialysed in HDF/high-flux. Analyte and method differ; reconcile before selecting a session-timing protocol.'
p['status']='source_difference'
for ident in ['nifedipine','verapamil']:
    p=find_drug(ident)['pharmacokinetics']['dialysability']['ihd']
    p['sourceIds'].append('ukka-bp-2025')
    p['context']+=' UKKA specifically marks HDF/high-flux removal as unknown; the product-label statement does not resolve every modern prescription.'

# Every record has the requested fields. Empty is not zero or non-dialysable.
for d in drugs:
    if 'pharmacokinetics' not in d:
        d['pharmacokinetics']=dict(status='not_curated',sourceCheckedAt=None,
            halfLife=missing_fact(),renalHalfLife=missing_fact(),volumeOfDistribution=missing_fact(),proteinBinding=missing_fact(),
            dialysability={k:missing_dialysis() for k in ['ihd','pd','crrt','sled']},notes='No pharmacokinetic value or dialytic removal is inferred from another drug or drug class.')
