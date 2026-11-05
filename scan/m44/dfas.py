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
