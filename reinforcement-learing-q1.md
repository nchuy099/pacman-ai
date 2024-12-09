### Reinforcement Learning

#### Q1: Value Iteration

##### Nhiệm vụ

- Cài đặt thuật toán Value Iteration - `V*(s)` sử dụng phiên bản batch, `Vk(s)` dựa trên` Vk-1(s')`, cụ thể giá trị của trạng thái` `s tại vòng lặp` `k được tính từ các giá trị của các trạng thái mà trạng thái s có thể chuyển đến` (s')` trong vòng lặp trước đó` (k-1)` .
- Mục tiêu của thuật toán Value Iteration là tính toán giá trị tối ưu của các trạng thái trong một MDP (Markov Decision Process) và xác định hành động tối ưu tại mỗi trạng thái, sao cho phần thưởng lâu dài mà tác nhân nhận được là lớn nhất.

##### Phương pháp

Cài đặt các hàm sau

- Cài V\*(s): `__init__` và `runValueIteration(self)`: Hàm thực hiện thuật toán Value Iteration, lưu kết quả values của các states vào self.values
- Cài Q\*(s,a): `computeQValueFromValues(state, action)`: Tính giá trị `Q(s,a)` dựa trên self.values
- `computeActionFromValues(state)`: Tìm action tốt nhất tại 1 state dựa trên self.values

##### Code

-

```python
def runValueIteration(self):
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
```

-

```python
def computeQValueFromValues(self, state, action):
    q_value = 0  # Khởi tạo giá trị Q-value
    # Duyệt qua các trạng thái tiếp theo và xác suất chuyển
    for next_state, prob in self.mdp.getTransitionStatesAndProbs(state, action):
        reward = self.mdp.getReward(state, action, next_state)  # Lấy phần thưởng
        # Cập nhật giá trị Q-value
        q_value += prob * (reward + self.discount * self.values[next_state])

    return q_value  # Trả về giá trị Q-value
```

-

```python
def computeActionFromValues(self, state):
    # Lấy danh sách các hành động khả thi từ trạng thái hiện tại
    possible_actions = self.mdp.getPossibleActions(state)

    # Nếu không có hành động khả thi (trạng thái terminal), trả về None
    if not possible_actions:
        return None

    best_action = None  # Biến lưu hành động tốt nhất
    best_value = float('-inf')  # Khởi tạo giá trị tối ưu ban đầu bằng âm vô cùng

    # Duyệt qua từng hành động khả thi để tìm hành động có giá trị tốt nhất
    for action in possible_actions:
        # Tính giá trị Q cho hành động
        q_value = self.computeQValueFromValues(state, action)
        # Cập nhật hành động tốt nhất nếu giá trị Q lớn hơn
        if q_value > best_value:
            best_value = q_value
            best_action = action

    # Trả về hành động có giá trị Q cao nhất
    return best_action

```
