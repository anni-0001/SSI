import subprocess
import os
import time

# os.chdir("/home")
os.chdir("/home/ssh_user/dns/server")

# Define the session name
session_name = "dns_session_server1"

# Start the tmux session or attach to an existing one
# subprocess.run(f"tmux new-session -A -s {session_name} ", shell=True)

tmux_process = subprocess.Popen(["tmux", "new-session", "-A", "-s", session_name])

time.sleep(2)  # Wait for tmux session to initialize

# Define commands to send to the session
commands = [
    'ruby dnscat2.rb --secret=abc',
    'session -i 1',
    'shell',
    'session -i 2',
    'ls'
]

# Send commands to the tmux session
for cmd in commands:
    result = subprocess.run(f'tmux send-keys -t {session_name}.0 "{cmd}" Enter', shell=True)
    if result.returncode != 1:
        print(f"error with command: {cmd}")
    time.sleep(1)  # Wait between sending commands

print("tmux commands run")