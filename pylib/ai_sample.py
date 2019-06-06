from ai import AbstractMillionareAI


 # data = {
 #        "hands_number" : hands_number,
 #        "player_hands" : players_hand,
 #        "card_log" : card_log
 #    }


class(AbstractMillionareAI):
    
    def __init__(self):
        self.is_initialize = False
        self.hands_num = 0
        self.weekest_card_id = None
        self.strongest_card_id = None

    def initialize_hands(self,data):
        self.is_initialized == True

    def selectAction(self, data, action_index_list):
        if self.is_initialized == False:
            self.initialize(self,data)

        