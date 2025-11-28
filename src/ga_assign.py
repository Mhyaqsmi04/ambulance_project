import random
from src.a_star_multi_goal import a_star_multi_goal

# ✅ FIXED RANDOM SEED FOR CONSISTENT RESULTS
random.seed(1)


# ============================================
# CACHED TRUE SHORTEST PATH COST USING A*
# ============================================
def build_cost_cache(gridmap, starts, incidents):
    points = starts + incidents
    cache = {}

    for p1 in points:
        for p2 in points:
            if p1 == p2:
                cache[(p1, p2)] = 0
            else:
                old_goals = gridmap.goals
                gridmap.goals = [p2]
                cost, _, _, _ = a_star_multi_goal(gridmap, p1)
                gridmap.goals = old_goals

                if cost is None:
                    cost = 10**9

                cache[(p1, p2)] = float(cost)

    return cache


# ============================================
# CORRECT ROUTE TIME (GREEDY TSP ORDER)
# ============================================
def route_time(start, assigned, cost_cache):
    if not assigned:
        return 0.0

    remaining = assigned.copy()
    current = start
    total = 0.0

    while remaining:
        nearest = min(remaining, key=lambda x: cost_cache[(current, x)])
        total += cost_cache[(current, nearest)]
        current = nearest
        remaining.remove(nearest)

    return total


# ============================================
# ✅✅✅ FINAL WORKING GENETIC ALGORITHM
# ============================================
def run_ga_assignment(gridmap, starts, incidents, pop_size=120, generations=300):

    m = len(starts)      # number of ambulances
    n = len(incidents)   # number of incidents

    # ✅ PRECOMPUTE ALL TRUE PATH COSTS (NO FREEZING)
    cost_cache = build_cost_cache(gridmap, starts, incidents)

    # ============================================
    # GENOTYPE: list of length n, value in [0..m-1]
    # ============================================
    def random_individual():
        return [random.randrange(m) for _ in range(n)]

    def decode(ind):
        assigns = [[] for _ in range(m)]
        for i, amb in enumerate(ind):
            assigns[amb].append(incidents[i])
        return assigns

    def fitness(ind):
        assigns = decode(ind)
        times = [
            route_time(starts[i], assigns[i], cost_cache)
            for i in range(m)
        ]
        return -max(times)   # minimize makespan

    # ============================================
    # INITIAL POPULATION
    # ============================================
    population = [random_individual() for _ in range(pop_size)]
    best = population[0]
    best_f = fitness(best)

    # ============================================
    # EVOLUTION LOOP
    # ============================================
    for _ in range(generations):

        scored = [(fitness(ind), ind) for ind in population]
        scored.sort(reverse=True)

        if scored[0][0] > best_f:
            best_f = scored[0][0]
            best = scored[0][1]

        elite_count = max(1, pop_size // 5)
        next_pop = [ind for (_, ind) in scored[:elite_count]]

        def tournament():
            cand = random.sample(population, 3)
            cand.sort(key=lambda x: fitness(x), reverse=True)
            return cand[0]

        while len(next_pop) < pop_size:
            p1 = tournament()
            p2 = tournament()

            if random.random() < 0.8:
                child = [
                    p1[i] if random.random() < 0.5 else p2[i]
                    for i in range(n)
                ]
            else:
                child = p1.copy()

            for i in range(n):
                if random.random() < 0.15:
                    child[i] = random.randrange(m)

            next_pop.append(child)

        population = next_pop

    # ============================================
    # FINAL RESULT
    # ============================================
    final_assign = decode(best)

    final_times = [
        route_time(starts[i], final_assign[i], cost_cache)
        for i in range(m)
    ]

    return {
        "makespan": max(final_times),
        "assignments": final_assign,
        "times": final_times,
    }
