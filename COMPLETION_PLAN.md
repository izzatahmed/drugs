# RenalRounds v0.11.0 · 30 October 2026

The upper area is reduced to two compact rows: smaller text/theme/eGFR controls first, then a 40-px search field with Filters and Clear filters beside it. Filter actions use icons on narrow phones and visible labels on larger screens. Clear filters is disabled when no filter is active and does not erase the search query. Filter details remain collapsed until opened. Clinical-review badges and informational missing-data notices follow the clinical findings; explicit do-not-use warnings remain with their relevant setting.

The manual day/night choice, text-size preference, calculator and in-app semicircular back arrows are retained. Clinical text size remains readable and can increase independently of the compact controls.

Medication information is expanded for 32 records: two partial adult institutional renal profiles (omadacycline and telavancin), plus 30 historical PK-only panels in pain/neurology. The 668-entry inventory now has 260 partial renal profiles, 28 shared safety notes and 380 renal-dose-pending catalog entries. There are 99 PK panels; 55 have all four core items. Thirty new panels contain half-life, Vd and binding; their dialysis removal and dose schedules remain uncurated.

Online primary-source search and retrieval were unavailable during this batch. No new current product-label verification is claimed. The renal additions use the supplied institutional protocol approved April 2026; the PK additions use selected supplied fifth-edition handbook tables published in 2018 (copyright 2019). Historical reference numbers are distinguished from numeric values, and total Litres from L/kg. No historical renal-dose table or new dialysis-removal category is imported. Telavancin's current label, indication and jurisdiction need reconciliation; its numeric renal regimen is withheld.

Coverage remains incomplete. REMAINING_MEDICATIONS.json lists 408 records without a drug-specific renal profile (380 catalog entries plus 28 shared safety notes). PK availability does not establish a dose. Existing renal profiles also retain formulation/indication/RRT gaps. Independent clinical approval and BNF monograph reconciliation remain pending.

## Next clinical work

Resume current authorised product verification when online primary sources are available. Prioritise the newly described pain/neurology products for indication/formulation-specific renal dosing, free/metabolite kinetics and measured dialysis removal. Reconcile telavancin source/jurisdiction differences. Complete the remaining local adult formulary and missing prescription-specific IHD/PD/CRRT/PIRRT data; retain explicit gaps and obtain independent nephrology plus renal-pharmacy sign-off before clinical release.
