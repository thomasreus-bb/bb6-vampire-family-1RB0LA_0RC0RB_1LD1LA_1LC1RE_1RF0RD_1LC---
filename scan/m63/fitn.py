import sys
ev=[]
for l in sys.stdin:
    f=l.split(); bl=[int(x) for x in f[1:] if not x.startswith('|')]
    if len(bl)<3: continue
    k=0
    while 2+k<len(bl) and bl[2+k]==1: k+=1
    ev.append((int(f[0][1:-1]),bl[0],bl[1],k,tuple(bl[2+k:])))
for i in range(len(ev)-1):
    s,f,n,k,t=ev[i]; s2,f2,n2,k2,t2=ev[i+1]
    if n>30 and n2>n: print(f,'n mod 2 =',n%2,'->',f2,'  2n2-3n =',2*n2-3*n,' dk',k2-k, t, t2 if t2!=t else '')
