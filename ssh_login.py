import pexpect
import sys

def main():
    print("Connecting to echs_akash@samar.iitk.ac.in...")
    child = pexpect.spawn("ssh -o StrictHostKeyChecking=no echs_akash@samar.iitk.ac.in")
    
    # Wait for password prompt
    index = child.expect(["password:", pexpect.EOF, pexpect.TIMEOUT], timeout=30)
    
    if index == 0:
        print("Sending password...")
        child.sendline("Akash@2026")
        
        # Pass control to user (interactive mode)
        print("Logged in successfully. Interactive session started:\n")
        child.interact()
    else:
        print("Failed to connect or prompt for password.")
        print(child.before)

if __name__ == "__main__":
    main()
