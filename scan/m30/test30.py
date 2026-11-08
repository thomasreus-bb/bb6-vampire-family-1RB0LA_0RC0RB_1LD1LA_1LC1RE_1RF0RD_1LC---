# compare the recursion G with the direct simulation results of f30 (files f30_*.txt)
import glob,sys
import g30
bad=n=0
for fn in sorted(glob.glob('f30_*.txt')):
    for l in open(fn):
        f=l.split(); k=int(f[0])
        g30.active.clear()
        try: want=str(g30.G(k))
        except g30.Halt: want='HALT'
        except g30.Loop: want='MAX'
        got=f[1]; n+=1
        if want!=got: bad+=1; print('MISMATCH',k,want,got)
print(n,'values,',bad,'mismatches')
