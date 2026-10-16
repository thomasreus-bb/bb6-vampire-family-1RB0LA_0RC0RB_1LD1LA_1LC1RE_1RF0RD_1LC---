// cyc.c - Bell simulator for the TM2-type machines of the family.
//
// A Bell ends in the configuration   0^inf  P  (10)^n  11  Z>  0^inf
// (state Z reads the 0 at the right end of the tape; n maximal, so P does not end in 10).
//
// Usage:
//   cyc real TM Z N      simulate TM from the blank tape and print the first N Bell ends
//                        as "steps n P" (P = "e" for the empty word).
//                        The start state is A; set the environment variable START=0..5
//                        to start in another state (0 = A, ..., 5 = F).
//   cyc rule TM Z LIM    read lines "P n" from stdin, start at 0^inf P (10)^n 11 Z> 0^inf and
//                        run to the next Bell end (at most LIM steps). Output per line:
//                        "P n -> P' n' steps", "P n -> HALT steps", "P n -> LIMIT" or "P n -> OVF".
//
// Build: gcc -O2 -o cyc cyc.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NT (1 << 22)                   // tape cells
static unsigned char t[NT];
static int W[6][2], M[6][2], X[6][2];  // write, move, next state (-1 = halt)
static long lo, hi, h;                 // leftmost / rightmost visited cell, head
static int st;                         // current state

// Is the machine at a Bell end? If so, return n and the word P.
static int at_bell_end(int Z, long *n, char *P) {
    if (st != Z || t[h] != 0) return 0;
    for (long x = h + 1; x <= hi; x++) if (t[x]) return 0;
    if (t[h - 1] != 1 || t[h - 2] != 1) return 0;
    long x = h - 3, m = 0;
    while (t[x] == 0 && t[x - 1] == 1) { m++; x -= 2; }
    long a = lo; while (a <= x && t[a] == 0) a++;
    int L = 0; for (long y = a; y <= x; y++) P[L++] = '0' + t[y];
    P[L] = 0; *n = m; return 1;
}

static int step(void) {                // one TM step; returns 0 on halt, -1 on tape overflow
    int b = t[h], nx = X[st][b];
    if (nx < 0) return 0;
    t[h] = W[st][b]; h += M[st][b]; st = nx;
    if (h < lo) lo = h;
    if (h > hi) hi = h;
    return (h < 4 || h > NT - 4) ? -1 : 1;
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: cyc real|rule TM Z N|LIM\n"); return 2; }
    const char *tm = argv[2]; int Z = argv[3][0] - 'A';
    for (int s = 0; s < 6; s++) for (int b = 0; b < 2; b++) {
        const char *p = tm + s * 7 + b * 3;
        if (p[0] == '-') { X[s][b] = -1; continue; }
        W[s][b] = p[0] - '0'; M[s][b] = p[1] == 'R' ? 1 : -1; X[s][b] = p[2] - 'A';
    }
    static char P[1 << 20];
    if (!strcmp(argv[1], "real")) {
        int N = atoi(argv[4]), c = 0;
        memset(t, 0, NT); h = NT / 2; lo = hi = h;
        st = getenv("START") ? atoi(getenv("START")) : 0;
        for (long long i = 0; c < N; i++) {
            long n;
            if (at_bell_end(Z, &n, P)) { printf("%lld %ld %s\n", i, n, P[0] ? P : "e"); fflush(stdout); c++; }
            int r = step();
            if (r == 0) { printf("HALT %lld\n", i); return 0; }
            if (r < 0) { printf("OVF\n"); return 1; }
        }
        return 0;
    }
    long long lim = atoll(argv[4]); char in[1000]; long n0;
    while (scanf("%999s %ld", in, &n0) == 2) {
        memset(t, 0, NT); h = NT / 4; long x = h;
        int L = strcmp(in, "e") ? (int)strlen(in) : 0;
        for (int j = 0; j < L; j++) t[x++] = in[j] - '0';
        for (long j = 0; j < n0; j++) { t[x++] = 1; t[x++] = 0; }
        t[x++] = 1; t[x++] = 1;
        lo = h; h = x; hi = h; st = Z;
        int done = 0;
        for (long long i = 0; i < lim; i++) {
            long n;
            if (i > 0 && at_bell_end(Z, &n, P)) { printf("%s %ld -> %s %ld %lld\n", in, n0, P[0] ? P : "e", n, i); done = 1; break; }
            int r = step();
            if (r == 0) { printf("%s %ld -> HALT %lld\n", in, n0, i); done = 1; break; }
            if (r < 0) { printf("%s %ld -> OVF\n", in, n0); done = 1; break; }
        }
        if (!done) printf("%s %ld -> LIMIT\n", in, n0);
        fflush(stdout);
    }
    return 0;
}
