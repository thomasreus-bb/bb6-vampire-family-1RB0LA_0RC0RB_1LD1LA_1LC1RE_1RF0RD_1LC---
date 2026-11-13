"""First macro configuration C(m, r) = [0] 10 1^m r (state A, head on the blank left of the tape) of the table of
no. 51 started on the blank tape in state Q.  usage: python3 first51.py Q [KMIN]"""
import sys
M='1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---'
T={}
for i,g in enumerate(M.split('_')):
    for b in (0,1):
        x=g[3*b:3*b+3]; T[(i,b)]=None if x[0]=='-' else (int(x[0]),1 if x[1]=='R' else -1,ord(x[2])-65)
q=ord(sys.argv[1])-65; KMIN=int(sys.argv[2]) if len(sys.argv)>2 else 4
t={}; h=0; lo=0; hi=0
for n in range(1,10**7):
    tr=T[(q,t.get(h,0))]
    if tr is None: print('HALT',n); break
    t[h],d,q=tr; h+=d; hi=max(hi,h)
    if h<lo:
        lo=h
        if q==0:
            a=h+1
            while a<=hi and not t.get(a,0): a+=1
            z=hi
            while z>=a and not t.get(z,0): z-=1
            if a<z and t.get(a,0)==1 and t.get(a+1,0)==0:
                p=a+2; k=0
                while p<=z and t.get(p,0)==1: k+=1; p+=1
                if k>=KMIN and (p>z or (t.get(p,0)==0 and z-p+1<=64)):
                    print('C',k,''.join(str(t.get(i,0)) for i in range(p,z+1)) or '-',n); break
