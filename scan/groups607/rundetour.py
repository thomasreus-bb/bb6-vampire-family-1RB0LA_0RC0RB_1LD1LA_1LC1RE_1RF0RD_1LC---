import json,subprocess,sys
from meetpairs_lib import parse,align
info={int(k):v for k,v in json.load(open('info607.json')).items()}
PAIRS=[(52,216),(265,407),(196,404),(81,520),(123,223),(88,312),(88,449),(312,449),(253,432)]
N=sys.argv[1]; L=sys.argv[2]
out=open('detour.txt','w')
for k1,k2 in PAIRS:
  for a,b in ((k1,k2),(k2,k1)):
    X=info[a][0]; Y2,Q2,slot=align(X,info[b][0])
    r=subprocess.run(['./detour',X,Y2,'A',slot[0],str(slot[1]),N,L,'2000','1000'],capture_output=True,text=True).stdout.strip()
    line='run of #%d, detour #%d vs #%d at slot %s%d:\n%s'%(a,a,b,slot[0],slot[1],r); print(line,flush=True); out.write(line+'\n')
