"""Restore the reviewed metadata snapshot for local preview and GitHub Pages."""
import gzip,hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
raw=gzip.decompress((root/'data/articles.json.gz').read_bytes())
data=json.loads(raw)
assert len(data['articles'])==data['manifest']['indexed']
assert len({a['url'] for a in data['articles']})==len(data['articles'])
(root/'dist/articles.json').write_bytes(raw)
print(f"Prepared {len(data['articles']):,} article records; SHA-256 {hashlib.sha256(raw).hexdigest()}")
