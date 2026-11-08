# watch the arguments inside the slow evaluation of G at orbit step 697 (no. 30)
import sys,time
sys.set_int_max_str_digits(0)
import g30
n=1
for k in range(697): n=g30.G(n)
print('start: log10 n=%.1f'%(n.bit_length()*.30103),flush=True)
calls=0;stack=[];t0=time.time()
while True:
    calls+=1
    while n%2==0:
        stack.append([n,0]); n=n//2-2
    v=(3*n+7)//2
    if calls%100000==0: print('calls',calls,'depth',len(stack),'log10 arg %.1f'%(n.bit_length()*.30103),'stack stage1 frames',sum(f[1] for f in stack),'%.0fs'%(time.time()-t0),flush=True)
    if time.time()-t0>40: break
    while stack:
        f=stack[-1]
        if f[1]==0: f[1]=1; n=1+v; break
        stack.pop(); v=f[0]+v
    else: print('done'); break
