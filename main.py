# -------------------------------#
# ========== SETTINGS ========== #
# -------------------------------#

# Starting position, zero-indexed.
start = 1  # island = 1, dock = 1, garden = 1

# Total number of moves.
moves = 5  # island = 5, dock = 5, garden = 3

# Maximum amount of charge that can be stored by the console conductors.
max_charge = 34  # island = 34, dock = 7, garden = 4

# Amounts of charge accumulated in the console conductors when moving to each position.
nodes = (7, -3, 10, 2)  # island = (7, -3, 10, 2), dock = (1, -2, 4), garden = (1, 2, -1)

# -------------------------------#
# ========== INTERNAL ========== #
# -------------------------------#


def neighbors(pos):
    return [1] if pos == 0 else ([len(nodes) - 2] if pos == len(nodes) - 1 else [pos - 1, pos + 1])


class State:
    def __init__(self, score, pos, path):
        self.score = score
        self.pos = pos
        self.path = path

    def iterate(self, state_list):
        for i in neighbors(self.pos):
            state_list.append(State(max(0, min(max_charge, self.score + nodes[i])), i, self.path + [i]))

    def path_str(self):
        path_str = '->'.join([str(pos) for pos in self.path])
        return f'->{path_str}'

    def __lt__(self, other):
        return self.score < other.score or self.path < other.path

    def __hash__(self):
        return hash((self.score, self.pos, tuple(self.path)))


def main():
    move = 0
    state_lists = ([State(0, start, [])], [])

    def state_list(flag):
        return state_lists[flag ^ ((move & 1) == 1)]

    while move < moves:
        prev = state_list(False)
        curr = state_list(True)
        for state in prev:
            state.iterate(curr)
        prev.clear()
        move += 1

    final_state_list = state_list(False)
    final_state_list.sort()

    import collections
    final_state_dict = collections.defaultdict(list)
    for state in final_state_list:
        final_state_dict[state.score] += [state]

    final_state_dict = collections.OrderedDict(final_state_dict)
    for k in final_state_dict.keys():
        print(f'{k}:')
        print('\n'.join(state.path_str() for state in final_state_dict[k]))


if __name__ == '__main__':
    main()
