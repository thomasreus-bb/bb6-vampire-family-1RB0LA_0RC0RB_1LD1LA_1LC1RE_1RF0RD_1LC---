import subprocess,re
M=''.join({'L':'R','R':'L'}.get(c,c) for c in '1RB1LF_1LC1RD_1RA1LA_0RA0RE_0RC---_1RF0LC')
def S2str(S): return ''.join('0'+'1'*k for k in S)
def xmap(m,S,maxsteps='4000000000'):
    r=subprocess.run(['./xmap',M,'00'+'1'*m+S2str(S),maxsteps],capture_output=True,text=True).stdout.split()
    if r[0]!='X': return r[0],None
    s=r[2]; mm=re.match(r'00(1+)',s)
    if not mm: return 'ODD:'+s[:40],None
    rest=s[2+len(mm.group(1)):]
    if not re.fullmatch(r'(01+)*',rest): return 'ODDS:'+s[:60],None
    return len(mm.group(1)),[len(x) for x in rest.split('0')[1:]]
def sh(p):
    s=[];i=0
    while i<len(p):
        j=i
        while j<len(p) and p[j]==p[i]: j+=1
        s.append('%d^%d'%(p[i],j-i) if j-i>2 else '.'.join([str(p[i])]*(j-i))); i=j
    return '.'.join(s) or '-'
