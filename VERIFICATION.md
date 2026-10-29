# RenalRounds 0.4 software verification

29 October 2026

Automated checks cover 668 unique IDs; 101 renal profiles, 28 safety notes and 539 renal-dose-pending catalog entries; all source references; explicit draft status; unchanged original 70 profiles; unchanged v0.3 modality content except the requested captopril/amlodipine expansions; PK schema/provenance and null-state integrity for all entries; 27 sourced PK profiles, 15 with all four core reference items; total-daily captopril amounts and indexed units; modality-specific unknowns; beta-blocker high-flux classifications; ramipril source differences; embedded JSON/document equality and no external runtime assets.

Browser checks passed: captopril/Capoten and amlodipine searching; visible half-life/Vd/binding/IHD fields; captopril total daily renal table; PD versus CRRT removal states with no invented dose; exact-name recovery from route filters; 27-record PK filter; PK-only losartan with no dose table; absent PK for warfarin; no-match removal of stale PK/dosing content. Phone frames at 320, 390 and 430 CSS pixels had no document horizontal overflow, including expanded captopril evidence at 320 pixels.

These are software checks, not independent clinical validation. Physical iOS/Android use and local-file launching were not exercised; the cloud browser permits HTTP(S) but blocks file:// navigation. Single-file completeness is checked statically. Editorial-document downloads were not confirmed in the prior browser environment; the actual Markdown files remain in the ZIP. No complete formulary, all-drug PK curation, exhaustive licensed-reference reconciliation or patient-specific dose engine is claimed. GitHub upload remains unavailable because the connection was declined.
