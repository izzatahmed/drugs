# Clinical completion plan · software v0.8.0 / drug data v0.7.0

668 indexed drug/formulation entries: 133 renal profiles, 28 shared safety notes and 507 renal-dose-pending catalog entries. 53 source-based PK profiles, including 26 historical handbook summaries. No entry has independent clinical approval.

## Next clinical work

1. Confirm the local adult formulary and prioritise common rounds drugs, oral/parenteral formulations and OTC products.
2. Complete each indication/route-specific kidney-function table using current product information and licensed references. CrCl, indexed eGFR and CKD stage are not substitutes for each other.
3. Reconcile the six issues in SOURCE_AUDIT.json with a renal pharmacist. Do not fill continuous-PD schedules from intermittent-HD wording or mix parent/prodrug analytes.
4. Replace or corroborate historical handbook PK with contemporary measured evidence. Preserve analyte, Vd units, conventional versus high-flux HD and within/between-session half-lives.
5. Complete IHD, systemic PD and CRRT/PIRRT evidence separately. Record delivered modality, session length, dialysate/effluent flows, residual function, loading, infusion duration, timing and TDM requirements. No intraperitoneal peritonitis regimen is implied.
6. Obtain authorised BNF (British National Formulary) and PDR monograph access for comparison. BNF verification is not claimed; the supplied handbook is a different reference.
7. Record independent nephrologist and renal-pharmacist review, names, dates and resolution of source conflicts before a clinical release.
8. After GitHub upload, verify HTTPS offline reopen and update activation on a physical phone.

CURATION_QUEUE.json records field/modality gaps for every entry. “Summarized” means a selected source summary, potentially nonnumeric; it does not mean a complete or approved prescribing monograph. Unknown, not reported and not curated remain separate.
