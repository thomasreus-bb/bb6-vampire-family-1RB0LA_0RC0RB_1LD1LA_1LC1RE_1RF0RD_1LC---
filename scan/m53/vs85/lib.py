# Compile first: gcc -O2 -o syn syn.c ; gcc -O2 -o evE evE.c
import subprocess,re
T53='1RB1RE_1LC1RE_---1LD_1LE0LB_0RF0LD_1RD1RA'
def run(tape,mx=10**9,T=T53):
    o=subprocess.run(['./syn',T,tape,str(mx)],capture_output=True,text=True).stdout.split()
    if o[0] in('HALT','MAX','OVF'): return (o[0],)
    return (int(o[0]),o[1])
def comp(s):
    # compress into tokens: (10)^k and single bits
    out=[];i=0
    while i<len(s):
        k=0
        while s[i:i+2]=='10' and (i+2<len(s)): k+=1;i+=2
        if k: out.append('(10)^%d'%k); continue
        out.append(s[i]); i+=1
    return ' '.join(out)
def parse(s):
    m=re.fullmatch(r'((?:10)*)1',s)
    if m: return ('P',len(m.group(1))//2)
    m=re.fullmatch(r'((?:10)*)11100((?:10)*)1',s)
    if m: return ('Q',len(m.group(1))//2,len(m.group(2))//2)
    m=re.fullmatch(r'((?:10)*)11101100((?:10)*)1',s)
    if m: return ('R',len(m.group(1))//2,len(m.group(2))//2)
    return ('?',comp(s))
def P(a): return '10'*a+'1'
def Q(a,b): return '10'*a+'11100'+'10'*b+'1'
def R(a,b): return '10'*a+'11101100'+'10'*b+'1'
