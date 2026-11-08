import sys
# split tape (from the left end) into 3-cell words, run-length encode the words
def comp3(s,off=0):
    w=[s[:off]] if off else []
    w+= [s[i:i+3] for i in range(off,len(s),3)]
    out=[];i=0
    while i<len(w):
        j=i
        while j<len(w) and w[j]==w[i]: j+=1
        out.append(w[i]+('^%d'%(j-i) if j-i>1 else '')); i=j
    return ' '.join(out)
if __name__=='__main__':
    off=int(sys.argv[1]) if len(sys.argv)>1 else 0
    for l in sys.stdin:
        f=l.split()
        if len(f)<3: print(l.strip()); continue
        print(f[0], comp3(f[2],off))
