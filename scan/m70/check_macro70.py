# compare the macro simulator with the level starts of the direct run (l70.txt.gz, 3e9 steps)
import gzip,re
from macro70 import step
real=[]
for l in gzip.open('l70.txt.gz','rt'):
    st,s=l.split(':',1); t=s.split()
    if t[0]!='1' or not t[1].startswith('|'): continue
    nums=[int(v.strip('|')) for v in t[1:]]
    if len(nums)<2 or (nums[0]==6 and nums[1]==4): continue
    real.append((int(st[1:]),nums))
x,S,steps=30,[11,18,4],1607
i=[k for k,(st,n) in enumerate(real) if st==1607][0]
ok=0
for st,n in real[i+1:]:
    x,S,dst=step(x,S); steps+=dst
    if steps!=st or [x]+S!=n[:len(S)+1] or len(n)!=len(S)+1:
        print('MISMATCH at real step',st,n[:12],'macro',steps,[x]+S[:11]); break
    ok+=1
print('level starts compared:',ok,'all equal' if ok==len(real)-i-1 else '')
