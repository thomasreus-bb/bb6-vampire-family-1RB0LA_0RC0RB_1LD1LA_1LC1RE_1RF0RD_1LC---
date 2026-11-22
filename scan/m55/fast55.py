# no. 55 (1RB1LF_0RC1RD_1LA1LD_1LE0RA_---1LC_0LA1LA): simplified rules from the wiki (Marco Dos Santos), checked on 2,160 synthetic starts.
# C(a,b) = 0^inf 110 A> 11^a 0 1^b 0^inf, b >= 6. Start C(0,9) after 74 steps.
def step(a,b):
    if b%2==0:
        k=(b-6)//2
        if a==0: return (k+1,9)
        a1=a-1
        if k<=a1+3: return (a1-k+4,6*k+12)
        if k in (a1+4,a1+5): return None
        return (k-a1-5,6*a1+39)
    k=(b-1)//2
    if k>a: return (k-a,6*a+6)
    if a in (k,k+1): return None
    return (a-k-1,6*k+9)
if __name__=='__main__':
    import sys
    sys.set_int_max_str_digits(0)
    a,b=0,9; s_all=0; s_after=0; n=int(sys.argv[1]) if len(sys.argv)>1 else 2000000
    for i in range(n):
        m=max(a,b//2)+1; 
        if m<10**300: s_all+=2/m; s_after+= 2/m if m>10**5 else 0
        r=step(a,b)
        if r is None: print('HALT at event',i,a,b); break
        a,b=r
    else: print(n,'events without HALT; b has about',int(b.bit_length()*0.30103),'digits')
    print('heuristic halting chance: all %.3f, after max > 10^5: %.2e'%(s_all,s_after))
