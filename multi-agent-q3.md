### Multi-Agent Search

#### Q2: Alpha-Beta Pruning

##### Nhiệm vụ

- Cài đặt thuật toán Alpha-Beta Pruning mở rộng để hỗ trợ nhiều tác nhân minimizer (minimizer agents), không chỉ tác nhân Pacman.

##### Phương pháp

- Tương tự với Minimax pacman, ta triển khai thuật toán Alpha-Beta với
  - Pacman là tác nhân tối đa (Maximizer), cố gắng tối ưu hóa điểm số.
  - Ghosts là các tác nhân tối thiểu (Minimizer), cố gắng làm giảm điểm của Pacman.

##### Code

- Hàm getAction lấy ra hành động tốt nhất

```python
    def getAction(self, gameState: GameState):
        "*** YOUR CODE HERE ***"
        # Kết quả được định dạng là [score, action]
        # Trạng thái ban đầu: index = 0, depth = 0, alpha = -vô cùng, beta = +vô cùng
        result = self.get_value(gameState, 0, 0, float("-inf"), float("inf"))

        # Trả về action từ result
        return result[1]
```

- Hàm `get_value`: Tính giá trị và hành động tốt nhất

```python
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
```

- Hàm max_value cho Maximizer (Pacman)

```python
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
```

- Hàm min_value cho Minimizer (Ghosts)

```python
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
```
