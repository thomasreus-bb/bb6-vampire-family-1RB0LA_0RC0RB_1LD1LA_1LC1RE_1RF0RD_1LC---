# compare the accelerated simulator msim48 with direct simulation (at48.c) at many event times
import sys,subprocess,random
from msim48 import Sim,tape_str
T=float(sys.argv[1]); nsample=int(sys.argv[2])
sim=Sim(); recs=[]
def cb(s):
    l,r=tape_str(s)
    recs.append((s.steps,'ABCDEF'[s.q],l+r,len(l)))
sim.run(T,cb)
random.seed(1)
pick=sorted(random.sample(range(len(recs)),min(nsample,len(recs))))
sel=[recs[i] for i in pick]
open('/tmp/claude-0/-home-claude/67237a5a-00c9-59c6-8915-11e66e9078ee/scratchpad/steps48.txt','w').write('\n'.join(str(r[0]) for r in sel)+'\n')
out=subprocess.run(['./at48','/tmp/claude-0/-home-claude/67237a5a-00c9-59c6-8915-11e66e9078ee/scratchpad/steps48.txt'],capture_output=True,text=True).stdout.split('\n')
bad=0
for r,o in zip(sel,out):
    f=o.split()
    tape=r[2]; a=tape.find('1'); e=tape.rfind('1')
    want=(r[0],r[1],r[3]-1-a if False else None,tape[a:e+1])
    ok = int(f[0])==r[0] and f[1]==r[1] and f[3]==tape[a:e+1]
    if not ok: bad+=1; print('MISMATCH at',r[0],f[1],r[1],len(f[3]),len(tape[a:e+1]))
print(len(sel),'events compared,',bad,'mismatches; jumps used',sim.jumps,'last step',sim.steps)
