import sys; sys.path.insert(0,'/tmp/an83')
from sym import Lin, L, Halt, Touched, NeedSplit
import symbell
def show(e): return str(e)
rows=[
 ('r=1, g=4', 1, [L(30,a=2), L(4), L(30,b=2)]),
 ('r=1, g>=6', 1, [L(30,a=2), L(30,g=2), L(30,b=2)]),
 ('r=3, g=4', 3, [L(30,a=2), L(4), L(30,b=2)]),
 ('r=3, g>=6', 3, [L(30,a=2), L(30,g=2), L(30,b=2)]),
 ('r=1, g=2, a=2 mod 4, b=2 mod 4', 1, [L(30,a=4), L(2), L(30,b=4), L(30,h=2), L(6)]),
 ('r=1, g=2, a=2 mod 4, b=0 mod 4', 1, [L(30,a=4), L(2), L(32,b=4), L(30,h=2), L(6)]),
 ('r=1, g=2, a=0 mod 4', 1, [L(32,a=4), L(2), L(30,b=2), L(30,h=2), L(6)]),
 ('r=3, g=2, a even, b=2 mod 4', 3, [L(30,a=2), L(2), L(30,b=4), L(30,h=2), L(6)]),
 ('r=3, g=2, a even, b=0 mod 4', 3, [L(30,a=2), L(2), L(32,b=4), L(30,h=2), L(6)]),
 ('r=2, g>=5 odd', 2, [L(30,a=2), L(31,g=2), L(30,b=2)]),
 ('r=2, g=1', 2, [L(30,a=2), L(1), L(30,b=2)]),
]
for name,r,runs in rows:
    for c0 in (101,103):
        try:
            M,r2,out=symbell.symbell(L(c0,n=4),r,runs)
            print(f"{name:34s} N=4n+{c0}: S={' '.join(w+'^('+show(e)+')' for w,e in [('1' if i%2==0 else '0',x) for i,x in enumerate(runs)])} -> N'={M}, r'={r2}, S'={' '.join(w+'^('+show(e)+')' for w,e in out)} T")
        except Exception as ex:
            print(f"{name:34s} N=4n+{c0}: {type(ex).__name__} {ex}")
