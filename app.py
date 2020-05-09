from flask import Flask, redirect, url_for, render_template, request
import random
app = Flask(__name__)

test_loc = {
    'player1': 'Clark',
    'player2': [3,5],
    'player3': 'ARC',
    'player4': 'ARC'
}

imgs = {
    'player1': 'AR.jpeg',
    'player2': 'TD.jpeg',
    'player3': 'MB.jpeg',
    'player4': 'DirtyDieds.jpeg' 
}

info = {

}

@app.route('/start', methods=['POST', 'GET'])
def enter():
    if request.method == "POST":
        game = random.randint(1000,9999)
        game_name = request.form['name']
        return redirect(url_for("setup", game_num=game))
    else:
        return render_template('enter.html')

@app.route('/setup/<game_num>', methods=['POST', 'GET'])
def setup(game_num):
    if request.method =='POST':
        playerIP = request.environ['REMOTE_ADDR']
        player_name = request.form['player_name']
        return redirect(url_for('game',game_num=game_num,  player_name=player_name))
    else:
        return render_template('setup.html', g_n = game_num)

@app.route('/game/<game_num>/<player_name>', methods = ['POST','GET'])
def game(game_num, player_name):
	return render_template('index2.html', y=10, x=10, loc = test_loc, imgs = imgs)

if __name__ == '__main__':
	app.run(debug=True)

