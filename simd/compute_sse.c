#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <immintrin.h>

double get_timestamp()
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (double)tv.tv_sec + ((double)tv.tv_usec)/1000000.0;
}

void compute_sse(float* r, float const* a, float const* b, const int n)
{
    __m128 sse_a, sse_b, sse_r;

    size_t nb_items = (128 / (sizeof(float)*8));
    const size_t nsse = (n/nb_items)*nb_items;

    for (size_t i = 0; i < nsse; i += 4) {
        sse_a = _mm_load_ps(&a[i]);
        sse_b = _mm_load_ps(&b[i]);
        sse_r = _mm_add_ps(sse_a, sse_b);
        _mm_store_ps(&r[i], sse_r);
    }
}


int main(int argc, char** argv)
{
    double start_t, end_t;
    double diff_t;
    int dummy;

    float *data1, *data2, *result;

    if (argc < 2) {
        printf("Usage: %s <number of items in table>\n", argv[0]);
        return 1;
    }

    const size_t n = atoll(argv[1]);
    printf("Using a table of %lu floats\n", (unsigned long)n);

    /* Initializing the table content */
    dummy = posix_memalign((void**) &data1, 32, sizeof(float)*n);
    dummy = posix_memalign((void**) &data2, 32, sizeof(float)*n);
    dummy = posix_memalign((void**) &result, 32, sizeof(float)*n);

    for (size_t i = 0; i < n; i++) {
        data1[i] = (float)i;  /* items in data1 contain value of their indice */
        data2[i] = (float)i*2; /* the negative version if the indice */
    }


    /* Start time */
    start_t = get_timestamp();

    /* Computing  */
    compute_sse(result, data1, data2, n);

    /* End time and duration */
    end_t = get_timestamp();
    diff_t = end_t - start_t;

   printf("Execution time using manual sse: %f seconds\n", diff_t);
   printf("%f %f %f %f\n", result[0], result[1], result[2], result[3]);

    return 0;
}
