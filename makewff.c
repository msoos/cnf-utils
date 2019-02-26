/******************************************
Copyright (c) 2018, Henry Kautz <henry.kautz@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
***********************************************/

/************************************/
/* Compilation flags                */
/************************************/

/***************************************************************/
/* Please select only one of following flags: UNIX, ANSI or NT */
/* Description:                                                */
/*    UNIX:  uses some non-POSIX unix time routines, compile   */
/*           successful under SunOS 5.6, time accuracy 1/60sec */
/*    ANIS:  use POSIX time routines, can compile under all    */
/*           unix and NT, time accuracy is 1sec                */
/*    NT:    use NT/Win32 multimedia routines, compile under   */
/*           NT only, time accuracy is 1ms                     */
/*           Uses NT "timeGetTime" function:                   */
/*             Header: Decl. in Mmsystem.h; include Windows.h. */
/*             Library: Use Winmm.lib.                         */
/***************************************************************/

#define UNIX 1
/* #define ANSI 1 */
/* #define NT 1 */

#ifdef UNIX
#include <sys/time.h>
#include <sys/times.h>
#endif
#ifdef NT
#include <mmsystem.h>
#include <time.h>
#include <windows.h>
#endif
#ifdef ANSI
#include <sys/time.h>
#endif
#ifndef CLK_TCK
#define CLK_TCK 60
#endif

#ifndef UNIX /* ANSI or NT */
#define random() rand()
#define srandom(seed) srand(seed)
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TRUE 1
#define FALSE 0
#define MAX_CLEN 1000
#define CNF_style 0
#define F_style 1
#define KF_style 2

int nvars, nclauses;
int clen;
int style;
unsigned int seed;

unsigned int newseed()
{
    unsigned int seed;
#ifdef UNIX
    struct timeval tv;
    unsigned sec, usec;
    struct timezone tzp;
#else
    time_t long_time; /* elapsed time in seconds since 1970/01/01,00:00 */
#endif

#ifdef UNIX
    gettimeofday(&tv, &tzp);
    sec = tv.tv_sec;
    usec = tv.tv_usec;
    seed = (((sec & 3) << 20) | (usec << 22) | usec) & 0x7FFFFFFF;
#else
    time(&long_time); /* Get time as long integer. */
    seed = long_time;
#endif

    return seed;
}

void help()
{
    fprintf(stderr, "Bad arguments\n");
    fprintf(stderr, "Use: makecnf [-seed N] [-cnf] [-f] [-kf] clen nvars nclauses\n");
    exit(-1);
}

int flip()
{
    if (random() % 1000 < 500)
        return 0;
    return 1;
}

void scanoneu(int argc, char *argv[], int i, unsigned int *varptr)
{
    if (i >= argc)
        help();
    if (sscanf(argv[i], " %u", varptr) != 1)
        help();
}

void generate_wff()
{
    int i, j, k;
    int cl[MAX_CLEN];
    int lit;
    int dup;

    if (style == CNF_style) {
        printf("c seed= %u\np cnf %d %d\n", seed, nvars, nclauses);
    } else if (style == KF_style) {
        printf("%d %d\n", nvars, nclauses);
    }

    for (i = 1; i <= nclauses; i++) {
        for (j = 0; j < clen; j++) {
            do {
                lit = random() % nvars + 1;
                dup = FALSE;
                for (k = 0; k < j; k++)
                    if (lit == cl[k])
                        dup = TRUE;
            } while (dup);
            cl[j] = lit;
        }
        for (j = 0; j < clen; j++)
            if (flip())
                cl[j] *= -1;

        if (style == CNF_style) {
            for (j = 0; j < clen; j++)
                printf("%d ", cl[j]);
            printf("0\n");
        } else if (style == F_style) {
            printf("%d", cl[0]);
            for (j = 1; j < clen; j++)
                printf(" %d", cl[j]);
            printf("\n");
        } else if (style == KF_style) {
            printf("%d", j);
            for (j = 0; j < clen; j++)
                printf(" %d", cl[j]);
            printf("\n");
        }
    }

    if (style == F_style) {
        printf("%%\n0\n");
    }
}

int main(int argc, char *argv[])
{
    int i;
    static int *argptrs[] = {&clen, &nvars, &nclauses};
    int currarg;

    seed = newseed();
    currarg = 0;
    style = F_style;

    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-seed") == 0)
            scanoneu(argc, argv, ++i, &seed);
        else if (strcmp(argv[i], "-cnf") == 0)
            style = CNF_style;
        else if (strcmp(argv[i], "-f") == 0)
            style = F_style;
        else if (strcmp(argv[i], "-kf") == 0)
            style = KF_style;
        else if (currarg >= 3 || sscanf(argv[i], " %d", argptrs[currarg++]) != 1)
            help();
    }
    if (currarg != 3)
        help();

    fprintf(stderr, "    makewff: seed is %u\n", seed);

    srandom(seed);

    generate_wff();

    return 0;
}
