📨 CSNETWK: Message Board Demo Kit
=================================

A Python-based UDP messaging application built as a machine project for the CSNETWK course at De La Salle University. This project simulates a simple yet interactive message board system that supports server-client architecture, real-time broadcast and private messaging, and basic user command handling.

📌 Features
-----------

- Connects up to 3 clients to a central server (Alice, Bob, Charlie).
- Implements core commands:
  - `/join <ip> <port>` — Join a server
  - `/leave` — Leave the server
  - `/register <handle>` — Register a user handle
  - `/all <message>` — Send broadcast message to all users
  - `/msg <handle> <message>` — Send private (unicast) message
  - `/?` — View command list
- Proper command error handling and feedback
- Multithreaded for simultaneous listening and user input

🧠 Technologies Used
--------------------

- Python 3
- `socket` (UDP protocol)
- `threading`
- `json`

📂 File Structure
-----------------

    📁 CSNETWK/
    ├── client.py           # Client-side logic and command processing
    ├── server.py           # UDP server to handle multiple clients
    ├── template.txt        # Sample run commands and test inputs
    ├── .gitignore          # Python cache and env exclusions
    └── README.txt          # Project overview and instructions

🚀 Getting Started
------------------

1. Clone the repo:

    git clone https://github.com/toko-is-busy/csnetwk-message-board.git
    cd csnetwk-message-board

2. Run the server:

    python3 server.py

3. Run the clients (in separate terminals):

    python3 client.py

4. Each client can register a unique handle after joining:

    /join 127.0.0.1 12345
    /register {Name}

5. Try commands:

- Broadcast: `/all Hello everyone!`
- Unicast: `/msg Bob Hi Bob!`

🧪 Testing Scenarios
--------------------

Scenarios were based on the CSNETWK machine project rubric:
- Connection validation
- Registration handling
- Command syntax checks
- Broadcasting and messaging integrity

See `template.txt` for sample interactions.

👤 Author
---------

**Yasmin Audrey Datario**  
📧 datario.yasminaudrey@gmail.com  
🔗 GitHub: https://github.com/toko-is-busy

🏷️ Acknowledgments
-------------------

This project was created as part of the CSNETWK class under the College of Computer Studies, De La Salle University.
