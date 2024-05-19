# Real-World Use Case: Parsing and Aggregating Data from a Web Server Log
"""
Let's consider a more complex real-world example where we parse a web server
 log file and aggregate data to compute summaries, such as the number of
   requests per status code and total data transferred.

   Steps:
    1. Read the log file line by line.
    2. Parse each line to extract the relevant fields (e.g., status code, data transferred).
    3. Aggregate the data based on the extracted fields.
    4. Compute summaries (e.g., number of requests per status code, total data transferred).
    5. Display the summaries or save them to a file for further analysis.
"""

import re
from collections import defaultdict



def process_web_server_logs(file_path):
    log_pattern = r'\d{3} .* (\d+)$' # Regular expression pattern to extract status code and data transferred
    status_code_count = defaultdict(int) # Dictionary to store the count of each status code
    total_data_transferred = 0 # Variable to store the total data transferred


    try:
        with open(file_path, 'r') as file:
            for line in file:
                match = re.search(log_pattern, line)
                if match:
                    status_code, file_size = match.groups()
                    status_code_count[status_code] += 1
                    total_data_transferred += int(file_size)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return
    except PermissionError:
        print(f"Error: Permission denied to read file at {file_path}")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return
    
    return status_code, total_data_transferred



def display_summary(status_code_count, total_data_transferred):
    print("Summary:")
    print("Status Code Counts:")
    for status_code, count in status_code_count.items():
        print(f"Status Code {status_code}: {count} requests")


    print(f"Total Data Transferred: {total_data_transferred} bytes")



def main():
    file_path = "web_server.log"
    result = process_web_server_logs(file_path)
    if result:
        status_code, total_data_transferred = result
        display_summary(status_code, total_data_transferred)


# Run the main function, which processes the web server logs and displays the summary
if __name__ == "__main__":
    main()