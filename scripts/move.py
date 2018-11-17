from bge import logic, render, types
from random import randint
import math
import sys
import os

sys.path.insert(0, '/home/data/documents/python/shish-bish/scripts')
import player_logic as pl

dices = {'Dice_1': 0, 'Dice_2': 0}

def getOwner():
    controller = logic.getCurrentController()
    object = controller.owner
    return object

def goDice():
    global dices
    
    game_mouse = logic.mouse
    event_list = game_mouse.events
    object = getOwner()
    
    angle = - (math.pi / 2)
    
    dice_angle = {1: [2*angle, 0.0, 0.0], 2: [-angle, 0.0, 0.0], 3: [0.0, angle, 0.0], 4: [0.0, -angle, 0.0], 5: [angle, 0.0, 0.0], 6: [0.0, 0.0, 0.0]}
    
    if event_list[192] == 1:
        object.localOrientation = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    
        dice_num = randint(1,6)
        
        dices[object.name] = dice_num
        
        for i in list(dice_angle.keys()):
            if dice_num == i:
                rotation = dice_angle[i]
        
        #rotation = [0.0, 0.0, 1.570796327]
        local = False
        object.applyRotation(rotation, local)
        
        #chooseMarker()
        
def chooseMarker():
    #print(logic.getCurrentScene().objects)
    #marker = types.KX_GameObject(logic.getCurrentScene().objects[6])
    #print(marker.position)
    #pass
    
    object = getOwner()
    #print(object.name)
    #print(object.position)
    
    order_move = pl.chooseDiceNum(dices)
    #print(order_move)
    player_markers = {}
    all_markers = {}
    
    markers = logic.getCurrentScene().objects
    #markers[2].position = [0.01, 3.66, 0.37]
    #markers[2].position = [-3.04, 1.83, 0.37]
    for i in markers:
        if 'Green' in i.name:
            player_markers[i.name] = [round(i.position[0], 2), round(i.position[1], 2), round(i.position[2], 2)]
        #if 'marker' in i.name:
        all_markers[i.name] = [round(i.position[0], 2), round(i.position[1], 2), round(i.position[2], 2)]
        #print(i.name, i.position)
    #print(markers[2].position)   
    new_pos = pl.Move(player_markers, all_markers).moveMarker(object.name, order_move['value_big'])
    #print(new_pos[object.name])
    
    for i in range(len(markers)):
        if 'Green' not in markers[i].name and 'marker' in markers[i].name:
            if new_pos[1][markers[i].name] != markers[i].position:
                markers[i].position = new_pos[1][markers[i].name]
                        
    object.position = new_pos[0][object.name]
    #print("Mouse: ", controller.sensors["Mouse"].level)
    
    #print("Mouse.001: ", controller.sensors["Mouse.001"].level)
    
    #mouse_pos = logic.mouse.position
    
    #object.position = [mouse_pos[0], mouse_pos[1], 0.2006]
    #if controller.sensors["Mouse"].status == 1:
        #object.position = [4.0, 0.0, 0.2006]