# iterate n -> G(n) for no. 30 with exact integers; print a line every EVERY orbit steps
import sys,time,math
sys.set_int_max_str_digits(0)
import g30
lim=int(sys.argv[1]); every=int(sys.argv[2]); tmax=float(sys.argv[3]) if len(sys.argv)>3 else 1e9
n=1; t0=time.time(); evens=0; maxdepth=0
for k in range(lim):
    if n%2==0: evens+=1
    try: m=g30.G(n)
    except g30.Halt: print('HALT at orbit step',k); break
    except g30.Loop as e: print('LOOP at orbit step',k); break
    if k%every==0 or time.time()-t0>tmax:
        print(k,'log10 n = %.1f'%(n.bit_length()*math.log10(2)),'calls',g30.calls,'even values',evens,'%.1f s'%(time.time()-t0),flush=True)
        if time.time()-t0>tmax: break
    n=m
print('END orbit step',k,'log10 n = %.1f'%(n.bit_length()*math.log10(2)))
