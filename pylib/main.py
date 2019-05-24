import numpy as np
from copy import deepcopy

if __name__=="__main__":
    from utils import showPlayers, compareCards, flowGame, nextTurn
    from utils import number, suit, NUMBER, SUIT
    from utils import N_Player
else:
    from .utils import showPlayers, compareCards, flowGame, nextTurn
    from .utils import number, suit, NUMBER, SUIT
    from .utils import N_Player


class State():

    def __init__(self):
        
        self.players = [ [] for _ in range(N_Player) ]
        self.field = []
        self.garbege = []
        self.phase = 1
        self.turn = 0

        self.reverse = False
        self.back = False

        self.out = [False,False,False,False]
        self.rank = [-1,-1,-1,-1]
        self.last = None

    def distribution(self):

        shuffle = np.random.permutation(np.arange(54))

        for i,card in enumerate(shuffle):
            self.players[i%N_Player].append(int(card))


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

        if state.field == [] or compareCards(card, state.field[-1], back = state.back):
            action_list[card] = True
    
    return action_list

# 乱数で切る（Action関数）
def selectAction(state, action_list):

    # boolテーブルをカード値に変換
    index_list = np.where(action_list)[0]
    
    # ランダムに行動を選択する
    selected_action = np.random.choice(index_list)

    return selected_action

# 行動に応じて
def nextState(original_state, action):


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
        print(state.last,state)
        if state.last == nextTurn(state.turn, state.out, reverse=state.reverse):
            
            # 流れによる場の初期化
            flowGame(state)
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
        print(card_number)
        
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

if __name__ == "__main__":

    loop()

    