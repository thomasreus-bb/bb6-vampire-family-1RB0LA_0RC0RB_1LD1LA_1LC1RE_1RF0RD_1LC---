# abstract BFS over clean snapshots: blocks are exact (<= S) or big ('B', residue mod M)
import subprocess, sys, random, collections, json
S=int(sys.argv[1]); M=int(sys.argv[2]); T=int(sys.argv[3]); LIMIT=int(sys.argv[4])
random.seed(7)
def mstep(h,blocks):
    o=subprocess.run(["./mstep","200000000",str(h)]+list(map(str,blocks)),capture_output=True,text=True).stdout.split()
    if not o: return ("ERR",)
    if o[0]!="OK": return (o[0],)
    return (int(o[2]),tuple(map(int,o[4:])))
def big(r): return ("B",r)
def absv(v): return v if v<=S else big(v%M)
def rep(r,scale):
    v=scale+random.randrange(0,400)*M+r
    return v
def instantiate(state,scales):
    h,bl=state; vals=[]; bi=0
    for b in bl:
        if isinstance(b,tuple): vals.append(rep(b[1],scales[bi])); bi+=1
        else: vals.append(b)
    return h,vals
def succs(state):
    h,bl=state
    nb=sum(isinstance(b,tuple) for b in bl)
    out=set(); notes=[]
    # (a) generic: two independent large instantiations
    res=[]
    for trial in range(2):
        hh,vals=instantiate(state,[3000+trial*7000+i*20000 for i in range(nb)])
        r=mstep(hh,vals)
        if len(r)==1: return None,("SPECIAL",r[0],vals)
        res.append((vals,r))
    (v1,(h1,o1)),(v2,(h2,o2))=res
    if h1!=h2 or len(o1)!=len(o2): notes.append(("SHAPE",state,res)); 
    else:
        ab=[]
        for a,b in zip(o1,o2):
            if a==b and a<=S: ab.append(a)
            elif a>S and b>S and a%M==b%M: ab.append(big(a%M))
            elif a>S and b>S: ab.append("?")
            else: ab.append("!")
        if "!" in ab: notes.append(("MIXED",state,res))
        elif "?" in ab:
            # residue not determined by the input residues: over-approximate with all residues
            idx=[i for i,x in enumerate(ab) if x=="?"]
            import itertools
            for combo in itertools.product(range(M),repeat=len(idx)):
                ab2=list(ab)
                for i,rr in zip(idx,combo): ab2[i]=big(rr)
                out.add((h1,tuple(ab2)))
        else: out.add((h1,tuple(ab)))
    # (b) edge cases: each big block in turn takes the values just above S with its residue
    bpos=[i for i,b in enumerate(bl) if isinstance(b,tuple)]
    for i in bpos:
        r=bl[i][1]
        for v in range(S+1,S+1+T):
            if v%M!=r: continue
            hh,vals=instantiate(state,[3000+j*20000 for j in range(nb)])
            vals=list(vals); vals[i]=v
            rr=mstep(hh,vals)
            if len(rr)==1: return None,("SPECIAL",rr[0],vals)
            out.add((rr[0],tuple(absv(x) for x in rr[1])))
    return out,notes
start=(1,(1,1))
seen={start:None}; q=collections.deque([start]); allnotes=[]
while q and len(seen)<LIMIT:
    s=q.popleft()
    nx,notes=succs(s)
    if nx is None:
        print("SPECIAL from",s,notes); 
        # print path
        p=s; path=[]
        while p is not None: path.append(p); p=seen[p]
        for x in reversed(path): print("   ",x)
        sys.exit()
    allnotes+=notes
    for t in nx:
        if len(t[1])>14: allnotes.append(("LONG",t)); continue
        if t not in seen: seen[t]=s; q.append(t)
print("states",len(seen),"queue",len(q),"notes",len(allnotes))
for n in allnotes[:10]: print(n[0],n[1])
lens=collections.Counter(len(s[1]) for s in seen); print("list lengths",sorted(lens.items()))
json.dump([ [s[0],[list(b) if isinstance(b,tuple) else b for b in s[1]]] for s in seen],open("abs_states_S%d_M%d.json"%(S,M),"w"))
