from flask import Flask,render_template,jsonify,request
from pylib.main import State, nextState, initilizeGame, possibleAction, selectAction
import numpy as np
from pprint import pprint
app = Flask(__name__,template_folder='./public',static_folder='./public/js')

state = initilizeGame()
reward = None

def forReact(state):

    sending_data = { "player"+str(i): state.players[i] for i in range(4) }
    sending_data["field"] = [int(x) for x in state.field]
    sending_data["turn"] = int(state.turn)
    sending_data["reverse"] = state.reverse
    sending_data["back"] = state.back
    sending_data["rank"] = state.rank

    return sending_data

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/game',methods=["GET","POST"])
def game():

    global state
    global reward

    data = request.get_json()
    
    if reward != None:
        print(reward)
        state = initilizeGame()
        reward == None

    elif not data["start"]:

        #現在の状態において，現在ターンのプレイヤーが選択可能な行動リストを取得
        action_list = possibleAction(state)

        # 選択可能な行動リストから行動を選択する
        action = selectAction(state, action_list)

        # 現在の状態と選択行動から状態を進める
        state, reward = nextState(state, action)
    
    sending_data = forReact(state)
    #pprint(sending_data)
    
    return jsonify(sending_data)
    
    
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)