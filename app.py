from boggle import Boggle
from flask import Flask, render_template, session, request, jsonify
boggle_game = Boggle()
app = Flask(__name__)
app.config['SECRET_KEY'] = "something special"
boggle_ins = Boggle()

@app.route('/')
def board_home():
     """create a board and display it"""
     board = boggle_ins.make_board()
     session['board']=board

     return render_template("index.html", board = board)


@app.route('/check-guessed')
def checking_suggestion():
     """ check if guessed word is a valid word in board and dictionary """
     guessed_word = request.args.get("word")
     board = session.get('board')
     result= boggle_ins.check_valid_word(board, guessed_word)
     return jsonify({'result':result})


@app.route('/ending-game', methods=['POST'])
def end_Game():
     """ get the encountered score, update highscore if score is greater, and update the times the user played this game"""
     score = request.json['score']

     highscore = session.get("highscore", 0)

     session['num_played'] = session.get("num_played", 0) + 1

     session['highscore'] = max(score, highscore)

     return jsonify(brokeRecord=score > highscore)
