## SMTP Fuzzer


The reference for the SMTP protocol is the wikipedia page:<br />
https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol <br/>
<br/>


In this assignment we fuzz a SMTP server by sending inputs of variable symbols and lengths in the different fields that the protocol requires. The fuzzer is written in Python and has three classes: an InputGenerator class, a StartSMTPServers class, and a FuzzingHarness class. <br />

The StartSMTPServers class is responsible for starting the SMTP server processes. Right now, it is set to start ten servers. <br />

The InputGenerator class has the structure required for SMTP communication. Based on that structure, it varies the values that are sent with the different protocol commands, and the message body itself. <br />

The FuzzingHarness class does the actual fuzzing. It first creates an InputGenerator object and right now it is set up to create a hundred unique inputs, but it could generate as many as are needed. Each input is matched with a port number. The matching is done in a way that assures that each server receives about the same amount of requests. Once the inputs are ready, a number of threads are started (we use 10). These threads execute the send_email_wrapper method which is in charge of executing the communication with the servers. The threads keep executing this method until all inputs have been sent. <br/> 

You can run the fuzzer with:
```
python3 fuzzer.py
```
## Results
We got crashes by varying the length of the bofy of the message, and by varying the length of the value for the CC field in the protocol commands. 

