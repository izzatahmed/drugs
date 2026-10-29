# RenalRounds

An adult renal-drug reference prototype with instant search, mobile layout, generic/brand aliases, route/content/OTC filters, selected CKD/IHD/CRRT/PD/SLED summaries, linked references, favourites and text-size control.

Version 0.4 contains 668 drug/formulation entries: 101 sourced renal profiles, 28 shared safety-note records and 539 renal-dose-pending catalog records awaiting renal guidance. Renal profiles cover selected indications, sometimes adjustment/monitoring advice without numeric doses. No entry has independent clinical approval. This is not a comprehensive or approved prescribing formulary.

The generated `dist/index.html` embeds all data, CSS, JavaScript, icon and editorial documents. It runs without a server or runtime internet request. Source links require internet. Some phone file managers only preview HTML; GitHub Pages provides the most consistent phone access. No patient data, analytics or external code libraries are used. No service-worker installation is included.

Rebuild: `python3 build_data.py` then `python3 build_standalone.py`

Check: `node checks.mjs`

Serve through the Sites preview workflow with `.openai/hosting.json` declaring `dist` as the static directory. For ordinary local development, any static server can serve `dist`. Opening `dist/index.html` directly is supported by browsers that run local JavaScript. Local storage availability varies by browser/file origin; preferences fall back to the current session.

## GitHub Pages

1. Create or open your GitHub repository and upload the **contents** of the supplied `RenalRounds_GitHub_v0.4.zip`. `index.html` must be at the repository root, not inside a nested ZIP folder. Upload the extracted files, not the ZIP itself.
2. Commit the files to `main` (or your chosen branch).
3. Go to **Settings → Pages → Build and deployment → Deploy from a branch**. Choose the branch and **/(root)**, then Save. Repository visibility/Pages availability depends on your GitHub plan; never upload patient information.
4. Open the Pages URL displayed by GitHub, usually `https://YOUR-USERNAME.github.io/YOUR-REPOSITORY/`, on the phone. Use the browser's Add to Home Screen shortcut if desired; it does not create an auto-updating offline installation.

Only `index.html` is needed to run the app. `.nojekyll` disables Jekyll processing. The JSON database and editorial notes are included for maintenance. The `source/` folder contains rebuild/check scripts; rebuild from within `source/`, then copy the newly generated `source/dist/index.html` to the repository root when releasing an update.

GitHub documentation: [Creating a Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site) and [entry-file troubleshooting](https://docs.github.com/en/pages/getting-started-with-github-pages/troubleshooting-404-errors-for-github-pages-sites).

## Clinical and reference scope

See `dist/EDITORIAL_GUIDE.md` and `dist/CHANGELOG.md`. The requested PNF title/edition is not identified; no PNF comparison is claimed. BNF 92 monographs were inaccessible and reconciliation remains pending. Only explicitly linked PDR monographs are represented as consulted. Catalog inclusion does not establish current approval, local availability, renal safety or a dose. Some products are historical or formulation-specific.

## Maintenance files

`build_data.py`, `expansion_v02.py`, `expansion_v03.py`, `catalog_v03.py` and `expansion_v04.py` produce `dist/database.json`. `app-shell.html`, `dist/app.js`, `dist/pk.js` and `dist/styles.css` are the interface sources; `build_standalone.py` embeds them into `dist/index.html`. Edit these source files and rebuild rather than patching the generated HTML. No commercial formulary text is bulk reproduced.

## Version 0.4: BP medicines and pharmacokinetics

Captopril now has a sourced UK renal starting/maximum **total daily dose** table; it is not an HD prescription. Amlodipine has an explicit adult hypertension starting dose and maximum. Both have complete reference half-life, Vd, binding and IHD removal fields.

27 BP/cardiovascular medicines have source-based PK profiles; 15 have values for all four core fields. The other fields distinguish not reported in the checked source, unknown, and not yet curated. Existing renal-dose and PK source checks are separate. PK-only catalog entries still have no curated renal dose. The requested fields exist in the schema for every drug, but PK curation is not complete across all 668 records.

Each PK field retains its units, context and sources. Reference and renal/ESRF half-lives are separate; parent drugs, active metabolites, apparent volumes, Vss and release formulations are identified. UKKA January 2025 Appendix D provides selected ESRF/PD facts; source differences and uncertain analytes are explicit. No clearance, dosing interval or dialysis supplement is computed from binding or Vd.

Use Content → PK available to filter the 27 records. Updated in v0.4 shows expanded records; it does not mean new drug approvals. Captopril and Amlodipine have quick-search buttons. Exact names hidden by filters get a recovery button, which clears filters while keeping the search term.
