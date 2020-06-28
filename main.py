import logging
from flask import Flask, redirect, url_for, render_template, request
import random
import numpy as np
import json
import ast

app = Flask(__name__)

imgs = {
    'player1': 'AR.jpeg',
    'player2': 'TD.jpeg',
    'player3': 'MB.jpeg',
    'player4': 'DirtyDieds.jpeg' 
}
cards = ['Person','Aphra', 'Diedrichs','Tommy Dean', 'Mombo', 'Weapon','Calculator','Textbook', 'Pen', 'Glass Bottle','Locations','ARC', 'ILC', 'Stages', 'Clark']

doors = [[3,1],[1,3],[1,6],[3,8],[6,1],[8,3],[8,6],[6,8]]

def input_setup():
    player_input = {}
    for i in range(15):
        if i % 5 != 0:
            player_input[str(i)] = ''
    return player_input

test = [0,0]

def setpos():
    start_pos = {
    'player1': [4,0],
    'player2': [9,4],
    'player3': [5,9],
    'player4': [0,5]}
    return start_pos

def move(player, Up, Left, Down, Right, loc):
    if isinstance(loc[player], str) == True:
        if loc[player] == 'ARC':
            if Right == 1:
                loc[player] = [3,1]
            elif Down == 1:
                loc[player] = [1,3] 
            else:
                loc[player] = 'ARC'    

        elif loc[player] == 'ILC':
            if Right == 1:
                loc[player] = [3,8]
            elif Up == 1:
                loc[player] = [1,6]  
            else:
                loc[player] = 'ILC'

        elif loc[player] == 'Stages':
            if Left == 1:
                loc[player] = [6,1]
            elif Down == 1:
                loc[player] = [8,3]
            else:
                loc[player] = 'Stages'

        elif loc[player] == 'Clark':
            if Left == 1:
                loc[player] = [6,8]
            elif Up == 1:
                loc[player] = [8,6]
            else:
                loc[player] = 'Clark'
        return loc
    else:
       if loc[player] in doors:
           if (loc[player] == doors[0] or loc[player] == doors[1]) and (Up == 1 or Left == 1):
               loc[player] = 'ARC'
           elif (loc[player] == doors[2] or loc[player] == doors[3]) and (Down == 1 or Left == 1):
               loc[player] = 'ILC'
           elif (loc[player] == doors[4] or loc[player] == doors[5]) and (Up == 1 or Right == 1):
               loc[player] = 'Stages'
           elif (loc[player] == doors[6] or loc[player] == doors[7]) and (Down == 1 or Right == 1):
               loc[player] = 'Clark'
           else:
               loc[player][1] = loc[player][1] + Down - Up
               loc[player][0] = loc[player][0] + Right - Left
           return loc
       else:
            if Up == 1:
                loc[player][1] = loc[player][1] - 1
            elif Down == 1:
                loc[player][1] = loc[player][1] + 1
            elif Left == 1:
                loc[player][0] = loc[player][0] - 1
            elif Right == 1:
                loc[player][0] = loc[player][0] + 1
    return loc

@app.route('/', methods=['POST', 'GET'])
def entry():
    if request.method == "POST":
        game = random.randint(10000,99999)
        test = request.form['name']
        return redirect(url_for("setup", game_num=test))
    else:
        return render_template('enter.html')


@app.route('/setup/<game_num>', methods=['POST', 'GET'])
def setup(game_num):
    if request.method =='POST':
        if request.form['player_name'] == 'Aphra':
            player_name = 'player1'
        elif request.form['player_name'] == 'TD':
            player_name = 'player2'
        elif request.form['player_name'] == 'Mombo':
            player_name = 'player3'
        elif request.form['player_name'] == 'DD':
            player_name = 'player4'
        return redirect(url_for("game",game_num=game_num,  player_name=player_name, location=setpos(), player_input=input_setup()))
    else:
        return render_template('setup.html', g_n = game_num) 

@app.route('/game/<game_num>/<player_name>/<location>/<player_input>', methods = ['POST','GET'])
def game(game_num, player_name, location, player_input):
    if request.method =='POST':
        player_input = ast.literal_eval(player_input)
        try:
            if request.form['arrow-keys'] == 'Up':
                act_loc = move(player_name,1,0,0,0, ast.literal_eval(location))
                return redirect(url_for('game', game_num=game_num,  player_name=player_name, location=act_loc, player_input=player_input))
            elif request.form['arrow-keys'] == 'Left':
                act_loc = move(player_name,0,1,0,0, ast.literal_eval(location))
                return redirect(url_for('game', game_num=game_num,  player_name=player_name, location=act_loc, player_input=player_input))
            elif request.form['arrow-keys'] == 'Down':
                act_loc = move(player_name,0,0,1,0, ast.literal_eval(location))
                return redirect(url_for('game', game_num=game_num,  player_name=player_name, location=act_loc, player_input=player_input))
            elif request.form['arrow-keys'] == 'Right':
                act_loc = move(player_name,0,0,0,1, ast.literal_eval(location))
                return redirect(url_for('game', game_num=game_num,  player_name=player_name, location=act_loc, player_input=player_input))  
        except KeyError:
            for i in range(len(cards)):
                if i % 5 != 0:
                    player_input[str(i)] += (' ' + (request.form[str(i)]))
        return redirect(url_for('game', game_num=game_num,  player_name=player_name, location=location, player_input=player_input))
    else:
	    return render_template('index.html', y=10, x=10, situation = ast.literal_eval(location), imgs = imgs, cards=cards, pi = ast.literal_eval(player_input), game_num=game_num)

if __name__ == '__main__':
	app.run(debug=True)
    
