# phase starts of no. 88 (mirrored): head at the left end, short prefix, then the long zero gap; print once per phase
import os as _o,sys as _s; _s.path.insert(0,_o.path.join(_o.path.dirname(_o.path.abspath(__file__)),'..','mgen'))
import sys,os,math,re
os.environ['TM']='1RB0LE_1RC0RF_0RD0RB_1RE0RC_1LA0LA_1RA---'.translate(str.maketrans('LR','RL'))
from msim import Sim,BS
from ph_desc import describe
last=[None]
def cb(s):
    d=describe([],0,s.R)
    if '[0]^' not in d: return
    pre,rest=d.split('[0]^',1)
    if '[' in pre or len(pre)>60: return
    g,far=rest.split(' ',1) if ' ' in rest else (rest,'')
    if far==last[0]: return
    last[0]=far
    print('PH %.4f %s | %s| [0]^%s | %s'%(math.log10(max(s.steps,1)),chr(65+s.q),pre,g,far[:int(os.environ.get('MAXC','500'))]),flush=True)
s=Sim()
print(s.run(10**int(os.environ.get('CAPEXP','60')),cb), s.steps, s.halt)
