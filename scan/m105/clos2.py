# breadth-first closure of the tails of no. 105 under all residues, up to depth D; print the tails as entry lists
import glev,pickle,sys
g=glev.G('1RB1LF_1LC0RD_---1LA_0LA0RE_1LA1RA_1LB0LD','A','001110',3,4)
try: g.TAB=pickle.load(open('tab105.pkl','rb'))
except Exception: pass
f=lambda W: '.'.join(map(str,glev.tails(W))) or 'e'
D=int(sys.argv[1]); front={'011'}; seen=set(front)
for d in range(D):
    new=set()
    for W in front:
        for r in range(3):
            e,W2=g.entry(r,W)
            if W2 not in seen: seen.add(W2); new.add(W2)
    front=new
    print('depth',d+1,'new',len(new),'total',len(seen),flush=True)
pickle.dump(g.TAB,open('tab105.pkl','wb'))
for W in sorted(seen,key=lambda w:(len(glev.tails(w)),w)): print(f(W))
