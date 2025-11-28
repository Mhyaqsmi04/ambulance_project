# src/io_utils.py

def read_input_file(path):
    with open(path, "r") as f:
        lines = [line.rstrip("\n") for line in f if line.strip() != ""]
    # re-use existing GridMap parser
    from src.map_model import GridMap
    return GridMap.parse_from_lines(lines)


def print_result(cost, actions, nodes=None, logfile=None):
    # prints like: Cost: 24 min
    try:
        # make integer if close to int
        if abs(cost - round(cost)) < 1e-9:
            cost_print = int(round(cost))
        else:
            cost_print = cost
    except Exception:
        cost_print = cost

    print(f"Cost: {cost_print} min")
    print("Actions:", actions)
    if nodes is not None:
        print("Nodes expanded:", nodes)
    if logfile:
        print("Log file:", logfile)
