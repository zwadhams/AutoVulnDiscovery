## Example: 
https://thesquareplanet.com/blog/smashing-the-stack-21st-century/ <br />

## Exploiting a simple UDP server
To illustrate the buffer overflow attack, we created a simple UDP server and declared a buffer to store client messages (udp_server.c):<br /><br />
char buffer[100];<br /><br />
Next, we didn't follow best practices and allowed a vulnerability to occur in the recvfrom() function that the server is running to read messages from the client:<br /><br />
recvfrom(sockfd, buffer, 1000, 0, (struct sockaddr*)&client_addr,&client_addr_len); <br /><br /><br />
Good programming practices requires the thrid argument to this function to be sizeof(buffer). Instead, the function has a hardcoded value of 1000 bytes which in this case creates the buffer overflow vulnerability as that the number of bytes to be written to the buffer can be more than the memory allocated to the buffer.<br /><br />

To exploit the buffer overflow we want to overwrite the precise address. For this, we needed the exact starting addres in memory for the buffer, and we needed the precise location where the return address was stored. Precision is key. You have to know exactly how many bytes need to be written from the beginning of the buffer and up to the return address. In our approach, we wanted to place the exploit at the beginning of the buffer and then jump from the return address to the beginning of the buffer so that the exploit executes. Since we have to be precise in the number of bytes written so that we don't miss the exact location of the return address, we need to know the precise size of our exploit. To do this, we took code to execute a shell written in x86-64 assembly language and compiled it in a way that stripped symbols and just kept the essential instructions. This made the exploit smaller and allowed us to know it's exact size in bytes. The x86-64 assembly code was taken from the example linked above as well as the skeleton for exploit.py file which copies the shellcode from a file.  <br /><br />

We next needed to know the starting address for the server buffer and the return address for the main function. To get these values we  ran the server and attached GDB to the running process. We set a break point at recvfrom and the sent a bening message to the server. The buffer belongs to the main function frame. A reference to the buffer is passed to the recvfrom function and the buffer is written in main's frame. When recvfrom returns, we use  p &buffer to get the starting addres of the buffer and infor frame to get the return addres "rip at ...". Our exploit overwrites the return address of main.<br /><br/>

Once we had the addresses, we could calculate the amount of bytes between the address, subtract the length of the shellcode and the difference was the amount of padding that we needed to add. after that, we just needed to add simple socket functionality to the exploit, and it was ready to execute.<br />


    
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
Make sure the udp_Server file has execution permissions:
```
sudo chmod +x udp_server
```
Command to run without address randomization:
```
env - setarch -R ./udp_server
```
The intended functionality can be seen by going into another terminal and running:
```
sudo chmod +x simple_client.py
python3 simple_client.py
```
The cllient asks the server for the labs address, and the server returns it.<br />
Now, to exploit the vulnerability:
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
The return address is "rip at ...". Adjust the values in the Python script and restart the server:
```
env - setarch -R ./udp_server
```
Make sure your exploit has execute permissions:
```
sudo chmod +x udp_server
```
Run the exploit in another terminal:
```
python3 exploit.py
```
You can start executing shell commands in the server terminal. <br />
