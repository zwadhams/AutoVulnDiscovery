## SMTP Fuzzer


The reference for the SMTP protocol is the wikipedia page:<br />
https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol <br/>
<br/>


In this assignment we fuzz a SMTP server by sending inputs of variable symbols and lengths in the different fields that the protocol requires. The fuzzer is written in Python and has three classes: an InputGenerator class, a StartSMTPServers class, and a FuzzingHarness class. <br />

The StartSMTPServers class is responsible for starting the SMTP server processes. Right now, it is set to start ten servers. <br />

The InputGenerator class has the structure required for SMTP communication. Based on that structure, it varies the values that are sent with the different protocol commands, and the message body itself. <br />

The FuzzingHarness class does the actual fuzzing. It first creates an InputGenerator object and right now it is set up to create a hundred unique inputs, but it could generate as many as are needed. Each input is matched with a port number. The matching is done in a way that assures that each server receives about the same amount of requests. Once the inputs are ready, a number of threads are started (we use 10). These threads execute the send_email_wrapper method which is in charge of executing the communication with the servers. The threads keep executing this method until all inputs have been sent. <br/> 

During execution, a log file will be generated for each server. These files are named voidsmtpd_portNumber.log. They contain the message that the server sanitizer produces when the server crashes. Additionally, each individual input is saved to a smtp_interaction_fromAddress_randomInt.txt. The contents of any of these files can be sent to a server to reproduce a fuzzing run. <br/>

You can run the fuzzer with:
```
python3 fuzzer.py
```
## Results
We got crashes by varying the length of the bofy of the message, and by varying the length of the value for the CC field in the protocol commands. <br/>

To generate random length body: <br/>
Comment body variable and the call to escape_dots that follows it. Then uncomment the call to random body and up to the call to escape_dots. Then run the fuzzer. After an interruption in one of the execution of the servers, you can hit control + c to stop everything. To look for a crash message from the sanitizer you can run:
```
grep -i "sanitizer" voidsmtpd_*.log
```
From the results, you can open any log file that has a sanitizer crash message and look for it. Look for the from address, and the you can locate the smtp_interaction_fromAddress_randomInt.txt file that produced the particular crash. <br/>

To generate random to and cc random values:<br/>
Use the fixed body value (comment out the generate random body that we had turned on before). Use the generatey and generatex methods in the create message method fot the to_address and cc_address fields, respectively. The rest of the process is the same as before.<br/>
