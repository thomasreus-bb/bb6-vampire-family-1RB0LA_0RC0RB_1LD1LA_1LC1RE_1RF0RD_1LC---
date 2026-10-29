# Equivalence of the Bell candidates no. 11 and no. 37 (bell_candidates.md): Y is X mirrored with renamed states,
# and X at step 8,277,490 and Y at step 7,454,917 are the same configuration up to mirroring and renaming.
import itertools
X="1RB1LB_1RC---_1LD1LF_1LE0LD_0LA1RF_1LC0RE"
Y="1RB1RF_1RC0RB_0RD1LF_1LE1RE_1LA---_1RA0LC"
def parse(M):
    T={}
    for i,s in enumerate(M.split("_")):
        for b in range(2):
            x=s[3*b:3*b+3]; T[(i,b)]=None if x[0]=='-' else (int(x[0]),1 if x[1]=='R' else -1,ord(x[2])-65)
    return T
TX,TY=parse(X),parse(Y)   # no. 11 and no. 37 of bell_candidates.md
def run(T,n):
    tape={};p=0;q=0
    for i in range(n):
        t=T[(q,tape.get(p,0))]
        if t is None: return None
        tape[p]=t[0];p+=t[1];q=t[2]
    return tape,p,q
def norm(tape,p,mirror):
    ks=[k for k,v in tape.items() if v]; lo,hi=min(ks),max(ks)
    w="".join(str(tape.get(i,0)) for i in range(lo,hi+1))
    if mirror: return w[::-1], hi-p
    return w, p-lo
a=run(TX,8277490); b=run(TY,7454917)
wa,pa=norm(a[0],a[1],False); wb,pb=norm(b[0],b[1],True)
print("tapes equal after mirroring:",wa==wb, "head offsets",pa,pb,"states", "ABCDEF"[a[2]],"ABCDEF"[b[2]], "length",len(wa))
wb2,pb2=norm(b[0],b[1],False); print("unmirrored equal:",wa==wb2)
# find state bijections pi: X-state -> Y-state with Y[pi(s),b] = (w, -d, pi(s')) for all defined transitions
best=[]
for perm in itertools.permutations(range(6)):
    ok=0; bad=[]
    for s in range(6):
        for bb in range(2):
            tx=TX[(s,bb)]; ty=TY[(perm[s],bb)]
            if tx is None or ty is None:
                if (tx is None)==(ty is None): ok+=1
                else: bad.append((s,bb))
            elif ty==(tx[0],-tx[1],perm[tx[2]]): ok+=1
            else: bad.append((s,bb))
    best.append((ok,perm,bad))
best.sort(reverse=True)
for ok,perm,bad in best[:3]: print(ok,"/12", "map", {"ABCDEF"[s]:"ABCDEF"[perm[s]] for s in range(6)}, "mismatching X transitions:",[("ABCDEF"[s],bb) for s,bb in bad])
