import numpy as np
import random

from Simulation import Simulation, get_close_sim_for_box
from SystemBoxes import PendulumSystem, PHLevelSystem
from PygameBoxes import PendulumWindow, PHLevelWindow
from ExtraBoxes import DerivativeBox, ConstantBox, SubtractBox
from FuzzyControlBoxes import GeneticFuzzyController


def mutate_variables(variables_population):
    # print('begin', variables_population)
    variables_population = [
        [var + np.random.normal() for var in vars]
        for vars in variables_population]
    # print('interm', variables_population)
    for vars in variables_population:
        vars[0:7] = np.sort(vars[0:7])
        vars[7:14] = np.sort(vars[7:14])
    # print('final', variables_population)
    return variables_population


def reproduce_variables(variables_population):
    for vars in variables_population:
        vars_cross = random.choice(variables_population)
        for i in range(len(vars)):
            vars[i] = (vars[i] + vars_cross[i])/2
        vars[0:7] = np.sort(vars[0:7])
        vars[7:14] = np.sort(vars[7:14])
    return variables_population


def run_evolution(
        population_size, generations, keep_perc, muta_perc, repr_perc):

    keep_size = int(keep_perc*population_size)
    muta_size = int(muta_perc*population_size)
    repr_size = int(repr_perc*population_size)
    news_size = population_size - keep_size - muta_size - repr_size

    variables_population = get_random_population(population_size)
    for g in range(generations):
        results = sim_generation(variables_population)
        results.sort(key=lambda r: r['int_e'])
        print(results)

        variables_population = [r['variables'] for r in results]
        keep_population = variables_population[0:keep_size]
        muta_population = variables_population[0:muta_size]
        repr_population = variables_population[0:repr_size]
        news_population = get_random_population(news_size)

        muta_population = mutate_variables(muta_population)
        repr_population = reproduce_variables(repr_population)

        variables_population[0:keep_size] = keep_population
        temp = keep_size
        variables_population[temp:temp+muta_size] = muta_population
        temp += muta_size
        variables_population[temp:temp+repr_size] = repr_population
        temp += news_size
        variables_population[temp:temp+news_size] = news_population


def sim_generation(variables_population):
    results = []
    for vars in variables_population:
        results.append(run_sim(vars))
    return results


def get_random_population(population_size):
    variables_population = []
    for i in range(population_size):
        variables_population.append(get_random_variables())
    return variables_population


def get_random_variables():
    r1 = np.sort(np.random.uniform(low=0, high=14, size=(7,)))
    r2 = np.sort(np.random.uniform(low=0, high=14, size=(7,)))
    r3 = np.random.uniform(low=0, high=10, size=(9,))
    r4 = np.random.uniform(low=0, high=10, size=(9,))
    r = np.concatenate([r1, r2, r3, r4])
    return r


def run_sim(ctrl_variables):

    sim = Simulation(max_iters=1000)

    system = PHLevelSystem('p_sys', Ts, xi_0=3, zeta_0=2)
    # pygame_tracker = PHLevelWindow(
    #     'pygame', ['xi', 'zeta', 'pH', 'H'], 1/Ts,
    #     get_close_sim_for_box(sim),
    #     speed_up=1000)
    ref_box = ConstantBox('ref', 'r', 7)
    sub_box = SubtractBox('sub', 'r', 'pH', 'e')
    de_box = DerivativeBox('der', 'e', Ts)
    ctrl_box = GeneticFuzzyController(
        'ctrl', ['e', 'de'], ['f1', 'f2'], ctrl_variables)

    sim.add_box(system, {'f1': 0.081, 'f2': 0.512})
    # sim.add_box(pygame_tracker)
    sim.add_box(ref_box)
    sim.add_box(sub_box)
    sim.add_box(de_box)
    sim.add_box(ctrl_box)

    sim.run()

    # pygame_tracker.quit_pygame()

    return ctrl_box.get_performance()


if __name__ == "__main__":

    Ts = 0.1
    theta_0 = 0.3

    run_evolution(
        population_size=50, generations=30, keep_perc=0.25,
        muta_perc=0.25, repr_perc=0.25)
