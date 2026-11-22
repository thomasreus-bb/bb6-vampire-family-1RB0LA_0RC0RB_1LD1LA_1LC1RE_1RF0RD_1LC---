import subprocess,random
random.seed(1)
def run(tape,mx=20000000):
    return subprocess.run(['./syn70','0',tape,str(mx)],capture_output=True,text=True).stdout.strip()
H=[];n=0
for x in range(3,80):
  for m in (11,17,23,35):
    for g in (1,2,3,4,5,6,7,8,9,12):
      for rest in ("4 30 4","8 30 4","4 2 4 30 4","4 1 4 30 4","8 3 4 30 4"):
        o=run(f"1 {x} {m} {g} {rest}"); n+=1
        if not o[0].isdigit() or 'z0' not in o: H.append((x,m,g,rest,o))
print(n,'runs,',len(H),'not ending in a level start')
import collections
print(collections.Counter(h[4].split()[0] for h in H))
for h in H[:30]: print(h)
