import socket
import datetime

print("=" * 50)
print("BASIC PORT SCANNER")
print("=" * 50)

target = input("Enter IP address: ")

common_ports = [21,22,23,25,53,80,110,139,143,443,445,3389]

print("\n Scanning Target: ", target)
print("Scanning Started at: ", datetime.datetime.now())
print("-" * 50)

try:
    for port in common_ports :
        s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target,port))

        if result == 0 :
            print(f"[+] port {port} is OPEN")
        else:
            print(f"[-] port {port} is CLOSED")
    s.close()
    
except KeyboardInterrupt :
    print("\nScan Stopped by user.")

except socket.gaierror :
    print("\nHostname could not be resolved.")

except socket.error :
    print("\nServer not responding.")

print("-" * 50)
print("scanning finished at : ", datetime.datetime.now())
print("=" * 50)