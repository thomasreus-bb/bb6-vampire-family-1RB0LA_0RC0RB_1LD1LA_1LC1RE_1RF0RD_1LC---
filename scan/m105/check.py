# compare the level iteration with direct simulation (ev): M STATE PREFIX m a STEPS
import sys,subprocess,glev
M,st,pre,m,a,steps=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),int(sys.argv[5]),sys.argv[6]
out=subprocess.run(['./ev',M,st,steps],capture_output=True,text=True).stdout.split('\n')
ref=[]
for l in out:
    f=l.split()
    if len(f)==2 and f[1].startswith(pre) and len(f[1])>len(pre) and f[1][len(pre)]=='1' and '+' not in f[1]:
        x=f[1][len(pre):]; k=len(x)-len(x.lstrip('1')); ref.append((k,x[k:]))
g=glev.G(M,st,pre,m,a)
n,W=ref[0]; bad=0
for i in range(1,len(ref)):
    n,W=g.level(n,W)
    if (n,W)!=ref[i]: bad+=1; print('diff',i,(n,W),ref[i])
print('levels compared',len(ref)-1,'bad',bad)
