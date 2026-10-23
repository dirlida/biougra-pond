import pathlib
p=pathlib.Path('pond.py').read_text()

# fix get_last if exists, else define
if 'def get_last():' in p:
    p=p.replace('def get_last():', 'def get_last_filtered():\n    c=load_chain()\n    f=[b for b in c if b.get("type")!="thesis"]\n    return f[-1] if f else c[-1]\n\ndef get_last():')
    # make get_last call filtered
    p=p.replace('def get_last():\n    return load_chain()[-1]', 'def get_last():\n    chain=load_chain()\n    filtered=[b for b in chain if b.get("type")!="thesis"]\n    return filtered[-1] if filtered else chain[-1]')

# Ensure load_chain filtered? keep original

# Fix all last["payload"] direct accesses after get_last
p=p.replace('last_ts=datetime.datetime.fromisoformat(last["payload"]["ts"]', 'last_ts=datetime.datetime.fromisoformat(last.get("payload",{}).get("ts","2026-10-23T17:14:00Z")')
p=p.replace('last["payload"].get("sunAltitude"', 'last.get("payload",{}).get("sunAltitude"')
p=p.replace('last["payload"].get("btcHeight"', 'last.get("payload",{}).get("btcHeight"')

open('pond.py','w').write(p)
print("clean patched")
