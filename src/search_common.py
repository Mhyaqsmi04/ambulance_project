# src/search_common.py

import os

class Node:
    def __init__(self, r, c, mask, time, cost, parent=None, action=None, depth=0):
        self.r = r
        self.c = c
        self.mask = mask
        self.time = time      # minutes since start when we are at this node (after performing action)
        self.cost = cost      # accumulated cost (same as time)
        self.parent = parent
        self.action = action
        self.depth = depth

    def state(self):
        return (self.r, self.c, self.mask)


def reconstruct_actions(node):
    actions = []
    cur = node
    while cur is not None and cur.action is not None:
        actions.append(cur.action)
        cur = cur.parent
    return list(reversed(actions))


def goals_mask_for_positions(goals, pos):
    if pos in goals:
        idx = goals.index(pos)
        return 1 << idx
    return 0


def all_goals_mask(n):
    return (1 << n) - 1


def ensure_logs_dir():
    d = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(d):
        os.makedirs(d)
    return d
