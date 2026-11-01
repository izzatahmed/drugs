# ---- v0.19.0 batch: newer approved medicines and vaccines for CKD, dialysis and transplant ----
def P_(i, brand, flag, metric, summary, ckd, ihd=None, pd=None, considerations=None, folder='us3', extra=None):
    mods = dict(ckd=ckd)
    if ihd: mods['ihd'] = ihd
    if pd: mods['pd'] = pd
    LAB[i] = f'{folder}/{i}.json'
    add(i, brand, promote=True, flag=flag, metric=metric, summary=summary, mods=mods, considerations=considerations)
    if extra: C[i]['extraSources'] = extra
S = lambda ind, rows, ev, notes='': M('summarized', [T(ind, rows)], notes, ev)
HDT = lambda rows, ev, notes='': M('summarized', [T('Haemodialysis · US label', rows)], notes, ev)
CV, TI, VX, GL = 'Cardiovascular', 'Transplant & immunology', 'Vaccines', 'Gout & lipids'
NEW.update({
 'evinacumab': ('Evinacumab', ['Evkeeza'], GL, 'ANGPTL3 inhibitor (monoclonal antibody)', ['Parenteral']),
 'lomitapide': ('Lomitapide', ['Juxtapid', 'Lojuxta'], GL, 'MTP inhibitor', ['Oral']),
 'aprocitentan': ('Aprocitentan', ['Tryvio', 'Jeraygo'], CV, 'Endothelin receptor antagonist', ['Oral']),
 'sotagliflozin': ('Sotagliflozin', ['Inpefa'], CV, 'SGLT1/SGLT2 inhibitor', ['Oral']),
 'vericiguat': ('Vericiguat', ['Verquvo'], CV, 'Soluble guanylate cyclase stimulator', ['Oral']),
 'mavacamten': ('Mavacamten', ['Camzyos'], CV, 'Cardiac myosin inhibitor', ['Oral']),
 'belumosudil': ('Belumosudil', ['Rezurock'], TI, 'ROCK2 inhibitor', ['Oral']),
 'imlifidase': ('Imlifidase', ['Idefirix'], TI, 'IgG-cleaving enzyme (desensitisation)', ['Parenteral']),
 'vaccine-hepatitis-b-engerix': ('Hepatitis B vaccine (Engerix-B)', ['Engerix-B', 'HBV vaccine'], VX, 'Recombinant hepatitis B vaccine', ['Parenteral']),
 'vaccine-hepatitis-b-recombivax': ('Hepatitis B vaccine (Recombivax HB, dialysis formulation)', ['Recombivax HB', 'HBV vaccine'], VX, 'Recombinant hepatitis B vaccine', ['Parenteral']),
 'vaccine-hepatitis-b-heplisav': ('Hepatitis B vaccine, adjuvanted (Heplisav-B)', ['Heplisav-B', 'HBV vaccine'], VX, 'Recombinant hepatitis B vaccine (CpG 1018 adjuvant)', ['Parenteral']),
 'vaccine-zoster-recombinant': ('Zoster vaccine, recombinant (Shingrix)', ['Shingrix', 'RZV', 'herpes zoster vaccine'], VX, 'Recombinant adjuvanted zoster vaccine (non-live)', ['Parenteral']),
 'vaccine-pneumococcal-pcv20': ('Pneumococcal conjugate vaccine 20-valent (Prevnar 20)', ['Prevnar 20', 'PCV20', 'Prevenar 20'], VX, 'Pneumococcal conjugate vaccine', ['Parenteral']),
 'vaccine-pneumococcal-pcv21': ('Pneumococcal conjugate vaccine 21-valent (Capvaxive)', ['Capvaxive', 'PCV21'], VX, 'Pneumococcal conjugate vaccine', ['Parenteral']),
 'vaccine-influenza-high-dose': ('Influenza vaccine, high-dose (Fluzone High-Dose)', ['Fluzone High-Dose', 'flu vaccine'], VX, 'Inactivated influenza vaccine', ['Parenteral']),
 'vaccine-rsv': ('RSV vaccine (Arexvy)', ['Arexvy', 'respiratory syncytial virus vaccine'], VX, 'Recombinant adjuvanted RSV vaccine', ['Parenteral']),
 'vaccine-covid19-mrna': ('COVID-19 mRNA vaccine (Comirnaty)', ['Comirnaty', 'SARS-CoV-2 vaccine'], VX, 'mRNA vaccine', ['Parenteral']),
})
for i in NEW: LAB.setdefault(i, f'us3/{i}.json')
LAB['imlifidase'] = 'uk3/imlifidase.json'

# -------- Newer medicines --------
P_('evinacumab', 'EVKEEZA', 'no_adjust', 'Renal function', 'Exposure unchanged in mild–moderate impairment; no data in severe impairment.',
   S('HoFH · US label', [('Mild or moderate impairment', 'Usual dose'), ('Severe impairment', 'No data')], ['Observed trough serum evinacumab-dgnb concentrations at steady-state were comparable between patients with mild or moderate renal impairment and patients with normal renal function', 'No data are available in patients with severe renal impairment']))
P_('lomitapide', 'JUXTAPID', 'adjust', 'eGFR · mL/min/1.73 m²', 'ESRD on haemodialysis: maximum 40 mg daily (adults). Not studied in other renal impairment.',
   S('HoFH · US label', [('Mild, moderate or severe impairment, or ESRD not on dialysis', 'Not studied')], ['JUXTAPID has not been studied in patients with mild, moderate, or severe renal impairment, including those with end stage renal disease not receiving dialysis']),
   ihd=HDT([('ESRD on haemodialysis, adults', 'Maximum 40 mg per day')], ['Table 5: Dosage Adjustment for Patients with End Stage Renal Disease Receiving Hemodialysis Age GROUP MAXIMUM RECOMMENDED DAILY DOSAGE 2 to 10 years 15 mg 11 to 17 years 30 mg 18 years and older 40 mg', 'The maximum recommended dosage of JUXTAPID in patients with end-stage renal disease receiving hemodialysis is lower than in those with normal renal function']))
P_('aprocitentan', 'TRYVIO', 'caution', 'eGFR · mL/min', 'Not recommended at eGFR <15 or on dialysis. CKD raises oedema/fluid-retention risk; small early eGFR dip.',
   S('Resistant hypertension · US label', [('CKD (eGFR ≥15)', 'Usual dose; monitor for oedema/fluid retention'), ('eGFR <15 mL/min or dialysis', 'Not recommended')],
     ['TRYVIO is not recommended in patients with kidney failure (eGFR <15 mL/min) or on dialysis', 'Patients with renal impairment are at increased risk of edema/fluid retention', 'Initiation of TRYVIO may cause an initial small decrease in estimated glomerular filtration rate (eGFR) that occurs within the first 6 weeks of starting therapy and then stabilizes']),
   ihd=M('avoid', notes='Not recommended on dialysis.', ev=['TRYVIO is not recommended in patients with kidney failure (eGFR <15 mL/min) or on dialysis', 'Dialysis is unlikely to be effective because aprocitentan is highly protein-bound']))
P_('sotagliflozin', 'INPEFA', 'monitor', 'eGFR · mL/min/1.73 m²', 'Studied down to eGFR 25; not studied below 25 or on dialysis. Early creatinine rise expected.',
   S('Heart failure / CV risk · US label', [('eGFR 25–60', 'Usual dose (studied in SCORED)'), ('eGFR <25 or dialysis', 'Not studied')],
     ['Efficacy and safety studies with INPEFA did not enroll patients with an eGFR less than 25 mL/min/1', 'Initiation of SGLT2 inhibitors, including INPEFA, causes a small increase in serum creatinine and decrease in eGFR', 'Assess renal function prior to initiation of INPEFA and then as clinically indicated']))
P_('vericiguat', 'VERQUVO', 'no_adjust', 'eGFR · mL/min/1.73 m²', 'No adjustment at eGFR ≥15 not on dialysis; not studied below 15 or on dialysis.',
   S('Heart failure · US label', [('eGFR ≥15, not on dialysis', 'No dose adjustment'), ('eGFR <15 or dialysis', 'Not studied')], ['No dosage adjustment of VERQUVO is recommended in patients with estimated glomerular filtration rate (eGFR) ≥15 mL/min/1', 'VERQUVO has not been studied in patients with eGFR <15 mL/min/1']),
   ihd=M('insufficient_data', notes='Not studied on dialysis; unlikely to be removed by HD (highly protein bound).', ev=['VERQUVO is unlikely to be removed by hemodialysis because of high protein binding']))
P_('mavacamten', 'CAMZYOS', 'monitor', 'eGFR · mL/min/1.73 m²', 'No PK change at eGFR 30–89; effect of eGFR <30 or dialysis unknown.',
   S('Obstructive HCM · US label', [('eGFR 30–89', 'No clinically significant PK difference'), ('eGFR <30 or dialysis', 'Unknown')], ['No clinically significant differences in the pharmacokinetics of mavacamten were observed based on age (range: 18-82 years), sex, race, ethnicity, or mild (eGFR: 60 to 89 mL/min/1', 'The effects of severe (eGFR: 15 to 30 mL/min/1']))
P_('belumosudil', 'REZUROCK', 'caution', 'eGFR · mL/min/1.72 m²', 'No PK change in mild–moderate impairment; severe impairment not studied — weigh risk and benefit.',
   S('Chronic GVHD · US label', [('Mild to moderate impairment', 'Usual dose'), ('Severe impairment', 'Not studied; consider risks and benefits before starting')], ['For patients with pre-existing severe renal impairment, consider the risks and potential benefits before initiating treatment with REZUROCK', 'The effect of severe renal impairment on the pharmacokinetics of belumosudil has not been studied']))
P_('imlifidase', 'Idefirix', 'monitor', 'Kidney transplant candidates (on dialysis)', 'Used before deceased-donor kidney transplant in highly sensitised patients. Cleaves IgG: antibody medicines (basiliximab, rituximab, rATG, IVIG, belatacept) given around it are inactivated.',
   M('specialist', notes='Patients are on dialysis awaiting transplant; no renal dose statement.', ev=['Idefirix is indicated for desensitisation treatment of highly sensitised adult kidney transplant patients with positive crossmatch against an available deceased donor', 'Antibody-based medicinal products cleaved by imlifidase include, but are not limited to basiliximab, rituximab, alemtuzumab, adalimumab, denosumab, belatacept, etanercept, rabbit anti-thymocyte globulin (rATG) and intravenous immunoglobulin (IVIg)', 'Imlifidase does not degrade equine anti-thymocyte globulin and no time interval between administrations needs to be considered']),
   folder='uk3', considerations='EU authorisation (EMA); not approved in the US. Time antibody-based induction and rescue medicines around the imlifidase dose as the SmPC specifies.')

# -------- Vaccines --------
VXNOTE = 'Vaccines are not renally dose-adjusted except where the label gives a dialysis schedule. CDC: hepatitis B vaccination is recommended for all susceptible chronic haemodialysis patients and for people with CKD before they need dialysis; the adult immunization schedule by medical condition has a column for kidney failure, end-stage renal disease or dialysis. Live vaccines can cause adverse reactions with altered immunocompetence (chronic renal disease can itself alter immunocompetence); after transplant, immunosuppression generally rules out live vaccines, so vaccinate before transplant where possible (CDC General Best Practice Guidelines).'
VXSRC = ['cdc-hd-vaccination', 'cdc-adult-schedule', 'cdc-altered-immunocompetence']
P_('vaccine-hepatitis-b-engerix', 'ENGERIX-B', 'adjust', 'Dialysis status · anti-HBs', 'Adults on haemodialysis: 4 doses of 2 mL (40 mcg) at 0, 1, 2 and 6 months; annual anti-HBs; booster when <10 mIU/mL.',
   S('Hepatitis B prevention · US label', [('Adults (not on dialysis)', '1 mL at 0, 1 and 6 months'), ('Adults on haemodialysis', '2 mL at 0, 1, 2 and 6 months')], ['Adults on Hemodialysis Primary immunization consists of a series of 4 doses (2 mL each) given as a single 2 mL dose or two 1 mL doses on a 0‑, 1‑, 2‑, and 6‑month schedule']),
   ihd=HDT([('Primary series', '2 mL at 0, 1, 2 and 6 months'), ('Follow-up', 'Annual anti-HBs; 2 mL booster when below 10 mIU/mL')], ['Adults on Hemodialysis Primary immunization consists of a series of 4 doses (2 mL each) given as a single 2 mL dose or two 1 mL doses on a 0‑, 1‑, 2‑, and 6‑month schedule', 'Therefore, the need for booster doses should be assessed by annual antibody testing', 'A 2 mL booster dose (as a single 2 mL dose or two 1 mL doses) should be given when antibody levels decline below 10 mIU/mL1', 'In hemodialysis patients, antibody response is lower than in healthy persons and protection may persist only as long as antibody levels remain above 10 mIU/mL']),
   considerations=VXNOTE, extra=VXSRC)
P_('vaccine-hepatitis-b-recombivax', 'RECOMBIVAX HB', 'adjust', 'Predialysis / dialysis', 'Dialysis Formulation (40 mcg/1 mL): 3 doses at 0, 1 and 6 months; revaccinate if anti-HBs <10 mIU/mL 1–2 months after dose 3.',
   S('Hepatitis B prevention · US label', [('Adults on predialysis or dialysis', 'Dialysis Formulation 1.0 mL at 0, 1 and 6 months')], ['RECOMBIVAX HB Dialysis Formulation: Adults on predialysis and dialysis: A series of 3 doses (1.0 mL each) given on a 0-, 1-, and 6-month schedule']),
   ihd=HDT([('Primary series', 'Dialysis Formulation 1.0 mL at 0, 1 and 6 months'), ('Non-response', 'Booster or revaccination if anti-HBs <10 mIU/mL at 1–2 months after dose 3')], ['RECOMBIVAX HB Dialysis Formulation: Adults on predialysis and dialysis: A series of 3 doses (1.0 mL each) given on a 0-, 1-, and 6-month schedule', 'Consider a booster dose or revaccination with RECOMBIVAX HB Dialysis Formulation (blue color code) in predialysis/dialysis patients if the anti-HBs level is less than 10 mIU/mL at 1 to 2 months after the third dose']),
   considerations=VXNOTE, extra=VXSRC)
P_('vaccine-hepatitis-b-heplisav', 'HEPLISAV-B', 'caution', 'Dialysis status', 'Safety and effectiveness not established in adults on haemodialysis (label); immunosuppression may blunt response.',
   M('specialist', notes='Label: not established on haemodialysis. For dialysis patients use a vaccine with a labelled dialysis schedule unless local policy differs.', ev=['Safety and effectiveness of HEPLISAV-B have not been established in adults on hemodialysis', 'Immunocompromised persons, including individuals receiving immunosuppressant therapy, may have a diminished immune response to HEPLISAV-B']),
   ihd=M('insufficient_data', notes='Not established in adults on haemodialysis.', ev=['Safety and effectiveness of HEPLISAV-B have not been established in adults on hemodialysis']), considerations=VXNOTE, extra=VXSRC)
P_('vaccine-zoster-recombinant', 'SHINGRIX', 'no_adjust', 'Immunosuppression', 'Non-live: indicated from age 18 when immunodeficiency or immunosuppression raises zoster risk (studied in kidney transplant recipients).',
   S('Zoster prevention · US label', [('Immunosuppressed adults ≥18 (including kidney transplant)', 'Usual 2-dose series')], ['in adults aged 18 years and older who are or will be at increased risk of HZ due to immunodeficiency or immunosuppression caused by known disease or therapy', 'e The first dose was administered between 4 to 18 months after renal transplantation']), considerations=VXNOTE, extra=VXSRC)
P_('vaccine-pneumococcal-pcv20', 'Prevnar 20', 'no_adjust', 'Immunosuppression', 'No renal adjustment; response may be reduced by immunosuppressive therapy.',
   S('Pneumococcal prevention · US label', [('CKD, dialysis or transplant', 'Usual single dose; reduced response possible on immunosuppression')], ['Individuals with impaired immune responsiveness due to the use of immunosuppressive therapy (including irradiation, corticosteroids, antimetabolites, alkylating agents, and cytotoxic agents) may not respond optimally to Prevnar 20']), considerations=VXNOTE, extra=VXSRC)
P_('vaccine-pneumococcal-pcv21', 'CAPVAXIVE', 'no_adjust', 'Immunosuppression', 'No renal adjustment; studied in adults with CKD; response may be reduced on immunosuppression.',
   S('Pneumococcal prevention · US label', [('CKD, dialysis or transplant', 'Usual single dose; reduced response possible on immunosuppression')], ['Individuals with altered immunocompetence, including those receiving immunosuppressive therapy, may have a reduced immune response to CAPVAXIVE']), considerations=VXNOTE, extra=VXSRC)
P_('vaccine-influenza-high-dose', 'Fluzone High-Dose', 'no_adjust', 'Immunosuppression', 'No renal adjustment; immunosuppression may reduce the response. Annual vaccination.',
   S('Influenza prevention · US label', [('CKD, dialysis or transplant', 'Usual annual dose; response may be lower on immunosuppression')], ['If Fluzone High-Dose Southern Hemisphere is administered to immunocompromised persons, including those receiving immunosuppressive therapy, the expected immune response may not be obtained']), considerations=VXNOTE, extra=VXSRC)
P_('vaccine-rsv', 'AREXVY', 'no_adjust', 'Immunosuppression', 'No renal adjustment; studied in kidney and lung transplant recipients; response may be reduced.',
   S('RSV prevention · US label', [('CKD, dialysis or transplant', 'Usual single dose; response may be reduced on immunosuppression')], ['Immunocompromised persons, including those receiving immunosuppressive therapy, may have a diminished immune response to AREXVY', 'The safety and immunogenicity of AREXVY have been assessed in 261 solid organ transplant recipients']), considerations=VXNOTE, extra=VXSRC)
P_('vaccine-covid19-mrna', 'COMIRNATY', 'no_adjust', 'Immunosuppression', 'No renal adjustment; follow CDC guidance for immunocompromised people (transplant, dialysis).',
   S('COVID-19 prevention · US label', [('CKD, dialysis or transplant', 'Usual dose; follow CDC immunocompromised guidance for additional doses')], ['Immunocompromised persons, including individuals receiving immunosuppressant therapy, may have a diminished immune response to COMIRNATY', 'The Centers for Disease Control and Prevention has published considerations related to COVID-19 vaccination guidance for people who are immunocompromised']), considerations=VXNOTE, extra=VXSRC)
