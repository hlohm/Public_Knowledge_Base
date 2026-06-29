---
type: cheatsheet
area: "Programming Languages"
aliases: [C language, C99, C11]
tags: [c, programming, systems, pointers, memory]
status: working
---

# C

> **Area:** [[Programming Languages]]

C99/C11 reference — the things you forget and the traps that bite. Assumes you can read C already; this is a reminder and a gotcha list, not a tutorial.

---

## 1. Compile and build

```sh
# Compile a single file
gcc -std=c11 -Wall -Wextra -Wpedantic -o myapp main.c

# Recommended flags for development:
gcc -std=c11 -Wall -Wextra -Wpedantic -g -fsanitize=address,undefined -o myapp main.c
# -g                     debug symbols (for gdb)
# -fsanitize=address     AddressSanitizer: detect buffer overflows, use-after-free
# -fsanitize=undefined   UBSan: catch undefined behaviour at runtime

# Optimization (for release):
gcc -std=c11 -O2 -DNDEBUG -o myapp main.c

# Multiple source files
gcc -std=c11 -Wall -c utils.c -o utils.o
gcc -std=c11 -Wall -c main.c -o main.o
gcc utils.o main.o -o myapp

# Link libraries
gcc main.o -lm -lpthread -o myapp    # math, pthreads

# Show preprocessor output
gcc -E main.c
```

## 2. Types and sizes

```c
/* Exact-width types (include <stdint.h>) */
int8_t   int16_t  int32_t  int64_t     /* signed */
uint8_t  uint16_t uint32_t uint64_t    /* unsigned */
size_t                                  /* sizeof result; use for array sizes */
ptrdiff_t                               /* pointer difference */
intptr_t uintptr_t                      /* integer that can hold a pointer */

/* Platform-dependent widths (avoid for portable code) */
char    1 byte (signed or unsigned — implementation-defined)
short   ≥ 2 bytes
int     ≥ 2 bytes (typically 4)
long    ≥ 4 bytes (8 on 64-bit Linux; 4 on Windows 64-bit)
long long ≥ 8 bytes

/* Limits (include <limits.h> / <stdint.h>) */
INT_MAX, INT_MIN, UINT_MAX
INT32_MAX, UINT64_MAX
SIZE_MAX    /* maximum size_t */

/* Check size */
printf("int: %zu bytes\n", sizeof(int));
```

## 3. Pointers

```c
int  x = 42;
int *p = &x;    /* p holds the address of x */
*p = 99;        /* dereference: set x to 99 */

/* Pointer arithmetic */
int arr[] = {10, 20, 30};
int *q = arr;   /* arr decays to &arr[0] */
*(q + 1)        /* same as arr[1] = 20 */
q++;            /* advance by sizeof(int) */

/* Pointers and const */
const int *cp    = &x;   /* pointer to const int: can't modify *cp */
int * const pc   = &x;   /* const pointer to int: can't change pc itself */
const int * const cpc = &x;  /* both const */

/* NULL and void* */
int *p = NULL;            /* null pointer — always initialize */
void *vp = malloc(n);     /* void*: generic pointer; cast when using */
int  *ip = (int *)vp;

/* Function pointers */
int (*cmp)(const void *, const void *);   /* declare */
cmp = mycompare;                          /* assign */
qsort(arr, n, sizeof(int), mycompare);    /* pass to function */
```

## 4. Memory management

```c
#include <stdlib.h>

/* Allocate */
int *arr = malloc(n * sizeof(int));            /* uninitialized */
int *arr = calloc(n, sizeof(int));             /* zero-initialized */
arr = realloc(arr, new_n * sizeof(int));       /* resize */

/* Always check */
if (arr == NULL) { perror("malloc"); exit(1); }

/* Free (only once; set to NULL afterwards to catch use-after-free) */
free(arr);
arr = NULL;

/* VLA (C99) — stack allocation; dangerous for large or unknown sizes */
int n = get_count();
int arr[n];              /* stack; no free needed but stack overflow if n is large */

/* Stack vs heap rule of thumb:
   - Known, small size → stack (local variables)
   - Unknown or large size → heap (malloc/calloc)
   - Long lifetime (beyond function) → heap */
```

## 5. Strings

```c
#include <string.h>

/* C strings are null-terminated char arrays */
char s[50] = "hello";          /* buffer on stack */
char *sp   = "literal";        /* pointer to string literal — read-only! */

/* Safe copy (destination must be large enough) */
strncpy(dst, src, sizeof(dst) - 1);
dst[sizeof(dst) - 1] = '\0';   /* strncpy may not null-terminate */

/* Even safer: use snprintf */
snprintf(dst, sizeof(dst), "%s", src);
snprintf(dst, sizeof(dst), "%s %s", first, last);

/* Common operations */
strlen(s)                       /* length (not counting \0) */
strcmp(a, b)                    /* 0 if equal, <0 / >0 otherwise */
strncmp(a, b, n)                /* compare at most n chars */
strchr(s, 'c')                  /* pointer to first 'c' or NULL */
strstr(haystack, needle)        /* pointer to first occurrence or NULL */
strtok(s, ",")                  /* split (mutates s — use strtok_r for threads) */

/* AVOID — no bounds checking */
strcpy(dst, src);               /* use strncpy or snprintf instead */
gets(s);                        /* removed in C11; use fgets instead */
sprintf(s, fmt, ...);           /* use snprintf */
```

## 6. Structs

```c
/* Define */
typedef struct {
    int x;
    int y;
} Point;

typedef struct Node {
    int value;
    struct Node *next;    /* self-referential: must use struct Node here */
} Node;

/* Use */
Point p = { .x = 1, .y = 2 };   /* designated initializer (C99) */
p.x = 10;

/* Pointer to struct */
Point *pp = &p;
pp->x = 5;       /* equivalent to (*pp).x = 5 */

/* Dynamic allocation */
Node *node = malloc(sizeof(Node));
node->value = 42;
node->next = NULL;
free(node);
```

## 7. Header file pattern

```c
/* mymodule.h */
#ifndef MYMODULE_H      /* include guard — prevents double inclusion */
#define MYMODULE_H

#include <stdint.h>

typedef struct {
    int id;
    char name[64];
} Record;

int  record_init(Record *r, int id, const char *name);
void record_print(const Record *r);

#endif /* MYMODULE_H */
```

```c
/* mymodule.c */
#include "mymodule.h"
#include <stdio.h>
#include <string.h>

int record_init(Record *r, int id, const char *name) {
    r->id = id;
    snprintf(r->name, sizeof(r->name), "%s", name);
    return 0;
}

void record_print(const Record *r) {
    printf("Record %d: %s\n", r->id, r->name);
}
```

## 8. Undefined behaviour — top traps

```c
/* 1. Signed integer overflow (undefined; use uint or check first) */
int x = INT_MAX;
int y = x + 1;              /* UB — may wrap, may not */

/* 2. Out-of-bounds array access */
int arr[5];
arr[5] = 1;                  /* UB — one past the end */

/* 3. Use-after-free */
free(p);
*p = 1;                      /* UB */

/* 4. Null pointer dereference */
int *p = NULL;
*p = 1;                      /* UB (and crash on most platforms) */

/* 5. Uninitialized read */
int x;
printf("%d\n", x);           /* UB */

/* 6. Strict aliasing violation */
float f = 1.0f;
int *ip = (int *)&f;         /* UB; use memcpy for type punning */
int n; memcpy(&n, &f, sizeof n);   /* correct */

/* 7. Modifying a string literal */
char *s = "hello";
s[0] = 'H';                  /* UB; declare as char s[] = "hello"; */
```

---

## Daily workflows

### "Run with sanitizers enabled"
```sh
gcc -std=c11 -g -fsanitize=address,undefined -o prog main.c && ./prog
# AddressSanitizer prints detailed reports on memory errors
```

### "Debug with gdb"
```sh
gcc -std=c11 -g -O0 -o prog main.c
gdb ./prog
(gdb) run
(gdb) backtrace
(gdb) frame 2
(gdb) print myvar
```

## Gotchas / Golden rules

1. **`sizeof` is a compile-time operator, not a function** — `sizeof arr / sizeof arr[0]` gives the element count for stack arrays, but fails silently when `arr` decays to a pointer (function parameter).
2. **`char` signedness is implementation-defined** — never compare `char` to `EOF` (-1) directly; use `unsigned char` or cast.
3. **Pointer arithmetic is only valid within an array** — incrementing a pointer past `&arr[n]` (one-past-end) is the only legal "out-of-bounds" pointer; dereferencing it is UB.
4. **`malloc` does not zero memory** — always initialize, or use `calloc` for zero-fill.
5. **`realloc` may return a new pointer** — always assign the return value; never `realloc(ptr, ...)` into the same variable without checking for `NULL` first (the old allocation is freed on `NULL` return).
