### Multi-Agent Search

#### Q2: Minimax Agent

##### Nhiệm vụ

- Triển khai hàm getAction với thuật toán Minimax
- Nhằm giúp Pacman có thể đưa ra quyết định tốt nhất trong môi trường đa tác nhân (multi-agent), nơi các "ma" cũng đóng vai trò như các tác nhân cạnh tranh.
- Chú thích:
  - Minimax là thuật toán trong trò chơi đối kháng 2 người, với Maximizer là người chơi cố gắng tối đa hóa điểm số và Minimizer là đối thủ cố gắng giảm điểm của Maximizer.
  - Thuật toán này giúp Maximizer chọn nước đi tối ưu

##### Phương pháp

- Triển khai thuật toán Minimax với
  - Pacman là tác nhân tối đa (Maximizer), cố gắng tối ưu hóa điểm số.
  - Ghosts là các tác nhân tối thiểu (Minimizer), cố gắng làm giảm điểm của Pacman.

##### Code

- Hàm getAction lấy ra hành động tốt nhất

```python
    def getAction(self, gameState: GameState):
    ...
        # Format of result = [score, action]
        result = self.get_value(gameState, 0, 0)

        # Return the action from result
        return result[1] # is the score
```

- Hàm `get_value`: Tính giá trị trạng thái và hành động tốt nhất

```python
    def get_value(self, gameState, index, depth):
        """
        Recursively evaluates the game state and returns the utility value and best action.
        Handles different cases:
        1. Terminal state
        2. Max-agent (Pacman)
        3. Min-agent (Ghosts)
        """
        # Terminal state: no legal actions or reached max depth
        if len(gameState.getLegalActions(index)) == 0 or depth == self.depth:
            return gameState.getScore(), ""  # Return score and no action

        # Max-agent (Pacman), index = 0
        if index == 0:
            return self.max_value(gameState, index, depth)

        # Min-agent (Ghosts), index > 0
        else:
            return self.min_value(gameState, index, depth)

```

- Hàm max_value cho Maximizer (Pacman)

```python
    def max_value(self, gameState, index, depth):
        """
        Evaluates and returns the best utility for Max-agent (Pacman).
        Finds the highest utility score among all possible actions.
        """
        legalMoves = gameState.getLegalActions(index)  # All possible actions for Pacman
        max_value = float("-inf")  # Start with the worst possible score
        max_action = ""  # Best action to be chosen

        for action in legalMoves:
            # Generate the successor state after taking the action
            successor = gameState.generateSuccessor(index, action)
            successor_index = index + 1  # Move to the next agent (Ghost)
            successor_depth = depth

            # If all agents (including ghosts) have moved, increase the depth level
            if successor_index == gameState.getNumAgents():
                successor_index = 0  # Reset to Pacman
                successor_depth += 1  # Increase the depth

            # Recursively evaluate the successor state and get its score
            current_value = self.get_value(successor, successor_index, successor_depth)[0]

            # Update the best value and action if a better value is found
            if current_value > max_value:
                max_value = current_value
                max_action = action

        return max_value, max_action
```

- Hàm min_value cho Minimizer (Ghosts)

```python
    def min_value(self, gameState, index, depth):
        """
        Evaluates and returns the worst utility for Min-agent (Ghosts).
        Finds the lowest utility score among all possible actions.
        """
        legalMoves = gameState.getLegalActions(index)  # All possible actions for Ghost
        min_value = float("inf")  # Start with the best possible score
        min_action = ""  # Best action to be chosen

        for action in legalMoves:
            # Generate the successor state after taking the action
            successor = gameState.generateSuccessor(index, action)
            successor_index = index + 1  # Move to the next agent
            successor_depth = depth

            # If all agents (including ghosts) have moved, increase the depth level
            if successor_index == gameState.getNumAgents():
                successor_index = 0  # Reset to Pacman
                successor_depth += 1  # Increase the depth

            # Recursively evaluate the successor state and get its score
            current_value = self.get_value(successor, successor_index, successor_depth)[0]

            # Update the worst value and action if a better value is found
            if current_value < min_value:
                min_value = current_value
                min_action = action

        return min_value, min_action
```
