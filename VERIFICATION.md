# v0.10 verification

Run checks.mjs, checks_v10.mjs, checks_interface.mjs and checks_calculator.mjs after the full ordered build. They verify schema/source provenance, unchanged v0.9 records and prior PK/regimens, selected high-consequence thresholds/formulations/units, remaining-work exports, actual search functions, in-app navigation history, manual theme persistence/fallback, text control logic, calculator arithmetic and privacy, embedded documents/data, and actual service-worker offline/update/cache-isolation contracts.

Browser checks cover search-first order, collapsed filters, day/night toggling and reload persistence, back navigation through drugs/settings and dialog closure, enlarged clinical fonts, narrow phone overflow and the retained calculator. Fresh extraction/build and byte comparison verify package reproducibility; ZIP CRC and root SHA256 sums are checked.

Software and arithmetic checks do not establish clinical validity. BNF reconciliation, complete clinical coverage and independent approval remain pending. A physical phone and hosted HTTPS offline installation/update require verification after GitHub upload.
