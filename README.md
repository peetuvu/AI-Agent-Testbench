# Snake (logic only)

Implement snake game logic in `snake/game.py`.

Rules:
- Snake is list of (x, y) tuples, head first.
- step() moves the snake in action direction.
- If head moves onto food: grow by 1, score +1, respawn food deterministically.
- Wall collision: alive=False if head leaves bounds.
- Self collision: alive=False if head hits body.

Food respawn must be deterministic:
scan grid left-to-right, top-to-bottom, pick first empty cell.
