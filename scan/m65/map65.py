# exact rules of no. 65 (mirrored; A-event tape (01)^a 1^b), derived from direct simulation:
#   b >= 4: (a, b) -> (floor((3a+8)/2), b-4)
#   b = 3:  (a, 3) -> (floor((3a+6)/2), 0)
#   b = 2:  (a, 2) -> (2, 3a+3-(a mod 2))
#   b = 1:  HALT
#   b = 0:  a even -> (2, 3a); a odd -> HALT
def step(a,b):
    if b>=4: return (3*a+8)//2,b-4
    if b==3: return (3*a+6)//2,0
    if b==2: return 2,3*a+3-(a%2)
    if b==1: return None
    return (2,3*a) if a%2==0 else None
if __name__=='__main__':
    from f65 import f
    bad=0; n=0
    for a in range(2,140):
        for b in range(0,12):
            r=f(a,b); s=step(a,b); n+=1
            ok=(r=='HALT' and s is None) or (isinstance(r,tuple) and r[0]=='ab' and (r[1],r[2])==s)
            if not ok: bad+=1; print('diff',a,b,r,s)
    print('checked',n,'cases, differences',bad)
