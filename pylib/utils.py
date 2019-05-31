# -*- coding: utf-8 -*-
"""
Created on Thu May 16 17:21:52 2019

@author: yassi
"""

N_Player = 4

# 0  - 12 => spade
# 13 - 25 => heart
# 26 - 38 => clover
# 39 - 51 => dia

NUMBER = ["3","4","5","6","7","8","9","10","J","Q","K","A","2","JOKER"]
SUIT = ["S","H","C","D","JOKER"]

def number(card):
    """
    Parameters
    ----------
    card: int
        カードID(0~53)
    
    Returns
    ----------
    number_id: int
        数字ID(0~13)
    
    Notes
    ----------
    返り値は強さ巡なので，0が3，12が2，13がJOKERに相当する
    """

    if card>=52:
        return 13
    return card%13

def suit(card):
    """
    Parameters
    ----------
    card: int
        カードID(0~53)
    
    Returns
    ----------
    number_id: int
        スートID(0~4)
    
    Notes
    ----------
    0=spade, 1=heart, 2=clover, 3=diamond, 4=JOKER 
    """
    return card//13

def compareCards(challenger, field, back):
    """
    Parameters
    ----------
    challenger: int
        場に出そうとしているカードのID(0~53)
    field: int
        場に出ているカードのID(0~53)
    back: bool
        11バック発動中か否か

    Returns
    ----------
    win: bool
        カードの強さからchallengerを場に出せるのかどうか
    """

    # 場がジョーカーの場合
    if SUIT[suit(field)]=="JOKER" and SUIT[suit(challenger)]=="S" and NUMBER[number(challenger)]=="3":
        return True
    
    # 出す側がジョーカー
    if SUIT[suit(challenger)]=="JOKER":
        return True

    # 数字勝負
    elif (-1 if back else 1)*(number(field) - number(challenger)) < 0:
        return True

    return False

def considerOrder(challenger, fields, back):
    """
    Parameters
    ----------
    challenger: int
        場に出そうとしているカードのID(0~53)
    fields: list(int)
        場
    back: bool
        11バック発動中か否か

    Returns
    ----------
    win: bool
        challengerを場に出せるのかどうか

    Notes
    ---------
        カードの連続性からchallengerが場に出せるか判断
        階段縛り・スート縛り・スぺ3
    """

    # 場がジョーカー or 切り出しがジョーカーの場合は階段・スート共に問題なし
    if not( SUIT[suit(fields[-1])]=="JOKER" or SUIT[suit(challenger)]=="JOKER"):
        
        # 階段縛り
        if len(fields)>1 and ( number(fields[-1]) - number(fields[-2]) )*(-1 if back else 1) == 1:
        
            if (number(challenger)-number(fields[-1]))*(-1 if back else 1)!=1:
                return False
        
        # スート縛り
        if len(fields)>1 and suit(fields[-1]) == suit(fields[-2]):
        
            if not suit(challenger) == suit(fields[-1]):
                return False

    # スぺ3
    if len(fields)>1 and SUIT[suit(fields[-2])]=="JOKER" and SUIT[suit(fields[-1])]=="S" and NUMBER[number(fields[-1])]=="3":
        return False
    
    return True

def nextTurn(current_turn, out, reverse=False, skip=False, kill=False, win=False):
    """
    Parameters
    ----------
    currnt_turn: int
        巡目（0 ~ N_Player-1）
    out: list(bool)
        各プレイヤーが抜けているかどうかを表すブール変数
    reverse: bool
        9リバース発動中かどうか
    skip: bool
        5スキップの有無
    kill: bool
        8切りの有無
    win: bool
        今出した人が上がったかどうか

    Returns
    ----------
    next_turn: int
        カード効果や抜けた人等を考慮して，次に切る人が誰か
    """

    r = -1 if reverse else 1
    k = 0 if kill else 1
    w = 1 if win else 0

    # rはリバースによる反転項
    # max(k,w)は和了と8切りによる残存項（8切りで和了でない場合のみcurrent残存）
    # sはスキップによる遷移回数
    
    next_turn = ( current_turn + max(k,w)*r )%N_Player

    # 抜けていた場合は次の人へ
    while out[next_turn]:
        next_turn = ( next_turn + max(k,w)*r )%N_Player

    if skip:

        next_turn = ( next_turn + max(k,w)*r )%N_Player

        # 抜けていた場合は次の人へ
        while out[next_turn]:
            next_turn = ( next_turn + max(k,w)*r )%N_Player

    return next_turn

def flowGame(state):
    """
    Parameters
    ----------
    state: State Object
        状態オブジェクト

    Notes
    ----------
        巡目が流れたときに呼ぶ関数（全員パス，8切り）
    """

    state.garbege.append(state.field)
    state.field = []
    state.back = False
    state.reverse = False

def showPlayerCards(player):
    """
    Parameters
    ----------
    player: list(int)
        プレイヤーの手札

    Notes
    ----------
        playerの手札を人が読めるように表示
    """

    for card in player:
        s = suit(card)
        n = number(card)

        card_string = SUIT[s] + "_" + NUMBER[n] if n!=None else SUIT[s]
        print( "["+card_string+"]", end=" " )

def showPlayers(players):
    """
    Parameters
    ----------
    players: list(list(int))
        プレイヤー全員の手札

    Notes
    ----------
        player全員の手札を人が読めるように表示
    """

    for i,player in enumerate(players):
        print("player{0}".format(i),end=": ")
        showPlayerCards(player)
        print()
    print()