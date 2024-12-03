# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodList = successorGameState.getFood().asList()
        closestFood = float('inf')

        # XỬ LÝ FOOD: Tìm khoảng cách đến thức ăn gần nhất
        for food in foodList:
            closestFood = min(closestFood, manhattanDistance(food, newPos))

        # XỬ LÍ GHOST: Kiểm tra khoảng cách đến từng con ma
        for ghost in successorGameState.getGhostPositions():
            # Nếu Pacman quá gần ma (khoảng cách < 2), phạt nặng, trả về giá trị âm lớn
            if manhattanDistance(newPos, ghost) < 2:
                return -float('inf')

        # Trả về điểm đánh giá
        # Thưởng dựa trên khoảng cách đến thức ăn gần nhất (càng gần càng tốt)
        return successorGameState.getScore() + 1.0 / (1.0 + closestFood)

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        # result có dạng [score, action]
        result = self.get_value(gameState, 0, 0)

        # Trả về action tốt nhất từ result
        return result[1] 
    
    def get_value(self, gameState, index, depth):
        """
        Đệ quy đánh giá gameState rồi trả về score tốt nhất cùng action
        Xử lý các trường hợp:
        1. Trạng thái kết thúc (terminal state)
        2. Maximizer (Pacman)
        3. Minimizer (Ghosts)
        """
        # Trạng thái kết thúc: Không có hành động hợp lệ hoặc đạt đến độ sâu tối đa
        if len(gameState.getLegalActions(index)) == 0 or depth == self.depth:
            return gameState.getScore(), ""  # Trả về điểm số và không có hành động

        # Maximizer (Pacman), index = 0
        if index == 0:
            return self.max_value(gameState, index, depth)

        # Các minimizers (Ghosts), index > 0
        else:
            return self.min_value(gameState, index, depth)

    def max_value(self, gameState, index, depth):
        """
        Đánh giá và trả về ulitity tốt nhất và action cho Max-agent (Pacman).
        Tìm giá trị cao nhất trong số các hành động có thể thực hiện.
        """
        legalMoves = gameState.getLegalActions(index)  # Tất cả các hành động hợp lệ của Pacman
        max_value = float("-inf")  # Khởi tạo giá trị tối thiểu ban đầu
        max_action = ""  # Hành động tốt nhất

        # Duyệt qua tất cả các hành động hợp lệ của Pacman
        for action in legalMoves:
            # Sinh trạng thái kế tiếp sau khi thực hiện hành động
            successor = gameState.generateSuccessor(index, action)
            successor_index = index + 1  # Chuyển sang tác nhân tiếp theo (Ghost)
            successor_depth = depth

            # Nếu tất cả các tác nhân (bao gồm Ghost) đã thực hiện hành động, tăng độ sâu
            if successor_index == gameState.getNumAgents():
                successor_index = 0  # Quay lại Pacman
                successor_depth += 1  # Tăng độ sâu

            # Đệ quy đánh giá trạng thái kế tiếp và lấy giá trị của nó
            current_value = self.get_value(successor, successor_index, successor_depth)[0]

            # Cập nhật giá trị tối đa và hành động tốt nhất nếu tìm được giá trị lớn hơn
            if current_value > max_value:
                max_value = current_value
                max_action = action

        return max_value, max_action

    def min_value(self, gameState, index, depth):
        """
        Đánh giá và trả về giá trị tối ưu cho Min-agent (Ghosts).
        Tìm giá trị thấp nhất trong số các hành động có thể thực hiện.
        """
        legalMoves = gameState.getLegalActions(index)  # Tất cả các hành động hợp lệ của Ghost
        min_value = float("inf")  # Khởi tạo giá trị tối đa ban đầu
        min_action = ""  # Hành động tốt nhất

        # Duyệt qua tất cả các hành động hợp lệ của Ghost
        for action in legalMoves:
            # Sinh trạng thái kế tiếp sau khi thực hiện hành động
            successor = gameState.generateSuccessor(index, action)
            successor_index = index + 1  # Chuyển sang tác nhân tiếp theo
            successor_depth = depth

            # Nếu tất cả các tác nhân (bao gồm Ghost) đã thực hiện hành động, tăng độ sâu
            if successor_index == gameState.getNumAgents():
                successor_index = 0  # Reset to Pacman
                successor_depth += 1  # Increase the depth

            # Đệ quy đánh giá trạng thái kế tiếp và lấy giá trị của nó
            current_value = self.get_value(successor, successor_index, successor_depth)[0]

            # Cập nhật giá trị tối thiểu và hành động tốt nhất nếu tìm được giá trị nhỏ hơn
            if current_value < min_value:
                min_value = current_value
                min_action = action

        return min_value, min_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # Kết quả được định dạng là [score, action] 
        # Trạng thái ban đầu: index = 0, depth = 0, alpha = -vô cùng, beta = +vô cùng
        result = self.get_value(gameState, 0, 0, float("-inf"), float("inf"))

        # Trả về action từ result
        return result[1]

    def get_value(self, gameState, index, depth, alpha, beta):
        """
        Trả về cặp [score, action] tùy theo tình huống:
        1. Trạng thái kết thúc (terminal state)
        2. Tác nhân tối đa (Max-agent)
        3. Tác nhân tối thiểu (Min-agent)
        """
        # Kiểm tra terminal state: Không có action hợp lệ hoặc đạt đến depth tối đa
        if len(gameState.getLegalActions(index)) == 0 or depth == self.depth:
            return gameState.getScore(), ""

        # Max-agent: Pacman, index = 0
        if index == 0:
            return self.max_value(gameState, index, depth, alpha, beta)

        # Min-agent: Ghosts, index > 0
        else:
            return self.min_value(gameState, index, depth, alpha, beta)

    def max_value(self, gameState, index, depth, alpha, beta):
        """
        Tính score tốt nhất và action tương ứng cho Maximizer (Pacman) 
        sử dụng thuật toán Alpha-Beta Pruning
        """
        legalMoves = gameState.getLegalActions(index)
        max_value = float("-inf")
        max_action = ""

        for action in legalMoves:
            # Sinh trạng thái kế tiếp
            successor = gameState.generateSuccessor(index, action)
            successor_index = index + 1 # agent kế tiếp
            successor_depth = depth # depth hiện tại

            # Nếu đã đi qua tất cả agents, quay lại Pacman và tăng depth
            if successor_index == gameState.getNumAgents():
                successor_index = 0
                successor_depth += 1

            # Tính value
            current_value = self.get_value(successor, 
            successor_index, successor_depth, alpha, beta)[0]

            # Cập nhật giá trị tối đa và hành động tốt nhất nếu tìm thấy giá trị lớn hơn
            if current_value > max_value:
                max_value = current_value
                max_action = action

            # Cập nhật giá trị alpha
            alpha = max(alpha, max_value)

            # Nếu giá trị hiện tại vượt qua beta, dừng duyệt (cắt tỉa)
            if max_value > beta:
                return max_value, max_action

        return max_value, max_action

    def min_value(self, gameState, index, depth, alpha, beta):
        """
        Tính toán giá trị tối thiểu và hành động tương ứng cho Min-agent (Ghosts) 
        sử dụng thuật toán Alpha-Beta Pruning
        """
        legalMoves = gameState.getLegalActions(index)
        min_value = float("inf")
        min_action = ""

        for action in legalMoves:
            # Sinh trạng thái kế tiếp
            successor = gameState.generateSuccessor(index, action)
            successor_index = index + 1
            successor_depth = depth

            # Nếu tất cả tác nhân đã đi xong, quay lại Pacman và tăng độ sâu
            if successor_index == gameState.getNumAgents():
                successor_index = 0
                successor_depth += 1

            # Tính giá trị cho trạng thái kế tiếp
            current_value = self.get_value(successor, 
            successor_index, successor_depth, alpha, beta)[0]

            # Cập nhật giá trị tối thiểu và hành động tốt nhất nếu tìm thấy giá trị nhỏ hơn
            if current_value < min_value:
                min_value = current_value
                min_action = action

            # Update beta value cho minimizer hiện tại
            beta = min(beta, min_value)

            # Cập nhật giá trị beta
            if min_value < alpha:
                return min_value, min_action

        return min_value, min_action


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)
        currentScore = float("-inf")
        returnAction = ''
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            # Next level is a expect level. Hence calling expectLevel for successors of the root.
            score = self.expectValue(nextState, 0, 1)
            # Choosing the action which is Maximum of the successors.
            if score > currentScore:
                returnAction = action
                currentScore = score
        return returnAction

    def maxValue(self, gameState, depth):
        currDepth = depth + 1
        if gameState.isWin() or gameState.isLose() or currDepth==self.depth:
            return self.evaluationFunction(gameState)
        maxvalue = float("-inf")
        actions = gameState.getLegalActions(0)
        for action in actions:
            successor= gameState.generateSuccessor(0, action)
            maxvalue = max (maxvalue, self.expectValue(successor, currDepth, 1))
        return maxvalue
    
    def expectValue(self, gameState, depth, agentIndex):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        actions = gameState.getLegalActions(agentIndex)
        totalexpectedvalue = 0
        numberofactions = len(actions)
        for action in actions:
            successor= gameState.generateSuccessor(agentIndex,action)
            if agentIndex == (gameState.getNumAgents() - 1):
                expectedvalue = self.maxValue(successor, depth)
            else:
                expectedvalue = self.expectValue(successor, depth, agentIndex+1)
            totalexpectedvalue = totalexpectedvalue + expectedvalue
        if numberofactions == 0:
            return  0
        return float(totalexpectedvalue)/float(numberofactions)
        

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
