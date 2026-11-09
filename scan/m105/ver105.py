# independent check with the accelerated simulator: P(n0, 011) of no. 105 should halt after 35 levels
import os,sys
os.environ['TM']='1RB1LF_1LC0RD_---1LA_0LA0RE_1LA1RA_1LB0LD'; os.environ.setdefault('BS48','40')
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from build import make
n0=int(sys.argv[1])
s=make([(0,2),(1,3),(0,1),(1,n0),(0,1),(1,2)],0)
r=s.run(10**int(sys.argv[2]))
print(r,s.halt,s.steps)
