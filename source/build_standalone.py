"""Build an entirely self-contained HTML entry point; no runtime fetches."""
from pathlib import Path
import base64
import json

ROOT=Path(__file__).parent
DIST=ROOT/'dist'
def safe_json(obj):
    return json.dumps(obj,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')

html=(ROOT/'app-shell.html').read_text()
css=(DIST/'styles.css').read_text()
js=(DIST/'pk.js').read_text()+'\n'+(DIST/'app.js').read_text()
assert '</script' not in js.lower()
data=json.loads((DIST/'database.json').read_text())
docs={'guide':(DIST/'EDITORIAL_GUIDE.md').read_text(),'changelog':(DIST/'CHANGELOG.md').read_text()}
icon=base64.b64encode((DIST/'icon.svg').read_bytes()).decode()
html=html.replace('href="icon.svg"',f'href="data:image/svg+xml;base64,{icon}"')
html=html.replace('<link rel="stylesheet" href="styles.css">','<style>\n'+css+'\n</style>')
html=html.replace('  <script src="app.js" defer></script>','')
html=html.replace('</body>',f'<script id="renalrounds-data" type="application/json">{safe_json(data)}</script>\n<script id="renalrounds-docs" type="application/json">{safe_json(docs)}</script>\n<script>\n{js}\n</script>\n<noscript><p>Enable JavaScript to search this local reference. No dosing result is available without it.</p></noscript>\n</body>')
(DIST/'index.html').write_text(html)
(DIST/'.nojekyll').write_text('')
print(f'Built standalone index.html: {len(html.encode()):,} bytes; {len(data["drugs"])} entries')
