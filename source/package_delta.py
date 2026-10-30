"""Byte-based changed-file package from an exact earlier cumulative ZIP."""
from pathlib import Path
import hashlib,json,sys,zipfile
if len(sys.argv)!=4:raise SystemExit('Usage: package_delta.py BASE_V010.zip CURRENT.zip OUTPUT_DELTA.zip')
base,current,out=map(Path,sys.argv[1:])
with zipfile.ZipFile(base) as b,zipfile.ZipFile(current) as c:
 assert b.testzip() is None and c.testzip() is None
 assert json.loads(b.read('database.json'))['version']=='0.10.0'
 version=json.loads(c.read('database.json'))['version'];assert version=='0.11.2'
 old={n:b.read(n) for n in b.namelist()};now={n:c.read(n) for n in c.namelist()}
 deleted=sorted(set(old)-set(now));assert not deleted,'This update would require deletions'
 changes={n:v for n,v in now.items() if old.get(n)!=v}
 manifest=dict(baseVersion='0.10.0',targetVersion=version,baseArchiveSha256=hashlib.sha256(base.read_bytes()).hexdigest(),complete=False,deletedFiles=deleted,changedFiles=[dict(path=n,sha256=hashlib.sha256(v).hexdigest(),bytes=len(v)) for n,v in sorted(changes.items())])
 text='''RenalRounds v0.11.2 — modified files since v0.10

This is an update, not a complete project. Use with the exact v0.10 cumulative
package or the v0.11/v0.11.1 packages derived from it. Extract all folders/files into the
existing publishing root, preserve paths and replace matching files. Do not add
another enclosing folder or upload the ZIP itself. No deletion is required.

Included source/ paths keep the maintained code consistent. This patch contains
all v0.11/v0.11.1 updates AND the v0.11.2 Home/handbook expansion. You do not
need to apply v0.11 first. The cumulative ZIP is the alternative for a fresh
install or an uncertain base. Do not apply both packages.

After GitHub Pages redeploys, confirm v0.11.2 at the top/footer. If an old offline
copy remains, use Database & offline status → Check for update → Load available
update. Clinical review remains pending; read README.md and SOURCE_AUDIT.md.

PATCH_MANIFEST.json records exact changed paths, sizes and SHA-256 checksums.
'''
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n,v in sorted(changes.items()):z.writestr(n,v)
  z.writestr('UPDATE_FROM_v0.10.txt',text);z.writestr('PATCH_MANIFEST.json',json.dumps(manifest,indent=2))
 reconstructed=dict(old);reconstructed.update(changes);assert reconstructed==now
with zipfile.ZipFile(out) as z:assert z.testzip() is None
print(json.dumps(dict(package=str(out),bytes=out.stat().st_size,changedFiles=len(changes),version=version,cumulativeBytes=current.stat().st_size)))
