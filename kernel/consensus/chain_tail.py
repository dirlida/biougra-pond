# A13 safe - never load full chain
import pathlib, json, re
ROOT=pathlib.Path.home()/"pond"
CHAIN=ROOT/"chain.json"
def get_tail(n=5):
    try:
        data=CHAIN.read_bytes()[-16384:]  # last 16KB only
        # crude but A13 safe
        blocks=re.findall(b'"index":\s*(\d+).*?"hash":\s*"([a-f0-9]{64})"', data)
        return blocks[-n:]
    except Exception as e:
        return [(0,str(e))]
if __name__=="__main__":
    print(get_tail(4))
