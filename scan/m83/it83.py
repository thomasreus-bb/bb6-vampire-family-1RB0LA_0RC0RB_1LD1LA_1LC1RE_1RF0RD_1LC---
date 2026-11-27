import sys,re; sys.path.insert(0,'/tmp/an83'); from mac83 import *
def rl(t): return ' '.join(m.group(0)[0]+str(len(m.group(0))) for m in re.finditer(r'0+|1+',t))
def step(N,r,S,mod=96,base=10):
    Nr = N if N<3000 else (N%mod)+mod*base
    res=sweep(Nr,r,S)
    if res[0]!='OK': return None
    z=N-1; S2=res[2].rstrip('0')
    return 6*(z//4)+3, (1 if z%4==0 else 3), S2
