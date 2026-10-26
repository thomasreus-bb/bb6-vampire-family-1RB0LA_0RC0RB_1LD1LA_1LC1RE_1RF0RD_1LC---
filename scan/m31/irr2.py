import sys,collections
L=[l.split("|") for l in open(sys.argv[1])]
S=[(int(h.split()[0][1:]), list(map(int,r.split()))) for h,r in L]
def strip(r): return r[:-1] if len(r)>=2 and r[-1]==1 else r
def regular(a,b):
    (ha,ra),(hb,rb)=a,b
    ra2,rb2=strip(ra),strip(rb)
    if len(ra2)!=len(rb2): return False
    d=[y-x for x,y in zip(ra2,rb2)]; nz=[(i,x) for i,x in enumerate(d) if x]
    if len(nz)!=2: return False
    (i,a1),(j,a2)=nz
    return j==i+1 and ((a1,a2) in [(4,-3),(4,-2),(4,-4),(5,-3),(3,-3)] )
irr=collections.Counter()
for k in range(len(S)-1):
    if not regular(S[k],S[k+1]):
        print("h%d %s  ->  h%d %s"%(S[k][0]," ".join(map(str,S[k][1])),S[k+1][0]," ".join(map(str,S[k+1][1]))))
