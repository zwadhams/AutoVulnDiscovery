# README
This repository contains two projects that are intentionally vulnerable to common security exploits, showcasing different attack techniques.


## Buffer Overflow
A buffer overflow occurs when a program writes more data to a memory buffer than it can hold. This overflow can overwrite adjacent memory, potentially allowing an attacker to:  
  
Alter the program's execution flow.  
  -Change the return address of functions.  
Crash the application.  
Inject and execute malicious code.  

## Command Injection  
Command injection happens when an attacker is able to execute arbitrary commands on the host operating system. This vulnerability arises when user inputs are  
 improperly sanitized before being passed to a system shell. As a result, an attacker can:  

Execute unintended commands on the host system.  
Gain unauthorized access or control over system resources.  
Cause significant damage to the system and data.  

## Notes
These examples are provided for educational purposes to demonstrate how such vulnerabilities can be exploited and how they can be mitigated.  
