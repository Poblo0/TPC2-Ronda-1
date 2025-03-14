import socket
import json
import time
from submission import MiBot

# Client settings
HOST = "127.0.0.1"
PORT = 5000

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    bot = MiBot()
    round = 0
    bot.read_map("./maps/map_{}.txt".format(round))
    try:
        while True:
            # Receive game state
            game_state = client_socket.recv(1024).decode("utf-8")
            state_data = json.loads(game_state)

            if (state_data['state'][8] == 1):
                bot = MiBot()
                round += 1
                bot.read_map("./maps/map_{}.txt".format(round))

            bot.set_state(state_data)

            # Get bot input
            bot.clear_commands()
            bot.behavior()
            presses = bot.get_controls()

            client_socket.sendall(json.dumps({"presses": presses}).encode("utf-8"))
            time.sleep(0.005)  # Prevents spamming the server
    except (ConnectionResetError, BrokenPipeError, json.JSONDecodeError):
        print("Client disconnected gracefully")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
