# Event rules of no. 42 and their check against direct simulation (ev42).
# Events: state A, head on a new leftmost cell. X(a,b): tape (10)^a 1^b.  Z(c,e): tape 00 (10)^c 1^e.
# M(c,e): tape (10)^3 11 0 (10)^c 1^e (reached from Z(c,e) after two events).
import subprocess,random
def D(k): return 6*3**k-1
def A(k): return 3**(k+1)-3-k
def X2(a):
    """X(a,2) -> next event, closed formula"""
    k=0
    while A(k+1)<=a: k+=1
    j=a-A(k); Dk=D(k)
    if j==0: return ('X',1,Dk)            # a = A(k): reset
    i=(j-1)//2
    if j%2==1: return ('Z',2+3*i,Dk-2-2*i)
    return ('X',4+3*i,Dk-2-2*i)
def rule(ev):
    t,x,y=ev
    if t=='X':
        if y>=3: return ('X',x+2,y-2)
        if y==1: return ('X',1,2*x+6)
        if y==2: return X2(x)
    if t=='M' and x%2==1 and y>=2: return ('X',x+6,y-1)
    return None
def batch(evs):
    inp=''.join('%s %d %d\n'%e for e in evs)
    out=subprocess.run(['./ev42'],input=inp,capture_output=True,text=True).stdout.strip().split('\n')
    res=[]
    for l in out:
        f=l.split()
        res.append(('HALT',) if f[0]=='HALT' else (f[0],int(f[1]),int(f[2])) if f[0] in 'XZ' else (f[0],))
    return res
if __name__=='__main__':
    rnd=random.Random(1)
    tests=[('X',a,b) for a in range(1,60) for b in range(1,40)]
    tests+=[('X',a,2) for a in range(1,3000)]
    tests+=[('X',rnd.randrange(1,20000),rnd.choice([1,2,3,4,rnd.randrange(3,20000)])) for _ in range(300)]
    tests+=[('M',c,e) for c in range(1,80,2) for e in range(2,60)]
    tests+=[('M',2*rnd.randrange(0,5000)+1,rnd.randrange(2,10000)) for _ in range(200)]
    res=batch(tests); bad=0
    for ev,r in zip(tests,res):
        if rule(ev)!=r: bad+=1; print('differs',ev,rule(ev),r)
    print(len(tests),'cases,',bad,'differ')
