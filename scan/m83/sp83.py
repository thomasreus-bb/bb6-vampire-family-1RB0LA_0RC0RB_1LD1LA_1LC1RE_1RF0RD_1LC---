import sys; sys.path.insert(0,'/tmp/an83')
from sym import *
TM='1LB1LA_1RC0LB_1RD0RB_1LA0RE_---1RF_1RB0RA'
def run_until_left_record(cfg, states, maxsteps=100000):
    s=Sim(TM); k=[0]
    def stop(Ls,q,Rs,d):
        k[0]+=1
        return k[0]>1 and q in states and d=='L' and Ls==[ZEROS]
    return s.run(cfg,maxsteps,stop), s.steps
for m0 in range(0,25):
    start=([ZEROS],'A',norm([('1',L(m0,x=2)),('0',L(4,z=1)),REST]),'L')
    try:
        out,st=run_until_left_record(start,'A')
        print(m0,'->',out[1],out[2],'steps',st)
    except Exception as e: print(m0,'fail',type(e).__name__, e)
