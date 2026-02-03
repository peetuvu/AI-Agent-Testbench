import copy

def init_state(width, height, snake, food, direction, wrap=False, obstacles=None):
    if obstacles is None:
        obstacles = []
        
    # Validate snake bounds
    for (x, y) in snake:
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError("Snake part out of bounds")
            
    # Validate snake no duplicates
    if len(set(snake)) != len(snake):
        raise ValueError("Snake has duplicates")
        
    # Validate food keys
    if set(food.keys()) != {"apple", "big"}:
        raise ValueError("Food keys must be 'apple' and 'big'")
        
    # Validation helpers sets
    snake_set = set(snake)
    obs_set = set(obstacles)
    
    # Validate obstacles
    for (x, y) in obstacles:
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError("Obstacle out of bounds")
    if len(obs_set) != len(obstacles):
        raise ValueError("Obstacles have duplicates")
    if not obs_set.isdisjoint(snake_set):
        raise ValueError("Obstacle overlaps snake")
        
    # Validate food positions
    apple = food["apple"]
    big = food["big"]
    
    foods = [("apple", apple), ("big", big)]
    for name, (fx, fy) in foods:
        if not (0 <= fx < width and 0 <= fy < height):
            raise ValueError(f"Food {name} out of bounds")
        if (fx, fy) in snake_set:
            raise ValueError(f"Food {name} overlaps snake")
        if (fx, fy) in obs_set:
            raise ValueError(f"Food {name} overlaps obstacle")
            
    if apple == big:
        raise ValueError("foods overlap")
        
    return {
        "width": width,
        "height": height,
        "snake": snake,
        "direction": direction,
        "alive": True,
        "score": 0,
        "steps": 0,
        "wrap": wrap,
        "obstacles": obstacles,
        "food": food
    }

def step(state, action):
    # Pure function
    new_state = copy.deepcopy(state)
    
    if not new_state["alive"]:
        return new_state
        
    # Update steps (happens regardless of validity of move? "steps: number of steps taken so far")
    # Actually, logic sequence:
    # 1. Parse action
    # 2. Move (or attempt)
    # 3. Update result
    
    # "If state['alive'] is False: return an unchanged copy with steps unchanged." -> Handled.
    # So Alive steps increment.
    
    current_dir = new_state["direction"]
    final_dir = current_dir
    
    opposites = {"U": "D", "D": "U", "L": "R", "R": "L"}
    
    if action is not None:
        if opposites.get(action) != current_dir:
            final_dir = action
            
    # Calculate target
    head_x, head_y = new_state["snake"][0]
    dx, dy = 0, 0
    if final_dir == "U": dy = -1
    elif final_dir == "D": dy = 1
    elif final_dir == "L": dx = -1
    elif final_dir == "R": dx = 1
    
    target_x = head_x + dx
    target_y = head_y + dy
    
    width = new_state["width"]
    height = new_state["height"]
    wrap = new_state["wrap"]
    
    out_of_bounds = False
    
    if wrap:
        target_x %= width
        target_y %= height
    else:
        if not (0 <= target_x < width and 0 <= target_y < height):
            out_of_bounds = True
            
    # Check Eating (Growth)
    # Determine growth before constructing body, but validation comes after?
    # Logic:
    # If we are effectively "landing" on food, we grow.
    # But if we die (wall/obstacle), we don't eat.
    # BUT we need to know if we grow to know if we die (self collision)?
    # "If head hits snake body (after movement)..."
    # If out_of_bounds -> Die.
    # If obstacle -> Die.
    
    # Let's assume we need to calculate potential growth to form the body to check self-collision.
    # However, if we die by Wall or Obstacle, it overrides eating.
    
    growth = 0
    eaten_type = None
    
    valid_position_for_eating = not out_of_bounds and (target_x, target_y) not in new_state["obstacles"]
    
    if valid_position_for_eating:
        if (target_x, target_y) == new_state["food"]["apple"]:
            growth = 1
            eaten_type = "apple"
        elif (target_x, target_y) == new_state["food"]["big"]:
            growth = 2
            eaten_type = "big"
            
    # Construct Snake
    current_snake = new_state["snake"]
    new_snake = [(target_x, target_y)]
    
    if growth == 0:
        new_snake.extend(current_snake[:-1])
    elif growth == 1:
        new_snake.extend(current_snake)
    elif growth == 2:
        new_snake.extend(current_snake)
        new_snake.append(current_snake[-1])
        
    new_state["snake"] = new_snake
    new_state["direction"] = final_dir
    new_state["steps"] += 1
    
    # Check Death
    died = False
    if out_of_bounds:
        died = True
    elif (target_x, target_y) in new_state["obstacles"]:
        died = True
    elif (target_x, target_y) in new_snake[1:]: # Head hits body
        died = True
        
    if died:
        new_state["alive"] = False
        return new_state
        
    # If not died, apply score and respawn
    if eaten_type:
        new_state["score"] += (1 if eaten_type == "apple" else 3)
        
        # Respawn
        other_food = new_state["food"]["big"] if eaten_type == "apple" else new_state["food"]["apple"]
        blockers = set(new_snake) | set(new_state["obstacles"]) | {other_food}
        
        found_pos = None
        for y in range(height):
            for x in range(width):
                if (x, y) not in blockers:
                    found_pos = (x, y)
                    break
            if found_pos: break
            
        if found_pos:
            new_state["food"][eaten_type] = found_pos
            
    return new_state
