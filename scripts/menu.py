from bge import logic
import sys
import os

scripts_path = os.path.join(os.path.split(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])[0], 'scripts')
scripts_path_export = os.path.join(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0], 'scripts')

#players_file = os.path.join(scripts_path, 'players')
players_file = os.path.join(scripts_path_export, 'players')

def getScenes():
    logic.getCurrentController().activate(logic.getCurrentController().actuators["Scene"])
    
def getSettings():
    logic.getCurrentController().activate(logic.getCurrentController().actuators["Scene"])

def setPlayers():
    global players_file

    controller = logic.getCurrentController()
    object = controller.owner
    
    players_number = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4}

    num_player = players_number[object.name]
    print(players_file)
    with open(players_file, 'w') as f:
        f.write(str(num_player))
        
    logic.getCurrentController().activate(logic.getCurrentController().actuators["Scene"])
    
def quitGame():
    logic.endGame()
