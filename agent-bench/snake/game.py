# Implement init_state and step to satisfy the spec in agent-bench/README.md.

def init_state(width, height, snake, food, direction, wrap=False, obstacles=None):
    """Initialize the game state.
    
    Args:
        width: Grid width
        height: Grid height
        snake: List of (x, y) tuples, head first
        food: Dict with "apple" and "big" keys mapping to (x, y) or None
        direction: Initial direction ("U", "D", "L", "R")
        wrap: Whether the snake wraps around the edges
        obstacles: List/set of (x, y) obstacle positions
    
    Returns:
        Dictionary containing the game state
    """
    if obstacles is None:
        obstacles = set()
    else:
        obstacles = set(obstacles)
    
    return {
        "width": width,
        "height": height,
        "snake": list(snake),  # Copy to avoid mutation
        "food": dict(food),  # Copy to avoid mutation
        "direction": direction,
        "wrap": wrap,
        "obstacles": obstacles,
        "alive": True,
        "score": 0,
        "steps": 0,
        "pending_growth": 0,
    }


def step(state, action):
    """Execute one game step.
    
    Args:
        state: Current game state dictionary
        action: Direction to move ("U", "D", "L", "R")
    
    Returns:
        New state dictionary after the step
    """
    # Create a new state (don't mutate the original)
    new_state = {
        "width": state["width"],
        "height": state["height"],
        "snake": list(state["snake"]),  # Copy
        "food": dict(state["food"]),  # Copy
        "direction": state["direction"],
        "wrap": state["wrap"],
        "obstacles": state["obstacles"],
        "alive": state["alive"],
        "score": state["score"],
        "steps": state["steps"] + 1,
        "pending_growth": state["pending_growth"],
    }
    
    # If already dead, return the state as is
    if not state["alive"]:
        return new_state
    
    # Determine the new direction (check for instant reversal)
    opposites = {"U": "D", "D": "U", "L": "R", "R": "L"}
    current_dir = state["direction"]
    
    if action == opposites[current_dir]:
        # Ignore the reverse direction
        new_direction = current_dir
    else:
        new_direction = action
    
    new_state["direction"] = new_direction
    
    # Calculate new head position
    head_x, head_y = state["snake"][0]
    
    if new_direction == "U":
        new_head = (head_x, head_y - 1)
    elif new_direction == "D":
        new_head = (head_x, head_y + 1)
    elif new_direction == "L":
        new_head = (head_x - 1, head_y)
    else:  # "R"
        new_head = (head_x + 1, head_y)
    
    # Handle wrapping or wall collision
    if state["wrap"]:
        new_head = (new_head[0] % state["width"], new_head[1] % state["height"])
    else:
        # Check for wall collision
        if (new_head[0] < 0 or new_head[0] >= state["width"] or
            new_head[1] < 0 or new_head[1] >= state["height"]):
            new_state["alive"] = False
            return new_state
    
    # Check for obstacle collision
    if new_head in state["obstacles"]:
        new_state["alive"] = False
        return new_state
    
    # Check for self-collision (don't include the tail since it will move)
    snake_body = state["snake"][:-1] if new_state["pending_growth"] == 0 else state["snake"]
    if new_head in snake_body:
        new_state["alive"] = False
        return new_state
    
    # Check if snake ate food
    ate_food = False
    food_type_eaten = None
    
    for food_type in ["apple", "big"]:
        if state["food"].get(food_type) == new_head:
            ate_food = True
            food_type_eaten = food_type
            
            # Update score (apple = 1, big = 5)
            if food_type == "apple":
                new_state["score"] += 1
                new_state["pending_growth"] += 1
            else:  # "big"
                new_state["score"] += 5
                new_state["pending_growth"] += 3
            
            break
    
    # Move the snake
    new_state["snake"] = [new_head] + state["snake"]
    
    # Handle growth or tail removal
    if new_state["pending_growth"] > 0:
        new_state["pending_growth"] -= 1
        # Keep the tail (snake grows)
    else:
        # Remove the tail (snake moves without growing)
        new_state["snake"] = new_state["snake"][:-1]
    
    # Respawn food if it was eaten
    if ate_food:
        new_state["food"][food_type_eaten] = _find_respawn_position(new_state)
    
    return new_state


def _find_respawn_position(state):
    """Find the first empty cell scanning left-to-right, top-to-bottom.
    
    Args:
        state: Current game state
    
    Returns:
        (x, y) tuple of the first empty position, or None if no space available
    """
    occupied = set(state["snake"])
    occupied.update(state["obstacles"])
    
    # Add all food positions to occupied
    for food_type in ["apple", "big"]:
        food_pos = state["food"].get(food_type)
        if food_pos is not None:
            occupied.add(food_pos)
    
    # Scan left-to-right, top-to-bottom
    for y in range(state["height"]):
        for x in range(state["width"]):
            if (x, y) not in occupied:
                return (x, y)
    
    return None  # No empty space available
