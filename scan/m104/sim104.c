/* sim104.c - fast simulator for BB6 candidate 104 using the DeepMind
 * acceleration (cryptids repo, BB6 Accelerations README, section 2.5).
 *
 * State (d, R): R is a stack of naturals, front = top.  One macro step:
 *   scan:  while d odd: read e = R.pop(); ks.push_front(d/2); d = e
 *          (d even with an entry e: drain(ks, d+e+2, R))
 *   end of R: d odd -> HALT
 *             ks empty -> (1, [0]^(d/2+1))
 *             else drain(ks[1:], 2*ks[0]+5, [0]^(d/2))
 *   drain(ks,d,R): take pairs (j1,j2) from ks:
 *             j1 == 0: d = 2*j2+d+6
 *             j1 >  0: R = [0]^(j1-1)+[d+1]+R ; d = 2*j2+5
 *          ks exhausted -> (d+2, R); one entry k left -> (1, [0]^k+[d+1]+R)
 *
 * R is stored run-length encoded (value,count), top at the array end.
 * Values are 64-bit; overflow aborts.
 *
 * Usage: sim104 [max_macro_steps] [report_every]
 * Output per report: step, stack length, #odd entries, #runs, top value,
 *   max scan depth since last report, min stack length since last report.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef uint64_t u64;
static u64 *val, *cnt; static size_t nr = 0, cap = 0;
static u64 len = 0, nodd = 0;
static u64 *ks; static size_t nks = 0, kcap = 0;

static void die(const char *m){ fprintf(stderr, "%s\n", m); exit(2); }
static void push(u64 v, u64 c){
    if (!c) return;
    len += c; if (v & 1) nodd += c;
    if (nr && val[nr-1] == v){ cnt[nr-1] += c; return; }
    if (nr == cap){ cap = cap ? 2*cap : 1<<20;
        val = realloc(val, cap*sizeof *val); cnt = realloc(cnt, cap*sizeof *cnt);
        if (!val || !cnt) die("oom"); }
    val[nr] = v; cnt[nr] = c; nr++;
}
static u64 pop(void){
    u64 v = val[nr-1];
    if (--cnt[nr-1] == 0) nr--;
    len--; if (v & 1) nodd--;
    return v;
}
static void kpush(u64 v){
    if (nks == kcap){ kcap = kcap ? 2*kcap : 1024; ks = realloc(ks, kcap*sizeof *ks); if (!ks) die("oom"); }
    ks[nks++] = v;
}
#define CHK(x) do{ if ((x) > (UINT64_MAX>>2)) die("overflow"); }while(0)

/* ks is stored reversed: ks[nks-1] is the first element.  drain consumes
 * from index hi-1 downwards, hi = number of elements still in use. */
static u64 drain(size_t hi, u64 d){
    for (;;){
        if (hi == 0){ CHK(d); nks = 0; return d + 2; }
        if (hi == 1){ u64 k = ks[0]; push(d+1, 1); push(0, k); nks = 0; return 1; }
        u64 j1 = ks[hi-1], j2 = ks[hi-2]; hi -= 2;
        CHK(j2); CHK(d);
        if (j1 == 0) d = 2*j2 + d + 6;
        else { push(d+1, 1); push(0, j1-1); d = 2*j2 + 5; }
    }
}

int main(int argc, char **argv){
    u64 maxs = argc > 1 ? strtoull(argv[1], 0, 10) : 100000000ULL;
    u64 rep  = argc > 2 ? strtoull(argv[2], 0, 10) : 10000000ULL;
    u64 dumpat = getenv("DUMP") ? strtoull(getenv("DUMP"), 0, 10) : 0;
    u64 d = 0; push(0, 1);
    u64 bells = 0, nextrep = rep; int verbose = getenv("BELLS") != 0;
    u64 maxscan = 0, minlen = UINT64_MAX, ends = 0;
    for (u64 s = 1; s <= maxs; s++){
        nks = 0; u64 depth = 0;
        /* acceleration: (d odd, [3, 0^c, ..]) -> (d+6, [3, 0^(c-2), ..]) */
        if ((d & 1) && nr >= 2 && val[nr-1] == 3 && cnt[nr-1] == 1 && val[nr-2] == 0 && cnt[nr-2] >= 4){
            u64 m = (cnt[nr-2] - 2) / 2;
            if (m > maxs - s) m = maxs - s;
            if (dumpat >= s && m > dumpat - s) m = dumpat - s;
            if (m > 0){
                if (m > (UINT64_MAX>>3)/6 || d > (UINT64_MAX>>3)) die("overflow");
                cnt[nr-2] -= 2*m; len -= 2*m; d += 6*m; s += m - 1;
                bells++;
                if (verbose){ printf("bell %llu step %llu d %llu len %llu odd %llu runs %zu top:",
                    (unsigned long long)bells, (unsigned long long)s, (unsigned long long)d,
                    (unsigned long long)len, (unsigned long long)nodd, nr);
                    for (size_t r = nr; r-- > 0 && r + 12 > nr;) printf(" %llu^%llu", (unsigned long long)val[r], (unsigned long long)cnt[r]);
                    printf("\n"); fflush(stdout); }
                continue;
            }
        }
        for (;;){
            if (len == 0){
                ends++;
                if (d & 1){ printf("HALT at macro step %llu\n", (unsigned long long)s); return 0; }
                if (nks == 0){ push(0, d/2 + 1); d = 1; }
                else { u64 k0 = ks[nks-1]; CHK(k0); size_t hi = nks - 1;
                       /* R is empty: push zeros first, then drain on top */
                       push(0, d/2); d = drain(hi, 2*k0 + 5); }
                break;
            }
            u64 e = pop(); depth++;
            if (d & 1){ kpush(d/2); d = e; }
            else { CHK(e); d = drain(nks, d + e + 2); break; }
        }
        if (dumpat == s){ printf("DUMP %llu", (unsigned long long)d);
            for (size_t r = nr; r-- > 0;) for (u64 c = 0; c < cnt[r]; c++) printf(" %llu", (unsigned long long)val[r]);
            printf("\n"); return 0; }
        if (depth > maxscan) maxscan = depth;
        if (len < minlen) minlen = len;
        if (s >= nextrep){ nextrep = (s/rep + 1)*rep;
            printf("%llu len %llu odd %llu runs %zu d %llu maxscan %llu minlen %llu ends %llu\n",
                (unsigned long long)s, (unsigned long long)len, (unsigned long long)nodd, nr,
                (unsigned long long)d, (unsigned long long)maxscan,
                (unsigned long long)minlen, (unsigned long long)ends);
            fflush(stdout); maxscan = 0; minlen = UINT64_MAX;
        }
    }
    return 0;
}
