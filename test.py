import os
import subprocess

venv_activate = r'.venv/Scripts/activate'
python_file_dir = r'src/gui/worker/BookingWorker.py'

# Construct the commands
initial_command = f'cls'
activate_command = f'call {venv_activate}'
python_command = f'python  {python_file_dir} --credential_mode=signin --day=25 --selector=.day-unit:nth-child(29) --headless=False'

# Combine the commands using the command separator '&' (Windows) or ';' (Unix-like)
combined_command = f'{initial_command} && {activate_command} && {python_command}'

# Run the combined command in a new shell
process = subprocess.Popen(['cmd.exe', '/C', combined_command], creationflags=subprocess.CREATE_NEW_CONSOLE)
process.wait()  # Wait for the process to finish
