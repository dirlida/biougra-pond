import pathlib
p=pathlib.Path('pond.py').read_text()
# Fix 1: get last mining block, not thesis
p=p.replace('last = chain[-1]', 'last = [b for b in chain if b.get("type")!="thesis"][-1]')
p=p.replace('last["index"]', 'last.get("index", last.get("idx"))')
p=p.replace("last['index']", "last.get('index', last.get('idx'))")
open('pond.py','w').write(p)
print("patched pond.py")
