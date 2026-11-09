# parse a phase description into a run-length list [(bit,count),...]
import re
def toks_to_rl(s):
    rl=[]
    def add(b,n):
        if n==0: return
        if rl and rl[-1][0]==b: rl[-1]=(b,rl[-1][1]+n)
        else: rl.append((b,n))
    for t in s.split():
        if t=='|': continue
        m=re.fullmatch(r'[\(\[]?([01]+)[\)\]]?\^(\d+)',t)
        if m:
            u,k=m.group(1),int(m.group(2))
            if len(set(u))==1: add(int(u[0]),len(u)*k)
            else:
                if k>100000: raise ValueError('long periodic run '+t)
                for _ in range(k):
                    for c in u: add(int(c),1)
        elif re.fullmatch(r'[01]+',t):
            for c in t: add(int(c),1)
        else: raise ValueError(t)
    return rl
