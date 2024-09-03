Example: https://thesquareplanet.com/blog/smashing-the-stack-21st-century/ <br />


Commands: <br />
```
cc -m64 -c -o shellcode.o shellcode.S
objcopy -S -O binary -j .text shellcode.o shellcode.bin
gcc -g -fno-stack-protector -z execstack vulnerable.c -o vulnerable -D_FORTIFY_SOURCE=0
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
env - setarch -R ./vulnerable
echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope
gdb -p $(pgrep vulnerable)
python3 exploit.py | env - setarch -R ./vulnerable
```