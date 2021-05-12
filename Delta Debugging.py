import fuzzingbook_utils
from Fuzzer import RandomFuzzer, Runner
import re

def quicksort(numbers, low, high):
    i = low
    j = high
    pivot = numbers[int(low + (high-low)/2)]
    while i <= j:
        while numbers[i] < pivot:
            i+= 1
        while numbers[j] > pivot:
            j -= 1
        if i <= j:
            exchange(numbers, i, j)
        i += 1
        j -= 1
    if low < j:
        quicksort(numbers, low, j)
    if i < high:
        quicksort(numbers, i, high)


def exchange(numbers, i, j):
    temp = numbers[i]
    numbers[i] = numbers[j]
    numbers[j] = temp

class MysteryRunner(Runner):
    def run(self, inp):
        inp_list = list(inp.strip())
        quicksort(inp_list, 0, len(inp)-1)
        
        if inp_list == sorted(inp):
            return (inp, Runner.PASS)
        else:
            return (inp, Runner.FAIL)
        

import random

mystery = MysteryRunner()
random_fuzzer = RandomFuzzer()
random.seed(random.random())
counter = 0
results = []

while True:
    inp = '48956598643725345'
    result, outcome = mystery.run(inp)
    if outcome == mystery.FAIL:
        results.append(result)
        counter += 1
        if counter == 1:
            break

failing_input = results[0]
print('fail-inducing input: ', failing_input)
print('-------------------------------------------------------------------------------------------------------------------------------------------')

class Reducer(object):
    def __init__(self, runner, log_test=False):
        """Attach reducer to the given `runner`"""
        self.runner = runner
        self.log_test = log_test
        self.reset()

    def reset(self):
        self.tests = 0

    def test(self, inp):
        result, outcome = self.runner.run(inp)
        self.tests += 1
        if self.log_test:
            print("Test #%d" % self.tests, repr(inp), repr(len(inp)), outcome)
        return outcome

    def reduce(self, inp):
        self.reset()
        # Default: Don't reduce
        return inp

class CachingReducer(Reducer):
    def reset(self):
        super().reset()
        self.cache = {}

    def test(self, inp):
        if inp in self.cache:
            return self.cache[inp]

        outcome = super().test(inp)
        self.cache[inp] = outcome
        return outcome

class DeltaDebuggingReducer(CachingReducer):
    def reduce(self, inp):
        self.reset()
        assert self.test(inp) != Runner.PASS

        n = 2     # Initial granularity
        while len(inp) >= 2:
            start = 0
            subset_length = len(inp) / n
            some_complement_is_failing = False

            while start < len(inp):
                complement = inp[:int(start)] + \
                    inp[int(start + subset_length):]

                if self.test(complement) == Runner.FAIL:
                    inp = complement
                    n = max(n - 1, 2)
                    some_complement_is_failing = True
                    break

                start += subset_length

            if not some_complement_is_failing:
                if n == len(inp):
                    break
                n = min(n * 2, len(inp))

        return inp

dd_reducer = DeltaDebuggingReducer(mystery, log_test=True)

print(dd_reducer.reduce(failing_input))