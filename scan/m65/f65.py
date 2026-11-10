# no. 65 (mirrored): A-event (01)^a 1^b -> next A-event
import subprocess,re,sys
M=''.join({'L':'R','R':'L'}.get(c,c) for c in '1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF')
def nxt(tape,maxsteps='40000000000'):
    r=subprocess.run(['./nextev',M,tape,maxsteps,'A'],capture_output=True,text=True).stdout.split()
    if r[0]!='X': return r[0],None
    return 'A',r[2]
def parse(t):
    m=re.fullmatch(r'((?:01)*)(1*)',t)
    if m: return ('ab',len(m.group(1))//2,len(m.group(2)))
    m=re.fullmatch(r'010(1*)',t)
    if m: return ('r',len(m.group(1)))
    return ('?',t[:50])
def f(a,b):
    r,t=nxt('01'*a+'1'*b)
    return r if t is None else parse(t)
if __name__=='__main__':
    for a in range(int(sys.argv[1]),int(sys.argv[2])):
        print(a,' '.join('b%d:%s'%(b,f(a,b)) for b in range(0,9)))
