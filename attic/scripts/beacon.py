import os, requests, json
from datetime import datetime, timezone

TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHANNEL = os.getenv("TG_CHANNEL")

def send_beacon(text):
    if not TG_TOKEN or not TG_CHANNEL:
        print("Missing TG_TOKEN or TG_CHANNEL")
        return
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    data = {"chat_id": TG_CHANNEL, "text": text, "parse_mode": "Markdown"}
    r = requests.post(url, data=data)
    print(r.text)
    return r.json()

if __name__ == "__main__":
    try:
        chain = json.load(open("chain.json"))
        last = chain[-1]
        height = len(chain)-1
        h = last['hash'][:16]
    except:
        height = "?"
        h = "no-chain"
    now = datetime.now(timezone.utc).isoformat()
    msg = f"🔵 *POND BEACON v3* | Height: `{height}` | Hash: `{h}` | {now} | Alive"
    send_beacon(msg)
