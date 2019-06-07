from ai import AbstractMillionareAI
from utils import number, suit
import numpy as np


# data = {
#         "hands_number" : hands_number,
#         "player_hands" : players_hand,
#         "card_log" : card_log,
#         "garbege" : garbege,
#         "reverce" : reverce,
#         "back" : back
#     }


# "panda" has no meaning 
class PandaAI(AbstractMillionareAI):
    flow_log = [99,99]
    
    def __init__(self):
        self.is_initialized = False
        self.hands_num = 0
        self.weakest_card_id = None
        self.strongest_card_id = None

    # 未使用
    def initialize(self,data):
        self.is_initialized == True

    # 弱いカードを優先して選ぶ
    def selectWeakestCard(self,action_index_list):
        weakest_card_num = 15
        selected_action = None
        for action_id in action_index_list:
            card_num = number(action_id)
            if card_num == 2 and suit(action_id) == 0:
                continue
            if card_num < weakest_card_num:
                weakest_card_num = card_num
                selected_action = action_id

        if selected_action == None:
            selected_action = action_id[0]
        return selected_action

    def selectAction(self, data, action_index_list):
        if self.is_initialized == False:
            self.initialize(data)

        if len(action_index_list) == 1:
           selected_action = action_index_list[0]

        elif len(data["card_log"]) == 0 or data["card_log"][-1] == self.flow_log:
            # weakest card shoulu be selected
            selected_action = self.selectWeakestCard(action_index_list)

        elif data["back"] == True:
            # weakest card shoulu be selected
            selected_action = self.selectWeakestCard(action_index_list)

        else:
            # select action randomly
            if len(action_index_list)>1 and 54 in action_index_list:
                action_index_list = action_index_list[:-1]
            selected_action = np.random.choice(action_index_list)

        return selected_action

