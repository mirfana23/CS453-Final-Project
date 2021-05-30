import copy
import random
import os

def delete_random_character(s):
    if s == "":
        return s
    pos = random.randint(0, len(s) - 1)
    return s[:pos] + s[pos + 1:]

def insert_random_character(s):
    pos = random.randint(0, len(s))
    random_character = chr(random.randrange(32, 127))
    return s[:pos] + random_character + s[pos:]

def flip_random_character(s):
    if s == "":
        return s
    pos = random.randint(0, len(s) - 1)
    c = s[pos]
    bit = 1 << random.randint(0, 6)
    new_c = chr(ord(c) ^ bit)
    return s[:pos] + new_c + s[pos + 1:]

class InputFuzzer():
    def __init__(self, init_seed, max_one_mutate=3):
        self.initial_seed = init_seed
        self.input_queue_set = set(copy.deepcopy(self.initial_seed))
        self.input_queue_list = list(self.input_queue_set)
        self.queue_size = len(self.input_queue_list) 
        self.crash_input = set()
        self.list_mut_opr = [
            delete_random_character,
            insert_random_character,
            flip_random_character
        ]
        self.operator_size = len(self.list_mut_opr)
        self.max_one_mutate = max_one_mutate

    def reinit(self, init_seed, max_one_mutate=3):
        self.__init__(init_seed, max_one_mutate)

    def mutate(self, input, operator, ntimes):
        ret = input
        for _ in range(ntimes):
            ret = operator(ret)
        return ret

    def get_fuzzed_input(self):
        i_idx = random.randint(0, self.queue_size - 1)
        o_idx = random.randint(0, self.operator_size - 1)
        fuzzed_inp = copy.deepcopy(self.input_queue_list[i_idx])
        n_time = random.randint(1, self.max_one_mutate)
        fuzzed_inp = self.mutate(fuzzed_inp, self.list_mut_opr[o_idx], n_time)
        return fuzzed_inp

    def add_input(self, input):
        if input not in self.input_queue_set:
            self.input_queue_set.add(input)
            self.input_queue_list.append(input)
            self.queue_size = len(self.input_queue_list)

    def add_crash(self, crash):
        self.crash_input.add(crash)

    def save_input(self, path):
        os.makedirs(path, exist_ok=True)
        iq_path = os.path.join(path, "input")
        cq_path = os.path.join(path, "crash")
        os.makedirs(iq_path, exist_ok=True)
        for i_inp, inp in enumerate(self.input_queue_set):
            with open(os.path.join(iq_path, "input_{}".format(i_inp)), "w") as inpfile:
                inpfile.write(inp)
        os.makedirs(cq_path, exist_ok=True)
        for i_inp, inp in enumerate(self.crash_input):
            with open(os.path.join(cq_path, "crash_{}".format(i_inp)), "w") as inpfile:
                inpfile.write(inp)
