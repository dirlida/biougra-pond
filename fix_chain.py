import json
with open("chain.json") as f:
    txt=f.read().strip()
# repair ]{ case
txt=txt.replace("]\n{", "},\n{").replace("]{", "},{")
if not txt.endswith("]"):
    # ensure array
    if txt.startswith("[") and "}\n{" in txt and not txt.endswith("]"):
        pass
    else:
        # rebuild
        lines=[l for l in txt.splitlines() if l.strip()]
        # last line is block10 json
        import json as js
        blocks=[]
        # try parse
        try:
            blocks=js.loads(txt)
        except:
            # manual
            import re
            objs=re.findall(r'\{.*?\}', txt, re.DOTALL)
            # last is block10, keep 9+1
            blocks=[js.loads(o) for o in objs[-10:]]
        txt=json.dumps(blocks, indent=2)

with open("chain.json","w") as out:
    out.write(txt)
print("chain.json fixed")
print(open("chain.json").read()[-500:])
