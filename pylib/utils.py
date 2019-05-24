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
    if card>=52:
        return 13
    return card%13

def suit(card):
    return card//13

def compareCards(challenger, field, back):

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

    state.garbege.append(state.field)
    state.field = []
    state.back = False
    state.reverse = False

def showPlayerCards(player):

    for card in player:
        s = suit(card)
        n = number(card)

        card_string = SUIT[s] + "_" + NUMBER[n] if n!=None else SUIT[s]
        print( "["+card_string+"]", end=" " )

def showPlayers(players):

    for i,player in enumerate(players):
        print("player{0}".format(i),end=": ")
        showPlayerCards(player)
        print()
    print()