# conjectured exact map for 1RB0LF_1LC1RA_0RE0RD_---1LE_1LF1RC_1LC1LA, at left extensions in state C:
# tape (01)^m 1^r
import sys,collections
def cycle(R):
    # start (m=1, r=R)
    m,r=1,R; ev=[(m,r)]
    while r>=2*m: r-=2*m; m=2*m+1; ev.append((m,r))
    j=0
    X=3*m+(r+1)//2
    while True:
        j+=1
        if X%2==0: m=X//2; r=0; ev.append((m,r)); return m,j,ev
        m=(X-1)//2; r=2; ev.append((m,r))
        X=3*m+3
if __name__=="__main__":
    # check against the simulation list
    sim=[tuple(int(x.split('=')[1]) for x in l.split()[2:4]) for l in open("ev14.txt") if l.startswith(tuple("0123456789")) and "m=" in l]
    # start from the first cycle start in sim with m=1 and large r
    idx=[i for i,(m,r) in enumerate(sim) if m==1 and r>20][0]
    R=sim[idx][1]; pred=[]
    for c in range(12):
        me,j,ev=cycle(R); pred+=ev; R=2*me+1
    ok=all(a==b for a,b in zip(sim[idx:],pred)); print("map reproduces simulation events:",ok,len(sim)-idx)
    for a,b in zip(sim[idx:],pred):
        if a!=b: print("diff",a,b); break
