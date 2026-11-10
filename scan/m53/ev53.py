import subprocess,re,sys
exec(open('comp.py').read().split('for l in sys.stdin')[0])
M=''.join({'L':'R','R':'L'}.get(c,c) for c in '1RB1RE_1LC1RE_---1LD_1LE0LB_0RF0LD_1RD1RA')
def nxt(tape,maxsteps='20000000000'):
    r=subprocess.run(['./nextev',M,tape,maxsteps,'E'],capture_output=True,text=True).stdout.split()
    if r[0]!='X': return r[0],None,(int(r[1]) if len(r)>1 and r[1].isdigit() else None)
    return 'E',r[2],int(r[1])
def c2(s): return re.sub(r'\^(\d{5,})',lambda m:'^'+m.group(1),comp(s))
if __name__=='__main__':
    for a in range(int(sys.argv[1]),int(sys.argv[2])):
        tape='110110'+'1011'*a+'1'
        out=[]
        for i in range(int(sys.argv[3])):
            r,t,st=nxt(tape)
            if r!='E': out.append('%s@%s'%(r,st)); break
            out.append(c2(t)); tape=t
        print('a=%d:'%a,' || '.join(out)[:400])
