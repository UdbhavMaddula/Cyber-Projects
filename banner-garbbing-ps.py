import socket
import threading
import queue
import datetime

target = input("Enter Target IP: ")
start_port = int(input("Enter Start Port: "))
end_port = int(input("Enter End Port: "))

print(f"Scanning Target: {target}")
print(f"Port Range: {start_port} - {end_port}")
print("Scanning Started at:", datetime.datetime.now())
print("-" * 60)

q = queue.Queue()
open_ports = []

def banner_grab(sock):
    try:
        sock.send(b"Hello\r\n")
        banner = sock.recv(1024)
        return banner.decode().strip()
    except:
        return "Unknown Service"

def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        result = s.connect_ex((target, port))

        if result == 0:
            banner = banner_grab(s)
            print(f"[+] Port {port} OPEN | Service: {banner}")
            open_ports.append((port, banner))

        s.close()

    except:
        pass


def worker():
    while not q.empty():
        port = q.get()
        scan_port(port)
        q.task_done()


for port in range(start_port, end_port + 1):
    q.put(port)

threads = []

for _ in range(100):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("-" * 60)
print("Scanning Finished at:", datetime.datetime.now())
print(f"Total Open Ports Found: {len(open_ports)}")