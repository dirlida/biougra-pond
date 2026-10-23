
import pathlib, json, datetime
ROOT=pathlib.Path.home()/"pond"
CHAIN=ROOT/"chain.json"
FEED=ROOT/"kernel/modules/cables/raw_feeds"
FEED.mkdir(parents=True, exist_ok=True)
SEABED=ROOT/"kernel/modules/cables/seabed_state.json"
def ingest():
    try:
        chain=json.loads(CHAIN.read_text())
        last=chain[-1]
        p=last["payload"]
        entry={
          "index": last["index"],
          "hash": last["hash"],
          "ts": p.get("ts"),
          "btcHeight": p.get("btcHeight"),
          "sunAltitude": p.get("sunAltitude"),
          "driftMin": p.get("driftMin"),
          "gps": "Biougra 30.36N 9.39W attested",
          "ingested_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        (FEED/f"feed-{last['index']}.json").write_text(json.dumps(entry, indent=2))
        try: state=json.loads(SEABED.read_text())
        except: state={"cables":[]}
        state["cables"]=state.get("cables",[])[-99:]+[entry]
        SEABED.write_text(json.dumps(state, indent=2))
        print(f"[CABLES] ingested {last['index']}")
    except Exception as e:
        print(f"[CABLES ERR] {e}")
if __name__=="__main__":
    ingest()
