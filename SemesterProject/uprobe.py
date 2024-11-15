#!/usr/bin/python3
from bcc import BPF

program = r"""
int trace_main(struct pt_regs *ctx) {
 bpf_trace_printk("main called!\\n");
 return 0;
}
"""
# Initialize BPF
b = BPF(text=program)
# Attach to the symbol `my_function` in the `test` binary
binary_path = "./hello"
symbol = "main"
syscall = b.get_syscall_fnname("execve")
b.attach_uprobe(name=binary_path, sym=symbol, fn_name="trace_main")

# Print trace output
print("Tracing my_function. Run your program. Hit Ctrl+C to stop.")
b.trace_print()
