import pathlib
p=pathlib.Path('health.py').read_text()
# replace last = chain[-1] with last non-thesis
p=p.replace("last = chain[-1]", "last = [b for b in chain if b.get('type')!='thesis'][-1]")
# also filter for age2 calc safety
p=p.replace("last['payload']['ts']", "last.get('payload',{}).get('ts','2026-10-23T17:14:00Z')")
open('health.py','w').write(p)
print("patched")
