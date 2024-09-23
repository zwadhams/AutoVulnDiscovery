import socket
import logging
import time
import random
import string

def generate_random_email():
    def random_string(length):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    username = random_string(random.randint(5, 10))
    domain = random_string(random.randint(5, 10))
    tld = random.choice(['com', 'org', 'net', 'edu', 'gov'])
    
    return f"{username}@{domain}.{tld}"

# Example usage
print(generate_random_email())


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

def send_email():
    server = "localhost"
    port = 2525
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, port))
    response = s.recv(1024)
    logging.info(f"Received: {response.decode().strip()}")

    # Send the HELO command
    send_and_log(s, "HELO relay.example.org\r\n".encode())
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

    from_address = "bob@example.org"
    to_address = "alice@example.com"
    cc_address = "theboss@example.com"
    date = "Tue, 15 Jan 2008 16:02:43 -0500"
    subject = "Test message"

    # Construct the entire message
    message = (
        f"From: \"Bob Example\" <{from_address}>\r\n"
        f"To: \"Alice Example\" <{to_address}>\r\n"
        f"Cc: {cc_address}\r\n"
        f"Date: {date}\r\n"
        f"Subject: {subject}\r\n"
        "\r\n"  # End of headers
        f"{escaped_body}"
        "\r\n.\r\n"  # End of data
    )

    # Send the entire message in smaller chunks
    for line in message.splitlines(True):
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
#send_email()