# RenalRounds v0.6.0 — cumulative GitHub Pages package

Adult renal drug reference for CKD, IHD, PD, CRRT and SLED. Clinical content remains draft. This release expands 12 cardiovascular entries using individual UK product labels, corrects BNF terminology and adds a directory of renal reference resources. It does not confer independent clinical approval.

## Update the active site

The active site is https://izzatahmed.github.io/drugs/ .

1. Extract this ZIP. In the existing drugs repository, choose **Add file → Upload files**. Upload the extracted root files; do not upload the ZIP itself or a containing folder.
2. Replace **index.html** at the publishing root. Upload **sw.js**, **manifest.webmanifest**, all icon files and **.nojekyll** alongside it. The documents, database and completion queue are included for maintenance. Upload source/ too if you want the editable source in the repository.
3. Commit to the branch/folder already configured for GitHub Pages. No Pages-setting change is needed for the existing site.
4. Open the site and refresh. Verify **ADULTS · v0.6** at the top or release **0.5.0** in About. If a previous RenalRounds service worker controls the site, use **Check for update → Load available update**.
5. Wait for **Offline ready · cached v0.6.0**. Open captopril or amlodipine. On a real phone, switch to airplane mode and reopen the exact site URL to verify the saved copy. External source links still need internet.

GitHub deployment can take several minutes. Check your repository's Pages deployment status if v0.6 does not appear. Editing database.json alone does not update index.html: data are embedded when built.

The ZIP is cumulative. No older ZIP or patches are needed. GitHub account writes have not been performed for you.

## Changes

- Twelve new renal-guidance profiles, with HD guidance only where explicitly supported. Some labels give nonnumeric adjustment/monitoring advice, which is retained without a fabricated renal dose.
- References directory separates product labels, professional guidance, institutional protocols, patient education and portal discovery.

- Bounded phone result list, Open reference shortcut, return-to-search button and keyboard dismissal.
- Cached search keys and direct drug lookup; explicit spelling suggestions require a selection.
- Setting filter for existing sourced summaries; original route, content, OTC, category and favourites filters remain.
- Completion dashboard with modality/PK counts, downloadable 668-drug queue and completion plan.
- Scoped offline cache, cached-release status and deliberate update activation.
- Add-to-home-screen manifest/icons, copy selected-drug link and selected-setting print layout.

## Clinical completion

668 indexed entries: 113 renal profiles, 28 shared safety notes and 527 renal-dose-pending catalog records. 27 have source-based PK profiles; 15 have all four core PK items. The 12 expanded profiles are bisoprolol, candesartan, clonidine, enalapril, hydralazine, indapamide, irbesartan, losartan, methyldopa, ramipril, telmisartan and valsartan. The remaining 656 records and all existing PK profiles are unchanged from v0.5. Every entry awaits independent nephrology and renal-pharmacy approval. A searchable record is not a completed prescribing monograph.

See **COMPLETION_PLAN.md**, **CURATION_QUEUE.json** **EDITORIAL_GUIDE.md** and **REFERENCE_DIRECTORY.json**. The completion queue distinguishes uncurated, unknown, not reported, specialist and summarized fields. No dose is inferred across modalities or from PK parameters. BNF is the British National Formulary, as clarified by the user; BNF monograph comparison remains pending access; only individually linked PDR material has been consulted.

## Offline behavior

index.html still embeds all search code, styling and clinical data. It can run by itself in a browser that opens local HTML/JavaScript; phone file previews may not run JavaScript. Optional manifest/icons need their companion files. On HTTPS, sw.js saves a versioned copy of index.html scoped to the app directory (for this site, /drugs/). It does not control other GitHub Pages repositories or cache external clinical sources.

Once controlled, page reopens use the saved release until a new worker is installed and **Load available update** is selected. Source-check dates stay visible and are never advanced by a software update. Browser storage can be cleared/evicted; the status bar confirms current readiness. No patient data, analytics or background clinical-update feed is collected.

## Source and rebuilding

Python 3 and Node.js are sufficient; no package install or network is required. From source/:

    python3 build_data.py
    python3 release_v06.py
    python3 build_standalone.py
    node checks.mjs
    node checks_v06.mjs

Run release_v06.py after build_data.py for this software release. Copy the generated runtime files from source/dist/ to the repository root together. Source/dist/ also contains the editable app.js, pk.js, workflow.js, offline.js, styles.css and icons. Standalone HTML builds them into one entry point.

To rebuild the cumulative ZIP:

    python3 package_github.py /absolute/path/RenalRounds_GitHub_v0.6.zip

Checks prove software/data integrity, not clinical validity. See VERIFICATION.md for test coverage and remaining HTTPS/physical-phone checks.

Official references for hosting/offline implementation:

- https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
- https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers
