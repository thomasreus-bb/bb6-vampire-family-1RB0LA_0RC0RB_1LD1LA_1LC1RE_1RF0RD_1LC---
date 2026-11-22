import subprocess,collections,itertools
from fractions import Fraction as Fr
def run(a,b): 
    r=subprocess.run(['./ab2',str(a),str(b),'3000000000'],capture_output=True,text=True).stdout.split()
    return (r[0],)+tuple(int(x) for x in r[1:-1]) if r[0] in 'AB' else (r[0],)
def solve(rows):  # fit out = x*a + y*b + z exactly
    import itertools
    for r1,r2,r3 in itertools.combinations(rows,3):
        A=[[Fr(r1[0]),Fr(r1[1]),1],[Fr(r2[0]),Fr(r2[1]),1],[Fr(r3[0]),Fr(r3[1]),1]]; Y=[Fr(r1[2]),Fr(r2[2]),Fr(r3[2])]
        import copy
        M=[A[i]+[Y[i]] for i in range(3)]
        try:
            for c in range(3):
                piv=next(i for i in range(c,3) if M[i][c]!=0); M[c],M[piv]=M[piv],M[c]
                for i in range(3):
                    if i!=c and M[i][c]!=0:
                        f=M[i][c]/M[c][c]; M[i]=[M[i][j]-f*M[c][j] for j in range(4)]
            sol=[M[i][3]/M[i][i] for i in range(3)]
        except StopIteration: continue
        if all(sol[0]*r[0]+sol[1]*r[1]+sol[2]==r[2] for r in rows): return sol
    return None
for k in range(2,8):
    As=[2**k*m-3 for m in (3,5,7,9,11) if 2**k*m-3<700]
    groups=collections.defaultdict(list)
    for a in As:
        for b in range(1,11):
            o=run(a,b)
            groups[(b%2,o[0])].append((a,b,o))
    print('k=%d (a+3 = 2^%d * odd), a in %s'%(k,k,As))
    for key,rows in sorted(groups.items()):
        if key[1]=='A':
            f=solve([(a,b,o[1]) for a,b,o in rows]); print('   b %s -> A: a\' = %s'%('even' if key[0]==0 else 'odd', f and '%s*a + %s*b + %s'%tuple(f)), len(rows))
        elif key[1]=='B':
            f1=solve([(a,b,o[1]) for a,b,o in rows]); f2=solve([(a,b,o[2]) for a,b,o in rows])
            print('   b %s -> B: a\' = %s ; b\' = %s'%('even' if key[0]==0 else 'odd', f1 and '%s*a + %s*b + %s'%tuple(f1), f2 and '%s*a + %s*b + %s'%tuple(f2)), len(rows))
        else: print('   ',key,len(rows))
