import re,sys
U8="bEbCdEbC"; U12="dEbCdEbCbEbC"
R8={U8[i:]+U8[:i] for i in range(8)}; R12={U12[i:]+U12[:i] for i in range(12)}
def comp(s):
    out=[];i=0;lit=""
    while i<len(s):
        hit=None
        for u,R,name in ((12,R12,"P12"),(8,R8,"P8")):
            unit=s[i:i+u]
            if unit in R:
                r=1
                while s[i+r*u:i+(r+1)*u]==unit: r+=1
                if r>=3: hit=(name,u,r); break
        if hit:
            if lit: out.append(lit); lit=""
            out.append("%s^%d"%(hit[0],hit[2])); i+=hit[1]*hit[2]
        else: lit+=s[i]; i+=1
    if lit: out.append(lit)
    return out
lines=open(sys.argv[1]).read().split("\n")
for k,l in enumerate(lines):
    if not l: continue
    print(k+1, " ".join(comp(l)))
