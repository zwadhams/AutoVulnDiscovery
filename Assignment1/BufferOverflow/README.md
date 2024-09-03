## Example: 
https://thesquareplanet.com/blog/smashing-the-stack-21st-century/ <br />


## Commands: <br />
Compile the shellcode:
```
cc -m64 -c -o shellcode.o shellcode.S
objcopy -S -O binary -j .text shellcode.o shellcode.bin
```
Compile the vulnerable program without stack protection (canary) and allowing the stack to be executable:
```
gcc -g -fno-stack-protector -z execstack vulnerable.c -o vulnerable -D_FORTIFY_SOURCE=0
```
Turn off address randomization:
```
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
```
Command to run without address randomization:
```
env - setarch -R ./vulnerable
```
Allow the program to be traced:
```
echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope
```
Get the process id of the vulnerable program and attach GDB to it:
```
gdb -p $(pgrep vulnerable)
```
In GDB you want to set at break point at first128, and the get the address of the buffer and the return address:
```
b first128
c
p &buffer
info frame
```
Adjust the values in the Python script and run the exploit:
```
python3 exploit.py | env - setarch -R ./vulnerable
```
It appears that nothing is happening, but you can start executing shell commands.
