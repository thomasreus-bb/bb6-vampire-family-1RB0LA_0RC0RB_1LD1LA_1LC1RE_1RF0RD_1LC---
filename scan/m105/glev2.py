# level iteration for configs PREFIX UNIT^n W (see gmap2.c)
import subprocess,glev
class G2(glev.G):
    def __init__(s,M,state,prefix,unit,m,a,qmin=40,kmin=2):
        super().__init__(M,state,prefix,m,a,qmin); s.unit=unit; s.kmin=kmin
    def pm(s,n,W,maxsteps='40000000000'):
        r=subprocess.run(['./gmap2',s.M,s.state,s.prefix or '-',s.unit,s.prefix+s.unit*n+W,maxsteps,str(s.kmin)],capture_output=True,text=True).stdout.split()
        if r[0]!='P': return r[0],None
        return int(r[2]),(r[3] if len(r)>3 else '')
