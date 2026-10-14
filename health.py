import json, os, subprocess, datetime

print(f"=== BIOUGRA POND HEALTH — {datetime.datetime.now().strftime('%H:%M %d-%m-%Y')} ===")
print()

# verify.py
print("[verify.py]")
os.system("python verify.py")
print()

# BLOCKS from chain.json - THE FIX
try:
    with open("chain.json") as f:
        chain = json.load(f)
    print(f"[BLOCKS] found {len(chain)} blocks in chain.json")
    print(f"[STORAGE] chain.json size: {os.path.getsize('chain.json')/1024:.1f} KB")
    last = chain[-1]
    print(f"[LAST] last block: {last}")
except Exception as e:
    print(f"[BLOCKS] error: {e}")

print(f"[PWD] {os.getcwd()}")
print()

# GIT
print("[GIT] Uncommitted:")
os.system("git status --porcelain")
print()
print("[GIT] Last 5 commits:")
os.system("git log --oneline -5")
print()
print("=== END HEALTH ===")
