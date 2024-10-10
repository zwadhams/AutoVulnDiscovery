import socket
import logging
import time
import random
import string
import subprocess
import threading
import datetime
import pytz
from multiprocessing import pool


random_body_length = False
random_cc_address = False
random_date = False


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
        # Reset input_dictionary to ensure unique data for each call
        self.input_dictionary = {}

        from_address = self.generate_random_email()  
        self.input_dictionary["from_address"] = from_address

        if random_cc_address:
            to_address = self.generatey_random_email()  
            self.input_dictionary["to_address"] = to_address
            cc_address = self.generatex_random_email()  
            self.input_dictionary["cc_address"] = cc_address
        else:
            to_address = self.generate_random_email()  
            self.input_dictionary["to_address"] = to_address
            cc_address = self.generate_random_email() 
            self.input_dictionary["cc_address"] = cc_address

        if random_date:
            date = self.generate_random_date() 
            self.input_dictionary["date"] = date
        else:
            date = "Tue, 15 Jan 2008 16:02:43 -0500"  
            self.input_dictionary["date"] = date

        subject = f"Test message {random.randint(1000, 9999)}"  
        self.input_dictionary["subject"] = subject

        if random_body_length:
            random_body = self.generate_random_body(random.randint(1000, 5000))
            self.input_dictionary["body"] = random_body
            self.input_dictionary["body"] = self.escape_dots(self.input_dictionary["body"])
        else:
            body = f"""Hello Alice. This is a test message with 5 header fields and 4 lines in the message body. 
                   Your friend, Bob. Random number: {random.randint(1000, 9999)}"""  
            self.input_dictionary["body"] = self.escape_dots(body)
        
        message = (
            f"From: \"Bob Example\" <{self.input_dictionary['from_address']}>\r\n"
            f"To: \"Alice Example\" <{self.input_dictionary['to_address']}>\r\n"
            f"Cc: {self.input_dictionary['cc_address']}\r\n"
            f"Date: {self.input_dictionary['date']}\r\n"
            f"Subject: {self.input_dictionary['subject']}\r\n"
            "\r\n"  
            f"{self.input_dictionary['body']}\r\n"
            "\r\n.\r\n"  
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

    def generatey_random_email(self):

        def random_string(length):
            return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

        # need symbols for sanitizer
        at = "@"
        dot = "."

        # random length of names
        z = random.randint(2, 10)
        username = random_string(random.randint(1, z))
        domain = random_string(random.randint(1, z))
        tld = random.choice(['com', 'org', 'net', 'edu', 'gov'])

        emails = f"{username}{at}{domain}{dot}{tld}"

        return emails

    def generatex_random_email(self):

        x = random.randint(0, 10)

        emails = ""
        for i in range(x):
            def random_string(length):
                return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

            # random characters to sub
            characters = ("@ .*^&#$!?+=)(';,`\n")

            # sometimes change the @ symbol
            at = "@"
            if i % 4 == 0:
                at = random.choice(characters)

            # sometimes change the . symbol
            dot = "."
            if i % 3 == 0:
                dot = random.choice(characters)
                
            # random length of names
            z = random.randint(2, 100)
            username = random_string(random.randint(1, z))
            domain = random_string(random.randint(1, z))
            tld = random.choice(['com', 'org', 'net', 'edu', 'gov'])

            # put it all together
            if emails == "":
                emails = emails + f"{username}{at}{domain}{dot}{tld}"
            else:
                emails = emails + ";" + f"{username}{at}{domain}{dot}{tld}"

        return emails
    
    def generate_random_body(self, length):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))
    
    
    def create_input_list(self, number_of_inputs):
        input_list = []
        for i in range(number_of_inputs):
            inputDictionary = self.create_message()
            input_list.append(inputDictionary)
        return input_list
    

    def generate_random_date(self):
        start_date = datetime.datetime(2000, 1, 1)
        end_date = datetime.datetime.now()
        random_date = start_date + datetime.timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
        
        random_timezone = random.choice(pytz.all_timezones)
        random_date = random_date.replace(tzinfo=pytz.timezone(random_timezone))
        
        date_formats = [
            "%a, %d %b %Y %H:%M:%S %z",
            "%Y-%m-%d %H:%M:%S %z",
            "%d/%m/%Y %H:%M:%S %z",
            "%m-%d-%Y %H:%M:%S %z"
        ]
        random_format = random.choice(date_formats)
        
        padding_length = random.randint(0, 10000)
        
        return random_date.strftime(random_format) + " " * padding_length


    def save_smtp_interaction_to_file(self, full_interaction, from_address):
        # Create a unique filename using from_address and a random number
        filename = f"smtp_interaction_{from_address}_{random.randint(1000, 9999)}.txt"
        with open(filename, 'w') as f:
            f.write(full_interaction)
        logging.info(f"Saved SMTP interaction to {filename}")



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
    def __init__(self, port_numbers):
        self.port_numbers = port_numbers
        self.number_of_threads = 10
        self.input_generator = InputGenerator()  
        self.input_list = self.input_generator.create_input_list(100)
        
        # Create a list of (input, port) pairs for all ports 
        # The loop iterates over the input list and assigns each input to a port.
        # Each port will be assigned a proportionate number of inputs.
        # For example, if there are 100 inputs and 10 ports, each port will receive 10 inputs.
        # Since we have ten ports, i mod 10 will assign the first element of the list to multiples of 10.
        # the second elements to numbers whose remainder is 1 when divided by 10, and so on.
        self.inputs_with_ports = [ (self.input_list[i], self.port_numbers[i % len(self.port_numbers)]) for i in range(len(self.input_list)) ]

    def send_email_wrapper(self, args):
        input_data, port = args
        self.send_email(input_data, port)

    def send_and_log(self, s, data):
        logging.info(f"Sending: {data.strip()}")
        s.send(data)
        time.sleep(0.1)  # Add a small delay to ensure the server processes the data

    def send_email(self, input_dictionary, port_number):
        server = "localhost"
        port = port_number
        logging.info(f"Connecting to server {server} on port {port}")
        
        full_interaction = ""  # To store all commands sent for saving later

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, port))
        response = s.recv(1024)
        logging.info(f"Received: {response.decode().strip()}")

        # Send HELO command
        helo_command = f"HELO {input_dictionary['from_address']}\r\n"
        self.send_and_log(s, helo_command.encode())
        full_interaction += helo_command
        response = s.recv(1024)
        logging.info(f"Received: {response.decode().strip()}")

        # Send MAIL FROM command
        mail_from_command = f"MAIL FROM:<{input_dictionary['from_address']}>\r\n"
        self.send_and_log(s, mail_from_command.encode())
        full_interaction += mail_from_command
        response = s.recv(1024)
        logging.info(f"Received: {response.decode().strip()}")

        # Send RCPT TO command
        rcpt_to_command = f"RCPT TO:<{input_dictionary['to_address']}>\r\n"
        self.send_and_log(s, rcpt_to_command.encode())
        full_interaction += rcpt_to_command
        response = s.recv(1024)
        logging.info(f"Received: {response.decode().strip()}")

        # Send additional RCPT TO command
        cc_rcpt_command = f"RCPT TO:<{input_dictionary['cc_address']}>\r\n"
        self.send_and_log(s, cc_rcpt_command.encode())
        full_interaction += cc_rcpt_command
        response = s.recv(1024)
        logging.info(f"Received: {response.decode().strip()}")

        # Send DATA command
        data_command = "DATA\r\n"
        self.send_and_log(s, data_command.encode())
        full_interaction += data_command
        response = s.recv(1024)
        logging.info(f"Received: {response.decode().strip()}")

        # Send Message body line by line
        for line in input_dictionary['message'].splitlines(True):
            self.send_and_log(s, line.encode())
            full_interaction += line

        # Send QUIT command
        quit_command = "QUIT\r\n"
        self.send_and_log(s, quit_command.encode())
        full_interaction += quit_command
        response = s.recv(1024)
        logging.info(f"Received: {response.decode().strip()}")

        s.close()

        # Save the full input to a file
        self.input_generator.save_smtp_interaction_to_file(full_interaction, input_dictionary['from_address'])

    def send_fuzzing_emails(self): 
        with pool.ThreadPool(self.number_of_threads) as p:
            # Send each (input, port) pair in the list to the thread pool
            # The map function will call the send_email_wrapper function with each pair as an argument
            p.map(self.send_email_wrapper, self.inputs_with_ports) 

def main():
    logging.basicConfig(level=logging.INFO)
    
    start_servers = StartSMTPServers()
    start_servers.start_servers()

    # Delay to ensure the servers have time to start
    time.sleep(5)

    fuzzing_harness = FuzzingHarness(start_servers.port_numbers)
    fuzzing_harness.send_fuzzing_emails()


if __name__ == "__main__":
    main()
