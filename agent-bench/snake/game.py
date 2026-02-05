# Implement init_state and step to satisfy the spec in agent-bench/README.md.

OPPOSITES = {"U": "D", "D": "U", "L": "R", "R": "L"}
DELTAS = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}


def init_state(width, height, snake, food, direction, wrap=False, obstacles=None):
    """Initialize a new game state dictionary."""
    return {
        "width": width,
        "height": height,
        "snake": list(snake),
        "food": dict(food),
        "direction": direction,
        "wrap": wrap,
        "obstacles": set(obstacles) if obstacles else set(),
        "alive": True,
        "score": 0,
        "steps": 0,
        "pending_growth": 0,
    }


def _find_first_empty_cell(state):
    """Find the first empty cell scanning left-to-right, top-to-bottom."""
    snake_set = set(state["snake"])
    food_positions = {pos for pos in state["food"].values() if pos is not None}
    obstacles = state["obstacles"]
    
    for y in range(state["height"]):
        for x in range(state["width"]):
            pos = (x, y)
            if pos not in snake_set and pos not in food_positions and pos not in obstacles:
                return pos
    return None


def step(state, action):
    """Advance the game state by one step given an action."""
    # Create a new state (copy)
    new_state = {
        "width": state["width"],
        "height": state["height"],
        "snake": list(state["snake"]),
        "food": dict(state["food"]),
        "direction": state["direction"],
        "wrap": state["wrap"],
        "obstacles": set(state["obstacles"]),
        "alive": state["alive"],
        "score": state["score"],
        "steps": state["steps"],
        "pending_growth": state["pending_growth"],
    }
    
    # If already dead, return without changes
    if not new_state["alive"]:
        return new_state
    
    # Determine the actual direction (ignore reverse)
    current_dir = new_state["direction"]
    if action in DELTAS and OPPOSITES.get(action) != current_dir:
        current_dir = action
    new_state["direction"] = current_dir
    
    # Calculate new head position
    dx, dy = DELTAS[current_dir]
    head_x, head_y = new_state["snake"][0]
    new_x = head_x + dx
    new_y = head_y + dy
    
    # Handle wrapping or wall collision
    if new_state["wrap"]:
        new_x = new_x % new_state["width"]
        new_y = new_y % new_state["height"]
    else:
        if new_x < 0 or new_x >= new_state["width"] or new_y < 0 or new_y >= new_state["height"]:
            new_state["alive"] = False
            new_state["steps"] += 1
            return new_state
    
    new_head = (new_x, new_y)
    
    # Check obstacle collision
    if new_head in new_state["obstacles"]:
        new_state["alive"] = False
        new_state["steps"] += 1
        return new_state
    
    # Move the snake: add new head
    new_snake = [new_head] + new_state["snake"]
    
    # Check if eating food
    ate_apple = new_state["food"].get("apple") == new_head
    ate_big = new_state["food"].get("big") == new_head
    
    if ate_apple:
        new_state["score"] += 1
        new_state["pending_growth"] += 1
    
    if ate_big:
        new_state["score"] += 3
        new_state["pending_growth"] += 3
    
    # Handle tail: if pending_growth > 0, keep tail (grow), else remove
    if new_state["pending_growth"] > 0:
        new_state["pending_growth"] -= 1
        # Keep the tail (don't pop)
    else:
        new_snake.pop()
    
    new_state["snake"] = new_snake
    
    # Check self-collision (head collides with body)
    if new_head in new_state["snake"][1:]:
        new_state["alive"] = False
        new_state["steps"] += 1
        return new_state
    
    # Respawn food if eaten
    if ate_apple:
        new_state["food"]["apple"] = _find_first_empty_cell(new_state)
    if ate_big:
        new_state["food"]["big"] = _find_first_empty_cell(new_state)
    
    new_state["steps"] += 1
    return new_state
