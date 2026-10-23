#!/usr/bin/env python3
"""
POND EMBASSY - DIFFICULTY v5.2 VESTED
One Device Forever Law
"""
import pathlib
ROOT = pathlib.Path.home() / "pond"
DEVICE_RAM_GB = 4
if DEVICE_RAM_GB <= 4:
    MAX_DIFF = 3
elif DEVICE_RAM_GB <= 8:
    MAX_DIFF = 5
else:
    MAX_DIFF = 8

def get_device_info():
    return {"ram_gb": DEVICE_RAM_GB, "max_diff": MAX_DIFF, "target": "0"*MAX_DIFF, "device_id": "did:pond:biougra-a13", "law": "one-device-max-out"}

def get_difficulty(height=None):
    return MAX_DIFF

def get_target():
    return "0"*MAX_DIFF

if __name__ == "__main__":
    info = get_device_info()
    print(f"[DIFF VESTED] device={info['device_id']} ram={info['ram_gb']}GB")
    print(f"[DIFF VESTED] max_diff={info['max_diff']} target={info['target']} law={info['law']}")
    print(f"difficulty={get_difficulty()}")
