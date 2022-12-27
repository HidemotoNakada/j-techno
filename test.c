#include <stdio.h>
#include <time.h>
#define N 10000000

int buf[N];

int main() {
    struct timespec ts_before, ts_after;
    for (int i = 0; i < N; i++) buf[i] = 1;

    clock_gettime(CLOCK_REALTIME, &ts_before);
    int acc = 0;
    for (int i = 0; i < N; i++) 
        acc += buf[i];
    clock_gettime(CLOCK_REALTIME, &ts_after);
    double diff = (ts_after.tv_sec - ts_before.tv_sec) +
                ((ts_after.tv_nsec - ts_before.tv_nsec) / 1000000000.0);
    printf("%d, %lf\n", acc, diff);
}