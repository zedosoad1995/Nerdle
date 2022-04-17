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
        if not re.search("[^\d]0\*|\*0|^0|[^\d]0\/", comb):
            filtered_comb.append(comb)

    return filtered_comb

