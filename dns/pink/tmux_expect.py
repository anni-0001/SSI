import pexpect


open_dns = pexpect.spawn("ruby dnscat2.rb --secret=abc")

open_dns.expect("dnscat2>")




# Command to start the DNS client CLI (replace it with the actual command you use)
# dns_cli_command = "dns_cli"

# # Spawn the DNS client CLI process
# dns_cli_process = pexpect.spawn(dns_cli_command)

# # Expect the prompt to appear
# dns_cli_process.expect('dns_cli>')

# # Send commands to the DNS client CLI
# dns_cli_process.sendline('command1')  # Replace 'command1' with your desired command
# dns_cli_process.expect('dns_cli>')  # Wait for the prompt after sending the command

# dns_cli_process.sendline('command2')  # Replace 'command2' with another command
# dns_cli_process.expect('dns_cli>')  # Wait for the prompt after sending the command

# Add more commands as needed...

# Finally, close the DNS client CLI
dns_cli_process.close()