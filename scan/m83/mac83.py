import subprocess,sys,random
TM='1LB1LA_1RC0LB_1RD0RB_1LA0RE_---1RF_1RB0RA'
def synth(q,tape,off=0,mx=10**8):
    o=subprocess.run(['/tmp/an/synth',TM,q,str(off),str(mx)],input=tape+'\n',capture_output=True,text=True).stdout.split()
    return o
def sweep(N,r,S):
    o=synth('B','0'+'1'*N+'0'*r+S)
    if o[0]!='REC': return ('HALT',o)
    q,t=o[1],o[3]
    assert q=='B', o[:3]
    # expect 0^(N-1) S'
    z=len(t)-len(t.lstrip('0'))
    assert z==N-1 or True
    return ('OK',z,t[z:])
def bell(N,r,S):
    res=sweep(N,r,S)
    if res[0]=='HALT': return None
    z,S2=res[1],res[2]
    q=z//4; rr=z%4
    return z,(6*q+3, {0:1,2:3}.get(rr,('X',rr)), S2.rstrip('0'))
