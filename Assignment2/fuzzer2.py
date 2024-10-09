import socket
import logging
import time
import random
import string
import subprocess
import threading
from multiprocessing import pool


class InputGenerator:
    def __init__(self):
        self.input_dictionary = {}

    # Function to escape dots at the beginning of lines
    def escape_dots(self, body):
        lines = body.split("\n")
        escaped_lines = []
        for line in lines:
            if line.startswith("."):
                escaped_lines.append("." + line)
            else:
                escaped_lines.append(line)
        return "\n".join(escaped_lines)


    def create_message(self):
        from_address = self.generate_random_email()
        self.input_dictionary["from_address"] = from_address
        to_address = self.generate_random_email()
        self.input_dictionary["to_address"] = to_address
        cc_address = self.generate_random_email()   
        self.input_dictionary["cc_address"] = cc_address
        date = "Tue, 15 Jan 2008 16:02:43 -0500"
        self.input_dictionary["date"] = date
        subject = "Test message"
        self.input_dictionary["subject"] = subject

        # Creating a long random body of the email between 1000 and 5000 characters long at the moment. Change those values as you wish
        body = self.generate_random_body(random.randint(1000, 5000))
        size = len(body)
        # Un-comment the below line of code and comment the above line of code to use the default message
        #body = """Hello Alice.  This is a test message with 5 header fields and 4 lines in the message body.  Your friend, Bob"""  
        self.input_dictionary["body"] = body

        self.escape_dots(self.input_dictionary["body"])

        message = (
            f"From: \"Bob Example\" <{self.input_dictionary['from_address']}>\r\n"
            f"To: \"Alice Example\" <{self.input_dictionary['to_address']}>\r\n"
            f"Cc: {self.input_dictionary['cc_address']}\r\n"
            f"Date: {self.input_dictionary['date']}\r\n"
            f"Subject: {self.input_dictionary['subject']}\r\n"
            "\r\n"  # End of headers
            f"{self.input_dictionary['body']}\r\n"
            "\r\n.\r\n"  # End of data
        )
        self.input_dictionary["message"] = message

        return self.input_dictionary
    

    def generate_random_email(self):
        def random_string(length):
            return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        
        username = random_string(random.randint(5, 10))
        domain = random_string(random.randint(5, 10))
        tld = random.choice(['com', 'org', 'net', 'edu', 'gov'])
        
        return f"{username}@{domain}.{tld}"
    
    def generate_random_body(self, length):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))




class StartSMTPServers:
    def __init__(self):
        self.port_numbers = [9025, 9026, 9027, 9028, 9029, 9030, 9031, 9032, 9033, 9034]

    def start_servers(self):
        if len(self.port_numbers) < 1:
            raise ValueError("port_numbers must contain at least 10 ports")

        for i in range(10):
            port = self.port_numbers[i]
            thread = threading.Thread(target=self.run_voidsmtpd, args=(port,))
            thread.start()


    def run_voidsmtpd(self, port):
        try:
            logging.info(f"Starting voidsmtpd on port {port}")
            with open(f"voidsmtpd_{port}.log", "w") as log_file:
                subprocess.run(["./voidsmtpd", str(port)], stdout=log_file, stderr=log_file, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"voidsmtpd failed on port {port} with error: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred on port {port}: {e}")


class FuzzingHarness:
    def __init__(self, input_list, port_numbers):
        # Create a list of input data with ports
        self.input_data_with_ports = [(input_data, port) for input_data in input_list for port in port_numbers]
        self.number_of_threads = 10

    def send_email_wrapper(self, args):
        input_data, port = args
        self.send_email(input_data, port)

    def send_and_log(self, s, data):
        logging.info(f"Sending: {data}")
        s.send(data)
        time.sleep(0.1)  # Add a small delay to ensure the server processes the data

    def send_email(self, input_dictionary, port_number):
        server = "localhost"
        port = port_number
        logging.info(f"Connecting to server {server} on port {port}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, port))
        response = s.recv(1024)
        logging.info(f"Received: {response.decode().strip()}")

        # Send the HELO command

        self.send_and_log(s, f"HELO {input_dictionary['from_address']}\r\n".encode())
        response = s.recv(1024)
        logging.info(f"Received: {response.decode().strip()}")

        # Send the MAIL FROM command

        self.send_and_log(s, f"MAIL FROM:<{input_dictionary['from_address']}>\r\n".encode())
        response = s.recv(1024)
        logging.info(f"Received: {response.decode().strip()}")

        # Send the RCPT TO commands

        self.send_and_log(s, f"RCPT TO:<{input_dictionary['to_address']}>\r\n".encode())
        response = s.recv(1024)
        logging.info(f"Received: {response.decode().strip()}")

        self.send_and_log(s, f"RCPT TO:<{input_dictionary['cc_address']}>\r\n".encode())
        response = s.recv(1024)
        logging.info(f"Received: {response.decode().strip()}")

        # Send the DATA command
        self.send_and_log(s, "DATA\r\n".encode())
        response = s.recv(1024)
        logging.info(f"Received: {response.decode().strip()}")

        # Send the entire message in smaller chunks
        for line in input_dictionary['message'].splitlines(True):
            self.send_and_log(s, line.encode())

        logging.info("Sent email body and end of data sequence")

        response = s.recv(1024)
        logging.info(f"Received: {response.decode().strip()}")

        # Send the QUIT command
        self.send_and_log(s, "QUIT\r\n".encode())
        response = s.recv(1024)
        logging.info(f"Received: {response.decode().strip()}")

        s.close() 

        # Create a thread pool with 10 threads
    def send_fuzzing_emails(self):
        with pool.ThreadPool(self.number_of_threads) as p:
            p.map(self.send_email_wrapper, self.input_data_with_ports)



def main():
    logging.basicConfig(level=logging.INFO)
    #logging.info("Generating input data")
    input_generator = InputGenerator()
    #input_generator.create_message()

    logging.info("Starting smtp servers")
    start_servers = StartSMTPServers()
    start_servers.start_servers()
    
    # Delay to ensure the server has time to start
    time.sleep(5)

    logging.info("Generating input data")
    input_list = []
    for i in range(100):
        inputDictionary = input_generator.create_message()
        input_list.append(inputDictionary)

    logging.info("Starting fuzzing harness")
    fuzzing_harness = FuzzingHarness(input_list, start_servers.port_numbers)
    fuzzing_harness.send_fuzzing_emails()


if __name__ == "__main__":   
    main()