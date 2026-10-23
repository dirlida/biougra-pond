
import pathlib, os, tempfile
def atomic_write(path, data_str):
    p=pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(p.parent))
    try:
        os.write(fd, data_str.encode())
        os.fsync(fd)
        os.close(fd)
        os.replace(tmp, str(p))
    except:
        try: os.close(fd)
        except: pass
        try: os.remove(tmp)
        except: pass
        raise
