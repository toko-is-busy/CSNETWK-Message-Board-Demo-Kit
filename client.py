import socket
import threading
import json
import sys

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_addr = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # reuse of the local address, socket is closed and then reopened again quickly.
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # multiple sockets to bind to the same address and port
        if hasattr(socket, 'SO_REUSEPORT'):
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.sock.settimeout(1)  # Set a timeout of 1 second
        # later store a handle to the socket
        self.handle = None
        # indicating that the instance is currently running.
        self.running = True

    print("Type /? for the list of commands.")

    def start(self):
        # start continuously listen for and process incoming data on the UDP socket.
        threading.Thread(target=self.receive).start()

        # initially set as True
        while self.running:
            try:
                msg = input()
                # calls process_input to process the message
                self.process_input(msg)
            except KeyboardInterrupt:
                if self.server_addr:
                    print("\nDisconnecting from server.")
                    self.sock.sendto(json.dumps({"command": "leave"}).encode(), self.server_addr)
                else:
                    print("\nExiting without joining a server.")
                self.running = False
            except Exception as e:
                print(f"Error: {e}")
        # closes the UDP socket and exits the program
        self.sock.close()
        sys.exit()

    def process_input(self, msg):
        # splits message and removes whitespace
        tokens = msg.strip().split(" ")

        # likely indicates that the user entered an empty command, or a command with no arguments.
        if len(tokens) < 1:
            return

        # user must join a server before sending any commands
        if tokens[0] in ["/all", "/msg", "/register"]:
            if not self.server_addr:
                print("Error: You must join a server before sending any other commands.")
                return

        # sets server address (host number, port number)
        if tokens[0] == "/join":
            if len(tokens) == 3:
                if not self.server_addr:
                        if tokens[1] != "127.0.0.1" or tokens[2] != "12345":
                            print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
                        else:
                            self.server_addr = (tokens[1], int(tokens[2]))
                            self.sock.sendto(json.dumps({"command": "join"}).encode(), self.server_addr)
                else:
                    print("Error: You are already connected to a server.")
            else:
                print("Error: Invalid input. Usage: /join <server_ip_add> <port>")

        # sends a "leave" command to the server, encoded as a JSON object and sent via UDP
        elif tokens[0] == "/leave":
            if len(tokens) == 1:
                if self.server_addr:
                    self.sock.sendto(json.dumps({"command": "leave"}).encode(), self.server_addr)
                    self.server_addr = None
                    self.handle = None
                else:
                    print("Error: Disconnection failed. Please connect to the server first.")
            else:
                self.sock.sendto(json.dumps({"command": "error", "error": "Error: Invalid input. Usage: /leave"}).encode(), self.server_addr)

        # sends a "register" command to the server along with the handle
        elif tokens[0] == "/register":
            if len(tokens) == 2:
                if self.server_addr:
                    if not self.handle:
                        self.handle = tokens[1]
                        self.sock.sendto(json.dumps({"command": "register", "handle": tokens[1]}).encode(), self.server_addr)
                    else:
                        print("Error: You have already registered with a handle. You cannot change your handle.")
                else:
                    print("Error: Registration. Please connect to the server first.")
            else:
                self.sock.sendto(json.dumps({"command": "error", "error": "Error: Invalid input. Usage: /register <handle>"}).encode(), self.server_addr)

        elif tokens[0] == "/all":
            if len(tokens) >= 2:
                if self.server_addr:
                    if self.handle:
                        self.sock.sendto(
                            json.dumps(
                                {"command": "all", "message": " ".join(tokens[1:]), "handle": self.handle}).encode(),
                            self.server_addr)
                    else:
                        self.sock.sendto(
                            json.dumps(
                                {"command": "error", "error": "Error: You must register before sending a message."}).encode(),
                            self.server_addr)
                    # marissa check
            else:
                self.sock.sendto(
                    json.dumps({"command": "error", "error": "Error: Invalid input. Usage: /all <message>"}).encode(),
                    self.server_addr)
        elif tokens[0] == "/msg":
            if len(tokens) >= 3:
                if self.server_addr:
                    if self.handle:
                        self.sock.sendto(json.dumps(
                            {"command": "msg", "handle": tokens[1], "message": " ".join(tokens[2:]),
                             "from_handle": self.handle}).encode(), self.server_addr)
                    else:
                        self.sock.sendto(json.dumps({"command": "error", "error": "Error: You must register before sending a message."}).encode(), self.server_addr)
            else:
                self.sock.sendto(json.dumps(
                    {"command": "error", "error": "Error: Invalid input. Usage: /msg <handle> <message>"}).encode(),
                                 self.server_addr)
        elif tokens[0] == "/?":
            self.show_help()
        else:
            print("Invalid Command")

    # receives message from server
    def receive(self):
        while self.running:
            try:
                data, _ = self.sock.recvfrom(1024)
                msg = json.loads(data.decode())
                if msg['type'] == 'all' and self.handle is not None:
                    print(f"{msg['from_handle']}: {msg['message']}")
                elif msg['type'] == 'msg':
                    if msg['sender']:
                        print(f"[To {msg['to_handle']}]: {msg['message']}")
                    else:
                        print(f"[From {msg['from_handle']}]: {msg['message']}")
                elif msg['type'] == 'info':
                    if msg['message'] == "Error: Registration failed. Handle or alias already exists.":
                        self.handle = None

                    print(msg['message'])
            except socket.timeout:
                pass
            except Exception as e:
                if self.running:
                    print(f"Error: {e}")

    def show_help(self):
        print("""
            1. Connect to server application: /join <server_ip_add> <port>
            2. Disconnect to the server application:  /leave
            3. Register a unique handle or alias: /register <handle>
            4. Send message to all: /all <message>
            5.  Send direct message to a single handle:  /msg <handle> <message>
            """)

if __name__ == "__main__":
    client = Client("127.0.0.1", 12345)
    client.start()


