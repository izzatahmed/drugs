"""Cumulative GitHub Pages release; explicit public files only."""
from pathlib import Path
import hashlib,json,sys,zipfile
ROOT=Path(__file__).parent
data=json.loads((ROOT/'dist/database.json').read_text())
version=data['version']
if len(sys.argv)!=2:raise SystemExit('Usage: python3 package_github.py /absolute/output.zip')
out=Path(sys.argv[1]).resolve();out.parent.mkdir(parents=True,exist_ok=True)
runtime=['index.html','.nojekyll','sw.js','manifest.webmanifest','icon.svg','icon-180.png','icon-192.png','icon-512.png']
documents=['database.json','EDITORIAL_GUIDE.md','CHANGELOG.md','VERIFICATION.md','COMPLETION_PLAN.md','CURATION_QUEUE.json','REFERENCE_DIRECTORY.json','SOURCE_AUDIT.json','SOURCE_AUDIT.md','CALCULATOR.md']
source=['release_v08.py','baseline_v07.json','changelog_v07.md','verification_v07.md','checks_calculator.mjs','README.md','app-shell.html','build_data.py','build_standalone.py','release_v06.py','release_v07.py','source_inventory_v07.json','baseline_v06.json','changelog_v06.md','completion_plan_v06.md','checks_v07.mjs','sw-template.js','clinical_changelog_v04.md','changelog_v05.md','completion_plan_v05.md','baseline_v05_fingerprints.json','expansion_v02.py','expansion_v03.py','catalog_v03.py','expansion_v04.py','checks.mjs','checks_v06.mjs','baseline_v02.json','baseline_v03.json','package_github.py']
files={name:(ROOT/'dist'/name).read_bytes() for name in runtime+documents}
files['README.md']=(ROOT/'README.md').read_bytes()
files['SHA256SUMS.txt']=''.join(hashlib.sha256(body).hexdigest()+'  '+name+'\n' for name,body in sorted(files.items())).encode()
for name in source:files['source/'+name]=(ROOT/name).read_bytes()
for name in runtime+documents+['app.js','pk.js','workflow.js','offline.js','styles.css','renal-math.js','calculator.js']:files['source/dist/'+name]=(ROOT/'dist'/name).read_bytes()
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name,body in sorted(files.items()):z.writestr(name,body)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 assert z.read('index.html')==(ROOT/'dist/index.html').read_bytes()
 assert not any('.git/' in n or '.openai/' in n or 'qa-mobile' in n for n in z.namelist())
print(json.dumps(dict(package=str(out),bytes=out.stat().st_size,files=len(files),version=version)))
