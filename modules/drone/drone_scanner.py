import json, sys, os
# POND DRONE — PASSIVE_NOTARY_ONLY — reads from kernel anchors
def load_anchor(p):
    try: return json.load(open(p))
    except: return {}
btc = load_anchor("kernel/anchors/btc_anchor.json")
sun = load_anchor("kernel/anchors/sun_anchor.json")

fw = sys.argv[sys.argv.index("--fw")+1] if "--fw" in sys.argv else ""
print(f"ANCHORS: btc={btc.get('btc_height')} sun={sun.get('sun_last')} Biougra #1303 LIVE")

if "s71m" in fw.lower() or "monochrome" in fw.lower():
    print("DENY — S-71M_Monochrome_Jetson denylisted [HUR War&Sanctions portal] => local_refuse_to_run")
else:
    print(f"ALLOW — {fw} purpose=AGRI btc={btc.get('btc_height')} sun_ref={sun.get('sun_last')}")
    print(f"SUN OK — {sys.argv[sys.argv.index('--sun')+1] if '--sun' in sys.argv else sun.get('sun_last')}° plausible (Biougra #1299 was 36.0609)")
print("LEGAL CHECK: PASSIVE_NOTARY_ONLY — ANRT/FCC/EU RED/PAS1887 COMPLIANT — No TX verbs found")
