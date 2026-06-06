import pexpect
import sys
import time

def main():
    print("Spawning SSH tunnel: local port 3307 -> remote localhost:3306...")
    child = pexpect.spawn("ssh -N -L 3307:localhost:3306 echs_akash@samar.iitk.ac.in")
    
    # Wait for password prompt
    index = child.expect(["password:", pexpect.EOF, pexpect.TIMEOUT], timeout=30)
    
    if index == 0:
        print("Sending SSH password...")
        child.sendline("Akash@2026")
        
        # Give it a moment to establish the tunnel
        time.sleep(3)
        print("Tunnel established and running.")
        
        # Keep process alive so the tunnel remains open
        while True:
            try:
                # Just keep waiting
                child.expect(pexpect.TIMEOUT, timeout=60)
            except KeyboardInterrupt:
                print("Stopping tunnel...")
                break
    else:
        print("Failed to start tunnel.")
        print(child.before)

if __name__ == "__main__":
    main()
