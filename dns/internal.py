import subprocess
import time

repository_url1 = "https://github.com/iagox86/dnscat2.git"


# clone icmptunnel

subprocess.run("echo 'hi' > /hi.txt", shell=True)

try:
    subprocess.run("pwd")
    result = subprocess.run(["git", "clone", repository_url1, "/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    # result = subprocess.run(["git", "clone", repository_url2, "/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    print("Repository cloned successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error cloning repository: {e.stderr}")


# installing dnscat2
try:

    subprocess.run("cd",  "/dnscat2/server/")
    subprocess.run("gem", "install bundler")
    subprocess.run("bundle", "install")
except subprocess.CalledProcessError as e:
    print(f"Error cloning repository: {e.stderr}")

# SED ip values into the server/client config
ssh_command = ["service", "ssh", "start"]
subprocess.run(ssh_command)

new_username = 'ssh_user'

# Create the new user
create_user_command = f'sudo useradd -m {new_username}'
subprocess.run(create_user_command, shell=True, check=True)

# Set the user's password (replace [new_password] with the desired password)
new_password = 'password'
set_password_command = f'echo "{new_username}:{new_password}" | sudo chpasswd'
subprocess.run(set_password_command, shell=True, check=True)

# Add the user to the sudoers group
add_to_sudoers_command = f'sudo usermod -aG sudo {new_username}'
subprocess.run(add_to_sudoers_command, shell=True, check=True)


tcpdump_command = ["tcpdump", "-i", "eth0", "-w", "output.pcap"]

# Start tcpdump as a subprocess and capture the output
try:
    tcpdump_process = subprocess.Popen(tcpdump_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = tcpdump_process.communicate()
    if tcpdump_process.returncode == 0:
        print("tcpdump started successfully.")
    else:
        print(f"Error starting tcpdump: {stderr.decode()}")
except Exception as e:
    print(f"An error occurred: {str(e)}")


time.sleep(10000)


# make configurations automatic for icmp tunnel
# implement ICMP listneers & ssh connection into code base 