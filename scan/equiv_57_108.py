# usage: gcc -O2 -o meet meet.c; python3 equiv_57_108.py candidates_108.txt 20000000 200000000
import itertools,subprocess,sys
exec(open("groups.py").read().split("L=[l.split()[1]")[0])
L=[l.split()[1] for l in open(sys.argv[1]) if not l.startswith("#")]
N1,N2=sys.argv[2],sys.argv[3]
groups=[(44,81),(44,89),(44,96),(51,61),(51,71),(51,93),(58,68),(72,73),(72,97),(74,77),(75,106),(76,99),(78,79),(78,92),(80,91),(80,108),(94,103),(81,89),(81,96),(89,96),(61,71),(61,93),(71,93),(73,97),(79,92),(91,108)]
for g in groups:
    for i,j in itertools.combinations(g,2):
        X,Y=L[i-1],L[j-1]; TY=parse(Y); found=None
        for perm in itertools.permutations(range(6)):
            for mir in (0,1):
                if transform(TY,perm,mir)==X: found=(perm,mir); break
            if found: break
        perm,mir=found; Q="ABCDEF"[perm[0]]
        out=subprocess.run(["./meet",X,Q,N1,N2],capture_output=True,text=True).stdout.strip().replace("\n"," | ")
        print("no. %d / no. %d: no. %d = no. %d %s, started in %s  ->  %s"%(i,j,j,i,"mirrored" if mir else "(not mirrored)",Q,out),flush=True)
