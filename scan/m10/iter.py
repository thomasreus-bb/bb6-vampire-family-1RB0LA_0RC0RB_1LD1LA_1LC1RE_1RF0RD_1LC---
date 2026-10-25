import sys,collections
exec(open("bandmap.py").read())
def full(a,sep,b,e):
    if b==0: return ('Z',0,0,1,1,a+1,1)   # rare special case seen once (b=0,e=0)
    r=step(a,sep,b,e)
    if r: return r
    m=2*a+1+2*sep; Y=2*b+e-3*m-2-sep
    return ('C',0,m,2*m+2+sep,0,Y//2,Y%2)
a,sep,b,e=1,1,1,1   # start of band 1 (step 48)
N=int(sys.argv[1]); seq=[];rows=[]
for k in range(1,N+1):
    t=full(a,sep,b,e)
    lab=t[0] if t[0] in 'CZ' else ('A' if a<=b else 'B')
    seq.append(lab); rows.append((k,a,sep,b,e,lab,t[1]))
    a,sep,b,e=t[3],t[4],t[5],t[6]
    if b<0: print("NEG",k); break
s="".join(seq)
if N<=200:
    for r in rows: print(*r)
print(s[:100]); print(collections.Counter(s))
print("final a,b",a,b)
print(collections.Counter(s[i:i+2] for i in range(len(s)-1)))
if N<=200:
    import textwrap; print("\n".join(textwrap.wrap(s,10)))
    print([r[0] for r in rows if r[5]=='Z'], [ (r[0],r[1],r[3]) for r in rows if r[0]<=20])
