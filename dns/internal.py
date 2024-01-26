import subprocess
import os
import time
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

os.chdir("/home/ssh_user/dns/server")

# Install bundler
subprocess.run(["gem", "install","bundler"])

# Install dependencies
subprocess.run(["bundle", "install"])

# Start SSH service
subprocess.run(["service", "ssh", "start"])

# Start tcpdump as a subprocess
tcpdump_command = ["tcpdump", "-i", "eth0", "-w", "output.pcap"]
subprocess.Popen(tcpdump_command)

# Sleep for 10,000 seconds
time.sleep(10000)