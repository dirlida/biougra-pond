import pathlib
p=pathlib.Path('pond.py').read_text()
# make payload line 105 safe
old='payload={"ts":ts,"sunAltitude":last["payload"].get("sunAltitude",15.2),"btcHeight":last["payload"].get("btcHeight",972583)+1,"pondClock":p_now.isoformat().replace("+00:00","Z"),"driftMin":round(drift/60,1),"device":"did:pond:biougra-a13","law":"ghoul-v5.4"}'
# replace with safe version
new='lp=last.get("payload",{}) or {}\npayload={"ts":ts,"sunAltitude":lp.get("sunAltitude",15.2),"btcHeight":lp.get("btcHeight",972583)+1,"pondClock":p_now.isoformat().replace("+00:00","Z"),"driftMin":round(drift/60,1),"device":"did:pond:biougra-a13","law":"ghoul-v5.4"}'
if old in p:
    p=p.replace(old,new)
else:
    # fallback replace line containing payload
    lines=p.splitlines()
    for i,line in enumerate(lines):
        if 'last["payload"].get("sunAltitude"' in line or "last.get(\"payload\"" in line and "sunAltitude" in line:
            indent=line[:len(line)-len(line.lstrip())]
            lines[i]=indent+'lp=last.get("payload",{}) or {}\n'+indent+'payload={"ts":ts,"sunAltitude":lp.get("sunAltitude",15.2),"btcHeight":lp.get("btcHeight",972583)+1,"pondClock":p_now.isoformat().replace("+00:00","Z"),"driftMin":round(drift/60,1),"device":"did:pond:biougra-a13","law":"ghoul-v5.4"}'
            break
    p="\n".join(lines)
open('pond.py','w').write(p)
print("patched payload")
