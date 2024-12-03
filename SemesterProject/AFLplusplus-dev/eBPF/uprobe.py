#!/usr/bin/python3
from bcc import BPF
import sys

# Validate arguments, it expects binary and the function name"symbol"
if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <binary_path> <symbol>")
    sys.exit(1)

# Extract arguments
binary_path = sys.argv[1]
symbol = sys.argv[2]

# Define the eBPF program
program = f"""
int trace_function(struct pt_regs *ctx) {{
    bpf_trace_printk("Function {symbol} called!\\n");
    return 0;
}}
"""

# Initialize BPF
b = BPF(text=program)

# Attach to the specified symbol in the binary
try:
    b.attach_uprobe(name=binary_path, sym=symbol, fn_name="trace_function")
except Exception as e:
    print(f"Failed to attach to symbol '{symbol}' in binary '{binary_path}': {e}")
    sys.exit(1)

# Print trace output
print(f"Tracing {symbol}. Run your program. Hit Ctrl+C to stop.")
b.trace_print()