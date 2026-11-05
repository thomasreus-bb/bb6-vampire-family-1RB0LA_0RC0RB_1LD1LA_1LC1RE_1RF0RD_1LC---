"""DFA families for the left half of the tape (read from the far, all-zero end towards the head).
state = (window of the last K cells, trailing 1-run mod M1, trailing alternating-run mod M2,
         age = number of cells since the first 1, capped at K+1, 0 if no 1 yet)"""
def make(K,M1,M2):
    def step(st,c):
        w,a,b,age=st; last=w&1
        w2=((w<<1)|c)&((1<<K)-1)
        a2=(a+1)%M1 if c==1 else 0
        b2=(b+1)%M2 if c!=last else 1%M2
        age2=0 if (age==0 and c==0) else min(K+1,age+1)
        return (w2,a2,b2,age2)
    start=(0,0,1%M2,0); idx={start:0}; lst=[start]; table={}; i=0
    while i<len(lst):
        for c in (0,1):
            n=step(lst[i],c)
            if n not in idx: idx[n]=len(lst); lst.append(n)
            table[(i,c)]=idx[n]
        i+=1
    assert table[(0,0)]==0
    return len(lst), (lambda q,c: table[(q,c)]), lst

def make2(K, M1=3, CAP=4):
    """window of K cells + trailing 1-run length mod M1 (with a 'long' flag: run >= CAP)
    + memory of the 1-run (mod M1, long flag) that ended where the current alternating run began."""
    def step(st,c):
        w,a,lng,alt,mem=st; last=w&1
        w2=((w<<1)|c)&((1<<K)-1)
        if c==1: a2=(a+1)%M1; lng2=min(CAP,lng+1)
        else: a2=0; lng2=0
        # alternating run: extends if c != last
        if c!=last:
            alt2=min(alt+1,CAP)
            mem2=mem if alt>=1 else (a,lng)        # new alternating run starts: remember the 1-run before it
        else:
            alt2=0; mem2=(0,0)
        return (w2,a2,lng2,alt2,mem2)
    start=(0,0,0,0,(0,0)); idx={start:0}; lst=[start]; table={}; i=0
    while i<len(lst):
        for c in (0,1):
            n=step(lst[i],c)
            if n not in idx: idx[n]=len(lst); lst.append(n)
            table[(i,c)]=idx[n]
        i+=1
    assert table[(0,0)]==0, (table[(0,0)], lst[:3])
    return len(lst), (lambda q,c: table[(q,c)]), lst

def make3(R=3, CAP=4, MOD=3, AMOD=2):
    """run-window DFA: the last R tokens of the run-length encoding, where a constant run is
    ('c', bit, min(len,CAP), len mod MOD for 1-runs) and consecutive runs of length 1 are merged into an
    alternating token ('a', min(count,CAP), count mod AMOD).  The far end is a long 0-run."""
    Z=('c',0,CAP,0)
    def push_done(toks, tok):
        # tok = finished run token ('c',bit,L,m) ; merge length-1 runs into alternation tokens
        if tok[0]=='c' and tok[2]==1:
            if toks and toks[-1][0]=='a':
                a=toks[-1]; toks=toks[:-1]+(('a',min(CAP,a[1]+1),(a[2]+1)%AMOD),)
            else: toks=toks+(('a',1,1%AMOD),)
        else: toks=toks+(tok,)
        return toks[-(R-1):] if R>1 else ()
    def step(st,c):
        toks=st[:-1]; cur=st[-1]          # cur = current (open) constant run
        if cur[1]==c:
            L=min(CAP,cur[2]+1); m=(cur[3]+1)%MOD if c==1 else 0
            if cur==Z: return st
            return toks+(('c',c,L,m),)
        toks=push_done(toks,cur)
        return toks+(('c',c,1,1%MOD if c==1 else 0),)
    start=(Z,); idx={start:0}; lst=[start]; table={}; i=0
    while i<len(lst):
        for c in (0,1):
            n=step(lst[i],c)
            if n not in idx: idx[n]=len(lst); lst.append(n)
            table[(i,c)]=idx[n]
        i+=1
    assert table[(0,0)]==0
    return len(lst), (lambda q,c: table[(q,c)]), lst

def make4(L=10, K=4, CAPA=1):
    """shape DFA for the left half 0^inf (10)^x W: 'Z' = only zeros so far; ('A',last) = inside the
    alternating part; ('W',w) = exact word w (|w| <= L) after the alternating part; ('X',window) = W longer
    than L (only the last K cells are kept)."""
    def step(st,c):
        k=st[0]
        if k=='Z': return ('Z',) if c==0 else ('A',1,1)
        if k=='A':
            if c!=st[1]: return ('A',c,min(CAPA,st[2]+1))
            return ('W',(st[1],c),st[2])     # deviation: keep the last alternating bit and the capped length
        if k=='W':
            w=st[1]+(c,)
            if len(w)<=L: return ('W',w,st[2])
            return ('X',w[-K:])
        return ('X',(st[1]+(c,))[-K:])
    start=('Z',); idx={start:0}; lst=[start]; table={}; i=0
    while i<len(lst):
        for c in (0,1):
            n=step(lst[i],c)
            if n not in idx: idx[n]=len(lst); lst.append(n)
            table[(i,c)]=idx[n]
        i+=1
    assert table[(0,0)]==0
    return len(lst), (lambda q,c: table[(q,c)]), lst
