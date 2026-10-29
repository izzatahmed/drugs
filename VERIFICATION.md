# v0.5.0 software verification — 29 October 2026

Clinical coverage is unchanged from v0.4.0: 668 records, 101 renal profiles, 28 shared safety-note records, 539 renal-dose-pending catalog records; 27 PK profiles, 15 with four core PK items. All await independent clinical approval.

## Passed

- Original checks.mjs: record/source integrity, review state, modality status, original clinical regressions, explicit PK gaps, embedded database/documents.
- checks_v05.mjs: SHA-256 fingerprint of every drug field, source and shared safety note matches v0.4.0; all 668 queue records match source statuses.
- Actual search functions: generic/brand/case matches, deliberate spelling suggestions, setting/PK/latest-clinical filters. 1,000 queries completed in about 158–300 ms across observed runs on the development container; this is not a phone benchmark.
- Actual service-worker code under deterministic network/cache tests: install, offline navigation to root/index, explicit update activation, wrong-version, incomplete-bundle checksum and 404 rejection, isolation from other path caches and external sites.
- Browser: app startup, spelling suggestion without automatic substitution, hidden exact-match recovery, dashboard totals, setting navigation, mobile open-reference shortcut, captopril/amlodipine and modality selection.
- 320/390/430 px phone frames: document widths 305/375/415 px (scrollbar excluded); no horizontal overflow, bounded results and correctly positioned open reference.

## Limits

The HTTP-only preview cannot activate a service worker. HTTPS installation/update and airplane-mode reopen on the actual GitHub Pages site require testing after this package is uploaded. Physical-device installation, operating-system cache eviction, clinical validity, licensed-reference reconciliation and independent clinical sign-off have not been established by software checks. Source links require internet. No clinical content was expanded or rechecked in this software release.
