from snake.game import init_state, step

def test_move_right_shifts_tail():
    s = init_state(5, 5, snake=[(2,2),(1,2),(0,2)], food=(4,4), direction="R")
    s2 = step(s, "R")
    assert s2["snake"] == [(3,2),(2,2),(1,2)]
    assert s2["alive"] is True

def test_eat_grows():
    s = init_state(5, 5, snake=[(2,2),(1,2),(0,2)], food=(3,2), direction="R")
    s2 = step(s, "R")
    assert s2["snake"] == [(3,2),(2,2),(1,2),(0,2)]
    assert s2["food"] != (3,2)
    assert s2["score"] == 1

def test_wall_collision_kills():
    s = init_state(3, 3, snake=[(2,1),(1,1),(0,1)], food=(0,0), direction="R")
    s2 = step(s, "R")
    assert s2["alive"] is False

def test_self_collision_kills():
    s = init_state(5, 5, snake=[(2,2),(2,3),(1,3),(1,2),(1,1),(2,1)], food=(4,4), direction="L")
    s2 = step(s, "L")
    assert s2["alive"] is False
