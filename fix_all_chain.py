import pathlib
text=pathlib.Path('pond.py').read_text()
# Replace every chain[-1] with filtered version
text=text.replace('chain[-1]', '[b for b in chain if b.get("type")!="thesis"][-1] if [b for b in chain if b.get("type")!="thesis"] else chain[-1]')
# Also chain[-1]['hash'] pattern already covered, but fix prev_hash line safe
text=text.replace('[b for b in chain if b.get("type")!="thesis"][-1] if [b for b in chain if b.get("type")!="thesis"] else chain[-1][\'hash\']', '([b for b in chain if b.get("type")!="thesis"][-1] if [b for b in chain if b.get("type")!="thesis"] else chain[-1]).get("hash","0"*64)')
# Simplify: make helper function at top
if 'def get_filtered(chain):' not in text:
    text=text.replace('import os', 'import os\ndef get_filtered(chain):\n    f=[b for b in chain if b.get("type")!="thesis"]\n    return f if f else chain\n')
    text=text.replace('[b for b in chain if b.get("type")!="thesis"][-1] if [b for b in chain if b.get("type")!="thesis"] else chain[-1]', 'get_filtered(chain)[-1]')
open('pond.py','w').write(text)
print("patched all chain[-1]")
