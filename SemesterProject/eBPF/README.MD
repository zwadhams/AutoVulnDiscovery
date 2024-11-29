# Using uprobe to trace a function in a binary compilled with -g flag

This program consits of two parts `trace_function.sh` and `uprobe.py`. 

- `trace_function.sh` acts as a wrapper for the process and is the only part that the user need interact with. 
- `uprobe.py` is the python script that runs the uprobe trace on the selected function.

---

## Table of Contents

- [trace_function.sh](#bash script)
- [uprobe.py](#features)


## trace_function.sh

### Prerequisites

1. Make sure you have bcc tools installed:
```
sudo apt-get install linux-headers-$(uname -r) clang llvm libelf-dev libbpfcc-dev bpfcc-tools python3-bpfcc libclang-dev python3-distutils
pip install bcc
```
2. Make the script executable: `chmod +x trace_function.sh`

### Description

The `trace_function.sh` script is a wrapper that:
1. Extracts all functions from the symbol table of a given binary using `objdump -t`.
2. Presents the functions in an interactive menu for selection.
3. Passes the selected function and binary path to `uprobe.py` for tracing.

### How It Works

- Runs `objdump` to list all functions in the `.text` section of the binary.
- Prompts the user to select a function.
- Calls `uprobe.py` with the selected function and binary as arguments.

### Usage

- Run `./trace_function.sh <binary>`

---

## uprobe.py

### Features

- Uses bcc to attach an eBPF program to the specified function in the binary.
- Traces function calls dynamically and logs them in real time.
- Provides detailed trace output for debugging or performance monitoring.

### Key Components

1. **Argument Validation**: Ensures the correct number of arguments (binary path and function name) are provided.
2. **eBPF Program**: Dynamically generates and attaches a small eBPF program to trace function calls.
3. **Real-Time Output**: Prints trace logs every time the selected function is called.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.

---
