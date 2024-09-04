	.file	"udp_server.c"
	.text
	.section	.rodata
	.align 8
.LC0:
	.string	"Software Engineering and Cybersecurity Laboratory\nMontana State University\nSchool of Computing\nPO Box 173880\nBozeman, MT 59717\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB6:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$176, %rsp
	leaq	.LC0(%rip), %rax
	movq	%rax, -8(%rbp)
	leaq	-160(%rbp), %rax
	pxor	%xmm0, %xmm0
	movaps	%xmm0, (%rax)
	movl	$0, %edx
	movl	$2, %esi
	movl	$2, %edi
	call	socket@PLT
	movl	%eax, -12(%rbp)
	movl	$0, %edi
	call	htonl@PLT
	movl	%eax, -156(%rbp)
	movl	$7000, %edi
	call	htons@PLT
	movw	%ax, -158(%rbp)
	movw	$2, -160(%rbp)
	leaq	-160(%rbp), %rcx
	movl	-12(%rbp), %eax
	movl	$16, %edx
	movq	%rcx, %rsi
	movl	%eax, %edi
	call	bind@PLT
	movl	$16, -132(%rbp)
	leaq	-132(%rbp), %rcx
	leaq	-176(%rbp), %rdx
	leaq	-128(%rbp), %rsi
	movl	-12(%rbp), %eax
	movq	%rcx, %r9
	movq	%rdx, %r8
	movl	$0, %ecx
	movl	$1000, %edx
	movl	%eax, %edi
	call	recvfrom@PLT
	movl	%eax, -16(%rbp)
	movl	-16(%rbp), %eax
	cltq
	movb	$0, -128(%rbp,%rax)
	leaq	-128(%rbp), %rax
	movq	%rax, %rdi
	call	puts@PLT
	leaq	-176(%rbp), %rdx
	movq	-8(%rbp), %rsi
	movl	-12(%rbp), %eax
	movl	$16, %r9d
	movq	%rdx, %r8
	movl	$0, %ecx
	movl	$1000, %edx
	movl	%eax, %edi
	call	sendto@PLT
	movl	$0, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 13.2.0-23ubuntu4) 13.2.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
