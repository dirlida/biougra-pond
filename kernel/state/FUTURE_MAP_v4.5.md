# FUTURE MAP v4.5 - WIDEST KERNEL - VEST PROOFED
LAW: ROOT=Path.home()/pond, ONE WRITER pond.py only, all modules READ-ONLY.
PRIVATE: kernel/modules/cables/seabed_state.json + raw_feeds/ + drones/fleet_state.json - gitignored
PUBLIC: embassy/public/cables/summary.json (uptime%, congestion only) + drones/summary.json (count+hash)
CHAIN PAYLOAD: only hashes - cables_hash, drones_hash - no raw intel
RULES: A) only pond.py writes chain.json B) modules write private state + public summary C) health + sha check before push D) no autostart
OFFLINE: pond.py mines offline, frozen every 100, ots_guard moves .ots
