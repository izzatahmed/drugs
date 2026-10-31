"""Apply imported reviewer decisions (reviews/*.json) to dist/database.json.
Runs after the release scripts and before build_standalone.py. Safe to run with no review files.
An entry is shown as reviewed only when the decision is "approved"; "Approve after changes"
stays pending until a maintainer applies the corrections and re-imports an approval.
"""
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True
R = Path(__file__).parent; D = R/'dist'
data = json.loads((D/'database.json').read_text()); drugs = {d['id']: d for d in data['drugs']}
files = sorted((R/'reviews').glob('*.json')) if (R/'reviews').exists() else []
applied = 0
for f in files:
    rv = json.loads(f.read_text())
    for did, e in rv['drugs'].items():
        d = drugs.get(did)
        if not d: continue
        if 'review' in e:
            x = e['review']
            if x['decision'] == 'approved':
                d['review'].update(status='clinically_reviewed', clinicalReviewer=x['reviewer'], clinicalApprovedAt=x['date'])
            elif x['decision'] in ('changes_requested', 'not_approved'):
                d['review'].update(status=x['decision'], clinicalReviewer=None, clinicalApprovedAt=None)
            d['review']['reviewComment'] = x.get('comment', '')
        for k, v in e.get('references', {}).items():
            d['referenceChecks'][k] = dict(status=v, checkedBy=e.get('referenceBy'), checkedAt=e.get('referenceDate'), note=e.get('referenceNote', ''))
        if 'tga' in e and d.get('pregnancyLactation'):
            d['pregnancyLactation']['tgaCategory'] = e['tga']
        elif 'tga' in e:
            d['pregnancyLactation'] = dict(status='reviewer_entry', sourceIds=[], fdaLetterCategory=None, pregnancy=None, lactation=None, tgaCategory=e['tga'],
                                           note='TGA category entered by a reviewer from the TGA database; label excerpts not yet curated.')
        if 'jfda' in e:
            d['referenceChecks']['jfda'] = dict(status=e['jfda']['status'], note=e['jfda']['note'], checkedBy=e['jfda']['by'])
        applied += 1
data['reviewSummary'] = dict(files=[f.name for f in files], reviewed=sum(d['review']['status'] == 'clinically_reviewed' for d in data['drugs']))
(D/'database.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))
print(json.dumps(dict(reviewFiles=len(files), entriesUpdated=applied, reviewed=data['reviewSummary']['reviewed'])))
