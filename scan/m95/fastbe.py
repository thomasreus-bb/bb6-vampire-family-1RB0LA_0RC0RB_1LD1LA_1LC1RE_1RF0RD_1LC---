import sys,time
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import fast
M=sys.argv[1]; N=int(sys.argv[2])
st={'prev':False}
def fmt(out): return ' '.join(w if c==1 else '(%s)^%d'%(w,c) for w,c in out)
def rep(S,out):
    has=any(len(w)>=7 and c>=2 for w,c in out)
    if has!=st['prev']:
        print('B' if has else 'E', S.steps, fmt(out)[:600], flush=True)
    st['prev']=has
t0=time.time()
S=fast.run(M,N,int(sys.argv[3]) if len(sys.argv)>3 else 9,rep)
print('end',S.steps,S.halted,round(time.time()-t0,1))
