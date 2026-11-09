import subprocess,sys
def rl(s):
    # describe right part as 1^n then list of (0-run,1-run)
    out=[];i=0
    while i<len(s):
        j=i
        while j<len(s) and s[j]==s[i]: j+=1
        out.append((s[i],j-i)); i=j
    return out
def pm(n,tail):
    r=subprocess.run(['./pmap','1'*n+tail,'4000000000'],capture_output=True,text=True).stdout.split()
    if r[0]!='P': return r[0],None
    return int(r[1]),r[2] if len(r)>2 else ''
def fmt(s):
    return ' '.join(('1^%d'%k if b=='1' else ('0' if k==1 else '0^%d'%k)) for b,k in rl(s))
if __name__=='__main__':
    for tail in sys.argv[1:]:
        tail='' if tail=='e' else tail
        for n in range(30,36):
            st,out=pm(n,tail)
            print(n,n%3,'T=',fmt(tail) or 'e','->',st,fmt(out) if out is not None else '')
