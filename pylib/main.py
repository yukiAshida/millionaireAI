import numpy as np
from copy import deepcopy

# docs生成時


if __name__=="__main__":
    from utils import showPlayers, compareCards, considerOrder, flowGame, nextTurn
    from utils import number, suit, NUMBER, SUIT
    from utils import N_Player
else:
    from .utils import showPlayers, compareCards, considerOrder, flowGame, nextTurn
    from .utils import number, suit, NUMBER, SUIT
    from .utils import N_Player

class State():
    """
    Attributes
    ----------
    players: list(list(int))
        プレイヤーの手札を表す
    field: list(int)
        場に出ているカードのリスト（巡目ごとにリセットされる）
    garbege: list(list(int))
        流れて捨てられたカードのリスト（流れた時点でfieldが追加される）
    phase: int
        場の状態支配変数（現状使われてない）
    turn: int
        巡目の支配変数（0 ~ N_Player-1）
    reverse: bool
        9リバース（Trueなら切り巡が逆転）
    back: bool
        11バック（Trueならカードの強さが逆転）
    out: list(bool)
        その巡に抜けたかどうか（Trueなら抜けてる）
    rank: list(int)
        その巡の順位
    last: int or None
        最後に切った人（パスで一巡した時に誰から次の巡の開始点になる） 
    """
    
    def __init__(self):
        
        self.players = [ [] for _ in range(N_Player) ]
        self.field = [] 
        self.garbege = []
        self.phase = 1
        self.turn = 0

        self.reverse = False
        self.back = False

        self.out = [False]*N_Player
        self.rank = [-1]*N_Player
        self.last = None

    def distribution(self):

        shuffle = np.random.permutation(np.arange(54))

        for i,card in enumerate(shuffle):
            self.players[i%N_Player].append(int(card))


# 状態オブジェクトを生成し，手札を配る
def initilizeGame():
    """
    Returns
    ---------
    state: State Object
        初期化された状態オブジェクトを返す
    """

    state = State()
    state.distribution()

    return state

# 現在の状態から切れるカードを取得
def possibleAction(state):
    """
    Parameters
    ------------
    state: State Object
        状態オブジェクト

    Returns
    ------------
    action_list: ndarray(55, dtype=bool)
        選択可能行動のリスト
        0 ~ 53はどのカードを切るか，54はパス
    """

    player = state.players[state.turn]
    action_list = np.zeros(55).astype(bool)

    # 初順以外はパス可能
    action_list[54] = state.field != [] 

    # 初順 or 強カードであれば切れる
    for card in player:

        if state.field == [] or (compareCards(card, state.field[-1], back = state.back) and considerOrder(card, state.field, back = state.back)):
            action_list[card] = True
    
    return action_list


def selectAction(state, action_list):
    """
    Parameters
    ------------
    state: State Object
        状態オブジェクト
    action_list: ndarray(55, dtype=bool)
        選択可能行動リスト

    Returns
    ------------
    selected_action: int
        選択行動
    
    Notes:
    ------------
    乱数で適当に選ぶ
    """

    # boolテーブルをカード値に変換
    index_list = np.where(action_list)[0]
    
    # ランダムに行動を選択する
    if len(index_list)>1 and 54 in index_list:
        index_list = index_list[:-1]

    selected_action = np.random.choice(index_list)

    return selected_action


def nextState(original_state, action):
    """
    Parameters
    ------------
    original_state: State Object
        状態オブジェクト
    
    action: int
        行動

    Returns
    ------------
    next_state: State Object
        次の状態
    reward: list(int) or None
        報酬（ゲーム終了時のみ順位リストを返す，それ以外はNone）
    
    Notes:
    ------------
    現在の状態stateに対して，actionが選択されたときに，遷移する状態を返す
    非破壊的メソッド
    """

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
    """
    Notes:
    ------------
    基本的なゲームの進行
    """

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

    