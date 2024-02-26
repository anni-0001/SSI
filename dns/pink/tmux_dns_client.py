import subprocess
import os 
import time

os.chdir("/home/ssh_user/dns/client")

session_name = "dns_session_client"
# Start a new tmux session
subprocess.run(f"tmux new-session -d -s {session_name}", shell=True)
time.sleep(1)  # Wait for tmux session to initialize

# Send the command to start dnscat2
cmd = 'sleep 3'
subprocess.run(f'tmux send-keys -t {session_name} "{cmd}" Enter', shell=True)

cmd = "./dnscat --dns server=172.20.0.2,port=53 --secret=abc"
subprocess.run(f'tmux send-keys -t {session_name} "{cmd}" Enter', shell=True)


# Attach to the tmux session
subprocess.run(f"tmux attach -t {session_name}", shell=True)