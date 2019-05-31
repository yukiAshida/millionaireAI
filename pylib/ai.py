from abc import ABCMeta, abstractmethod
import numpy as np

# 行動選択を行うAIの抽象クラス
class AbstractMillionareAI(metaclass = ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def selectAction(self, data, action_index_list):
        pass



class MonkeyAI(AbstractMillionareAI):

    def __str__(self):
        return "I am a monkey"

    def selectAction(self, data, action_index_list):

        if len(action_index_list)>1 and 54 in action_index_list:
            action_index_list = action_index_list[:-1]

        selected_action = np.random.choice(action_index_list)

        return selected_action
