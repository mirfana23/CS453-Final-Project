from Fuzzer import RandomFuzzer, Runner
from Delta_Debugging import DeltaDebuggingReducer
import random
import time

import argparse
import subprocess


def fault_percentage(DDres, Failres):
    return len(DDres) / len(Failres)

def push_queue(pfi, failres):
    global queue
    global maxpfi
    queue.append(failres)
    maxpfi = pfi
    print(pfi)


random_fuzzer = RandomFuzzer()
random.seed(random.random())
counter = 0
results = []
queue = []
maxpfi = 0

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Proposed Fuzzer')
    parser.add_argument('-t', '--target', type=str, required=True)
    parser.add_argument('-r', '--reference', type=str, required=True)
    parser.add_argument('-s', '--save_dir', type=str, required=True)

    args = parser.parse_args()

    target_program = args.target
    ref_program = args.reference

    #accessing false and true program and build the runner
    class MysteryRunner(Runner):
        def run(self, inp):
            inp_list = list(inp.strip())
            for i in range(0, len(inp_list)):
                inp_list[i] = int(inp_list[i])
            false_cmd = "python3 %s %s" %(target_program, '"' + str(inp_list) + '"')
            falseres = subprocess.check_output(false_cmd, text=True)
            true_cmd = "python3 %s %s" %(ref_program, '"' + str(inp_list) + '"')
            trueres = subprocess.check_output(true_cmd,  text=True)
            if falseres == trueres:
                return inp, Runner.PASS
            else:
                return inp, Runner.FAIL
    mystery = MysteryRunner()



    current_time = time.time()
    #set fuzzer timer
    timer = 300

    #fuzzing process
    while True:
        elapsed = time.time() - current_time

        if timer < elapsed:
            break

        inp = random_fuzzer.fuzz()
        result, outcome = mystery.run(inp)
        if outcome == mystery.FAIL:
            results.append(result)
            dd_reducer = DeltaDebuggingReducer(mystery, log_test=False)
            ddres = dd_reducer.reduce(result)
            pfires = fault_percentage(ddres, result)
            if pfires >= maxpfi:
                push_queue(pfires, result)


    #save fault inducing output
    count = 0
    for i in queue:
        save_file = target_program.split('/')[-1][:-3] + str(count) + '.txt'
        f = open(args.save_dir + '/' + save_file, "a")
        f.write(str(i) + '\n')
        count += 1
        f.close()

