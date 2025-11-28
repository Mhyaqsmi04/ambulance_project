# src/ucs_multi_goal.py

from heapq import heappush, heappop
from src.search_common import Node, reconstruct_actions, goals_mask_for_positions, all_goals_mask, ensure_logs_dir
from src.cost_model import enter_cost, light_wait_time
import time, os

def uniform_cost_multi_goal(gridmap, start_pos, logname=None):
    """
    UCS multi-goal that explicitly inserts STAY actions when needed before
    entering a red traffic-light cell (L).
    Returns: cost, actions, nodes_expanded, logfile_path
    """
    goals = gridmap.goals
    n_goals = len(goals)
    target_mask = all_goals_mask(n_goals)
    start_mask = goals_mask_for_positions(goals, start_pos)

    start_node = Node(start_pos[0], start_pos[1], start_mask, 0, 0, parent=None, action=None, depth=0)

    frontier = []
    counter = 0
    heappush(frontier, (start_node.cost, counter, start_node))

    explored = dict()
    nodes_expanded = 0

    if logname is None:
        logname = f'ucs_log_{int(time.time())}.txt'
    logdir = ensure_logs_dir()
    logpath = os.path.join(logdir, logname)
    log_lines = []
    log_lines.append('UCS multi-goal log\n')

    while frontier:
        _, _, node = heappop(frontier)
        log_lines.append(f'POP state={(node.r,node.c,node.mask)} g={node.cost} time={node.time}\n')

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

        # expand successors
        for nr, nc, act in gridmap.neighbors(node.r, node.c):
            cell = gridmap.cell(nr, nc)

            # compute wait time BEFORE entering the neighbor
            wait = light_wait_time(cell, node.time)

            # If we must wait, we will create intermediate STAY nodes (staying in current cell)
            parent_for_entry = node
            # create STAY nodes one by one and push them as alternatives
            for i in range(wait):
                new_time = parent_for_entry.time + 1
                new_cost = parent_for_entry.cost + 1
                stay_node = Node(parent_for_entry.r, parent_for_entry.c, parent_for_entry.mask,
                                 new_time, new_cost, parent_for_entry, 'STAY', parent_for_entry.depth+1)
                counter += 1
                heappush(frontier, (stay_node.cost, counter, stay_node))
                log_lines.append(f'PUSH state={(stay_node.r,stay_node.c,stay_node.mask)} g={stay_node.cost} action=STAY time={stay_node.time}\n')
                parent_for_entry = stay_node

            # after waits, compute actual enter cost (should be enter_cost with updated time)
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
            counter += 1
            heappush(frontier, (child.cost, counter, child))
            log_lines.append(f'PUSH state={(child.r,child.c,child.mask)} g={child.cost} action={act} time={child.time}\n')

    # exhausted
    with open(logpath, 'w') as f:
        f.writelines(log_lines)
    return None, [], nodes_expanded, logpath
