"""fast90.py - fast simulator for BB6 candidate 90 (DeepMind map 2.2).

Both stacks L and R are run-length encoded (lists of [value, count],
top = list end = next to the head) and use Python big integers.
Bell acceleration (4 macro steps, checked against dm90.py):
    (0, [0^n, 3, 1], 5, [0^c] + R)  ->  (0, [0^(n+5), 3, 1], 5, [0^(c-2)] + R)
applied m = (c-2)//2 times at once.  One such jump = one Bell.

Usage: python3 fast90.py [bells] [report_every]
"""
import sys, math

class Stack:
    __slots__ = ('v', 'c', 'n')
    def __init__(self, items=()):
        self.v = []; self.c = []; self.n = 0
        for x in reversed(list(items)): self.push(x, 1)
    def push(self, x, k=1):
        if k <= 0: return
        self.n += k
        if self.v and self.v[-1] == x: self.c[-1] += k
        else: self.v.append(x); self.c.append(k)
    def pop(self):
        x = self.v[-1]; self.c[-1] -= 1; self.n -= 1
        if self.c[-1] == 0: self.v.pop(); self.c.pop()
        return x
    def poprun(self):               # remove the whole top run
        x, k = self.v.pop(), self.c.pop(); self.n -= k; return x, k
    def tolist(self):
        out = []
        for x, k in zip(reversed(self.v), reversed(self.c)): out += [x]*k
        return out

def mu(x): return 'A' if x % 2 == 0 else 'B'

class M90:
    def __init__(self):
        self.a = 1; self.L = Stack(); self.d = 0; self.R = Stack()
        self.steps = 0; self.bells = 0; self.halted = False
    def eta(self, d):
        R = self.R
        while True:
            if R.n == 0:
                if d % 2: self.halted = True; return
                self.a = 0; self.L = Stack(); self.L.push(1); self.L.push(0, d//2 + 1); self.d = 0; return
            if d % 2:
                e = R.pop(); self.a = 0; self.L = Stack(); self.L.push(1); self.L.push(0, d//2); self.d = e; return
            # d even: absorb a whole run of even values / single entries
            x, k = R.v[-1], R.c[-1]
            if x % 2 == 0:
                R.poprun(); d += (x + 4) * k
            else:
                R.pop(); d = x + d + 4
    def drain(self, m, d):
        L = self.L; R = self.R
        while L.n:
            x, k = L.poprun()
            if x == 0:
                if m == 'A': d += 2*k                 # A stays A on zeros
                elif m == 'B':
                    m = 'BR'; d += 1; k -= 1
                    if k: R.push(d); R.push(0, k - 1); d = 0
                else:
                    R.push(d); R.push(0, k - 1); d = 0
            else:
                for _ in range(k):
                    if m == 'A': m, d = mu(x), x + d + 2
                    elif m == 'B': R.push(d + 1); m, d = mu(x - 1), x - 1
                    else: R.push(d); R.push(0); m, d = mu(x - 1), x - 1
        if m == 'A': self.eta(d + 1)
        elif m == 'B': self.eta(d)
        else: self.a = 1; self.d = d          # L is empty already
    def step(self):
        a, d, R, L = self.a, self.d, self.R, self.L
        self.steps += 1
        if d == 0:
            if R.n == 0: R.push(0); self.drain(mu(a + 3), a + 3)
            else: e = R.pop(); self.drain(mu(a + 1), a + e + 4)
            return
        if d % 2:
            if R.n == 0: self.halted = True; return
            e = R.pop()
            if d == 1: self.a = a + 3; self.d = e; return
            L.push(a + 3); L.push(0, (d - 3)//2); self.a = 0; self.d = e; return
        L.push(a + 3); L.push(0, (d - 2)//2)
        if R.n == 0: R.push(0); self.drain('A', 0)
        else: e = R.pop(); self.drain('A', e + 1)
    def bell_jump(self, limit=None):
        L, R = self.L, self.R
        if (self.a == 0 and self.d == 5 and len(L.v) == 3 and L.v == [1, 3, 0] and L.c[0] == 1
                and L.c[1] == 1 and R.v and R.v[-1] == 0 and R.c[-1] >= 4):
            m = (R.c[-1] - 2)//2
            if limit is not None: m = min(m, (limit - self.steps)//4)
            if m <= 0: return False
            L.c[2] += 5*m; L.n += 5*m; R.c[-1] -= 2*m; R.n -= 2*m
            self.steps += 4*m; self.bells += 1
            return True
        return False
    def state(self):
        return (self.a, self.L.tolist(), self.d, self.R.tolist())

if __name__ == '__main__':
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    ev = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    M = M90()
    while M.bells < nb and not M.halted:
        if M.bell_jump():
            if M.bells % ev == 0:
                print('bell %d log10steps %.2f |L| %d |R| %d Rruns %d top R: %s' % (
                    M.bells, math.log10(M.steps), M.L.n, M.R.n, len(M.R.v),
                    ' '.join('%d^%d' % (x, k) for x, k in list(zip(M.R.v, M.R.c))[::-1][:10])))
                sys.stdout.flush()
            continue
        M.step()
    if M.halted: print('HALT after %d macro steps, Bell %d' % (M.steps, M.bells))
