import subprocess
import os
import time
import socket
# import git


def create_user():
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

    return new_username

def dns_install():

    repository_url1 = "https://github.com/iagox86/dnscat2.git"
    # os.mkdir("/home/ssh_user")

    # Clone dnscat
    try:
        subprocess.run(["git", "clone", repository_url1, "/dns"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        os.chdir("/dns/server")

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

    os.chdir(f"/dns/server")

    # Install bundler 
    # i used to gem --user-install bunlder and it broke the build, saying it neede more path information
    subprocess.run(["gem", "install","bundler"])
    subprocess.run(["gem", "install","sha3"])

    # installing icmptunnel
    # subprocess.run([])

    # Install dependencies
    subprocess.run(["bundle", "install"])

    # Start SSH service
    subprocess.run(["service", "ssh", "start"])

    # build dnscat client binary
    os.chdir(f"/dns/client")
    subprocess.run("make")
    print("client built")

def icmp_install():

# figure out the ssh fingerprinting to make the icmptraffic work seamlessly******
    subprocess.run(["sudo", "apt", "install", "ptunnel-ng"], check=True)


    # repository_url2= "https://github.com/DhavalKapil/icmptunnel.git"
    # # clone icmptunnel
    # try:
    #     subprocess.run(["git", "clone", repository_url2, "/icmp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    #     os.chdir("/icmp")

    #     # List the contents of the repository directory
    #     repo_contents = os.listdir()

    # except subprocess.CalledProcessError as e:
    #     print(f"Error cloning ICMP repository!!!: {e.stderr}")
    #     print()
    #     print()

    # subprocess.run("make")



def tcpdump():

    # tcpdump configuration to save unique pcap files in /pink volume
    hostname = socket.gethostname()
    output_file = f"/pink/output_{hostname}.pcap"
    tcpdump_command = ["tcpdump", "-i", "eth0", "-w", output_file]
    subprocess.Popen(tcpdump_command)

    # os.chdir("/pink")

def dns():
    server_path = '/pink/tmux_dns_server.py'
    client_path = '/pink/tmux_dns_client.py'
    comm_path = '/pink/tmux-dns-comm.py'
    try:
        subprocess.run(["python3", server_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"******Error: {e}")
    try:
        subprocess.run(["python3", client_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"******Error: {e}")
    try:
        subprocess.run(["python3", comm_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    
def icmp():
    server_path = '/pink/tmux_icmp_server.py'
    client_path = '/pink/tmux_icmp_client.py'

    try:
        subprocess.run(["python3", server_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"******Error: {e}")
    try:
        subprocess.run(["python3", client_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"******Error: {e}")
    
    

    



def main():
    new_user=create_user()

    dns_install()
    icmp_install()
    tcpdump()

    dns()
    icmp()
    # script_path1 = "/pink/"

# Run the script using subprocess





    

    # script_path = '/pink/dns_all.py'
    # try:
    #     subprocess.run(["python3", script_path], check=True)
    # except subprocess.CalledProcessError as e:
    #     print(f"Error: {e}")
    # # subprocess.run(['python3', script_path], check=True, shell=True)


    

    
    time.sleep(1000000)

main()
