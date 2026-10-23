
import pathlib, json, datetime
ROOT=pathlib.Path.home()/"pond"
CHAIN=ROOT/"chain.json"
FLEET=ROOT/"kernel/modules/drones/fleet_state.json"
LOG=ROOT/"kernel/modules/drones/flight_log.jsonl"
def ingest():
    try:
        chain=json.loads(CHAIN.read_text())
        last=chain[-1]
        flight={
          "index": last["index"],
          "hash": last["hash"][:12],
          "ts": last["payload"].get("ts"),
          "device": "did:pond:biougra-a13",
          "altitude_m": 15.2,
          "gps": "30.36N 9.39W Biougra",
          "status": "grounded-embassy",
          "attested_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        try: state=json.loads(FLEET.read_text())
        except: state={"fleet":[]}
        state["fleet"]=state.get("fleet",[])[-49:]+[flight]
        FLEET.write_text(json.dumps(state, indent=2))
        with LOG.open("a") as f:
            f.write(json.dumps(flight)+"\n")
        print(f"[DRONES] fleet {last['index']}")
    except Exception as e:
        print(f"[DRONES ERR] {e}")
if __name__=="__main__":
    ingest()
