# Pokemon Battle Simulator — Học OOP qua project thật

Project mô phỏng trận đấu Pokemon (turn-based, có team switch, status effect),
xây dựng để luyện 4 trụ cột OOP + composition thông qua debug thật, không chỉ
đọc lý thuyết.

## Cấu trúc file

| File | Vai trò |
|---|---|
| `Pokemon.py` | Dữ liệu + trạng thái 1 Pokemon (stats, HP, status, buff/debuff) |
| `Effect.py` | `Effect` (abstract) + `DamageEffect`, `InflictStatucEffect` |
| `Move.py` | 1 chiêu thức — chỉ giữ data + list `Effect`, không tự tính toán |
| `status.py` | `StatusCondition` (abstract) + `Burn`, `Poison`, `Paralysis` |
| `Trainer.py` | 1 trainer sở hữu team Pokemon, quản lý switch |
| `BattleSystem.py` | Điều phối turn: thứ tự đánh, thực thi move, cuối turn |
| `main.py` | Chương trình chính — chạy 1 trận đấu đầy đủ từ đầu tới khi có người thắng |

Chạy: `python3 main.py`

---

## OOP nằm ở đâu trong project này

### 1. Encapsulation — giấu trạng thái, chỉ lộ hành vi

| Chỗ nào | Vì sao không cho sửa trực tiếp |
|---|---|
| `Pokemon.take_damage()` | Là cổng duy nhất sửa `current_hp` — đảm bảo `max(0, ...)` clamp, HP không bao giờ âm |
| `Pokemon.apply_status()` | Là cổng duy nhất gán `status_condition` — đảm bảo `on_apply()` luôn được gọi, không bị quên |
| `Pokemon.get_effective_stat()` | Đọc stat đã áp buff/debuff, thay vì đọc thẳng field gốc (`self.atk`) lúc đang có `stat_stages` active |

### 2. Inheritance — class con thừa hưởng từ class cha

`Burn`, `Poison`, `Paralysis` kế thừa `StatusCondition`. `DamageEffect`,
`InflictStatucEffect` kế thừa `Effect`. Class con chỉ viết phần khác biệt,
phần còn lại dùng bản mặc định của cha (VD `Burn` không override
`on_turn_start` vì dùng nguyên bản `return True` từ `StatusCondition`).

### 3. Polymorphism — 1 lời gọi, nhiều hành vi tùy loại object thật

Giá trị lớn nhất, xuất hiện trong `BattleSystem`:

```python
move.execute(user, target)                     # không cần biết Move có bao nhiêu effect, loại gì
pokemon.status_condition.on_turn_start(user)    # không cần if isinstance(..., Burn)/(..., Paralysis)
```

Không có bất kỳ `if/elif` nào rẽ nhánh theo loại status hay loại effect —
Python tự chọn đúng method của class con dựa vào type thật lúc runtime.

### 4. Abstraction — giấu "cách làm", chỉ lộ "làm gì"

`Effect(ABC)` với `@abstractmethod apply()` — không cho phép tạo `Effect()`
trực tiếp, buộc mọi class con phải implement `apply()`. Nhờ vậy
`Move.execute()` tin tưởng tuyệt đối rằng mọi phần tử trong `effects` đều gọi
`.apply()` được, không cần kiểm tra kiểu.

### 5. Composition — quan hệ "has-a", bài học thiết kế lớn nhất

- `Trainer` **có** `list[Pokemon]` — không kế thừa từ `Pokemon`.
- `Move` **có** `list[Effect]` — bài học từ việc thiết kế chiêu **Ember**
  (vừa gây damage vừa có thể Burn): dùng inheritance đơn
  (`DamageMove`/`StatusMove`) sẽ bế tắc ngay khi cần kết hợp 2 hiệu ứng;
  composition (gắn nhiều `Effect` vào 1 `Move`) giải quyết gọn mà không cần
  thêm class mới cho mỗi tổ hợp.

---

## Các bug thật đã gặp trong lúc build (đáng nhớ hơn cả lý thuyết)

1. **Quên dấu `()` khi gọi hàm** — `random.random < self.chance` (thiếu `()`)
   so sánh function object với số → `TypeError` ngay lập tức. Loại lỗi
   Python không cảnh báo trước, phải chạy mới thấy.

2. **Đọc nhầm chỉ số của sai đối tượng** — `DamageEffect` từng lấy cả
   `atk`/`def` từ `target` thay vì `user`. Loại bug này **không crash**,
   chương trình chạy êm, số liệu nhìn "hợp lý" nhưng sai hoàn toàn logic —
   nguy hiểm hơn nhiều so với lỗi crash rõ ràng.

3. **Thụt lề sai khiến `print` thoát khỏi khối `if`** — thông báo
   "bị nhiễm status" vẫn hiện ra dù `random.random() < chance` là `False`.
   Python không có `{}` bao khối như C/Java, nên sai 1 khoảng trắng là đổi
   hẳn logic mà không có `SyntaxError` nào cảnh báo.

**Bài học chung:** OOP tốt (interface rõ ràng, encapsulation đúng) không
tự động ngăn được các loại bug logic âm thầm này — nó chỉ giúp khoanh vùng
lỗi nhanh hơn (bug chỉ nằm trong 1 method nhỏ, không lan khắp file) và giúp
viết test độc lập từng class dễ hơn. Cách duy nhất bắt được các bug loại 2
và 3 là **tự ép trường hợp biên** khi test (`chance=0.0`/`1.0`, so sánh
`raw` vs `effective` stat) — chạy với giá trị ngẫu nhiên bình thường không
đủ để lộ ra.

## Điểm cố ý đơn giản hoá (chưa làm, để giữ đúng mục tiêu học OOP)

- Damage formula không dùng `TypeChart` (hệ khắc hệ) — có thể tự thêm sau
  nếu muốn luyện thêm 1 class nữa.
- Chưa random 50/50 khi speed bằng nhau tuyệt đối (dùng stable sort, ai
  đứng trước trong list thắng).
- "Bắt buộc switch khi fainted" xử lý ở tầng gọi `run_turn()` (trong
  `main.py`), không tự động hoá bên trong `BattleSystem` — giữ
  `BattleSystem` đơn giản, chỉ điều phối 1 turn, không quản lý toàn bộ luồng
  trận đấu.
