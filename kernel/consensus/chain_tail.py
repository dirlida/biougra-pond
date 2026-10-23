import pathlib, re
ROOT=pathlib.Path.home()/"pond"
CHAIN=ROOT/"chain.json"
def get_tail(n=10):
    try:
        data=CHAIN.read_bytes()[-16384:]
        blocks=re.findall(rb'"index":\s*(\d+).*?"hash":\s*"([a-f0-9]{64})"', data)
        return [(b[0].decode(), b[1].decode()) for b in blocks[-n:]]
    except Exception as e:
        return [(0,str(e))]
if __name__=="__main__":
    for i,h in get_tail(10):
        print(f"#{i} {h[:8]} 00={h.startswith('00')}")
