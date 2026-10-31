"""v0.12.2: pregnancy/lactation label excerpts for the rest of the database, reviewer reference
checks (BNF, Lexidrugs, UpToDate, MIMS, JFDA product check), TGA category field, review import.
No dose table changes.
"""
from pathlib import Path
import json, sys
sys.dont_write_bytecode = True
R = Path(__file__).parent; D = R/'dist'
DATE = '2026-10-31'; VERSION = '0.12.2'
data = json.loads((D/'database.json').read_text()); assert data['version'] == '0.12.1'
ext = json.loads((R/'label_extract_v122.json').read_text())
sources = {s['id']: s for s in data['sources']}
NOTE = 'Quoted from the cited label. The FDA retired the A/B/C/D/X letter categories; a letter is shown only where this label still prints one. Not yet reviewed; safer alternatives are not listed.'
added = []
for d in data['drugs']:
    for k in ['lexidrugs', 'uptodate', 'mims', 'jfda']:
        d['referenceChecks'].setdefault(k, dict(status='not_checked'))
    e = ext.get(d['id'])
    if not e or d.get('pregnancyLactation'): continue
    m = e['meta']; sid = e['sourceId']
    sources[sid] = dict(id=sid, title=f"DailyMed · {m['brand'] or d['name']} ({m['manufacturer']}) · pregnancy and lactation", url=m['url'],
        section=f"US FDA label sections on pregnancy and lactation (8.1/8.2, or Pregnancy/Nursing Mothers in older labels). SPL version {m['splVersion']}, effective {m['effective']}; application {m['application']}. Used for this section only.",
        type='US FDA label (DailyMed)', accessed=DATE, label=dict(setid=m['setid'], splVersion=m['splVersion'], effective=m['effective'], application=m['application']))
    d['pregnancyLactation'] = dict(status='label_excerpt', sourceIds=[sid], fdaLetterCategory=e.get('letter'), pregnancy=e.get('pregnancy'),
                                   lactation=e.get('lactation'), checkedAt=DATE, note=NOTE)
    added.append(d['id'])
data['sources'] = list(sources.values())
data.update(version=VERSION, softwareReleaseDate=DATE)   # clinicalDataVersion unchanged: no dosing change
data['releaseChanges'] = dict(version=VERSION, changedIds=added, newRenalIds=[], newPKIds=[], pirrtSummaryIds=[],
    note=f'Pregnancy/lactation label excerpts added for {len(added)} entries; reviewer reference-check fields added. Dose tables unchanged.')
data['referenceScope'].update(verificationReferences=['BNF', 'Lexidrugs', 'UpToDate', 'MIMS (Australia)'],
    verificationPolicy='Commercial references are used by named reviewers to verify entries; only the outcome (agrees / differs / not listed) is recorded. Their text is not reproduced.',
    publishedSources='US FDA labels (DailyMed); EMA product information where no US label exists; UK SmPCs for six medicines without a US or EMA product; international guidelines (KDIGO, ISPD) and named US hospital protocols.')
(D/'database.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))
total = sum(1 for d in data['drugs'] if d.get('pregnancyLactation'))
header = f'''# RenalRounds v{VERSION} · 31 October 2026

- **Pregnancy and lactation** now covers {total} of {len(data['drugs'])} entries, quoted from each medicine's current US FDA label (matched by active ingredient and route). Legacy FDA letters appear only where a label still prints one; the TGA (Australian) category appears once a reviewer enters it.
- **Reference checks:** every entry shows BNF, Lexidrugs, UpToDate, MIMS (Australia) and a JFDA product check, each "Not yet checked" until a named reviewer records Agrees / Differs / Not listed. These references are used for verification only; their text is not reproduced.
- **Review workflow:** completed review sheets are imported with `import_review.py`; approved entries then show "Reviewed by … on …".
- No dose table changed in this release.

'''
for target, base in [('CHANGELOG.md', 'changelog_v121.md'), ('EDITORIAL_GUIDE.md', 'editorial_guide_v121.md'), ('SOURCE_AUDIT.md', 'source_audit_v121.md')]:
    (D/target).write_text(header + '## Earlier release record\n\n' + (R/base).read_text())
(D/'VERIFICATION.md').write_text(f'''# v{VERSION} verification

Current suites: checks.mjs, checks_v122.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v122.py and apply_reviews.py. checks_v122.mjs proves dose tables are unchanged from v0.12.1, every pregnancy/lactation excerpt is verbatim text of its stored label, the label's active ingredient matches the entry, and reviewer fields hold only recorded statuses.

These are software/source-integrity checks, not clinical validation.
''')
print(json.dumps(dict(version=VERSION, pregnancyAdded=len(added), pregnancyTotal=total)))
