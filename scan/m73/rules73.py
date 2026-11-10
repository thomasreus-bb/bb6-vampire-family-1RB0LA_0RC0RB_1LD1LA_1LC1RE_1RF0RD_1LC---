# C-events of mirrored no. 73: config X(m, S) = head left of "0 0 1^m S", S = 0 1^a1 0 1^a2 ... (runs list)
# print the rewrite rules between consecutive events in run-list form
import re,collections,sys
def runs(S):
    # S must be (0 1+)* exactly
    if not re.fullmatch(r'(01+)*',S): return None
    return [len(x) for x in S.split('0')[1:]]
ev=[]
for l in open(sys.argv[1]):
    f=l.split()
    if len(f)<2: continue
    m=re.match(r'00(1+)',f[1])
    if not m: ev.append(None); continue
    r=runs(f[1][2+len(m.group(1)):])
    ev.append((len(m.group(1)),r) if r is not None else None)
c=collections.Counter(); ex={}
for a,b in zip(ev,ev[1:]):
    if a is None or b is None: c['unparsed']+=1; continue
    ra,rb=a[1],b[1]; k=0
    while k<min(len(ra),len(rb)) and ra[-1-k]==rb[-1-k]: k+=1
    pa,pb=tuple(ra[:len(ra)-k]),tuple(rb[:len(rb)-k])
    def sh(p):
        s=[];i=0
        while i<len(p):
            j=i
            while j<len(p) and p[j]==p[i]: j+=1
            s.append('%d^%d'%(p[i],j-i) if j-i>2 else '.'.join([str(p[i])]*(j-i))); i=j
        return '.'.join(s) or '-'
    key=(sh(pa),sh(pb)) if len(pa)<6 and len(pb)<6 else ('LONG:'+sh(pa)[:40],'LONG:'+sh(pb)[:40])
    c[key]+=1; ex.setdefault(key,[]).append((a[0],b[0]-a[0],len(pa),len(pb)))
for k,v in sorted(c.items(),key=lambda x:-x[1]) if True else []:
    if k=='unparsed': print('unparsed',v); continue
    e=ex[k][:3]
    print(v,k[0],'->',k[1],' (m, dm):',[(x[0],x[1]) for x in e])
