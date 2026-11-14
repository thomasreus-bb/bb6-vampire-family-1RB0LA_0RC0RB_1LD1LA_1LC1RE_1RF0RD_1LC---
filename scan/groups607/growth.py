# growth exponent of the tape width over a long run: slope of log(width) vs log(steps) on [N/1000, N] and on [N/10, N]
import subprocess,math,sys
def slope(pts):
    mx=sum(p[0] for p in pts)/len(pts); my=sum(p[1] for p in pts)/len(pts)
    return sum((p[0]-mx)*(p[1]-my) for p in pts)/sum((p[0]-mx)**2 for p in pts)
def growth(tm,q,N):
    r=subprocess.run(['./recs',tm,q,str(N),'1000000000','0'],capture_output=True,text=True).stdout.split('\n')
    st=[int(l.split()[0]) for l in r if l and l[0].isdigit()]
    p1=[(math.log(s+1),math.log(i+1)) for i,s in enumerate(st) if s>=N/1000]
    p2=[(math.log(s+1),math.log(i+1)) for i,s in enumerate(st) if s>=N/10]
    return slope(p1),slope(p2),len(st)
for tm,q,lab in [('1RB0LD_1RC0RF_1LA1RF_0LA0RE_1LD---_0RA0RD','A','g8 #21'),('1RB0LD_1RC0RF_1LA1RF_0LA0RE_1LD---_0RA0RD','C','g8 #106'),('1RB0LD_1RC0RF_1LA1RF_0LA0RE_1LD---_0RA0RD','E','g8 #182'),('1RB0LD_1RC0RF_1LA1RF_0LA0RE_1LD---_0RA0RD','B','g8 #214'),
                 ('1RB0RE_0RC1RE_1RD1LE_0LE---_1RA1LF_1RF0LC','A','g28 #64'),('1RB0RE_0RC1RE_1RD1LE_0LE---_1RA1LF_1RF0LC','C','g28 #371'),('1RB0RE_0RC1RE_1RD1LE_0LE---_1RA1LF_1RF0LC','E','g28 #602')]:
    a,b,w=growth(tm,q,int(sys.argv[1])); print(lab,'start',q,'exp [N/1000,N] %.3f  [N/10,N] %.3f  width %d'%(a,b,w),flush=True)
