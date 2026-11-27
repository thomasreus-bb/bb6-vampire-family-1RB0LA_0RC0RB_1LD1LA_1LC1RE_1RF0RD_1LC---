import subprocess,re
def runs(s): return [len(m.group(0)) for m in re.finditer(r'0+|1+',s)]
TAIL='0'*22+'1'*10+'0'*30+'1'*6
def bell(r,S,N):
    o=subprocess.run(['./cyc83',str(N),str(r),S+TAIL,'400000000'],capture_output=True,text=True).stdout.split()
    if o[0]!='BELL': return o[0]
    rs=runs(o[3]); return (int(o[2]),tuple(rs[:-4]) if rs[-4:]==[22,10,30,6] else ('T?',tuple(rs)))
for r in (2,1,3):
  for a in (6,8,12):
    for g in (1,3,5,7,9,13):
      for b in (6,12):
        S='1'*a+'0'*g+'1'*b
        out=[bell(r,S,N) for N in (903,905)]
        print(r,a,g,b,out)
