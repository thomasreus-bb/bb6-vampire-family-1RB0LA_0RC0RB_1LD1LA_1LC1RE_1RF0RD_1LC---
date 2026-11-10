# no. 13 (mirrored): from B-event 1^n (head left of the tape, state B) to the next B-event; map n -> n' (or HALT)
import subprocess,sys
M=''.join({'L':'R','R':'L'}.get(c,c) for c in '1RB0RF_1RC1RF_1LD0LE_---1LC_1RA1LE_1LC1RB')
def f(n,maxsteps='40000000000'):
    r=subprocess.run(['./nextev',M,'1'*n,maxsteps,'B'],capture_output=True,text=True).stdout.split()
    if r[0]!='X': return r[0],None
    t=r[2]
    if set(t)!={'1'}: return 'ODD',t
    return len(t),int(r[1])
if __name__=='__main__':
    for n in range(int(sys.argv[1]),int(sys.argv[2])):
        r,st=f(n)
        print(n,r,st if r!='ODD' else st[:60])
