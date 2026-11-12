# Closed family of tails for the level map of M (mirrored A), and its limits.
#   gcc -O2 -o level level.c && gcc -O2 -o dstep dstep.c && python3 tail_family.py
#
# Tails are lists of runs of ones (a run 0 stands for "00").
# T = { tails whose runs are all = 0 or 2 (mod 3), first run > 0 and != 2, last run = 0 (mod 3) and > 0 }.
# Part 1: for a main counter n that is large compared with the tail, both residues map T into T, without HALT.
# Part 2: the chain of a block 3.5.2^j is a 3/2 counter of its own; its growth is paid by the counter to its left.
# Part 3: with a small main counter the level rules fail, and configurations inside the grammar X*Y can HALT.
import subprocess,itertools,random,collections,os
HERE=os.path.dirname(os.path.abspath(__file__))
def inT(w): return len(w)>0 and all(x%3!=1 for x in w) and w[0]>0 and w[0]!=2 and w[-1]>0 and w[-1]%3==0
def sh(t):
    s=[];i=0
    while i<len(t):
        j=i
        while j<len(t) and t[j]==t[i]: j+=1
        s.append('%d^%d'%(t[i],j-i) if j-i>2 else '.'.join([str(t[i])]*(j-i))); i=j
    return '.'.join(s)
def levels(tails):
    """[(e,W') for r=0, (e,W') for r=1] per tail, with q large compared with the tail (two values of q each)"""
    groups=collections.defaultdict(list)
    for idx,W in enumerate(tails):
        q=16*((sum(W)//3+len(W)+8)//16+1)
        for r in (0,1): groups[q].append((idx,r,'%d %s\n'%(r,' '.join(map(str,W)))))
    out={}
    for q,L in groups.items():
        o=subprocess.run([os.path.join(HERE,'level'),str(q),str(q+3)],input=''.join(x[2] for x in L),capture_output=True,text=True).stdout.split('\n')
        for (idx,r,_),line in zip(L,o):
            f=line.split(); out[(idx,r)]=(f[0],None) if f[0] in('HALT','MAX','EDGE','DIFF') else (int(f[0]),list(map(int,f[1:])))
    return [(out[(i,0)],out[(i,1)]) for i in range(len(tails))]
def dstep(tapes):
    o=subprocess.run([os.path.join(HERE,'dstep'),'step'],input=''.join(' '.join(map(str,t))+'\n' for t in tapes),capture_output=True,text=True).stdout.split('\n')
    return [line.split()[0] for line in o[:len(tapes)]]
def part1(tails,label):
    stat=collections.Counter(); shown=0
    for W,rr in zip(tails,levels(tails)):
        for r,(e,w) in enumerate(rr):
            good=w is not None and inT(w); stat['in T' if good else ('not in T' if w is not None else e)]+=1
            if not good and shown<5: print('   counterexample: r=%d'%r,sh(W),'->',e,w); shown+=1
    print('  %-52s %6d tails x 2 residues: %s'%(label,len(tails),dict(stat)),flush=True)
def rand(rnd,maxlen,zero,two,big):
    while True:
        w=[]
        for _ in range(rnd.randrange(0,maxlen+1)):
            u=rnd.random()
            w.append(0 if u<zero else 2 if u<zero+two else 3*rnd.randrange(1,big)+rnd.choice([0,2]) if rnd.random()<.3 else rnd.choice([3,3,6,9,5,5,8,11]))
        w.append(3*rnd.randrange(1,big) if rnd.random()<.3 else rnd.choice([3,3,6,9]))
        if inT(w): return w
if __name__=='__main__':
    rnd=random.Random(1)
    print('Part 1: T is closed under the level map when n is large compared with the tail')
    part1([list(b)+[e] for n in range(6) for b in itertools.product([0,2,3,5,6,8],repeat=n) for e in (3,6) if inT(list(b)+[e])],'all tails, runs in {0,2,3,5,6,8}, up to 6 runs')
    part1([rand(rnd,12,.1,.4,12) for _ in range(20000)],'random tails, up to 13 runs')
    part1([rand(rnd,30,.05,.5,40) for _ in range(5000)],'random tails, up to 31 runs, runs up to 120')
    part1([rand(rnd,20,.3,.2,15) for _ in range(5000)],'random tails with many 00')
    print('Part 2: tail 3.5.2^j.3, residue 1: chain 2i -> 3i (rest sees residue 1), 2i+1 -> 3i+4 (rest sees 0), e = 6 - ceil(j/2)')
    ok=0
    for j,(r0,r1) in zip(range(0,60),levels([[3,5]+[2]*j+[3] for j in range(0,60)])):
        i,s=divmod(j,2); ok+= r1==(6-(i+s),[3,5]+[2]*(3*i+4*s)+([3] if s else [3,6])) and r0==(7,[8]+[2]*j+[3])
    print('  j = 0..59: %d of 60 agree'%ok)
    print('  two blocks 3.5.2^a.3.5.2^b.3, residue 1, a even: first chain becomes 3a/2 - ceil(b/2) (b pays with the first chain)')
    cases=[(a,b) for a in (20,40,60) for b in range(0,2*a//3)]; ok=0
    for (a,b),(r0,r1) in zip(cases,levels([[3,5]+[2]*a+[3,5]+[2]*b+[3] for a,b in cases])):
        i,s=divmod(b,2); ok+= r1[1] is not None and r1[1][:2+3*a//2-(i+s)+2]==[3,5]+[2]*(3*a//2-(i+s))+[3,5]
    print('  %d of %d agree'%(ok,len(cases)))
    print('  if the first chain is too short, the result leaves the grammar X*Y (but stays in T):')
    for b,(r0,r1) in zip((12,14,16,18,20),levels([[3,5]+[2]*4+[3,5]+[2]*b+[3] for b in (12,14,16,18,20)])):
        print('    3.5.2^4.3.5.2^%d.3, r=1  ->  e=%+d, %s'%(b,r1[0],sh(r1[1])))
    print('Part 3: small main counter n (direct simulation from (110)^n W, state D)')
    for j in (24,48,96):
        i=j//2; exp=[3,5]+[2]*(3*i)+[3,6]; lastbad=None
        for n in range(1,j+12,2):
            o=subprocess.run([os.path.join(HERE,'level'),str(n//2),str(n//2)],input='1 %s\n'%' '.join(map(str,[3,5]+[2]*j+[3])),capture_output=True,text=True).stdout.split()
            if o[0] in('HALT','MAX','EDGE','DIFF') or (int(o[0]),list(map(int,o[1:])))!=(6-i,exp): lastbad=n
        print('  tail 3.5.2^%d.3: the rule for residue 1 holds for all odd n > %s (tested up to %d)'%(j,lastbad,j+11))
    tapes=[]
    for _ in range(60000):
        w=[2]*rnd.randrange(0,9)
        for _ in range(rnd.randrange(2,4)): w+=rnd.choice([[3,5],[3,5],[8]])+[2]*rnd.choice([1,2,3,4,5,6,rnd.randrange(1,30)])
        t=rnd.choice([1,1,2,3]); tapes.append(w+([3*t] if rnd.random()<.5 else [3,3*t]))
    H=sorted((t for t,k in zip(tapes,dstep(tapes)) if k=='HALT'),key=lambda t:(sum(t),len(t)))
    print('  random configurations (110)^n X X [X] Y of the grammar with n < 9: %d of %d HALT before the next left-edge configuration'%(len(H),len(tapes)))
    for t in H[:5]: print('    HALT: (110)^%d followed by the tail %s'%(next(i for i,x in enumerate(t) if x!=2),sh(t[next(i for i,x in enumerate(t) if x!=2):])))
