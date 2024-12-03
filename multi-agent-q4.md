### Multi-Agent Search

#### Q2: Minimax Agent

##### Nhiệm vụ

- Triển khai hàm getAction với thuật toán Expectimax nhằm giúp Pacman có thể đưa ra quyết định tốt nhất trong môi trường đa tác nhân (multi-agent).
- Chú thích:
    - Expectimax là tuật toán sử dụng trong trò chơi đối kháng trong đó các tác nhân cạnh tranh với người chơi sẽ đưa ra các quyết định một cách ngẫu nhiên, không hoàn toàn tối ưu.
    - Thuật toán này sẽ giúp người chơi chọn ra nước đi tối ưu trong hoàn cảnh này.

##### Phương pháp

- Triển khai thuật toán Expectimax với:
    - Pacman là tác nhân tối đa, luôn cố gắng tối ưu hóa điểm số.
    - Ghosts là các tác nhân ngẫu nhiên cạnh tranh với Pacman.
    - Chọn ra nước đi cho Pacman dựa vào điểm số trung bình của tất cả các nước đi có thể của tất cả các ghost agent trong trò chơi

##### Code

- Hàm getAction duyệt qua tất cả các nước đi hợp lệ của Pacman, gọi đên hàm expectValue để tìm ra nước đi mang lại điểm số cao nhất

```python
def getAction(self, gameState: GameState):
        actions = gameState.getLegalActions(0) # Lay ra danh sach cac nuoc di hop le cua Pacman
        currentScore = float("-inf")
        returnAction = ''
        for action in actions: # Duyet qua tung nuoc di trong danh sach
            nextState = gameState.generateSuccessor(0, action)
            score = self.expectValue(nextState, 0, 1) # Diem so du doan cho nuoc di da chon
            if score > currentScore:
                returnAction = action
                currentScore = score
        return returnAction # Nuoc di toi uu nhat

```

- Hàm expectValue dự đoán điểm số bằng cách lấy điểm trung bình của tất cả các nước đi có thể của đối thủ

```python
    def expectValue(self, gameState, depth, agentIndex):
        if gameState.isWin() or gameState.isLose(): # Tinh diem neu tro choi da ket thuc
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(agentIndex) # Lay ra danh sach cac nuoc di hop le cua ghost
        totalexpectedvalue = 0
        numberofactions = len(actions)
        for action in actions:
            successor= gameState.generateSuccessor(agentIndex,action)
            if agentIndex == (gameState.getNumAgents() - 1):
                expectedvalue = self.maxValue(successor,depth) # Goi den trang thai tiep theo cua Pacman
            else:
                expectedvalue = self.expectValue(successor,depth,agentIndex + 1) # Goi ham expectValue cua tat ca cac ghost agent con lai trong tro choi
            totalexpectedvalue = totalexpectedvalue + expectedvalue # Tinh tong diem cua tat ca cac nuoc di cua tat ca cac ghost agent
        if numberofactions == 0:
            return  0
        return float(totalexpectedvalue)/float(numberofactions) # Tra ve diem trung binh cua tat ca cac nuoc di cua cac ghost agent

```

- Hàm maxValue đưa ra các nước đi tối ưu cho Pacman dựa trên dự đoán từ expectValue

```python
    def maxValue(self, gameState, depth):
        currDepth = depth + 1
        if gameState.isWin() or gameState.isLose() or currDepth==self.depth: # Tra ve ket qua neu tro choi ket thuc hoac dat den gioi han do cao cua cay du doan
            return self.evaluationFunction(gameState)
        maxvalue = float("-inf") # Diem khoi tao
        actions = gameState.getLegalActions(0) # Lay ra cac hanh dong hop le cua Pacman
        for action in actions: # Duyet qua tat ca cac hanh dong 
            successor= gameState.generateSuccessor(0, action) # Trang thai tiep theo sau khi thuc hien hanh dong
            maxvalue = max (maxvalue, self.expectValue(successor, currDepth, 1)) # chon ra gia tri lon nhat giua maxvalue hien tai hoac expextvalue cua trang thai tiep theo
        return maxvalue

```