import subprocess,itertools,collections
res={}
def run(x,m,g,rest="4 30 4 30 4 30 4"):
    o=subprocess.run(['./syn70','0',f"1 {x} {m} {g} {rest}",'50000000'],capture_output=True,text=True).stdout.strip()
    return o
halts=[]
for x in range(6,121,6):
  for m in (11,23,35,47):
    for g in range(1,31):
      o=run(x,m,g)
      if o.startswith('HALT') or o in('MAX','OVF'): halts.append((x,m,g,o))
print(len(halts)); 
for h in halts[:60]: print(h)
