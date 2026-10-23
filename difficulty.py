#!/usr/bin/env python3
"""
POND EMBASSY - DIFFICULTY v5.2 VESTED
One Device Forever Law
A13 4GB -> 3 zeros, 12GB -> 5 zeros, 16GB+ -> 8 zeros
Kernel philosophy same, only max power scales
"""
import pathlib
import json
import os

ROOT = pathlib.Path.home() / "pond"
CHAIN = ROOT / "chain.json"
GENESIS_DIFF = 3
TARGET_BLOCK_TIME = 600
MIN_DIFF = 3

# === DEVICE POWER CAP — ONLY LINE YOU CHANGE WHEN YOU UPGRADE PHONE ===
# A13 4GB = 3, future 12GB = 5, future 16GB+ = 8
# This IS kernel law, not config
DEVICE_RAM_GB = 4  # <- change this on new phone

if DEVICE_RAM_GB <= 4:
    MAX_DIFF = 3
elif DEVICE_RAM_GB <= 8:
    MAX_DIFF = 5
else:
    MAX_DIFF = 8
# === END DEVICE CAP ===

def get_device_info():
    """Return device power profile for logging"""
    return {
        "ram_gb": DEVICE_RAM_GB,
        "max_diff": MAX_DIFF,
        "target": "0" * MAX_DIFF,
        "device_id": "did:pond:biougra-a13",
        "law": "one-device-max-out"
    }

def get_difficulty(height=None):
    """
    One Device Forever Law:
    Always return MAX_DIFF for this device
    No adjustment, no dead code, no multi-node logic
    Phone powers max, kernel same
    """
    return MAX_DIFF

def get_target():
    """Return PoW target string for current device"""
    return "0" * MAX_DIFF

if __name__ == "__main__":
    info = get_device_info()
    print(f"[DIFF VESTED] device={info['device_id']} ram={info['ram_gb']}GB")
    print(f"[DIFF VESTED] max_diff={info['max_diff']} target={info['target']} law={info['law']}")
    print(f"difficulty={get_difficulty()}")
