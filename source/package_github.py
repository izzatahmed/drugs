"""Package explicit public source files and a root-level standalone index."""
from pathlib import Path
import hashlib
import json
import sys
import zipfile

ROOT=Path(__file__).parent
data=json.loads((ROOT/'dist/database.json').read_text())
version=data['version']
if len(sys.argv)!=2: raise SystemExit('Usage: python3 package_github.py /absolute/output.zip')
out=Path(sys.argv[1]).resolve()
out.parent.mkdir(parents=True,exist_ok=True)
readme=f'''# RenalRounds {version} — GitHub Pages package

## Update your GitHub copy

1. Extract this ZIP. Upload its extracted contents to your repository; do not upload only the ZIP.
2. Keep index.html at the repository root. Replace the old index.html to update the app. Editing database.json alone does not update the embedded data.
3. Commit the files to your publishing branch.
4. In Settings → Pages, choose Deploy from a branch, select main (or your branch) and /(root), then Save.
5. Open the Pages URL GitHub displays on your phone. Repository visibility/Pages availability depends on your plan.
6. If an old version appears, refresh and check the release number in About / Coverage & sources (v{version}).

index.html embeds all code, styling and data. It has no build step or external runtime dependencies. It can also run in a browser that opens local HTML/JavaScript; phone file-preview applications may not execute it. Source links need internet. No service-worker installation is included. No patient data or analytics are collected.

## This release

{len(data['drugs'])} indexed drugs/formulations: {data['coverage']['renal']} renal profiles, {data['coverage']['safety']} shared safety-note records and {data['coverage']['catalog']} renal-dose-pending catalog records.

Captopril now has a sourced renal profile and amlodipine has expanded adult hypertension dosing. Pharmacokinetic summaries are available for {data['pharmacokineticCoverage']['profiles']} BP/cardiovascular medicines; {data['pharmacokineticCoverage']['allFourCoreFields']} have reference half-life, Vd, binding and an IHD removal statement. Other values distinguish not reported, unknown and not yet curated. PK-only records do not acquire a renal dose automatically. Use Content → PK available.

Reference/ESRF half-lives, active metabolites, distribution-volume methods/units and dialysis modalities are kept distinct. Source-specific differences remain explicit. Captopril's UK table is TOTAL daily mg, not mg per dose or mL. No RRT supplement is calculated.

All clinical content remains draft and requires independent renal-pharmacist/nephrologist review. This is not a complete or approved prescribing formulary. PNF title/edition remains unidentified; BNF monograph comparison remains pending; only individually linked PDR monographs are represented as consulted. See EDITORIAL_GUIDE.md, CHANGELOG.md and VERIFICATION.md.

## Files and rebuilding

- index.html: the only required runtime file.
- .nojekyll: disables Jekyll processing.
- database.json: structured export, including PK field provenance and explicit gaps.
- EDITORIAL_GUIDE.md, CHANGELOG.md, VERIFICATION.md: scope, change history and validation limits.
- SHA256SUMS.txt: root-file checksums.
- source/: editable source and scripts; no access credentials, Site identity or Git metadata.

With Python 3 and Node.js, run from inside source/:

    python3 build_data.py
    python3 build_standalone.py
    node checks.mjs

Copy source/dist/index.html to the repository root for the next release. Rebuild the ZIP with:

    python3 package_github.py /absolute/path/RenalRounds_GitHub.zip

GitHub documentation: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site

The preview is updated separately. Your GitHub copy is not updated until you upload the new index.html. Direct GitHub account upload was not performed in this session.
'''
files={name:(ROOT/'dist'/name).read_bytes() for name in ['index.html','.nojekyll','database.json','EDITORIAL_GUIDE.md','CHANGELOG.md','VERIFICATION.md']}
files['README.md']=readme.encode()
files['SHA256SUMS.txt']=''.join(hashlib.sha256(body).hexdigest()+'  '+name+'\n' for name,body in sorted(files.items())).encode()
for name in ['README.md','app-shell.html','build_data.py','build_standalone.py','expansion_v02.py','expansion_v03.py','catalog_v03.py','expansion_v04.py','checks.mjs','baseline_v02.json','baseline_v03.json','package_github.py']:
    files['source/'+name]=(ROOT/name).read_bytes()
for name in ['index.html','.nojekyll','app.js','pk.js','styles.css','database.json','EDITORIAL_GUIDE.md','CHANGELOG.md','VERIFICATION.md','icon.svg']:
    files['source/dist/'+name]=(ROOT/'dist'/name).read_bytes()
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name,body in sorted(files.items()): z.writestr(name,body)
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    assert z.read('index.html')==(ROOT/'dist/index.html').read_bytes()
    assert not any('.git/' in n or '.openai/' in n or 'qa-mobile' in n for n in z.namelist())
print(json.dumps(dict(package=str(out),bytes=out.stat().st_size,files=len(files),version=version)))
