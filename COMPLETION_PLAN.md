# RenalRounds v0.11.3 · 30 October 2026

Software and wording release. No dose table, setting status or PK value changed; drug content remains 0.11.2.

- Kidney-function calculator now has two tabs: eGFR (CKD-EPI 2021 / legacy MDRD) and Cockcroft–Gault creatinine clearance with actual, ideal and adjusted body weight. Most drug tables in this reference are banded by CrCl.
- Phone layout: the floating back button no longer covers dose tables; on phones a "Back" button sits at the top of each drug. Pressing Enter in search opens the selected drug. The calculator scrolls to its result.
- Converted creatinine is shown to two decimals.
- 426 entries whose class only repeated the category now have a pharmacological class (e.g. flecainide: Class Ic antiarrhythmic). Search understands common abbreviations (PPI, NSAID, DOAC, LMWH, SGLT2i, ACEi, ARB, ESA and others).
- Internal working notes were rewritten as neutral statements (e.g. "BNF comparison not yet done").
- Each drug has a "Report an error" link that opens a pre-filled GitHub issue.
- Link previews (Open Graph) added.

## Remaining clinical work

Independent nephrologist and renal-pharmacist review of every entry; renal profiles for the 285 catalog-only entries, prioritised by risk; dialysis-setting coverage (CRRT, SLED, PD); a single primary jurisdiction with country labels on every table; and a decision on handbook-derived content.
