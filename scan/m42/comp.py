import sys,re
def comp(s):
    # tokens: (10)^k, 1^m, 0^z
    out=[];i=0
    while i<len(s):
        m=re.match(r'(?:10){2,}',s[i:])
        if m and len(m.group(0))>=4:
            k=len(m.group(0))//2; out.append('(10)^%d'%k); i+=2*k; continue
        c=s[i]; j=i
        while j<len(s) and s[j]==c: j+=1
        out.append('%s^%d'%(c,j-i) if j-i>1 else c); i=j
    return ' '.join(out)
for l in sys.stdin:
    f=l.split()
    if len(f)==3 and f[2][0] in '01': print(f[0],f[1],comp(f[2]))
    else: print(l.strip())
