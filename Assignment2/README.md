## Beginning


The reference for the SMTP protocol is the wikipedia page:<br />
https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol <br/>
<br/>

You can run the fuzzer with:
```
python3 fuzzer2.py
```

This fuzzer is generating random email addresses and sending them to the server.<br/><br />

It saves a set of inputs (messages to be sent to the server) to a List.<br/>
Then it creates 10 servers threads. <br />
Each server has a log file whose name ends with the port number used by the server. Note: I got a warning from github that these log files are larger than the recommended size for a repo. (One of them is 87 MB long). Is something that needs stream lining. I added the log file to the .gitignore so they won't be commited.<br/>
Multiprocessing is implemented as something called a Pool where we specify the 
number of client threads that we want. We are creating a different thread for each 
send request. Right now we have ten clients and are sending a hundred requests. But we can do as many as we want. <br />

There is a map function that receives a send_email_wrapper function as an argument, as well as the list that contains the inputs that were generated. This wrapper function was created because the map function can not take a function as an argument that in turn needs to take another argument. I wanted to pass a different port to each call of the send_email function. Thus the wrapper.
This map function will pass an input from the list and a port number to each instance of the send function.<br/> <br />

I'm just using Python f-strings to substitute values in the send_email function. (Jinja2 templates had been mentioned, but maybe that is not necessary.)<br/>



## TODOs
We need to:<br/>
-  log the client's outputs to files whose name id's the input.<br/>
-  As mentioned above, we have to stream line the server logs. Right now they are logging everything to a single file. We need to be able to id to which input does a log entry belong.<br/>
-  We want ot be able to match a particular log of an input on the client side with a particular log of an output on the server side. This will probably be to different files that we will mtach by the input id (which we should use in the filename).<br/>
To crash the server, two initial ideas that come to mail to try to crash the server are:<br/>
- Send the email to many recipients<br/>
- make the body of the email very long<br/>

Here are a few more things to try:.<br/>
- String Mutations: Change lengths, introduce special characters, unicode, overly long inputs, etc.<br/>
- Field Injection: Insert SMTP commands or headers inside other fields.<br/>
- Malformed Inputs: Use invalid email addresses, missing angle brackets, broken headers, or invalid MIME types.<br/>
- Boundary Testing: Test minimum and maximum length constraints for each field.<br/>
- Command Sequences: Experiment with illegal command sequences or skipping mandatory steps (e.g., sending DATA before MAIL FROM).<br/>'

Heres what I tried already: 

crash2.py do not edit, it's the exact config that got me the second crash. I used random.seed() to recreate results. 
Tried and didn't work: 
I have messed with the date inputs, making them invalid etc. 
multiple emails cc, to and from
from and rcpt check for valid address, cc doesn't 
I tried removing or changing the order of smpt commands (FROM etc) these cases are handled. 

