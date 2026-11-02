# Bell table of no. 39 for the tail words that occur (BFS). usage: gcc -O2 -o step step.c; python3 table.py BASE LIMIT MOD (e.g. 400 80 4)
import subprocess,sys,collections
M='1RB1LC_1LC0RF_0LF1LD_0LE---_1RF1LC_1LE0RA'
def step(P,n,S):
    o=subprocess.run([__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'step'),M,P or '-',str(n),S or '-','400000000'],capture_output=True,text=True).stdout.split()
    if o[0]=='HALT': return ('HALT',o[2])
    if o[0]=='NONE': return ('NONE',)
    return (o[0].replace('-',''),int(o[1]),o[2].replace('-',''))
start=('','')
todo=collections.deque([start]); T={}; seen={start}
MOD=int(sys.argv[3]) if len(sys.argv)>3 else 2
base=int(sys.argv[1]) if len(sys.argv)>1 else 400
lim=int(sys.argv[2]) if len(sys.argv)>2 else 300
while todo and len(T)<lim:
    w=todo.popleft()
    for par in range(MOD):
        res=[]
        for k in range(3):
            n=base+MOD*k+par
            r=step(w[0],n,w[1])
            if r[0] in ('HALT','NONE'): res.append(r); continue
            res.append((r[0],r[2],2*r[1]-3*n))
        if len(set(res))!=1:
            T[(w,par)]=('INCONSISTENT',res); continue
        r=res[0]; T[(w,par)]=r
        if r[0] not in ('HALT','NONE'):
            nw=(r[0],r[1])
            if nw not in seen: seen.add(nw); todo.append(nw)
for (w,par),r in T.items(): print(repr(w[0]),repr(w[1]),par,'->',r)
print('words',len(seen),'entries',len(T),'open',len(todo))
