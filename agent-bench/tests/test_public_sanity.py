from snake.game import init_state, step

# These are just very minimal sanity checks.
# Real tests are in ~/eval/hidden_tests/

def test_init_sets_basics():
    s = init_state(
        4, 3,
        snake=[(1, 1), (0, 1)],
        food={"apple": (3, 2), "big": (2, 0)},
        direction="R",
        wrap=False,
        obstacles=[(3, 0)],
    )
    assert s["alive"] is True
    assert s["score"] == 0
    assert s["steps"] == 0
    assert s["direction"] == "R"
    assert s["width"] == 4 and s["height"] == 3
    assert set(s["obstacles"]) == {(3, 0)}
    assert set(s["food"].keys()) == {"apple", "big"}

def test_step_moves_one_cell():
    s = init_state(
        5, 5,
        snake=[(2,2),(1,2),(0,2)],
        food={"apple": (4,4), "big": (4,3)},
        direction="R",
    )
    s2 = step(s, "R")
    assert s2["snake"][0] == (3,2)
    assert s2["steps"] == 1
