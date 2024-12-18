### Reinforcement Learning

#### Q2: Policies

##### Nhiệm vụ

-  thiết lập các tham số cho một MDP (Markov Decision Process) để đạt được các chính sách tối ưu (optimal policies) mong muốn trong bài toán Gridworld. Cụ thể, mỗi câu hỏi (từ question2a đến question2e) yêu cầu phải thiết lập các giá trị phù hợp cho các tham số

#### Các thông số và ý nghĩa

##### Discount
- Đây là giá trị quyết định mức độ quan tâm của agent đến phần thưởng tương lai.

- Discount càng cao (γ≈1) agent sẽ ưu tiên phần thưởng dài hạn.

- Discount thấp (γ≈0), agent sẽ tập trung vào phần thưởng ngay lập tức.
##### Noise 
- Noise đại diện cho tính bất định trong môi trường, khiến hành động của agent không luôn đi đúng hướng mong muốn.

- Noise thấp (Noise≈0) giúp agent di chuyển chính xác hơn.

- Noise cao (Noise≈1) làm tăng tính ngẫu nhiên, khiến agent khó kiểm soát hành động.
##### Living Reward 
- Đây là phần thưởng hoặc hình phạt mà agent nhận được tại mỗi bước.

- Living reward dương khuyến khích agent tiếp tục di chuyển, tránh kết thúc sớm.

- Living reward âm( <0 ) ép agent tìm cách nhanh chóng thoát khỏi lưới.

### Cài đặt thông số
#### Câu a: Prefer the close exit (+1), risking the cliff (-10)
##### Yêu cầu:
- Chính sách của agent nên ưu tiên đi đến lối thoát gần nhất (+1).
- Agent chấp nhận rủi ro có thể rơi xuống vách đá (-10) để đạt được lối thoát gần hơn.
##### Cách giải:
- Discount (0.7): Agent nên tập trung vào phần thưởng ngắn hạn thay vì phần thưởng tương lai. Một giá trị medium-high như 0.7 khuyến khích chọn đường ngắn.
- Noise (0.05): Giữ noise thấp để giảm khả năng bị lệch khỏi đường đi mong muốn. Điều này giúp agent mạo hiểm nhưng vẫn có xác suất cao chọn đúng lối.
- Living Reward (-2): Giá trị sống âm khuyến khích agent nhanh chóng tìm lối thoát để giảm thiểu mất mát.
##### kết quả:
```python
def question2a():
    return 0.7, 0.05, -2
```

#### Câu b: Prefer the close exit (+1), but avoiding the cliff(-10)
##### Yêu cầu:
- Agent vẫn ưu tiên đi đến lối thoát gần nhất (+1).
- Tuy nhiên, agent không được mạo hiểm đi qua khu vực gần vách đá.

##### Cách giải:
- Discount (0.5):Vẫn ưu tiên lối thoát gần nhưng giảm độ ưu tiên so với trường hợp trước, khiến agent không quá "tham lam".

- Noise (0.2): Tăng noise lên mức trung bình để tăng khả năng agent chọn đường an toàn hơn.
- Living Reward (-1): Giá trị sống âm nhẹ, thúc đẩy agent nhanh chóng tìm lối thoát nhưng không ép buộc chọn đường rủi ro.
##### kết quả:
```python
def question2b():
    return 0.5, 0.2, -1

```

#### Câu c: Prefer the distant exit (+10), risking the cliff (-10)
##### Yêu cầu:
- Chính sách của agent nên ưu tiên đi đến lối thoát xa (+10), bất kể rủi ro rơi xuống vách đá.
##### Cách giải:
- Discount (0.9): Giá trị cao để khuyến khích agent ưu tiên phần thưởng lớn trong tương lai (lối thoát xa).
- Noise (0.05): Noise thấp để giữ chính xác đường đi, giúp agent chấp nhận mạo hiểm.

- Living Reward (-2): Giá trị sống âm để giảm động lực lang thang và khuyến khích kết thúc sớm.
##### kết quả:
```python
def question2c():
    return 0.9, 0.05, -2
```

#### Câu d: Prefer the distant exit (+10), avoiding the cliff (-10)
##### Yêu cầu:
- Chính sách của agent ưu tiên đến lối thoát xa (+10).
- Tuy nhiên, agent phải chọn đường an toàn và tránh đi gần vách đá.
##### Cách giải:
- Discount (0.9): Giá trị cao để khuyến khích agent tập trung vào phần thưởng lớn ở tương lai.
- Noise (0.2): Tăng noise để giảm khả năng rơi vào các trạng thái gần vách đá.
- Living Reward (-1): Giá trị sống âm nhẹ khuyến khích tìm lối thoát nhưng không quá ép buộc.
##### kết quả:
```python
def question2d():
    return 0.9, 0.2, -1

```

#### Câu e: Avoid both exits and the cliff (so an episode should never terminate)
##### Yêu cầu:
- chính sách của agent phải tránh tất cả các lối thoát, không được rơi xuống vách đá, và lang thang vô tận.
##### Cách giải:
- Discount (0.01): Discount rất thấp để agent không quan tâm đến phần thưởng tương lai.

- Noise (0.3): Noise trung bình giúp tạo hành vi ngẫu nhiên hơn, giảm khả năng đến gần vách đá hoặc lối thoát.
- Living Reward (+20): Giá trị sống cao giúp agent cảm thấy việc tiếp tục di chuyển là tốt hơn so với việc kết thúc.
##### kết quả:
```python
def question2e():
    return 0.01, 0.3, 20
```
### Tóm tắt
![alt text](image.png)