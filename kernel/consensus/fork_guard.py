
FINALITY_HEIGHT=819
def can_reorg_simple(height):
    return height >= FINALITY_HEIGHT
def assert_finality(height):
    if height < FINALITY_HEIGHT:
        raise RuntimeError(f"FINALITY VIOLATION {height} < {FINALITY_HEIGHT}")
