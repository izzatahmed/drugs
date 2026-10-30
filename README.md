# RenalRounds v0.10.0 — cumulative GitHub Pages package

Search-first adult CKD and kidney-replacement drug reference. This release simplifies the interface, adds a manually controlled night theme and in-app back arrows, and adds 40 selected renal profiles plus 3 PK panels. The 668-entry inventory contains 258 partial renal profiles, 28 shared safety notes and 382 catalog entries without renal guidance. There are 69 PK profiles, including 39 historical handbook profiles; 55 contain all four core items, including qualified qualitative IHD statements. This is an incomplete draft without independent clinical approval.

## Update the existing site

1. Extract this cumulative ZIP. Upload all its contents to the existing repository publishing root, preserving folders and replacing matching files. Do not upload the ZIP itself or create another enclosing folder.
2. Replace root index.html, sw.js, icons, manifest, database and documents together. Preserve source/ and its nested source/dist/ for maintenance. There is no separate top-level dist/ in this package. A workflow publishing another directory must use that configured output.
3. Commit to the branch/folder configured for GitHub Pages and wait for deployment. Confirm v0.10 in the footer or Release 0.10.0 in Sources & scope.
4. If an older offline copy remains active, open Database & offline status at the bottom, then Check for update → Load available update. Confirm cached v0.10.0 on HTTPS. Test reopening the exact URL on a physical phone in airplane mode; source links need internet.

Downloading this file does not update the live site. No GitHub writes have been performed. The root index embeds the full database and code: replacing JSON alone does not change the running app. No earlier ZIP or patch is required.

## Interface

Search is the first visible control. The toolbar below it has A−, percentage reset, A+, day/night, eGFR and source information. Filters start collapsed on every screen; category, favourites and latest additions are available inside Filters. Renal dosing leads each drug entry; PK and secondary copy/print/coverage tools follow it. Database information and offline controls are below the findings.

Text sizes are 100%, 115%, 130% and 150%; clinical text starts at 16 px. Enlarged dose rows stack on narrow phones. Day/night is an explicit saved choice, independent of operating-system preferences; first use defaults to day mode. These settings work for the session if storage is unavailable.

The small ↶ button stays near the bottom of the screen. It returns through in-app medicine, setting, search/filter and phone scroll positions; if no earlier state exists, it returns to search. It never leaves the app. Each dialog has a matching arrow to close the panel. Navigation history is session-only and excludes calculator inputs.

## Clinical scope

The new selected product summaries cover 15 cardiovascular/diuretic/lipid drugs, 11 BPH/bladder drugs, 6 allergy/respiratory medicines and 8 GI/constipation treatments. Some contain cautions or insufficient-data statements without numeric dosing. Exact formulation, indication, source kidney-function metric and limits remain visible. Three selected-product PK panels cover doxazosin XL, torsemide and tamsulosin capsules; qualitative overdose statements are not measured modern circuit-clearance estimates.

Sources for new entries were checked on 30 October 2026. Existing drug regimens, PK and source dates are unchanged. The supplied fifth-edition Renal Drug Handbook is historical (2018, copyright 2019); original uploaded PDFs are not redistributed. Inaccessible BNF monographs have not been verified. Source differences and local product authorisation need reconciliation.

REMAINING_MEDICATIONS.json lists 410 entries without drug-specific renal profiles: 382 catalog records plus 28 shared safety notes. CURATION_QUEUE.json tracks each field/modality. Every existing renal profile also requires completion of indication/formulation/RRT evidence and independent nephrology plus renal-pharmacy approval. Missing dialysis regimens are never copied from CKD, another modality or PK.

## Calculator and privacy

CKD-EPI 2021 creatinine is the race-free default; IDMS MDRD without its historical race multiplier remains clearly labelled as a legacy alternative. Both support mg/dL and µmol/L conversion. Optional Mosteller BSA shows non-indexed eGFR. The tool withholds estimates for AKI, dialysis, pregnancy and children, and selects no drug dose. eGFR and Cockcroft–Gault CrCl are different measures. See CALCULATOR.md.

Calculator inputs clear when the panel closes and are not stored, exported or sent. Favourites, text size and theme use browser-local storage when available. No patient identifiers, analytics or automatic clinical-update feed are collected.

## Rebuild and verify

Run from the extracted source/ folder with Python 3 and Node.js; no package installation or network is required:

    python3 build_data.py
    python3 release_v06.py
    python3 release_v07.py
    python3 release_v08.py
    python3 release_v09.py
    python3 release_v10.py
    python3 build_standalone.py
    node checks.mjs
    node checks_v10.mjs
    node checks_interface.mjs
    node checks_calculator.mjs
    python3 package_github.py /absolute/path/RenalRounds_GitHub_v0.10.zip

Copy generated runtime/documents from source/dist/ to the publishing root together, or extract the new cumulative ZIP there. CSS/JS source assets remain in source/dist/ and are embedded by the builder into index.html. Earlier version checks are historical; use the four current checks above. SHA256SUMS.txt covers public root files.

Software, arithmetic, provenance and browser layout checks do not establish clinical validity. Physical-phone installation and hosted HTTPS update/offline verification remain pending after upload.
