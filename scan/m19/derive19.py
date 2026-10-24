# BFS over Bell states (L, T) of 1RB0LC_1LA1RE_1LD1RE_1RE0LA_0RA1RF_0RB---:  tape L 1^n T, head at the right end, state E.
# For each state and residue r = n mod P: 3 values of n -> (L', T', n' = a n + b) or HALT.
import subprocess,sys,collections
from fractions import Fraction as F
TM='1RB0LC_1LA1RE_1LD1RE_1RE0LA_0RA1RF_0RB---'
P=int(sys.argv[1]); MAXS=int(sys.argv[2]); MAXL=int(sys.argv[3]) if len(sys.argv)>3 else 60
def step(L,T,n):
    o=subprocess.run(['./bstep',TM,'R','E','1',L or '-',T or '-',str(n),'1.3',str(MAXL),'40000000000'],capture_output=True,text=True).stdout.split()
    if o[0]=='OK': return ('OK',o[1].strip('-'),int(o[2]),o[3].strip('-'))
    return (o[0],)
table={}; Q=collections.deque([('','0')]); seen={('','0')}
while Q and len(seen)<=MAXS:
    L,T=Q.popleft()
    base=P*((80+12*len(L))//P+1)
    for r in range(P):
        ns=[base+r, base+r+P*5, base+r+P*17]
        res=[step(L,T,n) for n in ns]
        if all(x[0]=='HALT' for x in res): table[(L,T,r)]='HALT'; continue
        if not all(x[0]=='OK' for x in res) or len({(x[1],x[3]) for x in res})!=1:
            table[(L,T,r)]=('IRREG',res); continue
        a=F(res[1][2]-res[0][2],ns[1]-ns[0]); b=res[0][2]-a*ns[0]
        if res[2][2]!=a*ns[2]+b: table[(L,T,r)]=('NONAFF',res); continue
        L2,T2=res[0][1],res[0][3]
        table[(L,T,r)]=(L2,T2,a,b)
        if (L2,T2) not in seen: seen.add((L2,T2)); Q.append((L2,T2))
print('states',len(seen),'closed',not Q,'entries',len(table),'HALT',sum(v=='HALT' for v in table.values()),'irregular',sum(1 for v in table.values() if v!='HALT' and v[0] in('IRREG','NONAFF')))
for k,v in sorted(table.items(),key=lambda x:(len(x[0][0]),x[0])):
    if v=='HALT' or v[0] in ('IRREG','NONAFF'): print(k,v if v=='HALT' else v[0], '' if v=='HALT' else v[1][:3])
    else: print(k,'->',(v[0] or 'e',v[1] or 'e','n\'=%s n + %s'%(v[2],v[3])))
