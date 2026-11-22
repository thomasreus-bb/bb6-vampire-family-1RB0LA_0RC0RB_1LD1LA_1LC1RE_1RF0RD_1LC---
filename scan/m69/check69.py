# check Racheline's rules for no. 69 (wiki) on synthetic starts A(N,m), N >= 7
import subprocess
def rule(N,m):
    if m==1: N,m=N+1,0
    if m>=3: return (3*(N//2),m-3) if N%2==0 else (3*(N//2)+1,m-2)
    if m==0: return 'CYCLER' if N%2==0 else (6,6*(N//2)-15)
    if m==2: return 'HALT' if N%2==0 else (6,6*(N//2)-10)
bad=n=0
for N in range(7,60):
    for m in range(0,40):
        o=subprocess.run(['./syn69',str(N),str(m),'20000000'],capture_output=True,text=True).stdout.split()
        got='HALT' if o[0]=='HALT' else ('CYCLER' if o[0]=='NONE' else (int(o[1]),int(o[2])))
        exp=rule(N,m)
        if isinstance(exp,tuple) and exp[1]==1: exp=(exp[0]+1,0)
        if got==(6,0): got='CYCLER'   # A(6,0) -> A(6,0) (blank tape, shifted): translated cycler
        if isinstance(exp,tuple) and exp[0]==6 and exp[1]<0: continue
        n+=1
        if got!=exp:
            bad+=1
            if bad<10: print(N,m,'machine',got,'rule',exp)
print(n,'starts checked, mismatches',bad)
