import socket
import logging
import time
import random
import string
import subprocess
import threading

def generate_random_email():
    def random_string(length):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    username = random_string(random.randint(5, 10))
    domain = random_string(random.randint(5, 10))
    tld = random.choice(['com', 'org', 'net', 'edu', 'gov'])
    
    return f"{username}@{domain}.{tld}"


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

def send_email(input_dictionary):
    server = "localhost"
    port = 2525
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, port))
    response = s.recv(1024)
    logging.info(f"Received: {response.decode().strip()}")

    # Send the HELO command
    send_and_log(s, f"HELO {input_dictionary['from_address']}\r\n".encode())
    response = s.recv(1024)
    logging.info(f"Received: {response.decode().strip()}")

    # Send the MAIL FROM command
    send_and_log(s, f"MAIL FROM:<{input_dictionary['from_address']}>\r\n".encode())
    response = s.recv(1024)
    logging.info(f"Received: {response.decode().strip()}")

    # Send the RCPT TO commands
    send_and_log(s, f"RCPT TO:<{input_dictionary['to_address']}>\r\n".encode())
    response = s.recv(1024)
    logging.info(f"Received: {response.decode().strip()}")

    send_and_log(s, f"RCPT TO:<{input_dictionary['cc_address']}>\r\n".encode())
    response = s.recv(1024)
    logging.info(f"Received: {response.decode().strip()}")

    # Send the DATA command
    send_and_log(s, "DATA\r\n".encode())
    response = s.recv(1024)
    logging.info(f"Received: {response.decode().strip()}")

    # Send the entire message in smaller chunks
    for line in input_dictionary['message'].splitlines(True):
        send_and_log(s, line.encode())

    logging.info("Sent email body and end of data sequence")

    response = s.recv(1024)
    logging.info(f"Received: {response.decode().strip()}")

    # Send the QUIT command
    send_and_log(s, "QUIT\r\n".encode())
    response = s.recv(1024)
    logging.info(f"Received: {response.decode().strip()}")

    s.close()


def create_message():
    input_dictionary = {}
    from_address = generate_random_email()
    input_dictionary["from_address"] = from_address
    to_address = generate_random_email()
    input_dictionary["to_address"] = to_address
    cc_address = generate_random_email()   
    input_dictionary["cc_address"] = cc_address
    date = "Tue, 15 Jan 2008 16:02:43 -0500"
    input_dictionary["date"] = date
    subject = "Test message"
    input_dictionary["subject"] = subject
    body = """Hello Alice.  This is a test message with 5 header fields and 4 lines in the message body.  Your friend, Bob"""   
    input_dictionary["body"] = body
    escape_dots(input_dictionary["body"])

    message = (
        f"From: \"Bob Example\" <{input_dictionary['from_address']}>\r\n"
        f"To: \"Alice Example\" <{input_dictionary['to_address']}>\r\n"
        f"Cc: {input_dictionary['cc_address']}\r\n"
        f"Date: {input_dictionary['date']}\r\n"
        f"Subject: {input_dictionary['subject']}\r\n"
        "\r\n"  # End of headers
        f"{input_dictionary['body']}\r\n"
        "\r\n.\r\n"  # End of data
    )
    input_dictionary["message"] = message

    return input_dictionary

logging.basicConfig(level=logging.INFO)
logging.info("starting smtp server")

# create thread for voidsmtpd
threading.Thread(target=subprocess.run, args=(["./voidsmtpd"],)).start()
#subprocess.run(["./voidsmtpd"])

# Delay to ensure the server has time to start
time.sleep(5)

logging.info("Starting the telnet client")

for i in range(10):
    inputDictionary = create_message()
    send_email(inputDictionary)