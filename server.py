from flask import Flask, request, render_template, redirect, url_for;
import logic
import pandas as pd
import os.path as path
import matplotlib.pyplot as plt
import matplotlib

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        return redirect(url_for('play', player1=request.form['player1'], player2=request.form['player2']))

@app.route('/play')
def play():
    return render_template('play.html')

@app.route('/win', methods=['GET'])
def win():
    moves = request.args['moves'].split(',')
    game = logic.Game()
    player = 'X'
    winner = None
    game.reset()

    for move in moves:
        coordinate = [x for x in move]
        game.update_board(int(coordinate[0]), int(coordinate[1]), player)
        player = game.other_player(player)
    winner = game.get_winner()
    if (winner == None):
        winner = ''
    return winner

def getPlayerStatus(winner, curr):
    if (winner == curr):
        return 1
    else:
        if (winner == 'Draw'):
            return 0
        else:
            return -1

@app.route('/record', methods=['GET'])
def record():
    winner = request.args['winner']
    player1 = request.args['player1']
    player2 = request.args['player2']
    player1Status = getPlayerStatus(winner, 'X')
    player2Status = getPlayerStatus(winner, 'O')


    if player1Status == 1:
        player_data = pd.DataFrame([[player1, 1, 0, 0, 2]], columns=['player', 'wins', 'losses', 'draws', 'total_score'])
    if player1Status == 0:
        player_data = pd.DataFrame([[player1, 0, 0, 1, 1]], columns=['player', 'wins', 'losses', 'draws', 'total_score'])
    if player1Status == -1:
        player_data = pd.DataFrame([[player1, 0, 1, 0, 0]], columns=['player', 'wins', 'losses', 'draws', 'total_score'])

    if player2Status == 1:
        player2_data = pd.DataFrame([[player2, 1, 0, 0, 2]], columns=['player', 'wins', 'losses', 'draws', 'total_score'])
    if player2Status == 0:
        player2_data = pd.DataFrame([[player2, 0, 0, 1, 1]], columns=['player', 'wins', 'losses', 'draws', 'total_score'])
    if player2Status == -1:
        player2_data = pd.DataFrame([[player2, 0, 1, 0, 0]], columns=['player', 'wins', 'losses', 'draws', 'total_score'])
    player_data = pd.concat([player_data, player2_data])

    if path.exists('tictactoe_global_data.csv') != False:
        load_player_data = pd.read_csv('tictactoe_global_data.csv')
        player_data = pd.concat([player_data, load_player_data])

        aggregation_functions = {'wins': 'sum', 'losses': 'sum', 'draws': 'sum', 'total_score': 'sum'}
        player_data = player_data.groupby(player_data['player'], sort = True).aggregate(aggregation_functions).reset_index()

    player_data = player_data.sort_values(by=['total_score'], ascending=False).reset_index(drop=True)

    player_data.to_csv('tictactoe_global_data.csv')

    matplotlib.use('agg')

    df = pd.read_csv('./tictactoe_global_data.csv', index_col='player')

    #1
    df[['wins', 'losses', 'draws']].plot(kind = 'bar')
    plt.savefig('./static/stats_1.png')

    # 2
    df[['total_score']].plot(kind = 'pie', y='total_score', autopct='%.f')
    plt.savefig('./static/stats_2.png')

    # 3
    df[['wins', 'losses', 'draws']].plot(kind = 'bar', stacked=True)
    plt.savefig('./static/stats_3.png')

    # 4
    df[['wins', 'losses', 'draws']].plot(kind = 'area', stacked=False)
    plt.savefig('./static/stats_4.png')

    return ''


@app.route('/stats')
def stats():
    return render_template('stats.html')