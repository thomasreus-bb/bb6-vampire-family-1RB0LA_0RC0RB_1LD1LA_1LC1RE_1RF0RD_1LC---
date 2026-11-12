# Reachable tails under every residue sequence, by an exact model of the level map built from the event rules.
# Chains are stored as numbers, so there is no size limit.  usage: python3 reachable_exact.py DEPTH   (400: about 2 minutes)
# The model was compared with direct simulation on 14,970 level computations (no mismatch).
import sys
class Exh(Exception): pass
MARG=[]
def push2(c,S):
    if c<=0: return S
    if S and S[0][0]==2: return [(2,S[0][1]+c)]+S[1:]
    return [(2,c)]+S
def run(m,S,top,off):
    S=list(S); x=0
    while True:
        a,c=S[0]
        if a==2:
            p=c//2; m+=9*p; x+=p
            if c%2==0: S=S[1:]; continue
            k=S[1][0]; assert S[1][1]==1 and k!=2
            m+=k+7; S=S[2:]; x+=1
            if k%3==2: continue
            if S:
                assert S[0][0]!=2
                S=[(S[0][0]+3,1)]+S[1:]
            else: S=[(3,1)]
            return ((m//3+1) if top else (m-3)//3)-off, S, x
        if a%3==2:
            cc=(a-2)//3; m+=6; x+=1; nx=S[1]
            if nx[0]==2: S=push2(cc-1,[(5,1)]+push2(nx[1]-1,S[2:]))
            else: S=push2(cc-1,[(nx[0]+3,1)]+S[2:])
            continue
        cnt=(m+1)//3 if top else (m-5)//3
        if len(S)==1: return cnt-off,[(3,1),(a+3,1)],x
        b=S[1][0]
        if b%3==0: return cnt-off,[(3,1),(5,1)]+push2(b//3-1,[(3,1)]),x
        j,R,xin=run(b,S[2:],False,0)
        if not top:
            MARG.append((cnt,xin))
            if cnt-xin<0: raise Exh()
        return cnt-xin-off,[(3,1),(5,1)]+push2(j,R),x
def level(r,W):
    return run(35,push2(1-r,list(W)),True,6 if r else 9)
def show(W):
    return '.'.join(('2^%d'%c if c<10**6 else '2^(%d digits)'%len(str(c))) if a==2 else str(a) for a,c in W)
if __name__=='__main__':
    D=int(sys.argv[1])
    for name,start in (('A',((3,1),(9,1))),('B',((3,1),(3,1))),('C',((3,1),(6,1)))):
        cur={start}; seen=set(cur); exh=[]; ratio=(0,None); maxblocks=0; byd=[]
        for d in range(1,D+1):
            nxt=set(); dr=0
            for W in cur:
                for r in (0,1):
                    del MARG[:]
                    try: e,S,x=level(r,W)
                    except Exh: exh.append((d,W,r)); continue
                    for cnt,xin in MARG:
                        if cnt>0 and xin/cnt>dr: dr=xin/cnt
                        if cnt>0 and xin/cnt>ratio[0]: ratio=(xin/cnt,(d,W,r,cnt,xin))
                    S=tuple(S)
                    if S not in seen: seen.add(S); nxt.add(S)
            cur=nxt; byd.append(dr)
            maxblocks=max([maxblocks]+[sum(1 for i in range(len(W)-1) if W[i][0]==3 and W[i+1][0]==5) for W in cur])
        print('machine %s: depth %d, %d tails (%d new at the last depth), at most %d blocks 3.5, exhaustions inside the tail: %d'%(name,D,len(seen),len(cur),maxblocks,len(exh)))
        print('   largest share taken from a lending chain: %.4f at depth %d (tail %s)'%(ratio[0],ratio[1][0],show(ratio[1][1])[:90]))
        print('   largest share by depth range:',' '.join('%d-%d: %.3g'%(i+1,min(i+50,D),max(byd[i:i+50])) for i in range(0,D,50)))
        for d,W,r in exh[:3]: print('   EXHAUSTION at depth',d,'tail',show(W)[:80],'residue',r)
        sys.stdout.flush()
