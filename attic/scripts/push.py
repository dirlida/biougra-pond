import shutil, os, subprocess, json
os.makedirs('embassy/public', exist_ok=True)
shutil.copy2('chain.json','embassy/public/chain.json')
shutil.copy2('chain.json','embassy/public/blocks.json')
print(f"Chain: {len(json.load(open('chain.json')))} blocks - synced to embassy/public/")
subprocess.run(["git","add","chain.json","embassy/public/"])
subprocess.run(["git","add","-u"])
subprocess.run(["git","commit","-m","auto sync embassy"])
subprocess.run(["git","push","origin","main"])
