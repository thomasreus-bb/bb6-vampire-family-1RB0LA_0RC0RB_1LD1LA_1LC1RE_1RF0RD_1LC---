import sys; sys.path.insert(0,'.')
import fast38 as F
j,X=121,1; seq=[]
for L in range(150000):
    k=0
    if X==1:
        while True:
            if k>=len(F.DELTA): print('>30 bells at level',L); sys.exit()
            cont=j%4 in F.CONT[k]; j=(5*j+F.DELTA[k]+(1 if j%2==0 else 0))//2; k+=1
            if not cont: break
    seq.append(k)
    if F.is_halt_end(j): print('HALT',L); sys.exit()
    X=1 if j%4 in (0,1) else 0
    j=j//2-3 if j%2==0 else (j-7)//2
t=seq[-6000:]
per=[p for p in range(1,2000) if all(t[i]==t[i+p] for i in range(len(t)-p))]
print('levels',len(seq),'max bells',max(seq),'eventual period in last 6000 levels:',per[:3])
