import re,subprocess
def name(t):
    if t=='1': return 'S'
    m=re.fullmatch(r'0001((?:01)*)',t)
    if m: return 'P%d'%(len(m.group(1))//2)
    m=re.fullmatch(r'11((?:01)*)',t)
    if m: return 'Q%d'%(len(m.group(1))//2)
    m=re.fullmatch(r'0001((?:01)*)00001',t)
    if m: return 'R%d'%(len(m.group(1))//2)
    return t
def ev(n,t):
    r=subprocess.run(['./syn18',str(n),t],capture_output=True,text=True).stdout.split(); return int(r[0]),r[1]
if __name__=="__main__":
 for k in range(0,9):
     P='0001'+'01'*k; Q='11'+'01'*k
     outP=[]; outQ=[]
     for n in (607,): pass
     m,t=ev(607,P); outP.append(name(t))   # 607 = 7 mod 8
     m2,t2=ev(602,Q); outQ.append(name(t2))  # 602 = 2 mod 8
     print('k=%d: P%d, n=7 mod 8 -> %s (m=%d=9n/8%+.3f) | Q%d, n=2 mod 8 -> %s (m=%d=9n/8%+.3f)'%(k,k,outP[0],m,m-9*607/8,k,outQ[0],m2,m2-9*602/8))
