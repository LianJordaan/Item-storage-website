import subprocess
import requests
import json
import time
import logging
import sys
import psutil
import re
import os

AUTH_TOKEN = "..."

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def kill_processes():
    current_pid = os.getpid()  # Get PID of the current process

    # Function to kill all processes running a specific script
    def kill_processes_by_script(script_name):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['pid'] != current_pid and proc.info['name'] == 'python' and script_name in ' '.join(proc.cmdline()):
                print(f"Killing process {proc.info['pid']} running {script_name}")
                proc.kill()

    # Kill all existing Gunicorn and Loophole processes
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['pid'] != current_pid and ('gunicorn' in proc.info['name']):
            print(f"Killing {proc.info['name']} (PID: {proc.info['pid']})")
            proc.kill()

    # Kill all processes running 'app.py'
    kill_processes_by_script('app.py')

def start_processes():
    try:
        # Kill existing Gunicorn and Loophole processes
        kill_processes()

        # Start Gunicorn to run the web app
        gunicorn_path = '/home/lian/itemsSite/.local/bin/gunicorn'  # Replace with the actual path
        gunicorn_process = subprocess.Popen([gunicorn_path, '-w', '4', '-b', '0.0.0.0:25574', '-t', '18000', 'web_app:app'])
        logger.info(f"Gunicorn Process ID: {gunicorn_process.pid}")

        # Start Loophole to expose the local web server
        #loophole_path = '/home/lian/itemsSite/loophole'  # Replace with the actual path
        #loophole_process = subprocess.Popen([loophole_path, 'http', '25574', '--hostname', 'itemsstore', '--verbose'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        #logger.info(f"Loophole Process ID: {loophole_process.pid}")

        #ngrok_url = None
        #while True:
            #line = loophole_process.stdout.readline()
            #if not line:
            #    logger.info("End of Loophole output reached.")
            #    break
            #logger.info(f"Loophole output: {line.strip()}")
            #if 'Forwarding' in line:
            #    match = re.search(r'Forwarding (\S+)', line)
            #    if match:
            #        ngrok_url = match.group(1)
            #        logger.info(f"Ngrok URL found: {ngrok_url}")
            #        break

#        if ngrok_url:
 #           # Send the ngrok URL to a specified endpoint
  #          update_url = f''
   #         payload = {'ngrok_url': remove_ansi_escape_codes(ngrok_url)}
    #        headers = {'Content-Type': 'application/json'}
     #       response = requests.post(update_url, data=json.dumps(payload), headers=headers)
      #      while True:
       #         line = loophole_process.stdout.readline()
        #    if response.status_code == 200:
         #       logger.info("Ngrok URL sent successfully.")
          #  else:
           #     logger.error("Failed to send Ngrok URL.")
        #else:
         #   logger.error("Failed to find Ngrok URL.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

# Define a regular expression pattern to match ANSI escape codes
#ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

# Function to remove ANSI escape codes from a string
#def remove_ansi_escape_codes(text):
 #   return ansi_escape.sub('', text)

if __name__ == "__main__":
    start_processes()
