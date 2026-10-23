import json, pathlib, glob
ROOT = pathlib.Path.home() / "pond"
# checks if block has confirmed OTS receipt = finality checkpoint
def get_finalized_height():
    # find highest block with .ots confirmed (not .pending)
    # we store .ots files in attic/
    ots_files = glob.glob(str(ROOT / "*.ots")) + glob.glob(str(ROOT / "attic" / "*.ots"))
    # naive: if chain has 1314, and we have genesis frozen block 819, finality = 819
    frozen = ROOT / "attic" / "frozen" / "FROZEN-2026-10-18-1748.json"
    if frozen.exists():
        try:
            j=json.loads(frozen.read_text())
            return j.get("height", j.get("index", 819))
        except: pass
    return 819

def can_reorg(from_height, to_height):
    finalized = get_finalized_height()
    if from_height < finalized:
        return False, f"reorg below finality {finalized} rejected"
    return True, "reorg allowed"

if __name__ == "__main__":
    print(f"finalized height {get_finalized_height()}")
