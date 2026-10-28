import sys,collections,math
sys.set_int_max_str_digits(0)
from map14 import cycle
def target(m):
    # is m = 2^k - k - 1 for some k?
    k=m.bit_length()
    for kk in (k,k+1):
        if 2**kk-kk-1==m: return kk
    return None
R=7   # first cycle start: (1,7) at width 9
seq=[];js=collections.Counter();ks=[];near=[]
for c in range(int(sys.argv[1])):
    m_end,j,ev=cycle(R)
    k=len([e for e in ev if e[1]>=0])  # events
    kd=sum(1 for e in ev[:-j] if True)-1
    seq.append(j); js[j]+=1
    if target(m_end) is not None: print("HALT target hit at cycle",c+1,"m_end=",m_end); break
    # closest target distance
    kk=m_end.bit_length()
    dist=min(abs(m_end-(2**t-t-1)) for t in (kk-1,kk,kk+1))
    near.append((dist/m_end, c+1))
    R=2*m_end+1
L="".join("ABCDEFGHIJ"[min(x,10)-1] for x in seq)
print("first 100 cycles (A: j=1, B: j=2, C: j=3, ...):")
for i in range(0,100,10): print("%3d-%3d  %s"%(i+1,i+10,L[i:i+10]))
tot=sum(js.values()); print({k:"%.3f"%(v/tot) for k,v in sorted(js.items())})
print("log2 of R after",len(seq),"cycles:",R.bit_length(), " per cycle %.3f bits"%(R.bit_length()/len(seq)))
near.sort(); print("closest relative approaches to a halting value:",[("%.2e"%a,c) for a,c in near[:5]])
