import subprocess
import time
import os
import sys

# Asegurar que el script usa su propio directorio como base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR + "\\src\\game_server\\")  # Cambia el directorio de trabajo
subprocess.Popen(["python", "main.py"])
time.sleep(0.5)  # Let server get started before players connect

os.chdir(BASE_DIR)  # Cambia el directorio de trabajo
subprocess.Popen(["python", "./submissions/team_name/client.py"])
time.sleep(2)  # Let the first client be player 1
subprocess.Popen(["python", "./submissions/blank/client.py"])