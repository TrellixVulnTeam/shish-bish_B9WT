from bge import logic, render, types
from random import randint
import math
import sys
import os

scripts_path = os.path.join(os.path.split(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])[0], 'scripts')

#sys.path.insert(0, '/home/data/documents/python/shish-bish/scripts')
sys.path.insert(0, scripts_path)
import player_logic as pl

dices = {'Dice_1': 0, 'Dice_2': 0}
movement = 1
circle = 0
player = {'Green': 1, 'Yellow': 0, 'Blue': 0, 'Red': 0}
#order_move = {'value_big': 0, 'value_small': 0, 'movement': 1}

def getOwner():
    controller = logic.getCurrentController()
    object = controller.owner
    return object

def getScene():
    markers = logic.getCurrentScene().objects
    
    return markers

def goDice():
    global dices, player
    
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
        
    markers = getScene()
    
    for i in list(player.keys()):
        if player[i] == 1:
            marker_color = i
            break
        
    markers_list = getMarkersList(markers, marker_color)
        
    if dices['Dice_1'] != 0 and dices['Dice_2'] != 0:
        for i in range(2):
            order_move = pl.chooseDiceNum(dices)
            #print(order_move)
            if isPlMarkersFree(markers_list[0], markers_list[1], order_move, circle) is not True:
                for i in list(dices.keys()):
                    if dices[i] == order_move['value_big']:
                        dices[i] = 0
            
    #changePlayer(order_move)
        
def chooseMarker():
    global circle, movement, player

    object = getOwner()
    
    order_move = pl.chooseDiceNum(dices)
    #print(order_move)
    if 0 not in order_move.values():
        movement = order_move['movement']
    player_markers = {}
    all_markers = {}
    
    markers = getScene()
    #markers[2].position = [0.01, 3.66, 0.37]
    #markers[2].position = [-3.04, 1.83, 0.37]
    #markers[2].position = [-3.65, 3.04, 0.37]
    marker_color = object.name.split('_')[0]
    
    markers_list = getMarkersList(markers, marker_color)
    
    new_pos = pl.Move(markers_list[1], markers_list[0], circle).moveMarker(object.name, order_move['value_big'])
    
    for i in range(len(markers)):
        if marker_color not in markers[i].name and 'marker' in markers[i].name:
            if new_pos[1][markers[i].name] != markers[i].position:
                markers[i].position = new_pos[1][markers[i].name]
    
    if isPosChange(object, new_pos[0]) is True:
        for i in list(dices.keys()):
            if order_move['value_big'] == dices[i]:
                dices[i] = 0
                break
        
    object.position = new_pos[0][object.name]
    circle = new_pos[2]
    
    #changePlayer(order_move)

#Create lists for logic all_markers - all markers from field, markers - markers that use by current player
def getMarkersList(markers, marker_color):
    all_markers = {}
    player_markers = {}
    for i in markers:
        if marker_color in i.name:
            player_markers[i.name] = [round(i.position[0], 2), round(i.position[1], 2), round(i.position[2], 2)]
        all_markers[i.name] = [round(i.position[0], 2), round(i.position[1], 2), round(i.position[2], 2)]
    
    return (all_markers, player_markers)
    
def isPosChange(object, new_pos):
    if pl.nearlyEqual(object.position[0], new_pos[object.name][0]) is True and \
            pl.nearlyEqual(object.position[1], new_pos[object.name][1]) is True:
        return False
    else:
        return True
    
def isPlMarkersFree(all_markers, player_markers, order_move, circle):
    markers_list = list(player_markers.keys())
    marker_color = markers_list[0].split('_')[0]
    for i in list(all_markers.keys()):
        if marker_color in i:
            if pl.getMarkersMove(player_markers, all_markers, circle, i, order_move['value_big'], all_markers[i]) is True:
                #print('ok')
                return True
            
def changePlayer(order_move):
    global player
    
    if order_move['value_big'] == 0 and order_move['value_small'] == 0 and order_move['movement'] == 1:
        pl_keys = list(player.keys())
        for i in range(len(pl_keys)):
            if player[pl_keys[i]] == 1:
                player[pl_keys[i]] = 0
                player[pl_keys[i+1]] = 1
                break