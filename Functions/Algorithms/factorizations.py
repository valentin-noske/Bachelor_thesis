from typing import List


# Relevant functions


def equivalent_marker_sets(marker_sets: List[List[str]]) -> List[List[str]]:
    marker = list(set_of_markers(marker_sets))
    set_list = []
    for m in marker:
        temp = set()
        for elem in marker_sets:
            if m in elem:
                for e in elem:
                    if e != m:
                        temp.add(e)
        set_list.append(temp)
    result = []
    for u in range(0, len(set_list)):
        a = []
        for v in range(0, len(set_list)):
            if set_list[u] == set_list[v]:
                a.append(marker[v])
        a.sort()
        if a not in result:
            result.append(a)
    return result


def get_factorizations(marker_sets: List[List[str]]) -> List[List[List[str]]]:
    equivalent_markers = equivalent_marker_sets(marker_sets)
    factorizations = []
    for m in marker_sets:
        factorization = []
        for element in m:
            for em in equivalent_markers:
                if element in em:
                    factorization.append(em)
                    break
        factorization.sort()
        if factorization not in factorizations:
            factorizations.append(factorization)
    return factorizations

# Help functions


def set_of_markers(marker_sets: List[List[str]]) -> set:
    marker = set()
    for elem in marker_sets:
        for x in elem:
            marker.add(x)
    return marker
