# construct the smallest n0 whose level residues follow a given path (exact level map), then iterate it
import glev,pickle,markov,sys
g=glev.G('1RB1LF_1LC0RD_---1LA_0LA0RE_1LA1RA_1LB0LD','A','001110',3,4)
g.TAB=pickle.load(open('tab105.pkl','rb'))
path=[int(c) for c in sys.argv[1]]; W0=sys.argv[2]; qmin=int(sys.argv[3])
# n0 = A t + B; keep the list of level maps to apply symbolically
Ws=[W0]; es=[]
W=W0
for r in path[:-1]:
    e,W2=markov.entry_safe(g,r,W); es.append(e); W=W2; Ws.append(W)
A,B=1,0
# represent n_i = A_i t + B_i in terms of the same t; constraints n_i = r_i mod 3 restrict t
cur=(1,0)  # n_i = a t + b
subs=[]   # t = 3 t' + t0 substitutions applied globally
def apply_sub(ab,s):
    a,b=ab; t0=s; return (3*a, a*t0+b)
lin=[(1,0)]
for i,r in enumerate(path):
    a,b=lin[-1]
    # solve a t + b = r mod 3
    t0=next(x for x in range(3) if (a*x+b-r)%3==0)
    lin=[apply_sub(x,t0) for x in lin]
    a,b=lin[-1]
    if i<len(path)-1:
        # n_{i+1} = 4 (n_i - r)/3 + e
        assert (a%3==0) and ((b-r)%3==0)
        lin.append((4*a//3, 4*(b-r)//3+es[i]))
a0,b0=lin[0]
n0=b0
while n0//3 < len(W0)+qmin: n0+=a0
print('n0 =',n0, 'period',a0)
n,W=n0,W0
for i,r in enumerate(path):
    assert n%3==r,(i,n%3,r)
    q,rr=divmod(n,3)
    e,W2=markov.entry_safe(g,rr,W)
    if W2 is None: print('HALT in level',i+1,'n=%d tail=%s'%(n,W)); break
    n,W=4*q+e,W2
