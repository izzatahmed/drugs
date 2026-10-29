# RenalRounds v0.9.0 — cumulative GitHub Pages package

Mobile adult renal drug reference for CKD, IHD, PD, CRRT and PIRRT/SLED. Clinical content remains draft. 668 indexed entries: 218 partial renal profiles, 28 shared safety notes and 422 renal-dose-pending catalog records. There are 66 source-based PK profiles, including 39 clearly labelled historical handbook profiles; 52 contain all four core PK items. No entry has independent clinical approval.

## Update the active site

The existing site is https://izzatahmed.github.io/drugs/ .

1. Extract this cumulative ZIP. Upload the **contents** to the existing repository; do not upload the ZIP or a new containing folder.
2. Replace the root files together, including **index.html**, **sw.js**, manifest, icons, database and documents. Upload **source/** with its nested **dist/** too, preserving that structure, to keep editable source consistent. There is no separate top-level dist folder in this package. A GitHub Pages workflow that publishes a different folder must use that configured output; for root publishing, root index.html is the live entry point.
3. Commit to the currently configured Pages branch/folder. Wait for its deployment to finish.
4. Open the site and verify **v0.9** or **Release 0.9.0** in About. If an older offline worker controls it, choose **Check for update → Load available update**.
5. Wait for **Offline ready · cached v0.9.0**. On a physical phone, open a drug, enable airplane mode and reopen the exact site URL. External source links need internet.

No previous ZIP or patch is needed. GitHub account writes have not been performed. Updating database.json alone does not update the embedded data inside index.html.

## eGFR calculator

Click **eGFR calculator** beside quick search or in the sidebar. CKD-EPI 2021 creatinine is the race-free default. MDRD (IDMS 175) is a legacy alternative without its historical race multiplier, as clearly labelled. Both support mg/dL and µmol/L; changing units converts the entered value. Optional height/weight shows non-indexed eGFR in mL/min using Mosteller BSA. Values clear on close and are not stored or transmitted.

No result is shown for AKI/changing creatinine, dialysis, pregnancy or children. eGFR is distinct from Cockcroft–Gault CrCl; the tool selects no drug dose. See CALCULATOR.md for formulas, sources, limits and verification. Clinical data and software are version 0.9.0.

## Clinical content and remaining work

- 85 new selected adult renal profiles, using current labels where selected and Nebraska institutional rows with route/indication limits.
- 39 historical PK/removal profiles from the supplied Renal Drug Handbook fifth edition, published 2018 (copyright 2019). Each has source/page provenance; “checked today” does not make an old PK study current.
- 16 prescription-specific PIRRT summaries and four CVVHD profiles. Session length, flow, timing, loading and extended infusion instructions remain attached.
- Retained source disagreements/ambiguities; numeric prescriptions are withheld where a clear source-supported schedule cannot be selected.
- Existing CKD/IHD/PD/CRRT tables for previously curated renal drugs and all 53 prior PK profiles are unchanged.

See **SOURCE_AUDIT.md/JSON**, **COMPLETION_PLAN.md**, **CURATION_QUEUE.json**, **REFERENCE_DIRECTORY.json** and **EDITORIAL_GUIDE.md**. The original supplied PDFs are research inputs and are excluded from the public ZIP. Only selected sections were reviewed. This is not a fully curated formulary. BNF (British National Formulary) monograph comparison and independent nephrology/renal-pharmacy approval remain pending.

## Offline and privacy

index.html embeds search code, styling and data, and can run by itself in a browser that executes local HTML/JavaScript. Some phone file previews do not execute JavaScript; GitHub Pages provides normal browser access. Optional PWA/offline installation needs the companion files and HTTPS. The worker scopes its cache to the app path and checks the release/checksum before accepting an update. A saved release stays active until the user loads the available update. Browser storage may be cleared or evicted.

No patient data, analytics or background clinical-update feed is collected. Favourites and text-size preferences stay in the browser. Source dates are separate from software release dates.

## Rebuilding

Python 3 and Node.js are sufficient. No package install or network is required. Run from source/:

    python3 build_data.py
    python3 release_v06.py
    python3 release_v07.py
    python3 release_v08.py
    python3 release_v09.py
    python3 build_standalone.py
    node checks.mjs
    node checks_v09.mjs
    node checks_calculator.mjs

Copy the generated runtime files from source/dist/ to the publishing root together. App source assets remain in source/dist/; the build embeds them into index.html. The versioned expansion scripts must run in the order above. Older checks_v06.mjs is retained as a historical check for v0.6; use checks_v09.mjs plus checks_calculator.mjs for this release.

To rebuild the cumulative ZIP:

    python3 package_github.py /absolute/path/RenalRounds_GitHub_v0.9.zip

SHA256SUMS.txt covers public root files. Checks prove software/data integrity, not clinical validity. See VERIFICATION.md for tested scope and remaining physical-phone/HTTPS checks.

## Readability fix and new profiles

Clinical reading text starts at 16 px. Use A+ for 115%, 130% or 150%, A− to decrease, and the percentage button to reset to 100%. Dose tables and PK values scale too; the setting persists when browser storage is available. Enlarged dose tables stack on narrow phones. Old enlarged-text preferences migrate to 115%.

This release adds 85 selected renal profiles and 13 historical PK profiles. All 24 indexed psychiatry medicines now have selected formulation-specific renal statements; this does not establish complete psychiatric prescribing or dialysis coverage. Other additions include selected anti-infectives and common cardiovascular, diabetes, bone and gastrointestinal medicines. Some profiles provide monitoring, caution or insufficient-data statements rather than numeric doses.

The formulary remains incomplete. REMAINING_MEDICATIONS.json lists 450 entries without drug-specific renal profiles (422 catalog entries and 28 shared safety notes). CURATION_QUEUE.json tracks all fields and modalities. Full formulation/indication/RRT evidence, BNF reconciliation and independent clinical approval remain pending. No missing regimen is extrapolated. Uploaded source PDFs are not redistributed.

Upload all extracted contents to the publishing root, preserving source/ and nested source/dist/. No separate top-level dist/ is required for root-based Pages. Downloading this package does not update the deployed site.
