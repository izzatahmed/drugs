# RenalRounds v0.11.2 — cumulative GitHub Pages package

Compact adult CKD and kidney-replacement drug reference. This release makes the top title a Home link and adds 60 selected renal profiles from the supplied Renal Drug Handbook, fifth edition (published 2018, copyright 2019). The 668-entry inventory now contains 355 partial renal profiles, 28 shared safety notes and 285 catalog entries. There are 157 source-based PK profiles, 99 with all four core items, including qualified historical removal statements. This remains an incomplete draft without independent clinical approval.

## Update the existing site

1. Extract this cumulative ZIP. Upload all its contents to the existing repository publishing root, preserving folders and replacing matching files. Do not upload the ZIP itself or create another enclosing folder.
2. Replace root index.html, sw.js, icons, manifest, database and documents together. Preserve source/ and its nested source/dist/ for maintenance. There is no separate top-level dist/ in this package. A workflow publishing another directory must use that configured output.
3. Commit to the branch/folder configured for GitHub Pages and wait for deployment. Confirm v0.11.2 in the footer or Release 0.11.2 in Sources & scope.
4. If an older offline copy remains active, open Database & offline status at the bottom, then Check for update → Load available update. Confirm cached v0.11.2 on HTTPS. Test reopening the exact URL on a physical phone in airplane mode; source links need internet.

Downloading this file does not update the live site. No GitHub writes have been performed. The root index embeds the full database and code: replacing JSON alone does not change the running app. No earlier ZIP or patch is required.

## Compact interface

Smaller font/theme controls are uppermost, RenalRounds v0.11.2 occupies the free centre, and the eGFR shortcut stays at the right. A shorter search box shares the next line with Filters and Clear filters. Phone filter controls use funnel and crossed-funnel icons; accessible labels and desktop text remain available. Filters start collapsed. Clear filters is disabled when inactive and resets route/content/setting/category/OTC choices while preserving the search query.

Clinical text starts at 16 px, with 100%, 115%, 130% and 150% settings. These reading sizes are independent of the smaller controls. Day/night remains an explicit saved choice, independent of the system theme. Renal dosing leads each drug entry. Approval badges, informational missing-data notices, PK and secondary tools follow the findings; do-not-use warnings remain with the relevant setting.

Clicking the centred title returns Home: it clears search, the selected medicine and all filters, selects CKD, closes panels and returns to the top. Theme, text size and favourites persist; Back can restore the prior browsing context.

The small fixed ↶ arrow returns through in-app medicine, setting, query/filter and phone-scroll history. Dialog arrows close their panels. It never leaves the app and captures no calculator inputs. If there is no earlier in-app state, it returns to search.

## Medication expansion and limits

This update adds 60 selected cardiovascular, steroid/endocrine, phosphate/vitamin, respiratory, GI and common-medicine renal profiles. It retains all existing clinical records, including the preceding 35 product-label profiles and 17 systemic PD additions. Selected numeric references include flecainide initial TOTAL oral dose versus IV reduction, nicardipine infusion titration, vildagliptin 50 mg/day and midodrine initiation with its unresolved exact-70-kg boundary. Many entries require no fixed renal reduction or individual titration rather than a reduced numeric schedule.

The fifth-edition year is visible beside each new dose table. Source GFR bands are not relabelled CrCl or indexed eGFR. Historical HD and HDF/high-flux categories remain distinct; the source's APD/CAPD category is combined and supplies systemic guidance, not intraperitoneal peritonitis dosing. No universal modern CRRT or SLED regimen is inferred from unspecified historical CAV/VVHD settings. No post-dialysis supplement is inferred from PK.

Three new profiles withhold numeric renal selection: hydroxychloroquine, mesalazine and cholecalciferol. Domperidone excludes the older high-dose/prolonged schedules in favour of the directly retrieved MHRA adult restrictions plus the handbook renal-frequency caution. Aminophylline distinguishes dialysable theophylline from the parent's table category. Other analyte/unit disagreements remain explicit. Calcium acetate has no source-reported PK parameters and is not counted among the 157 PK profiles; partial PK panels retain missing and withheld fields.

Exact PDF page/continuation locators and the original document checksum accompany source records. The PDF is not redistributed. These are edition-based factual summaries, not newly verified current labels, a completed BNF comparison or independent clinical approval. Current local product and indication reconciliation remains necessary. Earlier current-label sources retain their original provenance.

REMAINING_MEDICATIONS.json lists 313 entries without drug-specific renal profiles (285 catalog plus 28 shared safety). Existing profiles also retain formulation, indication and RRT gaps. Independent nephrology and renal-pharmacy review remains pending.

## Choose the download

The cumulative ZIP contains the full current release, including all updates after v0.10 and the maintenance source tree. For an existing v0.10, v0.11 or v0.11.1 installation, the smaller modified-files ZIP contains only files added or changed relative to the exact v0.10 cumulative ZIP, including updated source paths. Extract its contents directly into the existing publishing root, preserving paths and replacing matching files. No deletion is needed. It is not a complete standalone project. Both methods produce the same current files; do not apply both.

After upload, check the top title/footer for v0.11.2. An older cached app needs Database & offline status → Check for update → Load available update.

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
    python3 release_v111.py
    python3 release_v112.py
    python3 build_standalone.py
    node checks.mjs
    node checks_v112.mjs
    node checks_interface.mjs
    node checks_calculator.mjs
    python3 package_github.py /absolute/path/RenalRounds_GitHub_v0.11.2_cumulative.zip

Copy generated runtime/documents from source/dist/ to the publishing root together, or extract the new cumulative ZIP there. CSS/JS source assets remain in source/dist/ and are embedded by the builder into index.html. Earlier version checks are historical; use the four current checks above. SHA256SUMS.txt covers public root files.

Software, arithmetic, provenance and browser layout checks do not establish clinical validity. Physical-phone installation and hosted HTTPS update/offline verification remain pending after upload.
