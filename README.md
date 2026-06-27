# Tic-Tac-Toe
Tic-Tac-Toe with Socket Communication and a UI

This program consists of socket and tkinter imports 

A Tic-Tac-Toe Game between server and client only playable on one machine

# Install Dependencies
- Run the following command to install the requirements:

```bash
    pip install -r requirements.txt
```

# Create a Virtual Environment
- Create a virtual environment to avoid library conflicts and have an isolated environment:

```bash
    python3 -m venv myvenv
    source ./myvenv/bin/activate
```

# To launch Game
- You only need one machine to launch

1. Launch 2 seperate terminals on your machine
2. Navigate to the root directory of the project (../Tic-Tac-Toe)
3. Use the command to launch the server side first

```bash
    python3 Server.py
```

4. Then launch the client side

```bash
    python3 Client.py
```

5. Enter in a hostname and port number such as:
- localhost
- 3000