# statistics of the tail entries along the exact level sequence of no. 25
import pickle,lev,math,collections,sys
lev.TAB=pickle.load(open('tab.pkl','rb'))
n,W='3','011'; n=3
K=int(sys.argv[1]); H=collections.Counter(); Hl=collections.Counter(); R=collections.Counter(); mx=0
for i in range(K):
    n,W=lev.level(n,W)
    ks=[len(x) for x in W.split('0') if x]
    k=max(ks) if ks else 0
    H[k]+=1; Hl[len(ks)]+=1; R[n%3]+=1; mx=max(mx,k)
    if i==999: n1000=n
print('levels',K,'log10 n = %.1f'%math.log10(n),'max k',mx,'table',len(lev.TAB))
print('residues',dict(R)); print('number of tail entries',dict(Hl))
tot=sum(H.values()); acc=0
for k in sorted(H,reverse=True):
    acc+=H[k]
    print('k>=%d: %.3g'%(k,acc/tot))
pickle.dump(lev.TAB,open('tab.pkl','wb'))
