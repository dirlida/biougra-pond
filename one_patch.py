import pathlib
text=open('pond.py').read()
# add helper after imports
text=text.replace('import os', 'import os\n\ndef get_last_mining(chain):\n    f=[b for b in chain if b.get("type")!="thesis" and "hash" in b]\n    return f[-1] if f else chain[-1]\n')

# replace all load_chain()[-1] and chain[-1] usages
text=text.replace('load_chain()[-1]', 'get_last_mining(load_chain())')
text=text.replace('chain[-1]', 'get_last_mining(chain)')

# safe payload
text=text.replace('last["payload"]["ts"]', 'last.get("payload",{}).get("ts","2026-10-23T17:14:00Z")')
text=text.replace('last["payload"].get("sunAltitude"', 'last.get("payload",{}).get("sunAltitude"')
text=text.replace('last["payload"].get("btcHeight"', 'last.get("payload",{}).get("btcHeight"')
text=text.replace('last["payload"]', 'last.get("payload",{})')

open('pond.py','w').write(text)
print("ONE PATCH DONE")
