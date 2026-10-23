def atomic_write(path, data):
    import pathlib, os, json, tempfile
    p = pathlib.Path(path)
    tmp = p.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, indent=2))
    os.fsync(tmp.open('r').fileno())
    tmp.rename(p)  # atomic
