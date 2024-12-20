### Reinforcement Learning

#### Q3: Q-learning

##### Nhiệm vụ

-  Cài đặt thuật toán Q-learning - một phương pháp học tăng cường không giám sát, trong đó một tác nhân (agent) học cách tối ưu hóa hành động của mình dựa trên phản hồi từ môi trường. Mục tiêu chính là học được hàm Q-value, biểu thị giá trị dự đoán khi thực hiện hành động  tại trạng thái.

#### Các thông số của thuật toán

- qvalue: Bảng Q-value lưu trữ giá trị.

- alpha: Tốc độ học (learning rate).

- discount: Hệ số chiết khấu (discount factor).

- epsilon: Xác suất chọn hành động ngẫu nhiên để khám phá.

#### Cài đặt thuật toán

- getQValue: Trả về giá trị nếu cặp tồn tại trong bảng Q-value, ngược lại trả về giá trị mặc định.
```python
    def getQValue(self, state, action):
        """
        Returns Q(state, action)
        Should return 0.0 if we have never seen a state or action before.
        """
        return self.qvalue[(state, action)] if (state, action) in self.qvalue else 0.0
```

- computeValueFromQValues: Tính giá trị là giá trị lớn nhất trong tất cả các với các hành động hợp lệ tại trạng thái hiện tại, nếu không có hành động hợp lệ (trạng thái kết thúc), hàm trả về.
```python
    def computeValueFromQValues(self, state):
        """
        Returns max_action Q(state, action)
        If there are no legal actions, return 0.0.
        """
        legalActions = self.getLegalActions(state)
        if len(legalActions) == 0:
            return 0.0
        
        # Tìm giá trị lớn nhất của Q-values
        return max([self.getQValue(state, action) for action in legalActions])
```

- computeActionFromQValues: Tìm ra hành động đem lại điểm số bằng với kết quả của computeValueFromQValues, chọn ra một hành động ngẫu nhiên trong số đó nếu có nhiều hành động thỏa mãn.
```python
    def computeActionFromQValues(self, state):
        """
        Compute the best action to take in a state.
        If there are no legal actions, return None.
        """
        legalActions = self.getLegalActions(state)
        if len(legalActions) == 0:
            return None

        maxQValue = self.computeValueFromQValues(state)
        
        # Tìm tất cả các hành động có giá trị Q-value bằng maxQValue
        bestActions = [action for action in legalActions if self.getQValue(state, action) == maxQValue]
        
        # Chọn ngẫu nhiên một hành động tốt nhất
        return random.choice(bestActions)
```

- update: Cập nhật Q-value sau khi thực hiện hành động
![Screenshot 2024-12-20 230642](https://github.com/user-attachments/assets/cea05959-b259-4a88-822a-9f22d84d2162)
```python
    def update(self, state, action, nextState, reward: float):
        """
        Update Q-value based on state, action, nextState, and reward.
        """
        sample = reward + self.discount * self.computeValueFromQValues(nextState)
        self.qvalue[(state, action)] = (1 - self.alpha) * self.getQValue(state, action) + self.alpha * sample
```
