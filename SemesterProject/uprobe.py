#!/usr/bin/python3
from bcc import BPF

program = r"""
int hello(struct pt_regs *ctx) {
 bpf_trace_printk("Hello World!");
 return 0;
}
"""
# Initialize BPF
b = BPF(text=program)

# Attach to the symbol `my_function` in the `test` binary
binary_path = "/home/semester/semester_project/hello"
symbol = "hello_world"
syscall = b.get_syscall_fnname("execve")
b.attach_uprobe(name=binary_path, sym=symbol, fn_name="hello")

# Print trace output
print("Tracing my_function. Run your program. Hit Ctrl+C to stop.")
b.trace_print()