from macro import step,run2
def seg(kind,p):
    k,q=run2(kind,p)
    while k==kind and q is not None: k,q=run2(k,q)
    return k,q
