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
python3 client.py
```

The next step is to create a template for the same message using Jinja2. Reference:<br />
https://realpython.com/primer-on-jinja-templating/ <br /><br />

We probably want the template to have the required words (HELO, MAIL FROM:, ... and such) And then generate the values that we are sending with those keywords, as well as the body of the email.<br />

Two initial ideas that come to mail to try to crash the server are:<br/>
- Send the email to many recipients
- make the body of the email very long

We'l have to think about more.
