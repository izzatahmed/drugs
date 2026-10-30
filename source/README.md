# RenalRounds v0.11.0 — cumulative GitHub Pages package

Compact adult CKD and kidney-replacement drug reference. This release reduces the upper controls and search area, moves review notices below the findings, and adds two partial institutional renal profiles plus 30 historical PK-only panels. The 668-entry inventory contains 260 partial renal profiles, 28 shared safety notes and 380 catalog entries without renal guidance. There are 99 PK profiles, including 69 historical handbook profiles; 55 contain all four core items, including qualified qualitative IHD statements from prior releases. This is an incomplete draft without independent clinical approval.

## Update the existing site

1. Extract this cumulative ZIP. Upload all its contents to the existing repository publishing root, preserving folders and replacing matching files. Do not upload the ZIP itself or create another enclosing folder.
2. Replace root index.html, sw.js, icons, manifest, database and documents together. Preserve source/ and its nested source/dist/ for maintenance. There is no separate top-level dist/ in this package. A workflow publishing another directory must use that configured output.
3. Commit to the branch/folder configured for GitHub Pages and wait for deployment. Confirm v0.11 in the footer or Release 0.11.0 in Sources & scope.
4. If an older offline copy remains active, open Database & offline status at the bottom, then Check for update → Load available update. Confirm cached v0.11.0 on HTTPS. Test reopening the exact URL on a physical phone in airplane mode; source links need internet.

Downloading this file does not update the live site. No GitHub writes have been performed. The root index embeds the full database and code: replacing JSON alone does not change the running app. No earlier ZIP or patch is required.

## Compact interface

Smaller font/theme controls are uppermost, with the eGFR shortcut at the right. A shorter search box shares the next line with Filters and Clear filters. Phone filter controls use funnel and crossed-funnel icons; accessible labels and desktop text remain available. Filters start collapsed. Clear filters is disabled when inactive and resets route/content/setting/category/OTC choices while preserving the search query.

Clinical text starts at 16 px, with 100%, 115%, 130% and 150% settings. These reading sizes are independent of the smaller controls. Day/night remains an explicit saved choice, independent of the system theme. Renal dosing leads each drug entry. Approval badges, informational missing-data notices, PK and secondary tools follow the findings; do-not-use warnings remain with the relevant setting.

The small fixed ↶ arrow returns through in-app medicine, setting, query/filter and phone-scroll history. Dialog arrows close their panels. It never leaves the app and captures no calculator inputs. If there is no earlier in-app state, it returns to search.

## Medication expansion and limits

This release enriches 32 existing indexed medicines: two partial renal profiles for omadacycline and telavancin from the supplied adult institutional protocol, plus 30 historical PK panels in pain/neurology. The new panels contain selected reference/renal half-life, Vd and protein binding. No new historical renal-dose table or dialysis-removal category is imported; those fields require current-source reconciliation. A PK panel does not constitute a renal prescribing monograph.

Online primary-source search and retrieval were unavailable for this batch. No new current-label verification is claimed. The antimicrobial protocol was approved April 2026; the supplied handbook is fifth edition, published 2018 (copyright 2019). Each selected PDF page and file checksum is recorded. Superscript references are separated from numeric values, and total Litres from L/kg. Source-check date does not change publication date.

Telavancin has differing institutional/older UK restrictions; its numeric regimen is withheld pending current product, indication and jurisdiction review. Omadacycline has a selected no-renal-reduction statement; no complete route/loading/RRT regimen is selected. Original uploaded PDFs are not redistributed.

REMAINING_MEDICATIONS.json lists 408 entries without drug-specific renal profiles: 380 catalog records plus 28 shared safety notes. Some catalog records now have PK panels. CURATION_QUEUE.json tracks every field and modality. Existing renal profiles also retain indication/formulation/RRT gaps; BNF comparison and independent nephrology plus renal-pharmacy approval remain pending.

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
    python3 release_v11.py
    python3 build_standalone.py
    node checks.mjs
    node checks_v11.mjs
    node checks_interface.mjs
    node checks_calculator.mjs
    python3 package_github.py /absolute/path/RenalRounds_GitHub_v0.11.zip

Copy generated runtime/documents from source/dist/ to the publishing root together, or extract the new cumulative ZIP there. CSS/JS source assets remain in source/dist/ and are embedded by the builder into index.html. Earlier version checks are historical; use the four current checks above. SHA256SUMS.txt covers public root files.

Software, arithmetic, provenance and browser layout checks do not establish clinical validity. Physical-phone installation and hosted HTTPS update/offline verification remain pending after upload.
