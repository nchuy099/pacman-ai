### Multi-Agent Search

#### Q5: Evaluation Function

##### Nhiệm vụ

- Viết một hàm đánh giá tốt hơn cho Pacman trong hàm betterEvaluationFunction. Hàm đánh giá này đánh giá các trạng thái, thay vì các hành động như hàm đánh giá của (reflex agent) đã viết trước đó.


##### Phương pháp

- Khuyến khích Pacman tiến đến gần thức ăn hơn bằng cách giảm khoảng cách đến thức ăn gần nhất
- Tránh ma quái bằng cách phạt nặng các hành động đưa Pacman đến gần chúng.

##### Code

- Thu thập thông tin từ trạng thái hiện tại:

```python
    pacPosition = currentGameState.getPacmanPosition()  # Lấy vị trí hiện tại của Pacman
    gList = currentGameState.getGhostStates()  # Lấy danh sách các ma trong trò chơi
    Food = currentGameState.getFood()  # Lấy ma trận thức ăn (nơi có các viên thức ăn)
    Capsules = currentGameState.getCapsules()  # Lấy danh sách các viên năng lượng (capsules)
```

- Kiểm tra các điều kiện thắng/thua:

```python
    if currentGameState.isWin():
        return float("inf")  # Nếu Pacman thắng, trả về giá trị vô cùng
    if currentGameState.isLose():
        return float("-inf")  # Nếu Pacman thua, trả về giá trị âm vô cùng
```

- Tính khoảng cách đến các viên thức ăn (Food):

```python
    foodDistList = [manhattanDistance(food, pacPosition) for food in Food.asList()]
    minFDist = min(foodDistList) if foodDistList else 0
```

- Tính khoảng cách đến các con ma (Ghosts):

```python
    GhDistList = []
    ScGhDistList = []
    for ghost in gList:
    dist = manhattanDistance(pacPosition, ghost.getPosition())
    if ghost.scaredTimer == 0:
        GhDistList.append(dist)  # Ma bình thường
    else:
        ScGhDistList.append(dist)  # Ma bị sợ
    # gList: Là danh sách các con ma, mỗi con ma có một thuộc tính scaredTimer cho biết liệu con ma đó có bị sợ hay không.
    # manhattanDistance(pacPosition, ghost.getPosition()): Tính khoảng cách Manhattan giữa Pacman và mỗi con ma.
    # GhDistList: Lưu các khoảng cách đến các con ma bình thường (không bị sợ).
    # ScGhDistList: Lưu các khoảng cách đến các con ma bị sợ.
```
- Tính toán khoảng cách gần nhất đến ma bình thường và ma bị sợ:

```python
    minGhDist=-1
    if len(GhDistList) > 0:
        minGhDist=min(GhDistList)        # minGhDist: Tìm khoảng cách gần nhất đến ma bình thường. Nếu không có ma bình thường, trả về giá trị vô cùng (Pacman không phải tránh ma).                                                                    
    minScGhDist=-1                                                                                          
    if len(ScGhDistList)>0:
        minScGhDist=min(ScGhDistList)     # minScGhDist: Tìm khoảng cách gần nhất đến ma bị sợ. Nếu không có ma bị sợ, trả về giá trị vô cùng.
    
```
- Tính toán điểm dựa trên các yếu tố:

```python
    score -= 1.5 * minFDist + 2 * (1.0 / minGhDist) + 2 * minScGhDist + 20 * len(Capsules) + 4 * len(Food.asList())

    # 1.5 * minFDist: Trừ đi điểm dựa trên khoảng cách đến thức ăn, khuyến khích Pacman tiến gần tới thức ăn. Trọng số 1.5 là một giá trị được chọn ngẫu nhiên và có thể điều chỉnh.
    # 2 * (1.0 / minGhDist): Thưởng cho Pacman khi tránh xa các ma bình thường. minGhDist càng nhỏ, điểm càng bị trừ. Tuy nhiên, thay vì trừ trực tiếp, ta sử dụng 1.0 / minGhDist để # tạo ra một hệ số thưởng nhỏ hơn cho các ma xa.
    
    # 2 * minScGhDist: Thưởng cho Pacman khi gần ma bị sợ. Các ma bị sợ có thể bị ăn và tăng điểm cho Pacman.
    # 20 * len(Capsules): Thưởng cho Pacman dựa trên số lượng viên năng lượng (capsules) còn lại, khuyến khích Pacman thu thập chúng.
    # 4 * len(Food.asList()): Trừ điểm cho số lượng thức ăn còn lại, khuyến khích Pacman ăn hết thức ăn nhanh chóng.
    
```
