#!/usr/bin/env python3
"""Statistics of the left records of no. 35 (output of sim35): right-phase starts (a = 1 mod 3),
s = a + 3b, total number of ones T, near misses (small s)."""
import sys, math
rows=[]
for line in open(sys.argv[1]):
    if not line.startswith('L '): continue
    p=line.split(); step=int(p[1]); rest=line.split(': ',1)[1].split()
    if '|' not in rest: continue
    i=rest.index('|'); a=int(rest[i-1]) if i>0 else 0
    lst=[int(x) for x in rest[i+1:] if x.isdigit()]
    rows.append((step,a,lst))
starts=[(st,a,l) for st,a,l in rows if a%3==1 and l]
print('left records',len(rows),' right-phase starts (a = 1 mod 3):',len(starts))
# s values and normalised
near=[]; K=0
for st,a,l in starts:
    K+=1; T=a+sum(l); s=a+3*l[0]
    near.append((s,K,st,a,l[0],T))
near.sort()
print('smallest s = a+3b at right-phase starts:')
for s,K,st,a,b,T in near[:15]: print('  s=%d  (a=%d, b=%d)  start no. %d  step %.3e  T=%d  s/T=%.2e'%(s,a,b,K,st,T,s/T))
# growth of T with K
for frac in (0.01,0.1,0.3,1.0):
    idx=int(frac*len(starts))-1; st,a,l=starts[idx]; print('  K=%d  step=%.3e  T=%d  list length %d'%(idx+1,st,a+sum(l),len(l)))
# distribution of s/T
import collections
h=collections.Counter(min(9,int(10*(a+3*l[0])/(a+sum(l)+2*l[0]))) for st,a,l in starts)
print('histogram of s/(T+2b) in tenths:',[h[i] for i in range(10)])
