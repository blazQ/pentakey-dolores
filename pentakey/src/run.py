#!/usr/bin/env python3
import subprocess
import os
from config import DefaultConfig

# Run pentakey_adapter.py
pentakey_script = "src/pentakey_adapter.py" #os.path.join("pentakey/src", "pentakey_adapter.py")
pentakey_command = ['python3', pentakey_script]

try:
    subprocess.run(pentakey_command, check=True)
except subprocess.CalledProcessError:
    print(f"Error during the execution of {pentakey_script}")

# Run scoreParser.py
score_parser_script = "src/scoreParser.py" #os.path.join("pentakey/src", "scoreParser.py")
score_parser_command = ['python3', score_parser_script]

try:
    subprocess.run(score_parser_command, check=True)
except subprocess.CalledProcessError:
    print(f"Error during the execution of {score_parser_script}")

try:
    subprocess.run(score_parser_command, check=True)
except subprocess.CalledProcessError:
    print(f"Error during the execution of {score_parser_script}")

# Delete risultato_normalizzato.json
output_directory = DefaultConfig.OUTPUT_FOLDER
result_file = DefaultConfig.OUTPUT_NORMALIZED_FILE
result_path = os.path.join(output_directory, result_file)

if os.path.exists(result_path):
    try:
        os.remove(result_path)
        print(f"{result_file} deleted successfully")
    except Exception as e:
        print(f"Error while deleting {result_file}: {str(e)}")
else:
    print(f"{result_file} not found in the output folder")
    
# Delete bad list
