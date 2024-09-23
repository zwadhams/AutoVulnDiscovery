## Beginning

The server can be, the file voidsmtpd, can be started with:
```
./voidsmtpd
```

The reference for the SMTP protocol is the wikipedia page:<br />
https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol <br/>
<br/>

In another terminal, you can runthe client with:
```
python3 client4.py
```

This client is generating random email addresses to the server.<br/>
It is running on a loop (right now it is sending ten messages).<br/>
I'm just using Python f-strings (Jinja2 templates had been mentioned, but maybe that is not necessary.)<br/>



To crash the server, two initial ideas that come to mail to try to crash the server are:<br/>
- Send the email to many recipients<br/>
- make the body of the email very long<br/>

We'l have to think about more.<br/>
