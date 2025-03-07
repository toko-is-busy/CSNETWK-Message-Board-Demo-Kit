import socket
import threading
import json

class UDPServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.clients = {}

    # start the client to receive messages from the server while still being able to process user input in main thread.
    def start(self):
        threading.Thread(target=self.receive).start()

    # allows the client to receive messages from the server while still being able to process user input in main thread.
    def receive(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                threading.Thread(target=self.handle_client, args=(data, addr)).start()
            except KeyboardInterrupt:
                print("\nClosing server.")
                self.sock.close()
                break
            except Exception as e:
                print(f"Error: {e}")

    print("UDP server up and listening...")

    def handle_client(self, data, addr):
        try:
            msg = json.loads(data)
            # extract the value of the key "command" from the msg
            command = msg.get("command")

            # extract the value of the key "error" from the msg dictionary
            error = msg.get("error")

            if error:
                self.sock.sendto(json.dumps({"type": "info", "message": error}).encode(), addr)

            # joins in server
            if command == "join":
                if addr not in self.clients:
                    # creates space for new address
                    self.clients[addr] = None
                    self.sock.sendto(
                        json.dumps({"type": "info", "message": "Connection to the Message Board Server is successful!"}).encode(), addr)
                else:
                    self.sock.sendto(
                        json.dumps({"type": "info", "message": "You are already connected to the server."}).encode(),
                        addr)
            # leaves server
            elif command == "leave":
                if addr in self.clients:
                    del self.clients[addr]
                    self.sock.sendto(json.dumps({"type": "info", "message": "Connection closed. Thank you!"}).encode(),
                                     addr)
                else:
                    self.sock.sendto(
                        json.dumps({"type": "info", "message": "Error: Disconnection failed. Please connect to the server first."}).encode(), addr)
            elif command == "register":
                handle = msg.get("handle")
                if not any(client_handle == handle for client_handle in self.clients.values()):
                    self.clients[addr] = handle
                    self.sock.sendto(
                        json.dumps({"type": "info", "message": f"Welcome {handle}!"}).encode(), addr)
                else:
                    self.sock.sendto(json.dumps({"type": "info",
                                                "message": "Error: Registration failed. Handle or alias already exists."}).encode(), addr)
            elif command == "all":
                message = msg.get("message")
                handle = self.clients[addr]
                for client_addr in self.clients:
                    self.sock.sendto(json.dumps({"type": "all", "from_handle": handle, "message": message}).encode(),
                                     client_addr)
            elif command == "msg":
                target_handle = msg.get("handle")
                message = msg.get("message")
                handle = self.clients[addr]
                target_found = False
                for client_addr, client_handle in self.clients.items():
                    if client_handle == target_handle:
                        target_found = True
                        self.sock.sendto(json.dumps(
                            {"type": "msg", "from_handle": handle, "to_handle": target_handle, "message": message,
                             "sender": False}).encode(), client_addr)
                        self.sock.sendto(json.dumps(
                            {"type": "msg", "from_handle": handle, "to_handle": target_handle, "message": message,
                             "sender": True}).encode(), addr)
                        break
                if not target_found:
                    self.sock.sendto(
                        json.dumps({"type": "info", "message": "Error: Handle or alias not found."}).encode(), addr)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    try:
        server = UDPServer("127.0.0.1", 12345) # If you use "0.0.0.0" it will allow the server to accept connections from any IP address
        server.start()
    except KeyboardInterrupt:
        pass




