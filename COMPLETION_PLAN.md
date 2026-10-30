# RenalRounds v0.11.1 · 30 October 2026

This update prioritises renal instructions rather than search names or PK alone. It adds 35 selected product-specific renal profiles from official DailyMed SPLs, fills 17 previously empty systemic PD schedules from the supplied Nebraska protocol approved April 2026, and reconciles eight IHD-removal fields to the selected labels. It retains all previously populated dosing tables and all PK half-life/Vd/binding fields. There are 295 partial renal profiles, 28 shared safety entries and 345 catalog entries in the 668-medicine index. PK remains 99 profiles; 63 have all four core items, including qualified label statements and historical values.

Numeric additions include entecavir by indication/renal function/HD/CAPD, IR amantadine weekly HD, ropinirole HD by indication, adult lacosamide renal maximum and a qualified HD supplement, oxcarbazepine initial TOTAL daily dose, topiramate indexed-CrCl reduction, memantine IR target, sulbactam/durlobactam and imipenem/cilastatin/relebactam combination regimens, delafloxacin route-specific adjustment, ofloxacin and trimethoprim. Other labels specify titration or insufficient evidence rather than a safe universal numeric dose. Three new profiles withhold numeric selection because of study gaps or conflicting warnings (buprenorphine patch, lorazepam injection, cefixime product table).

Sources: search retrieval failed, but 35 selected SPLs were retrieved directly through the official DailyMed API. Source metadata records exact set ID, publication date, SPL version, retrieval endpoint and XML SHA-256. DailyMed presence is not FDA approval: phenobarbital's selected label is a marketed unapproved drug; molnupiravir is an EUA fact sheet, not full approval. BNF comparison and independent clinical approval remain pending. The supplied handbook's 2018 PK values retain their historical status. No old handbook renal-dose table is promoted into current prescribing.

PD tables describe systemic treatment, not intraperitoneal peritonitis prescriptions. CAPD does not establish APD dosing. Indications, formulation, residual function, susceptibility and institutional protocol differences remain material. Current removal evidence does not automatically establish a maintenance or replacement dose. No unlisted CRRT or SLED regimen is inferred.

The top centre now displays RenalRounds v0.11.1, with the existing compact font/theme controls retained. The cumulative package contains everything needed after v0.10. The smaller package contains only files changed or added since the exact v0.10 archive; apply it preserving paths. Both lead to the same release. No deployment or GitHub write is performed by downloading.

373 entries still lack drug-specific renal profiles; existing profiles also retain substantial gaps. This remains a draft, not a completed formulary or approved clinical decision system.

## Remaining work

Complete local-formulary indication/formulation and prescription-specific RRT coverage. Reconcile every conflict and obtain independent nephrology plus renal-pharmacy review before clinical release.
