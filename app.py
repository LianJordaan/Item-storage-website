import subprocess
import logging
import psutil
import os

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

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    start_processes()
