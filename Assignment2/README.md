## Beginning


The reference for the SMTP protocol is the wikipedia page:<br />
https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol <br/>
<br/>

You can run the fuzzer with:
```
python3 fuzzer.py
```

This fuzzer is generating random email addresses and sending them to the server.<br/>
It saves a set of inputs (messages to be sent to the server) to a List.<br/>
Then it creates 10 servers threads. <br />
Each server has a log file whose name ends with the port number used by the server.<br/>
Multiprocessing is implemented as something called a Pool where we specify the 
number of client threads that we want. We are creating a different thread for each 
send request. Right now we have ten clients. We can have as many as we want. <br />

There is a map function that receives a send_email_wrapper function as an argument, as well as the list that contains the inputs that were generated. This wrpper function was created because the map function can take a function as an argument that inturns needs to take another argument. I wanted to pass a different port to each call of the send_email function. Thus the wrapper.
This map function will pass an input from the list and a port number to each instance of the send function.<br/> <br />

I'm just using Python f-strings to substitute values in the send_email function. (Jinja2 templates had been mentioned, but maybe that is not necessary.)<br/>



To crash the server, two initial ideas that come to mail to try to crash the server are:<br/>
- Send the email to many recipients<br/>
- make the body of the email very long<br/>

We'l have to think about more.<br/>
