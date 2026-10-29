"""Copy reviewed Site assets without its hosting identity, credentials, or Git state."""
import gzip,json,shutil,sys
from pathlib import Path
source=Path(sys.argv[1]).resolve();root=Path(__file__).resolve().parents[1]
assert (source/'dist/index.html').is_file(),'Expected Site checkout containing dist/index.html'
raw=(source/'dist/articles.json').read_bytes();data=json.loads(raw)
assert data['manifest']['indexed']==len(data['articles'])
shutil.copytree(source/'dist',root/'dist',dirs_exist_ok=True)
(root/'data').mkdir(exist_ok=True)
(root/'data/articles.json.gz').write_bytes(gzip.compress(raw,mtime=0))
if (source/'INVENTORY.json').exists():shutil.copy2(source/'INVENTORY.json',root/'INVENTORY.json')
print('Copied reviewed dist assets and compressed metadata. Review the diff before committing.')
