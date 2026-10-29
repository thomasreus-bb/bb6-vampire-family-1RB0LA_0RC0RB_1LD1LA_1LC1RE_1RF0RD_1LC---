import itertools,subprocess,sys
exec(open("groups.py").read().split("L=[l.split()[1]")[0])
L=[l.split()[1] for l in open(sys.argv[1]) if not l.startswith("#")]
N1,N2=sys.argv[2],sys.argv[3]
groups=[(1,2,5),(3,7),(4,6),(11,37),(19,20,39),(22,42,43),(26,31,32),(45,52),(46,54)]
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
