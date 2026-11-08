# does a halting block size z still halt when other blocks lie behind it? (no. 52)
import sys
M='1RB0LC_1RC1RF_1LD0RA_1LE0LD_1RC0LA_0LA---'
T={}
for i,g in enumerate(M.split('_')):
    for b in (0,1):
        x=g[3*b:3*b+3]; T[(i,b)]=None if x[0]=='-' else (int(x[0]),1 if x[1]=='R' else -1,ord(x[2])-65)
def run(tape,q=4,maxs=5*10**6):
    t=bytearray(len(tape)+4*maxs//1000+10**6); off=10**6//2
    for i,c in enumerate(tape): t[off+i]=c
    p=off
    for s in range(maxs):
        tr=T[(q,t[p])]
        if tr is None: return s+1
        t[p]=tr[0]; p+=tr[1]; q=tr[2]
    return None
behinds={'none':'1','010^84 01':'010'*84+'01','001^171':'001'*171,'000 100^84 1':'000'+'100'*84+'1'}
for z in (17,44,285,18,43,286):
    for name,b in behinds.items():
        tape=[int(c) for c in '010'+'100'*z+b]
        print(z,name,run(tape,maxs=3*10**7 if z>100 else 3*10**6))
