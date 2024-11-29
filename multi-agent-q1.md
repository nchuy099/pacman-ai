### Multi-Agent Search

#### Q1: Reflex Agent

##### Nhiệm vụ

- Cải tiến ReflexAgent bằng cách tối ưu hàm evaluateFunction giúp Pacman đưa ra quyết định tức thì hiệu quả hơn
- ReflexAgent là agent phản ứng trực tiếp với trạng thái hiện tại, đưa ra hành động ngay lập tức mà không cần kế hoạch dài hạn.
- `evaluationFucntion` là hàm đánh giá giúp ReflexAgent biết được hành động nào là tốt hơn

##### Phương pháp

- Khuyến khích Pacman tiến đến gần thức ăn hơn bằng cách giảm khoảng cách đến thức ăn gần nhất
- Tránh ma quái bằng cách phạt nặng các hành động đưa Pacman đến gần chúng.

##### Code

#

```
def evaluationFunction(self, currentGameState: GameState, action):
    ...
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
```
