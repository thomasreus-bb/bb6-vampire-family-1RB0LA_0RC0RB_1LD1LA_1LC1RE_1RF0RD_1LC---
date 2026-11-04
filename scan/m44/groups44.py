#!/usr/bin/env python3
"""No. 44: brute force over memory words made of groups [1^a, k] (a ones-blocks, then a block k).
Reports any HALT or undecided class. (The carry check below is a first guess that only covers the T = [] case;
see bell_candidates.md no. 44 for the rules found: a >= 3, T non-empty: [1^a,2]+T -> [1^6,2a-6]+rule2(T).)
Old guess:
  [1^a, 2] + T  ->  [1^6, 2(a + a_T) - 10] + (m=2 rule applied to T)   for a + a_T >= 5,
where a_T is the number of leading 1-blocks of T and the m=2 rule on T is the usual one."""
import itertools, sys, rmodel51 as R
def enc(bl): return ''.join('0'+'1'*k for k in bl)
def dec(r): return [] if r=='' else [len(p) for p in r[1:].split('0')]
A=int(sys.argv[1]) if len(sys.argv)>1 else 6; K=int(sys.argv[2]) if len(sys.argv)>2 else 6; NG=int(sys.argv[3]) if len(sys.argv)>3 else 3
cache={}
def rule2(bl):
    r=enc(bl)
    if r not in cache: cache[r]=R.rules(r)
    for mod,c,l in cache[r]:
        if mod==3 and c==2: return dec(l[1]) if l[0]=='C' else l[0]
    return '?'
special=[]; carry_ok=carry_bad=0; n=0
groups=[[1]*a+[k] for a in range(A+1) for k in range(2,K+1)]
for g in range(1,NG+1):
    for combo in itertools.product(groups,repeat=g):
        bl=[x for grp in combo for x in grp]; n+=1
        r=enc(bl)
        if r not in cache: cache[r]=R.rules(r)
        for mod,c,l in cache[r]:
            if l[0]!='C': special.append((bl,mod,c,l[0]))
        # carry rule check
        if bl and combo[0][-1]==2 and g>=1:
            a=len(combo[0])-1; T=[x for grp in combo[1:] for x in grp]
            aT=0
            while aT<len(T) and T[aT]==1: aT+=1
            if a+aT>=5:
                exp=[1]*6+[2*(a+aT)-10]; tt=rule2(T)
                if isinstance(tt,list):
                    exp=exp+tt
                    got=rule2(bl)
                    # normalise: a 0 block at the very end is dropped by the tape
                    while exp and exp[-1]==0: exp.pop()
                    if got==exp: carry_ok+=1
                    else: carry_bad+=1; print('carry mismatch',bl,got,exp) if carry_bad<10 else None
print('words',n,'HALT/undecided classes',len(special),special[:10])
print('k=2 carry rule: ok',carry_ok,'mismatch',carry_bad)
