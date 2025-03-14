import socket
import threading
import json

from shark import coordinates

# Server settings
HOST = "127.0.0.1"
PORT = 5000
clients = [None, None]  # Inicialmente vacíos
update = [False, False] # Flag to check if the clients have issued their decision so that the game can be updated

# 2 Players and 4 buttons 
# Left, Right, Jump, Bomb
players = [[False, False, False, False],[False, False, False, False]]

next_game = [0, 0]

game_end = [0]

# Receives player input and updates its controllers
def handle_client(client_socket, player_id):
    global players

    try:
        while True:
            if (game_end[0] == 1):
                break
            # Send state
            while (update[player_id] and game_end[0] == 0):
                pass
            if (game_end[0] == 1):
                break
            game_state = {"state": coordinates[player_id] + coordinates[(player_id + 1) % 2] + [next_game[player_id]]}  # 9 integer list
            client_socket.sendall(json.dumps(game_state).encode("utf-8"))
            if (next_game[player_id] == 1):
                next_game[player_id] = 0

            # Receive presses
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                break

            input_data = json.loads(data)
            presses = input_data.get("presses")

            players[player_id][0] = False
            players[player_id][1] = False
            players[player_id][2] = False
            players[player_id][3] = False

            # Update player position
            if presses[0] == 'L':
                players[player_id][0] = True
            if presses[1] == 'R':
                players[player_id][1] = True
            if presses[2] == 'J':
                players[player_id][2] = True
            if presses[3] == 'B':
                players[player_id][3] = True
                
            update[player_id] = True

    finally:
        print(f"Player {player_id + 1} disconnected.")
        clients[player_id] = None
        client_socket.close()

# Starts the server and waits for the 2 players
def start_server():
    global clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(2)

    print("Waiting for 2 players to connect...")

    while len([c for c in clients if c]) < 2:
        client_socket, addr = server_socket.accept()
        player_id = clients.index(None)  # Encuentra el primer espacio vacío
        clients[player_id] = client_socket
        print(f"Player {player_id + 1} connected from {addr}")
        threading.Thread(target=handle_client, args=(client_socket, player_id), daemon=True).start()

    # Start threads for handling client input
    #for i in range(2):
    #    threading.Thread(target=handle_client, args=(clients[i], i), daemon=True).start()