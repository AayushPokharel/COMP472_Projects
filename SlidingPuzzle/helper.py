import numpy as np
from solver import Solver
import json


def BFS(init_state, goal_state, max_iter, heuristic):
    solver = Solver(init_state, goal_state, heuristic, max_iter)
    path = solver.solve_bfs()

    if len(path) == 0:
        exit(1)

    init_idx = init_state.flatten().tolist().index(0)
    init_i, init_j = init_idx // goal_state.shape[0], init_idx % goal_state.shape[0]

    result = {
        "initial_state": init_state.tolist(),
        "actions": [],
        "scores": [],
        "results": [],
        "solution": [],
    }

    for node in reversed(path):
        cur_idx = node.get_state().index(0)
        cur_i, cur_j = cur_idx // goal_state.shape[0], cur_idx % goal_state.shape[0]

        new_i, new_j = cur_i - init_i, cur_j - init_j
        action = ""
        if new_j == 0 and new_i == -1:
            action = "UP"
        elif new_j == 0 and new_i == 1:
            action = "DOWN"
        elif new_i == 0 and new_j == 1:
            action = "RIGHT"
        else:
            action = "LEFT"

        result["actions"].append(action)
        result["scores"].append(node.get_score() - node.get_level())
        result["results"].append(
            np.array(node.get_state())
            .reshape(goal_state.shape[0], goal_state.shape[0])
            .tolist()
        )
        result["solution"] = solver.get_summary()

    return json.dumps(result)


def A_star(init_state, goal_state, max_iter, heuristic):
    solver = Solver(init_state, goal_state, heuristic, max_iter)
    path = solver.solve_a_star()

    if len(path) == 0:
        exit(1)

    init_idx = init_state.flatten().tolist().index(0)
    init_i, init_j = init_idx // goal_state.shape[0], init_idx % goal_state.shape[0]

    result = {
        "initial_state": init_state.tolist(),
        "actions": [],
        "scores": [],
        "results": [],
        "solution": [],
    }

    for node in reversed(path):
        cur_idx = node.get_state().index(0)
        cur_i, cur_j = cur_idx // goal_state.shape[0], cur_idx % goal_state.shape[0]

        new_i, new_j = cur_i - init_i, cur_j - init_j
        action = ""
        if new_j == 0 and new_i == -1:
            action = "UP"
        elif new_j == 0 and new_i == 1:
            action = "DOWN"
        elif new_i == 0 and new_j == 1:
            action = "RIGHT"
        else:
            action = "LEFT"

        result["actions"].append(action)
        result["scores"].append(node.get_score() - node.get_level())
        result["results"].append(
            np.array(node.get_state())
            .reshape(goal_state.shape[0], goal_state.shape[0])
            .tolist()
        )
        result["solution"] = solver.get_summary()

    return json.dumps(result)


if __name__ == "__main__":
    # samples
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    init_state = np.array([[1, 8, 7], [3, 0, 5], [4, 6, 2]])

    # BFS(init_state, goal_state, max_iter=1000000, heuristic="misplaced_tiles")
    # BFS(init_state, goal_state, max_iter=1000000, heuristic="manhattan")

    # A_star(init_state, goal_state, max_iter=1000000, heuristic="misplaced_tiles")
    print(A_star(init_state, goal_state, max_iter=1000000, heuristic="manhattan"))
