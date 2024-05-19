"""
Challenge: Parse logs
The goal of this challenge is to parse log files and extract relevant information. You are given a log file containing entries with the following format:

INFO 2024-05-19 15:23:44 Data fetched successfully
WARNING 2024-05-19 15:23:45 Low disk space
ERROR 2024-05-19 15:23:46 Failed to connect to database
INFO 2024-05-19 15:23:47 User login successful

Each log entry consists of a log level (INFO, WARNING, ERROR), a timestamp, and a message. Your task is to write a Python program that reads the log file and extracts the following information:
 - Extract the log level, timestamp, and message from each log entry.
 - Count the number of log entries for each log level (INFO, WARNING, ERROR).
 - Calculate the total number of log entries processed.
 - Display the extracted information and summary statistics.
 - Save the extracted information and summary statistics to a file.
 - Handle exceptions that may occur while reading the log file.
 - Use regular expressions to parse the log entries.
 - Use dictionaries to store the log entries and summary statistics.
 - Use functions to modularize the code.
"""

import re
from collections import defaultdict



def parse_log_file(file_path):
    log_entries = defaultdict(list)
    total_log_entries = 0
    log_pattern = r'(\w+) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (.+)' # Regular expression pattern to extract log level, timestamp, and message

    try:
        with open(file_path, 'r') as file:
            for line in file:
                match = re.search(log_pattern, line)
                if match:
                    log_level, timestamp, message = match.groups()
                    log_entries[log_level].append((timestamp, message))
                    total_log_entries += 1
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    
    except PermissionError:
        print(f"Error: Permission denied to read file at {file_path}")
        return None
    return log_entries, total_log_entries



def display_summary(log_entries):
    print("Summary:")
    for log_level, entries in log_entries.items():
        print(f"Log Level: {log_level}")
        for timestamp, message in entries:
            print(f"Timestamp: {timestamp} - Message: {message}")
        print(f"Total Entries: {len(entries)}")
        print()



def save_summary_to_file(log_entries, file_path_for_save):
    try:
        with open(file_path_for_save, 'w') as file:
            file.write("Summary:\n")
            for log_level, entries in log_entries.items():
                file.write(f"Log Level: {log_level}\n")
                for timestamp, message in entries:
                    file.write(f"Timestamp: {timestamp} - Message: {message}\n")
                file.write(f"Total Entries: {len(entries)}\n\n")

    except Exception as e:
        print(f"An error occurred while saving the summary to file: {e}")


def main():
    file_path = "log_file.log"
    file_path_for_save = "log_summary.txt"
    result = parse_log_file(file_path)
    if result:
        log_entries, total_log_entries = result
        display_summary(log_entries)
        save_summary_to_file(log_entries, file_path_for_save)



if __name__ == "__main__":
    main()