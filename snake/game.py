# Implement init_state and step to satisfy tests.

def init_state(width, height, snake, food, direction):
    return {
        "width": width,
        "height": height,
        "snake": snake,
        "food": food,
        "direction": direction,
        "score": 0,
        "alive": True
    }

def step(state, action):
    if not state["alive"]:
        return state

    head_x, head_y = state["snake"][0]
    
    dx, dy = 0, 0
    if action == "R":
        dx = 1
    elif action == "L":
        dx = -1
    elif action == "U":
        dy = -1
    elif action == "D":
        dy = 1
        
    new_head = (head_x + dx, head_y + dy)
    nx, ny = new_head
    
    # Check wall collision
    if nx < 0 or nx >= state["width"] or ny < 0 or ny >= state["height"]:
        new_state = state.copy()
        new_state["alive"] = False
        return new_state
        
    # Check if eating food
    # If eating: grow (keep tail), score + 1, new food
    # If not eating: move (remove tail)
    
    snake = state["snake"]
    eaten = (new_head == state["food"])
    
    if eaten:
        new_snake = [new_head] + snake
    else:
        new_snake = [new_head] + snake[:-1]
        
    # Check self collision
    # Check if new_head is in the REST of the new body
    if new_head in new_snake[1:]:
        new_state = state.copy()
        new_state["alive"] = False
        return new_state
        
    new_state = state.copy()
    new_state["snake"] = new_snake
    new_state["direction"] = action # Update direction to new action
    
    if eaten:
        new_state["score"] = state["score"] + 1
        # Respawn food deterministic
        # Scan grid left-to-right, top-to-bottom, pick first empty cell.
        # Empty means not in new_snake
        
        found_food = None
        for y in range(state["height"]):
            for x in range(state["width"]):
                if (x, y) not in new_snake:
                    found_food = (x, y)
                    break
            if found_food is not None:
                break
        
        if found_food:
            new_state["food"] = found_food
        else:
            new_state["food"] = None 

    return new_state
