import subprocess,re,sys
def runs(s): return [len(m.group(0)) for m in re.finditer(r'0+|1+',s)]
TAIL='1'*10+'0'*30+'1'*6
def bell(r,S,N):
    o=subprocess.run(['./cyc83',str(N),str(r),S+TAIL,'400000000'],capture_output=True,text=True).stdout.split()
    if o[0]!='BELL': return o[0]
    rs=runs(o[3]); return (int(o[2]),tuple(rs[:-3]) if rs[-3:]==[10,30,6] else ('T?',tuple(rs)))
for r in (1,3):
  for a in (6,7,8,9,10,12,14):
    for b in (6,8,12):
      for h in (4,6,8,12,20):
        S='1'*a+'00'+'1'*b+'0'*h
        out=[bell(r,S,N) for N in (903,905,1203)]
        print(r,a,b,h,out)
