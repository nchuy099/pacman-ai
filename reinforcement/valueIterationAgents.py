# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # Lặp qua số lần iteration
        for i in range(self.iterations):  # Biến iteration lưu số vòng lặp hiện tại
            # Tạo một Counter mới để lưu giá trị tạm thời
            new_values = util.Counter()

            # Duyệt qua tất cả các trạng thái
            for state in self.mdp.getStates():
                # Nếu trạng thái là terminal, giá trị bằng 0
                if self.mdp.isTerminal(state):
                    new_values[state] = 0
                else:
                    # Tính giá trị tối ưu cho trạng thái
                    new_values[state] = max(
                        self.computeQValueFromValues(state, action)
                        for action in self.mdp.getPossibleActions(state)
                    )

            # Cập nhật giá trị sau mỗi vòng lặp
            self.values = new_values


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        q_value = 0  # Khởi tạo giá trị Q-value
        # Duyệt qua các trạng thái tiếp theo và xác suất chuyển
        for next_state, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            reward = self.mdp.getReward(state, action, next_state)  # Lấy phần thưởng
            # Cập nhật giá trị Q-value
            q_value += prob * (reward + self.discount * self.values[next_state])

        return q_value  # Trả về giá trị Q-value
        

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # Lấy danh sách các hành động khả thi từ trạng thái hiện tại
        possible_actions = self.mdp.getPossibleActions(state)

        # Nếu không có hành động khả thi (trạng thái terminal), trả về None
        if not possible_actions:
            return None

        best_action = None  # Biến lưu hành động tốt nhất
        best_value = float('-inf')  # Khởi tạo giá trị tối ưu ban đầu bằng âm vô cùng

        # Duyệt qua từng hành động khả thi để tìm hành động có giá trị tốt nhất
        for action in possible_actions:
            q_value = self.computeQValueFromValues(state, action)  # Tính giá trị Q cho hành động
            # Cập nhật hành động tốt nhất nếu tìm được giá trị Q lớn hơn giá trị tối ưu hiện tại
            if q_value > best_value:
                best_value = q_value
                best_action = action

        # Trả về hành động có giá trị Q cao nhất
        return best_action

        

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)