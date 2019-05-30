import numpy as np
from copy import deepcopy

import pickle
import datetime
import os
import pandas as pd

# 試合のログを取ってAIの評価・比較をするための仕様変更のために作成
# MatchLog: 試合結果を逐次保持していき、pickleファイルを作成するためのクラス 

if __name__=="__main__":
    from utils import showPlayers, compareCards, considerOrder, flowGame, nextTurn
    from utils import number, suit, NUMBER, SUIT
    from utils import N_Player
else:
    from .utils import showPlayers, compareCards, considerOrder, flowGame, nextTurn
    from .utils import number, suit, NUMBER, SUIT
    from .utils import N_Player

class MatchLog():
    def __init__(self):
        # 配られた初期手札
        self.initial_hand = None
        # 最初にカードを切る人
        self.first_player = None
        # 順番が逆転していないかどうか
        self.initial_reverse = None
        # 切られたカードのログを入れる。
        self.log = None
        # 結果の順位()
        self.rank = None
        # メタデータ（活用未定）
        self.meta_data = None

    def initialize(self,initial_state):
        # 配られた初期手札
        self.initial_hand = initial_state.players
        # 最初にカードを切る人
        self.first_player = initial_state.turn
        # 順番が逆転していないかどうか
        self.initial_reverse = initial_state.reverse
        # 切られたカードのログを入れる。
        self.log = []
        # 結果の順位()
        self.rank = [0]*4
        # メタデータ（活用未定）
        self.meta_data = None

    # 実装完了
    def writeLog(self,state,action):
        player_id = state.turn
        player_action = action
        self.log.append([player_id,player_action])

    # 場が流れる時のログ保存
    def writeFrowLog(self):
        flow_log = [99,99]

        self.log.append(flow_log)

    # 最終順位を記録
    def write_rank(self,state):
        self.rank = state.rank

    # logをpickleファイルに保存する。
    def savePickle(self,folder_path,file_name_):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_name = folder_path + '\\' + file_name_ + '.pickle'
        with open(file_name, "wb") as f:
            out_data = {
            "meta_data" : self.meta_data,
            "initial_hand" : self.initial_hand,
            "first_player" : self.first_player,
            "initial_reverse" : self.initial_reverse,
            "log" : self.log,
            "rank" : self.rank
            }

            pickle.dump(out_data,f)
        print('saved')



class State():

    def __init__(self):
        
        self.players = [ [] for _ in range(N_Player) ]
        self.field = []
        self.garbege = []
        self.phase = 1
        self.turn = 0

        self.reverse = False
        self.back = False
        # 既にあがった人はTrue
        self.out = [False,False,False,False]
        # 初期値を-1 -> N_playerに変更
        self.rank = [N_Player]*4
        self.last = None

    def distribution(self):

        shuffle = np.random.permutation(np.arange(54))

        for i,card in enumerate(shuffle):
            self.players[i%N_Player].append(int(card))

    # プレイヤー視点の情報を返す。
    def getPlayerView(self,player_id):
        hands_numer = []
        for hands in self.platers:
            hands_number.append(len(hand))
        players_hand = self.players[player_id]
        data = {
            "hands_number" : hands_number,
            "player_hands" : players_hand
        }
        return data



# 状態オブジェクトを生成し，手札を配る
def initilizeGame():

    state = State()
    state.distribution()

    return state

# 現在の状態から切れるカードを取得
def possibleAction(state):

    player = state.players[state.turn]
    action_list = np.zeros(55).astype(bool)

    # 初順以外はパス可能
    action_list[54] = state.field != [] 

    # 初順 or 強カードであれば切れる
    for card in player:

        if state.field == [] or (compareCards(card, state.field[-1], back = state.back) and considerOrder(card, state.field, back = state.back)):
            action_list[card] = True
    
    return action_list

# 乱数で切る（Action関数）
def selectAction(state, action_list):

    # boolテーブルをカード値に変換
    index_list = np.where(action_list)[0]
    
    # ランダムに行動を選択する
    if len(index_list)>1 and 54 in index_list:
        index_list = index_list[:-1]

    selected_action = np.random.choice(index_list)

    return selected_action

# 行動に応じて
def nextState(original_state, action, match_log =None):


    # 現状態のコピー
    state = deepcopy(original_state)
    player = state.players[state.turn]


    # 状態フラグ
    kill8 = False
    skip5 = False
    outX = False

    # パスの場合
    if action == 54:    
        
        # 流れの場合
        if state.last == nextTurn(state.turn, state.out, reverse=state.reverse):
            
            # 流れによる場の初期化
            flowGame(state)
            if match_log != None:
                match_log.writeFrowLog()

            state.turn = state.last
            
            return (state, None) 
    
    # パス以外の行動の場合
    else:

        # 状態遷移(プレイヤーの手札から)
        cut_index = np.where(player==action)[0]
        state.players[state.turn] = np.delete(player, cut_index).tolist()
        state.field.append(action)
        

        # カード効果の処理
        card_number = NUMBER[number(action)]
        
        if card_number == "8":
            flowGame(state)
            kill8 = True

        elif card_number == "5":
            skip5 = True
        
        elif card_number == "J":
            state.back = True

        elif card_number == "9":
            state.reverse = bool(1-state.reverse)

        # 和了
        if len(state.players[state.turn])==0:
            
            outX = True
            state.out[state.turn] = True
            state.rank[state.turn] = sum( state.out )
            state.last = nextTurn(state.turn, state.out, reverse=state.reverse, skip=skip5, kill=kill8, win=True)

        # 非和了
        else:
            state.last = state.turn
    
    # ターンを進める
    state.turn = nextTurn(state.turn, state.out, reverse=state.reverse, skip=skip5, kill=kill8, win=outX)

    if sum(state.out)==N_Player-1:

        return (state, state.rank)
    else:
        return (state, None)

def loop():

    # ゲーム状態を初期化
    state = initilizeGame()
    
    # ゲームループ開始
    reward = None
    while not reward:

        #現在の状態において，現在ターンのプレイヤーが選択可能な行動リストを取得
        action_list = possibleAction(state)

        # 選択可能な行動リストから行動を選択する
        action = selectAction(state, action_list)

        # 現在の状態と選択行動から状態を進める
        state, reward = nextState(state, action)

        # 状態の表示
        # showPlayers(state.players)
        # print(reward)
        # print(state.field, state.turn, state.last)

    
def loop_log(match_log,forlder_path, file_name):

    # ゲーム状態を初期化
    state = initilizeGame()
    match_log.initialize(state)

    # ゲームループ開始
    reward = None
    while not reward:

        #現在の状態において，現在ターンのプレイヤーが選択可能な行動リストを取得
        action_list = possibleAction(state)

        # 選択可能な行動リストから行動を選択する
        action = selectAction(state, action_list)
        match_log.writeLog(state,action)

        # 現在の状態と選択行動から状態を進める
        state, reward = nextState(state,action,match_log)


        # 状態の表示
        showPlayers(state.players)
        # print(reward)
        # print(state.field, state.turn, state.last)

    # 順位を記録する
    match_log.write_rank(state)
    # 保存する。
    match_log.savePickle(forlder_path, file_name)
    return match_log.rank

def iterateMatch(iteration):
    match_log = MatchLog()
    date = datetime.datetime.today().strftime("%Y_%m_%d_%H_%M")
    folder_path = '..\\data\\match_log\\' + date
    file_name_ = 'match'
    stats_ls = []

    for i in range(iteration):
        file_name = file_name_ + "_{}".format(i)
        stats_ls.append(loop_log(match_log,folder_path,file_name))
    
    rank_stats_df = pd.DataFrame(stats_ls)
    
    file_name = folder_path + '\\' +'stats.csv'
    rank_stats_df.to_csv(file_name)
        

if __name__ == "__main__":

    iterateMatch(10)
    # loop()