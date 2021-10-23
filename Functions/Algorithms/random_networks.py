

from typing import List
from itertools import product
import random

import pyboolnet.attractors as attractors
import pyboolnet.interaction_graphs as ig
import pyboolnet.state_transition_graphs as stg
import logging
import networkx

log = logging.getLogger(__name__)

# Relevant functions


def create_random_network_with_given_steady_states(
        steady_states: List[List[int]], max_predecessors: int, name: str
) -> None:
    states_length = len(steady_states[0])
    state_space = compute_state_space(n_components=states_length)

    nodes = ["v" + str(i) for i in range(states_length)]

    truth_table, predictor_set = create_truth_table_with_given_steady_states(steady_states=steady_states,
                                                                             max_predecessors=max_predecessors,
                                                                             state_space=state_space)
    bnet_on_the_basis_of_the_truth_table(truth_table, nodes, predictor_set, state_space, "models/"+name+".bnet")


def create_random_network_with_the_same_steady_states(primes: dict, name: str) -> None:
    igraph = ig.primes2igraph(primes)
    nodes = list(igraph.nodes())
    nodes.sort()
    stgraph = stg.primes2stg(primes, "asynchronous")
    steady_states, cyclic_states = attractors.compute_attractors_tarjan(stgraph)
    max_predecessors = compute_max_count_of_predecessors(igraph)
    steady_states = convert_steady_states_to_list(steady_states)
    states_length = len(steady_states[0])
    state_space = compute_state_space(n_components=states_length)
    truth_table, predictor_set = create_truth_table_with_given_steady_states(
        steady_states=steady_states, max_predecessors=max_predecessors, state_space=state_space
    )
    bnet_on_the_basis_of_the_truth_table(truth_table, nodes, predictor_set, state_space, name)

# Help functions


def compute_state_space(n_components: int) -> List[List[int]]:
    return [list(x) for x in product([0, 1], repeat=n_components)]


def compute_max_count_of_predecessors(igraph: networkx.DiGraph) -> int:
    return max([len(list(igraph.predecessors(n))) for n in igraph.nodes()])


def create_predictor_set_for_all_nodes(nodes_count: int, max_predecessor: int) -> List[List[int]]:
    predictor_set = []

    for i in range(nodes_count):
        k = random.randint(1, max_predecessor)
        predecessors = random.sample(population=range(nodes_count), k=k)
        predictor_set.append(predecessors)

    return predictor_set


def unintended_steady_states(
        truth_table: List[List[int]], steady_states: List[List[int]], state_space: List[List[int]]
) -> bool:

    for i, row in enumerate(truth_table):
        equal = True

        for j in range(len(row)):
            if state_space[i][j] != row[j]:
                equal = False
                break

        if equal and state_space[i] not in steady_states:
            return True

    return False


def column_is_equal_to_zero(truth_table: List[List[int]]) -> bool:
    return any(all(row[i] == 0 for row in truth_table) for i in range(len(truth_table[0])))


def convert_steady_states_to_list(steady_states: List[dict]) -> List[List[int]]:
    return [list(x.values()) for x in steady_states]


def equal_referring_to_predictor_set(state: List[int], comp_state: List[int], predictors: List[int]) -> bool:
    return all(state[x] == comp_state[x] for x in predictors)


def determine_value_in_truth_table(
        truth_table: List[List[int]],
        state_space: List[List[int]],
        state: List[int],
        predictors: List[int],
        index: int,
        value: int,
) -> bool:

    for i, row in enumerate(truth_table):
        comp_state = state_space[i]

        if equal_referring_to_predictor_set(state, comp_state, predictors):
            cell_has_already_different_value = abs(row[index] - state[index]) == 1
            if cell_has_already_different_value:
                return False
            else:
                row[index] = value
    return True


def initialize_truth_table(
        truth_table: List[List[int]],
        steady_states: List[List[int]],
        predictor_set: List[List[int]],
        state_space: List[List[int]],
) -> bool:
    states_length = len(truth_table[0])
    for i in range(states_length):
        if len(predictor_set[i]) == 0:
            for j, row in enumerate(truth_table):
                row[i] = state_space[j][i]

    for steady in steady_states:
        for i in range(states_length):
            successful = determine_value_in_truth_table(
                truth_table, state_space, steady, predictor_set[i], i, steady[i]
            )
            if not successful:
                return False
    return True


def fill_truth_table(truth_table: List[List[int]], predictor_set: List[List[int]], state_space: List[List[int]]):
    for i, row in enumerate(truth_table):
        for j in range(len(row)):
            if row[j] != 1 and row[j] != 0:
                value = random.randint(0, 1)
                determine_value_in_truth_table(truth_table, state_space, state_space[i], predictor_set[j], j, value)


def bnet_on_the_basis_of_the_truth_table(
        truth_table: List[List[int]],
        nodes: List[str],
        predictor_set: List[List[int]],
        state_space: List[List[int]],
        name: str,
):
    file = open(name, "w")

    for n, node in enumerate(nodes):
        options = []
        predictors = predictor_set[n]

        if len(predictors) > 0:
            file.write(node+", ")
            function = ""

            for i, row in enumerate(truth_table):
                row_function = ""
                pos = row[n]

                if pos:
                    for p, pred in enumerate(predictors):
                        value = state_space[i][pred]
                        if value == 0:
                            row_function += "!"+nodes[pred]
                        else:
                            row_function += nodes[pred]
                        if len(predictors)-1 > p:
                            row_function += "&"

                    if row_function not in options:
                        if len(options) > 0:
                            function += "|"
                        function += row_function
                        options.append(row_function)
            file.write(function)
        file.write("\n")

    file.close()

    log.info("saved network with the same steady states")


def create_truth_table_with_given_steady_states(
        steady_states: List[List[int]],
        max_predecessors: int,
        state_space: List[List[int]],
) -> (List[List[int]], list):
    states_count = 2 ** len(steady_states[0])
    states_length = len(steady_states[0])

    truth_table = []
    predictor_set = []
    used_predictor_sets = []
    completed = False

    while not completed:
        truth_table_created = False

        while not truth_table_created:
            predictor_set = create_predictor_set_for_all_nodes(states_length, max_predecessors)
            if predictor_set not in used_predictor_sets:
                used_predictor_sets.append(predictor_set)
                temp_truth_table = [[-5] * states_length for _ in range(states_count)]
                created = initialize_truth_table(temp_truth_table, steady_states, predictor_set, state_space)
                if created and not unintended_steady_states(temp_truth_table, steady_states, state_space):
                    truth_table = temp_truth_table
                    truth_table_created = True

        count_of_attempts = 10

        for i in range(count_of_attempts):
            temp = truth_table.copy()
            fill_truth_table(temp, predictor_set, state_space)

            if not unintended_steady_states(temp, steady_states, state_space) and not column_is_equal_to_zero(temp):
                truth_table = temp
                completed = True

    return truth_table, predictor_set
