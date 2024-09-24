## Beginning


The reference for the SMTP protocol is the wikipedia page:<br />
https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol <br/>
<br/>

You can run the fuzzer with:
```
python3 fuzzer.py
```

This fuzzer is generating random email addresses to the server.<br/>
It saves a set of inputs (messages to be sent to the server) to a file.<br/>
Then it creates the server as a subprocess in a thread. LAter we'll be able to read what is happening with this subprocess.<br />
Multiprocessing is implemented as something called a Pool where we specify the 
number of threads that we want. We are creating a different thread for each 
send request. Later we will probably have to create more instances of the server also. There is a map function that receives the send function as an argument, as well as a file that contains the inputs that were generated.
This map function will pass an input from the list inside the file to each instance of the send function.<br/> <br />

I'm just using Python f-strings (Jinja2 templates had been mentioned, but maybe that is not necessary.)<br/>



To crash the server, two initial ideas that come to mail to try to crash the server are:<br/>
- Send the email to many recipients<br/>
- make the body of the email very long<br/>

We'l have to think about more.<br/>
