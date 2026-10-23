lines=open('pond.py').read().splitlines()
# find import line
for i,l in enumerate(lines[:10]):
    print(i, repr(l))
