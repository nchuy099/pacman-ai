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
        # result có dạng [score, action]
        result = self.get_value(gameState, 0, 0)

        # Trả về action tốt nhất từ result
        return result[1] 
```

- Hàm `get_value`: Tính giá trị trạng thái và hành động tốt nhất

```python
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
```

- Hàm max_value cho Maximizer (Pacman)

```python
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
```

- Hàm min_value cho Minimizer (Ghosts)

```python
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
```
