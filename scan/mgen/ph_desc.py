import sys
import os
from msim import BS
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'comp.py')).read().split('for l in sys.stdin')[0])
def per(b):
    s=''.join(map(str,b))
    for L in range(1,len(s)+1):
        if len(s)%L==0 and s==s[:L]*(len(s)//L): return s[:L]
def describe(t,p,R):
    toks=[]; cur=''.join(map(str,t[p:]))
    for b,n in reversed(R):
        if n>3:
            if cur: toks.append(comp(cur)); cur=''
            u=per(b); toks.append('[%s]^%d'%(u,n*BS//len(u)))
        else: cur+=''.join(map(str,b))*n
    if cur: toks.append(comp(cur.rstrip('0')) if cur.rstrip('0') else '')
    s=' '.join(x for x in toks if x)
    return s
