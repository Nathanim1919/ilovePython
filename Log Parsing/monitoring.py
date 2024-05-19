import os # Import os module which provides a way of using operating system dependent functionality
import sys # Import sys module which provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter
import signal # Import signal module which provides mechanisms to use signal handlers in Python
import re # Import re module which provides support for regular expressions
import time # Import time module which provides various time-related functions
import smtplib # Import smtplib module which defines an SMTP client session object that can be used to send mail to any internet machine with an SMTP or ESMTP listener daemon
from email.message import EmailMessage # Import EmailMessage class from email.message module which represents an email message
import configparser # Import configparser module which provides a class to read and write INI files


# Read configuration from config.ini file
config = configparser.ConfigParser() # Create a ConfigParser object
config.read('config.ini') # Read configuration from config.ini file


# Initialize variables
LOG_FILE = config['monitoring']['log_file'] # Get log file path from config.ini file
ERROR_LOG_FILE = config['monitoring']['error_log_file'] # Get error log file path from config.ini file
ADMIN_EMAIL = config['monitoring']['admin_email'] # Get admin email from config.ini file


TERMINATION_SIGNALS = [signal.SIGINT, signal.SIGTERM] # Define termination signals


# Define error pattern which matches any line that starts with ERROR: followed by any character one or more times
ERROR_PATTERN = r'ERROR: (.+)' # Define error pattern



# Function to handle termination signals
def signal_handler(sig, frame):
    print('\nSIGINT or SIGTERM detected. Exiting gracefully...')
    cleanup()
    sys.exit(0)


# Function to clean up resources
def cleanup():
    # Close log file
    #log_file.close()

    # Close error log file
    #error_log_file.close()

    # Send email notification
    #send_email_notification()
    pass



# setup signal handlers
for sig in TERMINATION_SIGNALS:
    signal.signal(sig, signal_handler)



# Function to montior log file for errors
def monitor_log_file():
    # Open log file in read mode
    with open(LOG_FILE, 'r') as log_file:
       while True:
            line = log_file.readline()
            if not line:
               time.sleep(1) # Sleep for 1 second to avoid high CPU usage
               continue
           
            # Process the log entry
            process_log_entry(line)
           


# Function to process log entry
def process_log_entry(line):
    # Parse the log entry and check for errors using regular expression
    match = re.search(ERROR_PATTERN, line)
    if match:
        error_message = match.group(1) # Get the error message
        log_error(error_message)
        send_alert(error_message)



# Function to log error message to error log file
def log_error(error_message):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S') # Get current timestamp
    with open(ERROR_LOG_FILE, 'a') as error_log_file:
        error_log_file.write(f'{timestamp} - {error_message}\n')


# Function to send an email alert to the system administrator
def send_alert(error_message):
    msg = EmailMessage() # Create an EmailMessage object
    msg.set_content(error_message) # Set the content of the email message
    msg['Subject'] = 'Error Alert' # Set the subject of the email message
    msg['From'] = 'montirening@gmail.com' # Set the sender of the email message
    msg['To'] = ADMIN_EMAIL # Set the recipient of the email message

    # Send the email message
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('username', 'password')
        server.send_message(msg)


# Main function
def main():
    try:
        monitor_log_file() # Monitor the log file for errors
    except Exception as e:
        print(f'An error occurred: {e}')
        cleanup()


if __name__ == '__main__':
    main() # Call the main function