#!/usr/bin/env python3
"""No. 51 with the memory word r: C(m, r) = [0] 10 1^m r, state A (head left of the tape).
For each r and residue class of m, find r' and the affine law m' = (a*m + b) by sampling,
refining the modulus 3, 9, 27, ... when r' or the law is not constant on a class."""
import ctypes, sys, os
L=ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)),'clib.so'))
M=b'1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---'; L.setup(M)
L.cstep.argtypes=[ctypes.c_long,ctypes.c_char_p,ctypes.c_longlong,ctypes.c_long,ctypes.POINTER(ctypes.c_long),ctypes.c_char_p,ctypes.POINTER(ctypes.c_longlong)]
def step(m,r,mx=200000000):
    mo=ctypes.c_long(); ro=ctypes.create_string_buffer(512); st=ctypes.c_longlong()
    k=L.cstep(m,r.encode(),mx,4,ctypes.byref(mo),ro,ctypes.byref(st))
    return (['MAX','C','HALT'][k], mo.value, ro.value.decode(), st.value)
def law(r, mod, res, base=40):
    """samples m = res (mod mod), m >= base; returns ('C', r', a, b) with m' = (a m + b)/den exact, or ('HALT',..) or None"""
    ms=[]; m=res
    while m<base: m+=mod
    for j in range(4): ms.append(m+j*mod)
    out=[step(x,r) for x in ms]
    if all(o[0]=='HALT' for o in out): return ('HALT',)
    if any(o[0]!='C' for o in out) or len({o[2] for o in out})>1: return None
    y=[o[1] for o in out]
    d=[y[i+1]-y[i] for i in range(3)]
    if len(set(d))>1: return None
    slope=(d[0], mod)          # m' increases by d[0] per mod
    return ('C', out[0][2], slope, (ms[0], y[0]))
def rules(r, maxmod=3**6):
    """list of (mod, res, rule)"""
    todo=[(3,0),(3,1),(3,2)]; res=[]
    while todo:
        mod,c=todo.pop(0)
        l=law(r,mod,c)
        if l is None:
            if mod*3>maxmod: res.append((mod,c,('?',)))
            else: todo+= [(mod*3,c+mod*i) for i in range(3)]
        else: res.append((mod,c,l))
    return res
if __name__=='__main__':
    r=sys.argv[1] if len(sys.argv)>1 else ''
    for x in rules(r): print(x)
