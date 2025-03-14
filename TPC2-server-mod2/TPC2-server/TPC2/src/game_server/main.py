from server import *
from game import *
import os.path

def main():
    start_server()
    round = 0
    while(os.path.isfile("../../maps/map_{}.txt".format(round))):
        set_up_game("../../maps/map_{}.txt".format(round))
        game_loop()
        print("Round", round, "END")
        round += 1
    game_end[0] = 1

if __name__ == "__main__":
    main()
