
def enter_cost(cell, current_time):
    """
    Cost to ENTER the given cell, based on current_time (minutes).
    S and G: 1
    N (numeric): that many minutes
    L: 1 if green, 10 if red (based on current_time % 20)
    """
    t = current_time % 20
    if cell.type in ("S", "G"):
        return 1
    if cell.type == "N":
        return cell.value
    if cell.type == "L":
        return 1 if t < 10 else 10
    raise Exception("Unknown cell type: " + str(cell.type))


def light_wait_time(cell, current_time):
    """
    If cell is 'L' and currently red, return how many minutes we must wait
    (number of STAY actions) so that the light becomes green.
    If not 'L' or already green, returns 0.
    """
    if cell.type != "L":
        return 0
    t = current_time % 20
    if t < 10:
        return 0
    return 20 - t
