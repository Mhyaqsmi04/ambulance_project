from src.ucs_multi_goal import uniform_cost_multi_goal
from src.a_star_multi_goal import a_star_multi_goal
from src.ga_assign import run_ga_assignment
from src.map_model import GridMap   # ✅ import your class


def read_grid_from_user():
    print("Enter your grid map.")
    print("Format:")
    print("First row (optional): rows cols")
    print("Then enter the grid rows using:")
    print("S = Start")
    print("G = Goal")
    print("L = Lava")
    print("Numbers (0-9) = Normal cells with cost")
    print()
    print("Example:")
    print("5 7")
    print("S11111G")
    print("111L111")
    print("1111111")
    print("11L11G1")
    print("1111111")
    print()

    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)

    return GridMap.parse_from_lines(lines)


def main():
    # ✅ Ask for scenario
    print("Choose a scenario:")
    print("  1  -> Uniform Cost Search")
    print("  2  -> A* Search")
    print("  3  -> Genetic Algorithm Assignment")
    print("  both -> Run UCS + A*")

    scenario = input("Enter scenario (1, 2, 3, both): ").strip()

    # ✅ Read grid from terminal
    grid = read_grid_from_user()

    # ✅ Scenario 1
    if scenario == "1":
        start = grid.starts[0]
        cost, acts, nodes, log = uniform_cost_multi_goal(grid, start)
        print(cost, acts, nodes)

    # ✅ Scenario 2
    elif scenario == "2":
        start = grid.starts[0]
        cost, acts, nodes, log = a_star_multi_goal(grid, start)
        print(cost, acts, nodes)

    # ✅ BOTH
    elif scenario == "both":
        print("=== Running Scenario 1 (UCS) ===")
        start = grid.starts[0]
        cost, acts, nodes, log = uniform_cost_multi_goal(grid, start)
        print(cost, acts, nodes)

        print("\n=== Running Scenario 2 (A*) ===")
        cost, acts, nodes, log = a_star_multi_goal(grid, start)
        print(cost, acts, nodes)

    # ✅ Scenario 3
    elif scenario == "3":
        starts = grid.starts
        incidents = grid.goals
        res = run_ga_assignment(grid, starts, incidents)

        print(f"Best makespan: {res['makespan']}")
        for i, s in enumerate(starts):
            print(f"Ambulance S{i+1} at {s}")
            print(f"  incidents: {res['assignments'][i]}")
            print(f"  time: {res['times'][i]}")

    else:
        print("❌ Invalid scenario")


if __name__ == "__main__":
    main()
