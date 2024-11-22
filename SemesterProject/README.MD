The Frida Example directory contains the compiled files necessary for a run of AFL++. <br>

The angr directory contains the same files, but compiled without some optimizations that stripped function symbols. It contains instructions for installing angr and generating a control flow graph for the afl-fuzz binary.

The AFLplusplus-dev folder contains the AFL++ code. \
Here are instructions to set up and test AFL++

sudo apt update\
sudo apt install python3-pip\
pip3 install frida-tools\
sudo apt-get install -y ninja-build automake autoconf\
sudo make distrib

Check if the compilation was successful:\
./afl-fuzz -O frida_mode --version

The /proc/sys/kernel/core_pattern file defines the naming and location of core dumps.\
AFL++ is warning that your system’s core dump handling configuration (/proc/sys/kernel/core_pattern) may interfere with its ability to detect crashes properly. Here’s what’s happening and how to address it:

Explanation\
AFL++ uses core dumps to detect crashes, but your system is currently configured to send core dumps to an external utility or file path, likely via a pipe (|). This setup delays AFL++ from receiving crash information because it has to wait for the external utility to process the core dump.\
AFL++ expects core dumps to be handled locally (not redirected to an external utility), allowing it to quickly access crash information via the waitpid() API.\
Option 1: Change the core_pattern Temporarily\
You can adjust the core dump pattern to work locally by setting it to simply core. Run the following command as root:\
sudo sh -c 'echo core >/proc/sys/kernel/core_pattern'\
(This needs to be done at the start of every terminal session)
