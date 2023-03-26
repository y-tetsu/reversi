#include "xorshift.h"

#define SS 1812433253
#define SL 13
#define SR 17
#define SX 123464980
#define SY 3447902351
#define SZ 2859490775
#define SW 47621719

static unsigned long set_s(unsigned long s);

static unsigned long tx = 123456789;
static unsigned long ty = 362436069;
static unsigned long tz = 521288629;
static unsigned long tw = 88675123;

static unsigned long set_s(unsigned long s)
{
  s = (s * SS) + 1;
  s ^= s << SL;
  s ^= s >> SR;
  return s;
}

void init_rand(unsigned long s)
{
    do
    {
        s = set_s(s);
        tx = SX ^ s;

        s = set_s(s);
        ty = SY ^ s;

        s = set_s(s);
        tz = SZ ^ s;

        s = set_s(s);
        tw = SW ^ s;
    }
    while ((tx == 0) && (ty == 0) && (tz == 0) && (tw == 0));
}

unsigned long rand_int(void)
{
    unsigned long tt;
    tt = tx ^ (tx << 11);
    tx = ty;
    ty = tz;
    tz = tw;
    tw = (tw ^ (tw >> 19)) ^ (tt ^ (tt>>8));
    return tw;
}
