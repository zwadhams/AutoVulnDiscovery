import socket
import logging
import time
from jinja2 import Template


# Function to escape dots at the beginning of lines
def escape_dots(body):
    lines = body.split("\n")
    escaped_lines = []
    for line in lines:
        if line.startswith("."):
            escaped_lines.append("." + line)
        else:
            escaped_lines.append(line)
    return "\n".join(escaped_lines)

def send_and_log(s, data):
    logging.info(f"Sending: {data}")
    s.send(data)
    time.sleep(0.1)  # Add a small delay to ensure the server processes the data



# Email body
body = """Hello Alice.
This is a test message with 5 header fields and 4 lines in the message body.
Your friend,
Bob"""

    # Escape dots in the body
escaped_body = escape_dots(body)


template_str = """
HELO {{ helo_value }}\r\n
MAIL FROM: {{ from_value }}\r\n
RCPT TO: {{ to_value }}\r\n
DATA\r\n
Subject: {{ subject_value }}\r\n
\r\n  # End of headers
{{ body_value }}
\r\n.\r\n
"""

template = Template(template_str)

fuzzed_input = template.render(
    helo_value="example.com",
    from_value="fuzz@test.com",
    to_value="victim@test.com",
    subject_value="Testing the fuzzer",
    body_value="This is a test message\r\n"
)



def send_email():
    server = "localhost"
    port = 2525
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, port))
    response = s.recv(1024)
    logging.info(f"Received: {response.decode().strip()}")

    # Send the HELO command
    '''send_and_log(s, "HELO relay.example.org\r\n".encode())
    response = s.recv(1024)
    logging.info(f"Received: {response.decode().strip()}")

    # Send the MAIL FROM command
    send_and_log(s, "MAIL FROM:<bob@example.org>\r\n".encode())
    response = s.recv(1024)
    logging.info(f"Received: {response.decode().strip()}")

    # Send the RCPT TO commands
    send_and_log(s, "RCPT TO:<alice@example.com>\r\n".encode())
    response = s.recv(1024)
    logging.info(f"Received: {response.decode().strip()}")

    send_and_log(s, "RCPT TO:<theboss@example.com>\r\n".encode())
    response = s.recv(1024)
    logging.info(f"Received: {response.decode().strip()}")

    # Send the DATA command
    send_and_log(s, "DATA\r\n".encode())
    response = s.recv(1024)
    logging.info(f"Received: {response.decode().strip()}")

    # Email body
    body = """Hello Alice.
This is a test message with 5 header fields and 4 lines in the message body.
Your friend,
Bob"""

    # Escape dots in the body
    escaped_body = escape_dots(body)

    # Construct the entire message
    message = (
        "From: \"Bob Example\" <bob@example.org>\r\n"
        "To: \"Alice Example\" <alice@example.com>\r\n"
        "Cc: theboss@example.com\r\n"
        "Date: Tue, 15 Jan 2008 16:02:43 -0500\r\n"
        "Subject: Test message\r\n"
        "\r\n"  # End of headers
        + escaped_body +
        "\r\n.\r\n"  # End of data
    )

    # Send the entire message in smaller chunks
    for line in message.splitlines(True):
        send_and_log(s, line.encode())'''

    for line in fuzzed_input.splitlines(True):
        send_and_log(s, line.encode())

    logging.info("Sent email body and end of data sequence")

    response = s.recv(1024)
    logging.info(f"Received: {response.decode().strip()}")

    # Send the QUIT command
    send_and_log(s, "QUIT\r\n".encode())
    response = s.recv(1024)
    logging.info(f"Received: {response.decode().strip()}")

    s.close()

logging.basicConfig(level=logging.INFO)
logging.info("Starting the telnet client")
#logging.info(fuzzed_input)
#print(type(fuzzed_input))
send_email()