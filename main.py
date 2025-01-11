import os
import subprocess

def execute_script(script_name):
    script_path = script_name
    try:
        subprocess.run(['python3', script_path], check=True)
        print(f"{script_name} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing {script_name}: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")

# Execute contactplan_generater.py
execute_script('src/contactplan_generator.py')

# Execute get_contactid_todelete.py
execute_script('src/get_contactid_todelete.py')

