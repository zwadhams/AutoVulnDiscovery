# Frida Example
The Frida Example directory contains the compiled files necessary for a run of AFL++. <br>

# angr
The angr directory contains the same files, but compiled without some optimizations that stripped function symbols. It contains instructions for installing angr and generating a control flow graph for the afl-fuzz binary.

# AFLplusplus-dev
The AFLplusplus-dev folder contains the AFL++ code. \
Here are instructions to set up and test AFL++

within the AFLplusplus-dev folder run:
```
sudo apt update\
sudo apt install python3-pip\
pip3 install frida-tools\
sudo apt-get install -y ninja-build automake autoconf\
sudo make distrib
```
Check if the compilation was successful:
```
./afl-fuzz -O frida_mode --version
```

Redirect core dumps (This needs to be done at the start of every terminal session):
```
sudo sh -c 'echo core >/proc/sys/kernel/core_pattern'
```

# eBPF
Please see README in directory.
