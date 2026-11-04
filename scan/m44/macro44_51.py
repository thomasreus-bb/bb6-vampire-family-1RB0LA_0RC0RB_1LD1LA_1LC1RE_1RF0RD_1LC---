#!/usr/bin/env python3
"""Macro iteration for nos. 44 and 51 with the rules found on 4 Nov 2026 (checked by nxt.c on small values).
A(x,y): head left of the tape in state A;  Bell(n): head right of the tape in state B.
  no. 44: A(x,y) = [0] (10)^x 1^y,   Bell(n) = (10)^n 1 [0]
  no. 51: A(x,y) = [0] 1 (10)^x 1^y, Bell(n) = 1 (10)^n 1 [0]
Iterates until a case without a known rule (y = 2 with an irregular residue of x)."""
import sys
sys.set_int_max_str_digits(0)
def A44(x,y):
    L=max(0,(y-2)//3); x+=5*L; y-=3*L          # loop (x+5, y-3) while y >= 4  (y ends in 1..3, or 0)
    if y>=4: x+=5; y-=3
    if y==3: return ('B',x+5)
    if y==1: return ('B',x+1)
    if y==0: return ('B',x)
    if x%3==0: return ('A',10*x//3-12,4)
    if x%9==7: return ('A',100*(x-7)//9+32,4)
    return ('?',x,y)
def A51(x,y):
    L=max(0,(y-2)//3); x+=4*L; y-=3*L
    if y>=4: x+=4; y-=3
    if y==3: return ('B',x+4)
    if y==1: return ('B',x+1)
    if y==0: return ('B',x)
    if x%3==0: return ('A',3,16*x//3+5)
    if x%3==2: return ('A',8*(x-2)//3+4,6)
    if x%9==7: return ('A',64*(x-7)//9+46,3)
    return ('?',x,y)
def orbit(which,maxb=10**6):
    A,start,bell=(A44,6,lambda n:(1,2*n+3)) if which=='44' else (A51,3,lambda n:(3,2*n+1))
    n=start; bells=[n]; ev=[]
    st=('A',)+bell(n)
    while len(bells)<maxb:
        r=A(st[1],st[2])
        if r[0]=='B': n=r[1]; bells.append(n); st=('A',)+bell(n)
        elif r[0]=='A': ev.append((len(bells),'sub')); st=r
        else: return bells,ev,r
    return bells,ev,None
if __name__=='__main__':
    for w in ('44','51'):
        b,ev,stop=orbit(w)
        print('no.',w,':',len(b),'Bells, last n has',len(str(b[-1])),'digits; sub-runs after Bells',[e[0] for e in ev][:20])
        print('   stop:', stop[0], 'x mod 9 =', stop[1]%9, 'y =', stop[2], 'x has', len(str(stop[1])),'digits' if stop else '')
