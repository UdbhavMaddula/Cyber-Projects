import socket
import datetime
import threading
from queue import Queue

print("=" * 60)
print("        ADVANCED PYTHON PORT SCANNER")
print("=" * 60)

target = input("Enter IP address to scan: ")
start_port = int(input("Enter start port: "))
end_port = int(input("Enter end port: "))

print(f"\nScanning Target: {target}")
print(f"Port Range: {start_port} - {end_port}")
print("Scanning Started at:", datetime.datetime.now())
print("-" * 60)

queue = Queue()
open_ports = []

def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((target, port))

        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown Service"

            print(f"[+] Port {port} is OPEN ({service})")
            open_ports.append((port, service))

        s.close()

    except:
        pass

def worker():
    while not queue.empty():
        port = queue.get()
        scan_port(port)
        queue.task_done()

for port in range(start_port, end_port + 1):
    queue.put(port)

thread_count = 100 
threads = []

for _ in range(thread_count):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("-" * 60)
print("Scanning Finished at:", datetime.datetime.now())
print(f"Total Open Ports Found: {len(open_ports)}")


with open("scan_results.txt", "w") as file:
    file.write(f"Scan Results for {target}\n")
    file.write(f"Scanned at: {datetime.datetime.now()}\n\n")

    for port, service in open_ports:
        file.write(f"Port {port} OPEN ({service})\n")

print("Results saved to scan_results.txt")
print("=" * 60)