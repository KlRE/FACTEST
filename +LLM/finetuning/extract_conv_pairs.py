import json
import re
import os
from datetime import datetime

from rich.progress import track


def extract_conv_pairs(log_content):
    # Split the log into separate conversations
    conversations = re.split(r'# Motion Planning Task', log_content)

    # Remove the first element if it's empty (before the first task)
    if conversations and not conversations[0].strip():
        conversations.pop(0)

    conv = conversations[-1]
    # Check if the conversation was successful
    if "Path is successful" in conv:
        # Extract the input (everything up to the first timestamp)
        input_match = re.search(r'(.*?)(?=\[\d{2}/\d{2}/\d{4})', conv, re.DOTALL)
        if input_match:
            input_text = "# Motion Planning Task\n" + input_match.group(1).strip()

            # Extract the LLM's response (the log entry containing "new_path")
            response_match = re.search(
                r'(?s:.*)\[\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2} [AP]M] (.*?new_path.*?)\[\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2} [AP]M]',
                conv,
                re.DOTALL)
            if response_match:
                response_text = response_match.group(1).strip()

                # Add the pair to our list
                return {
                    "input": input_text,
                    "response": response_text
                }

        return None


def find_log_files(root_dir):
    log_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if 'log.txt' in filenames:
            log_files.append(os.path.join(dirpath, 'log.txt'))
    return log_files


def extract_all_successful_pairs(root_directory):
    """
    Extracts all successful conversation pairs from log files in the given directory and writes them to a file in json format.
    It also holds a backup log file where the plain inputs and outputs are recorded.
    Sample implementation:
        log_files = find_log_files(root_directory)
    log_path = os.path.join(root_directory, 'conversation_pairs.txt')
    data = {
        "conversations": []
    }

    for log_file in log_files:
        with open(log_file, 'r') as file:
            log_content = file.read()
        pair = extract_conv_pairs(log_content)
        if pair:
            data["conversations"].append(pair)
    """
    today = datetime.now().strftime("%Y-%m-%d")
    log_files = find_log_files(root_directory)
    log_path = os.path.join(root_directory, f'conversation_pairs_{today}.json')
    backup_path = os.path.join(root_directory, f'conversation_pairs_{today}_backup.txt')

    data = {
        "conversations": []
    }

    with open(backup_path, 'w') as backup_file:
        for log_file_path in track(log_files):
            try:
                with open(log_file_path, 'r') as file:
                    log_content = file.read()
            except Exception as e:
                print(f"Error processing log file with UTF-Encoding{log_file_path}: {e}")
                try:
                    with open(log_file_path, 'r', encoding='ISO-8859-1') as file:
                        log_content = file.read()
                        print(f"Successfully processed log file with ISO-8859-1 Encoding{log_file_path}")
                except Exception as e:
                    print(f"Error processing log file with ISO-8859-1 Encoding{log_file_path}: {e}")
                    continue

            pair = extract_conv_pairs(log_content)
            if pair:
                data["conversations"].append(pair)
                backup_file.write(f"Input: {pair['input']}\n")
                backup_file.write(f"Response: {pair['response']}\n")
                backup_file.write("----\n")
                backup_file.write("\n")
                backup_file.flush()

    json.dump(data, open(log_path, 'w'), indent=4)
    print(
        f"Conversation pairs written to {log_path} and backup to {backup_path} for {len(data['conversations'])} successful conversations.")


if __name__ == '__main__':
    root_directory = '../tests/random_env'
    extract_all_successful_pairs(root_directory)

    # # Example usage:

    # log_files = find_log_files(root_directory)
    #
    # # Print the found log files
    # for log_file in log_files:
    #     print(log_file)
    # print(len(log_files))

# # Read the log file
#     with open(
#             '../experiments/full_path_valid_path_break_points/2024-08-13_18-00-21/gemini-1.5-flash/box/2024-08-13_18-00-21/log.txt',
#             'r') as file:
#         log_content = file.read()
#
#     # Extract the conversation pairs
#     conversation_pairs = extract_conv_pairs(log_content)
#
#     # Print or process the extracted pairs
#     for pair in conversation_pairs:
#         print("Input:", pair["input"])
#         print("Response:", pair["response"])
#         print("---")
