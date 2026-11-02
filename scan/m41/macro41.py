#!/usr/bin/env python3
"""Macro model of no. 41 (1RB1LD_1RC0RA_1LA1RE_0LA0LB_0RB1RF_---1RD).
Regimes (configuration at a turn of the head, see bell_candidates.md):
  P1(a,b,c): (1)^a [0](10)^b (1)^c        state B  round: (a+3, b-1, c-1)
  P2(a,b,c): (1)^a 0[0](10)^b (1)^c       state A  round: (a-3, b+2, c-1)
  P3(a,b,c): (1)^a 0(01)^b 1[0](1)^c      state C  round: (a, b-1, c+2)
  Q (a,b,c): (1)^a (01)^b 1[0](1)^c       state C  round: (a, b-1, c+2)   (= P3 without separator 0)
  A (x,y):   [0](01)^x (1)^y              state B  sweep: (x+2, y-1)
Exits:
  P1: b=0 -> P2(a+3, 0, c-4);  c=1 -> P3(a+2, b-1, 2)
  P2: a=0 -> P1(1, b+1, c-1);  a=1 -> P1(1, b+2, c-1);  a=2 -> A(b+3, c-2);  c=1 -> Q(a, b+1, 2)
  P3: b=0 -> P2(a-3, 1, c+2)
  Q : b=0 -> P2(a-2, 0, c+2)
  A : y=0 -> Bell n = x+1 -> Q(2, n-1, 2)
"""
import sys
def run(n0, nbells, trace=False):
    reg, s = 'Q', (2, n0-1, 2)
    bells=[n0]; log=[]; cyc=[]
    it=0
    while len(bells) < nbells:
        it+=1
        if it>200000: raise Exception("loop "+reg+str(s))
        if trace and it<0: print(reg,s)
        if min(s)<0: raise Exception("neg "+reg+str(s))
        a = s
        if trace: cyc.append((reg, s))
        if reg == 'P1':
            a,b,c = s; k = min(b, c-1)
            a,b,c = a+3*k, b-k, c-k
            if b == 0: reg, s = 'P2', (a+3, 0, c-4)
            elif c == 1: reg, s = 'P3', (a+2, b-1, 2)
            else: raise Exception('P1 '+str(s))
        elif reg == 'P2':
            a,b,c = s
            ka = max(0, -(-(a-2)//3)); kc = c-1; k = min(ka, kc)
            a,b,c = a-3*k, b+2*k, c-k
            if a <= 2:
                if a == 0: reg, s = 'P1', (1, b+1, c-1)
                elif a == 1: reg, s = 'P1', (1, b+2, c-1)
                else: reg, s = 'A', (b+3, c-2)
            elif c == 1: reg, s = 'Q', (a, b+1, 2)
            else: raise Exception('P2 '+str(s))
        elif reg in ('P3', 'Q'):
            a,b,c = s
            c += 2*b; b = 0
            reg, s = ('P2', (a-3, 1, c)) if reg == 'P3' else ('P2', (a-2, 0, c))
            # note: c already includes +2 per round; exit adds +2
            s = (s[0], s[1], s[2]+2)
        elif reg == 'A':
            x,y = s; n = x+2*y+1
            if trace: log.append(cyc); cyc=[]
            bells.append(n); reg, s = 'Q', (2, n-1, 2)
    return bells, log
if __name__ == '__main__':
    bells, log = run(8, int(sys.argv[1]) if len(sys.argv)>1 else 20, trace=True)
    print(bells)
