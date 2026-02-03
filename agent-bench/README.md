# Snake v2 (logic only)

Implement snake game logic in `snake/game.py`.

## State representation

Use a plain dict (JSON-serializable) with these keys:

- `width` (int) : grid width, x in [0, width-1]
- `height` (int): grid height, y in [0, height-1]
- `snake` (list[tuple[int,int]]): list of (x, y) tuples, head first
- `direction` (str): one of "U","D","L","R" (current heading)
- `alive` (bool)
- `score` (int)
- `steps` (int): number of steps taken so far (starts at 0)
- `wrap` (bool): if True, crossing an edge wraps around; if False, wall kills
- `obstacles` (list[tuple[int,int]]): blocked cells
- `food` (dict[str, tuple[int,int]]): positions of foods by type:
  - "apple": grows by 1, +1 score
  - "big": grows by 2, +3 score

Notes:
- `food` always contains exactly these two keys: `"apple"` and `"big"`.
- Food and obstacles never overlap snake or each other.

## Functions

### `init_state(width, height, snake, food, direction, wrap=False, obstacles=None) -> dict`

- Validates inputs:
  - snake coordinates are in bounds
  - snake has no duplicates
  - food contains keys `"apple"` and `"big"`
  - foods are in bounds and not on snake/obstacles
  - obstacles are in bounds and unique and not on snake/food
  - direction is valid
- Initializes:
  - `alive=True`, `score=0`, `steps=0`
  - stores `wrap` and `obstacles` (empty list if None)

### `step(state, action) -> dict`

- Pure function: do not mutate `state`; return a new dict.
- If `state["alive"]` is False: return an unchanged copy with `steps` unchanged.
- `action` is one of "U","D","L","R" or None.
- If `action` is the direct reverse of current direction, ignore it.
  - reverse pairs: U<->D, L<->R
- Move the head by 1 cell in the resulting direction.
- Wrap behavior:
  - if `wrap` is True: x/y wrap with modulo
  - if `wrap` is False and head leaves bounds: `alive=False` and snake still updates to the out-of-bounds head (so behavior is explicit and testable)
- Collision:
  - If head hits snake body (after movement): `alive=False`
  - If head hits obstacle: `alive=False`
- Eating:
  - If head lands on `"apple"`: grow by 1 and `score += 1`
  - If head lands on `"big"`: grow by 2 and `score += 3`
  - Growing by g means: do not drop tail for this step (g=1), and additionally append the previous tail once more (g=2), i.e. net +g length
- Deterministic respawn:
  - When a food is eaten, respawn only that food type.
  - Respawn picks the first empty cell scanning:
    - x from 0..width-1 (left-to-right)
    - y from 0..height-1 (top-to-bottom)
    - (x changes fastest, then y)
  - An empty cell is not in snake, not in obstacles, and not occupied by the other food.

This project is used for benchmarking code generation. Determinism is mandatory.
