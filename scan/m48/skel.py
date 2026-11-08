import sys,re
from comp import comp
# skeleton: big blocks (exponent>=8) shown with exponent, small stuff as its raw cell count
for l in sys.stdin:
    f=l.split()
    if len(f)<3: continue
    toks=comp(f[2]).split()
    out=[];small=0
    for t in toks:
        m=re.match(r'^\(?([01]+)\)?\^(\d+)$',t)
        if m and int(m.group(2))>=8:
            if small: out.append(str(small)); small=0
            out.append(f'({m.group(1)})^{m.group(2)}')
        else:
            small+= len(m.group(1))*int(m.group(2)) if m else len(t)
    if small: out.append(str(small))
    print(f[0],f[1],' '.join(out))
