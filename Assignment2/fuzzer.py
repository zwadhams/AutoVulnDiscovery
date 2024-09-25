import socket
import logging
import time
import random
import string
import subprocess
import threading
from multiprocessing import pool

number_of_threads = 10

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

def send_email(input_dictionary, port_number):
    server = "localhost"
    port = port_number
    logging.info(f"Connecting to server {server} on port {port}")
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

def start_servers(port_numbers):
    if len(port_numbers) < 1:
        raise ValueError("port_numbers must contain at least 10 ports")

    for i in range(10):
        port = port_numbers[i]
        thread = threading.Thread(target=run_voidsmtpd, args=(port,))
        thread.start()

def run_voidsmtpd(port):
    try:
        logging.info(f"Starting voidsmtpd on port {port}")
        with open(f"voidsmtpd_{port}.log", "w") as log_file:
            subprocess.run(["./voidsmtpd", str(port)], stdout=log_file, stderr=log_file, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"voidsmtpd failed on port {port} with error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred on port {port}: {e}")

def send_email_wrapper(args):
    input_data, port = args
    send_email(input_data, port)


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("starting smtp server")
    port_numbers = [9025, 9026, 9027, 9028, 9029, 9030, 9031, 9032, 9033, 9034]
    start_servers(port_numbers)
    # Delay to ensure the server has time to start
    time.sleep(5)

    logging.info("Starting the telnet client")

    input_list = []
    for i in range(100):
        inputDictionary = create_message()
        input_list.append(inputDictionary)

    # Create a list of input data with ports
    input_data_with_ports = [(input_data, port) for input_data in input_list for port in port_numbers]

    with pool.Pool(number_of_threads) as p:
        p.map(send_email_wrapper, input_data_with_ports)

main()