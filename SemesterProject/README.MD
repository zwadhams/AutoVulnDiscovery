## Frida Example
The Frida Example directory contains the compiled files necessary for a run of AFL++ in frida mode. <br>

## angr
The angr directory contains the same files, but compiled without some optimizations that stripped function symbols. It contains instructions for installing angr and generating a control flow graph for the afl-fuzz binary.

## AFLplusplus-dev
The AFLplusplus-dev folder contains the AFL++ code. This is a provisional setup. When we are ready we will make our extensions to the AFL++ project through our fork of the project and then make a pull request to the project's maintainers. We use this setup to make our changes and build the project and make sure we are not breaking the project. The changes are being mirrored in the forked repo.

To build, within the AFLplusplus-dev folder run:
```
sudo apt update\
sudo apt install python3-pip\
pip3 install frida-tools\
sudo apt-get install -y ninja-build automake autoconf\
sudo make distrib
```
Check if the compilation was successful:
```
./afl-fuzz --version
```

Note: at this point, the eBPF functionality is built independently.

Redirect core dumps (This needs to be done at the start of every terminal session):
```
sudo sh -c 'echo core >/proc/sys/kernel/core_pattern'
```

## eBPF
Please see README in directory.
