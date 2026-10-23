text=open('pond.py').read()
# insert helper after line 2
helper='\n\ndef get_last_mining(chain):\n    f=[b for b in chain if b.get("type")!="thesis" and b.get("hash")]\n    return f[-1] if f else chain[-1]\n'
parts=text.split('\n',3)
# parts[0]=shebang, 1=import os..., 2=from datetime...
text=parts[0]+'\n'+parts[1]+'\n'+parts[2]+helper+parts[3]

# safe replacements
text=text.replace('chain[-1]', 'get_last_mining(chain)')
text=text.replace('load_chain()[-1]', 'get_last_mining(load_chain())')
text=text.replace('last["payload"]["ts"]', 'last.get("payload",{}).get("ts","2026-10-23T17:14:00Z")')
text=text.replace('last["payload"].get("sunAltitude"', 'last.get("payload",{}).get("sunAltitude"')
text=text.replace('last["payload"].get("btcHeight"', 'last.get("payload",{}).get("btcHeight"')
# handle remaining last["payload"] that weren't .get
text=text.replace('last["payload"]', 'last.get("payload",{})')

open('pond.py','w').write(text)
print("fixed")
