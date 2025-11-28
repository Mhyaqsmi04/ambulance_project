
from heapq import heappush, heappop
from src.search_common import Node, reconstruct_actions, goals_mask_for_positions, all_goals_mask, ensure_logs_dir
from src.cost_model import enter_cost, light_wait_time
import time, os

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def heuristic_max_manhattan(pos, goals, mask):
    if mask == all_goals_mask(len(goals)):
        return 0
    best = 0
    for i, g in enumerate(goals):
        if not (mask & (1 << i)):
            d = manhattan(pos, g)
            if d > best:
                best = d
    return best

def a_star_multi_goal(gridmap, start_pos, logname=None):
    goals = gridmap.goals
    n_goals = len(goals)
    target_mask = all_goals_mask(n_goals)
    start_mask = goals_mask_for_positions(goals, start_pos)
    start_node = Node(start_pos[0], start_pos[1], start_mask, 0, 0, parent=None, action=None, depth=0)

    h0 = heuristic_max_manhattan((start_node.r, start_node.c), goals, start_node.mask)

    frontier = []
    counter = 0
    heappush(frontier, (start_node.cost + h0, counter, start_node))

    explored = dict()
    nodes_expanded = 0

    if logname is None:
        logname = f'astar_log_{int(time.time())}.txt'
    logdir = ensure_logs_dir()
    logpath = os.path.join(logdir, logname)
    log_lines = []
    log_lines.append('A* multi-goal log\n')

    while frontier:
        _, _, node = heappop(frontier)

        hval = heuristic_max_manhattan((node.r, node.c), goals, node.mask)
        log_lines.append(f'POP state={(node.r,node.c,node.mask)} g={node.cost} h={hval} f={node.cost+hval} time={node.time}\n')

        if node.mask == target_mask:
            actions = reconstruct_actions(node)
            log_lines.append(f'FOUND cost={node.cost} nodes_expanded={nodes_expanded}\n')
            with open(logpath, 'w') as f:
                f.writelines(log_lines)
            return node.cost, actions, nodes_expanded, logpath

        key = (node.r, node.c, node.mask)
        if key in explored and explored[key] <= node.cost:
            continue
        explored[key] = node.cost
        nodes_expanded += 1

        for nr, nc, act in gridmap.neighbors(node.r, node.c):
            cell = gridmap.cell(nr, nc)

            wait = light_wait_time(cell, node.time)

            parent_for_entry = node
            for i in range(wait):
                new_time = parent_for_entry.time + 1
                new_cost = parent_for_entry.cost + 1
                stay_node = Node(parent_for_entry.r, parent_for_entry.c, parent_for_entry.mask,
                                 new_time, new_cost, parent_for_entry, 'STAY', parent_for_entry.depth+1)
                counter += 1
                heappush(frontier, (stay_node.cost + heuristic_max_manhattan((stay_node.r, stay_node.c), goals, stay_node.mask), counter, stay_node))
                log_lines.append(f'PUSH state={(stay_node.r,stay_node.c,stay_node.mask)} g={stay_node.cost} action=STAY time={stay_node.time}\n')
                parent_for_entry = stay_node

            step_cost = enter_cost(cell, parent_for_entry.time)
            new_time = parent_for_entry.time + step_cost
            new_cost = parent_for_entry.cost + step_cost
            new_mask = parent_for_entry.mask
            if (nr, nc) in gridmap.goals:
                try:
                    idx = gridmap.goals.index((nr, nc))
                    new_mask = parent_for_entry.mask | (1 << idx)
                except ValueError:
                    pass

            child = Node(nr, nc, new_mask, new_time, new_cost, parent_for_entry, act, parent_for_entry.depth+1)
            hchild = heuristic_max_manhattan((child.r, child.c), goals, child.mask)
            counter += 1
            heappush(frontier, (child.cost + hchild, counter, child))
            log_lines.append(f'PUSH state={(child.r,child.c,child.mask)} g={child.cost} h={hchild} f={child.cost+hchild} time={child.time}\n')

    with open(logpath, 'w') as f:
        f.writelines(log_lines)
    return None, [], nodes_expanded, logpath
