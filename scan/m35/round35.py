M='1RB---_0RC0LD_1LB1RC_0LE0LF_1RD1LE_1RF1RA'
T=[[None if st[3*b+2]=='-' else (int(st[3*b]),1 if st[3*b+1]=='R' else -1,ord(st[3*b+2])-65) for b in range(2)] for st in M.split('_')]
def cfg(X,Y,Z,pre=5):
    t=[1]*pre+[0]+[1]*X+[0]+[1]*Y+[0,0]+[1]*Z+[0]*5
    return t, pre+1+X
def match(t,h,s):
    # A on 0, left run of 1s, right: 1^Y 00 1^Z
    if s!=0 or t[h]!=0: return None
    i=h-1; X=0
    while i>=0 and t[i]==1: X+=1; i-=1
    j=h+1; Y=0
    while j<len(t) and t[j]==1: Y+=1; j+=1
    if j+2>=len(t) or t[j]!=0 or t[j+1]!=0: return None
    k=j+2; Z=0
    while k<len(t) and t[k]==1: Z+=1; k+=1
    if X and Y and Z: return (X,Y,Z)
for (X,Y,Z) in [(7,9,4),(10,9,4),(7,12,4),(7,9,8),(20,30,5),(20,31,5),(20,32,5),(20,4,5),(20,3,5)]:
    t,h=cfg(X,Y,Z); s=0; n=0
    while n<100000:
        tr=T[s][t[h]]
        if tr is None: print('HALT'); break
        t[h]=tr[0]; h+=tr[1]; s=tr[2]; n+=1
        m=match(t,h,s)
        if m: print((X,Y,Z),'->',m,'steps',n); break
    else: print((X,Y,Z),'no match')
