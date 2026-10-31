# RenalRounds v0.12.3 — cumulative GitHub Pages package

Compact adult CKD and kidney-replacement drug reference for **US and Jordan** use. The 669-entry inventory contains 357 partial renal profiles, 28 shared safety notes and 284 catalog entries. This remains an incomplete draft without independent clinical approval.

## What changed in 0.12.3

- Pharmacokinetics rebuilt from current product information for the 128 profiles that still quoted the Renal Drug Handbook (5th ed., 2018). Each value now shows the label sentence it came from: the US FDA label (DailyMed), or EMA product information (vildagliptin) or the UK SmPC (teicoplanin, domperidone, carbimazole, hyoscine butylbromide, alfacalcidol, colecalciferol) where there is no US label.
- Values a current label does not state are blank ("being rebuilt"); old handbook figures were not carried over. Metabolite values are labelled.
- The Renal Drug Handbook is no longer cited anywhere. PK coverage: 144 profiles, 45 with all four core items.
- No dose table changed.

## What changed in 0.12.2

- Pregnancy and lactation for 588 of 669 entries, quoted from each medicine's current US FDA label (ingredient-exact match; combination products excluded). Legacy FDA letters only where a label still prints one; TGA categories once a reviewer enters them.
- Reference checks on every entry: BNF, Lexidrugs, UpToDate, MIMS (Australia) and a JFDA product check, each "Not yet checked" until a named reviewer records the outcome. Their text is never reproduced.
- Review workflow: `python3 import_review.py <returned sheet.xlsx>` records approvals, reference checks and TGA categories in `reviews/`; `apply_reviews.py` applies them during the build; approved entries show "Reviewed by … on …". Requested corrections are listed for a maintainer and never applied automatically.
- No dose table changed.

## What changed in 0.12.1

- Vancomycin, gentamicin, amikacin and tobramycin have numeric CKD, haemodialysis and PD dosing (US labels; Nebraska Medicine/UNMC renal and haemodialysis protocols).
- Intraperitoneal PD-peritonitis doses from the ISPD 2022 guideline (Table 5) on the PD tab of 26 antibiotics, labelled separately from systemic PD doses.
- Vonoprazan (P-CAB) added from its US label.
- New "Pregnancy & lactation" section quoting the cited label for 63 entries; legacy FDA letters shown only where the label still prints one.
- Back arrow: icon only, lower-left corner, hides while scrolling down.

## What changed in 0.12.0

- Renal dose tables for 61 entries previously built from the Renal Drug Handbook (5th edition, 2018) were rebuilt from current product labels: 55 US FDA labels (DailyMed/openFDA, with set ID, SPL version and effective date) and 6 UK SmPCs (emc) for medicines with no US product. No dose table cites the handbook any more.
- Each table shows its source (US label, UK/EU SmPC, US hospital protocol…) and a reminder to check the JFDA-approved leaflet in Jordan.
- Where a label gives no renal statement, the entry says so instead of keeping older advice.
- Pharmacokinetic panels are unchanged in this release; handbook-cited PK values are rebuilt next.
- `checks_v120.mjs` proves that the other 607 entries are unchanged, and a cross-check confirmed every number in the rebuilt tables appears in the cited label text.

## Earlier: what changed in 0.11.3

- **Kidney function calculator** has two tabs: eGFR (CKD-EPI 2021 / legacy MDRD) and **Cockcroft–Gault creatinine clearance**, showing actual, ideal (Devine) and adjusted body weight results side by side. Most drug tables here are banded by CrCl. Neither tab selects a dose.
- **Phone layout:** the floating back button no longer covers dose tables; phones get a "Back" button at the top of each drug instead. Pressing Enter in search opens the selected drug. The calculator scrolls to its result and its back bar no longer overlaps the form.
- Converted creatinine is shown to two decimals.
- **Drug classes:** 426 entries whose class only repeated the category now show a pharmacological class.
- **Search** understands common abbreviations as whole words: PPI, H2RA, NSAID, DOAC, LMWH, SGLT2i, DPP4i, GLP1, ACEi, ARB, ARNI, CCB, SSRI, SNRI, TCA, MRA, ESA, TKI.
- Internal working notes were rewritten as neutral reader-facing statements (for example "BNF comparison not yet done").
- Each drug has a **Report an error** link that opens a pre-filled GitHub issue (no patient data).
- Link previews (Open Graph tags and canonical URL).

## Update the existing site

1. Extract this ZIP and upload all its contents to the repository's publishing root, replacing matching files and keeping folders. Do not upload the ZIP itself.
2. Wait for GitHub Pages to redeploy, then check that the top title and footer say v0.12.3.
3. If an older offline copy is still showing, open **Database & offline status** at the bottom → **Check for update** → **Load available update**.

The root `index.html` embeds the full database and code: replacing `database.json` alone does not change the running app.

## Calculator and privacy

CKD-EPI 2021 creatinine is the race-free eGFR default; IDMS MDRD without its historical race multiplier remains a labelled legacy alternative. Cockcroft–Gault uses (140 − age) × weight ÷ (72 × SCr) × 0.85 if female, with Devine ideal body weight and adjusted weight = IBW + 0.4 × (actual − IBW), shown only when actual weight exceeds IBW. Creatinine is not rounded up. All calculations are withheld for AKI, dialysis, pregnancy and children. See CALCULATOR.md.

Calculator inputs clear when the panel closes and are never stored, exported or sent. Favourites, text size and theme use browser-local storage when available. No patient identifiers or analytics are collected.

## Rebuild and verify

Run from the `source/` folder with Python 3 and Node.js; no package installation or network is required (`extract_labels_v121.py`, `extract_labels_v122.py`, `extract_pk_v123.py` and `extract_pk_v123b.py` are only rerun when labels are re-downloaded; `review_pk_v123b.py` holds the reviewer-accepted second-pass PK values):

    python3 build_data.py
    python3 release_v06.py
    python3 release_v07.py
    python3 release_v08.py
    python3 release_v09.py
    python3 release_v10.py
    python3 release_v11.py
    python3 release_v111.py
    python3 release_v112.py
    python3 release_v113.py
    python3 release_v120.py
    python3 release_v121.py
    python3 release_v122.py
    python3 release_v123.py
    python3 apply_reviews.py
    python3 build_standalone.py
    node checks.mjs
    node checks_v123.mjs
    node checks_interface.mjs
    node checks_calculator.mjs
    python3 package_github.py /absolute/path/RenalRounds_GitHub_v0.12.3_cumulative.zip

Earlier version checks (checks_v05 … checks_v122) are historical. SHA256SUMS.txt covers public root files.

Software, arithmetic and layout checks do not establish clinical validity. Independent nephrology and renal-pharmacy review remains pending.
