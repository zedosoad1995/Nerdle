import itertools
import re

def get_possible_evals(cmds):
    allowed_eval_by_slot = []
    for cmd in cmds.split(' '):
        if 'g' in cmd:
            allowed_eval_by_slot.append(['g'])
        else:
            allowed_eval_by_slot.append(['g', 'r', 'b'])

    return list(itertools.product(*allowed_eval_by_slot))


def filter_zero_mult_div(possible_combinations):
    filtered_comb = []
    for comb in possible_combinations:
        if not re.search("[^\d]0\*|\*0|^0|[^\d]0\/", comb[0]):
            filtered_comb.append(comb)

    return filtered_comb


def get_combinations_dict(combs):
    combinations_dict = {}
    anti_combinations_dict = {}

    for comb in combs:
        for i, val in enumerate(comb[0]):
            i = str(i)
            if i not in combinations_dict:
                combinations_dict[i] = {}

            if val in combinations_dict[i]:
                combinations_dict[i][val].append(comb)
            else:
                combinations_dict[i][val] = [comb]

        for c in list('0123456789+*-/='):
            if c in comb[0]:
                continue

            if c in anti_combinations_dict:
                anti_combinations_dict[c].append(comb)
            else:
                anti_combinations_dict[c] = [comb]

    return combinations_dict, anti_combinations_dict


def delete_refs(lst):
    for el in lst:
        del el[:]

    lst.clear()


def remove_empty_lists(lst):
    i = 0
    while i < len(lst):
        if lst[i] == []:
            del lst[i]
        else:
            i += 1


def has_red_or_green_instance(cmd_slots, digit):
    colors = set()
    for cmd_slot in cmd_slots:
        d, c = cmd_slot
        if digit == d and (c == 'r' or c == 'g'):
            colors.add(c)

    return list(colors)
